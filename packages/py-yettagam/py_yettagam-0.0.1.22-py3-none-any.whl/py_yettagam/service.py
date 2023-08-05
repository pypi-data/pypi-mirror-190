# Author: MetariumProject

# Standard libraries
import time
import os
from pathlib import Path
import json
import asyncio
# Third party libraries
import ipfshttpclient
from ipfshttpclient.exceptions import (
    ConnectionError,
    TimeoutError,
)
from blake3 import blake3
from substrateinterface import SubstrateInterface, Keypair
# Metarium libraries
from py_metarium import (
    FUTURE,
)
from py_metarium_encoder import (
    SubstrateServiceUpdaterAsService,
)
# local libraries
from .exceptions import (
    StorageConnectionRefusedError,
)
from .storage import (
    KuriSyncBase,
)

class Service(KuriSyncBase):

    RECONNECTION_WAIT_DURATION_SECONDS = 5
    MAX_RECONNECTION_ATTEMPTS = 10

    BLAKE3 = "blake3"

    """
        A Yettagam Service can perform the following functions:
        [x] Publish it's own status
        [x] Listen to a Scribe's kuris
        [#] Sync with a Scribe via IPFS Pub/sub
    """

    def __init__(self, node_url:str=None, path:str=None, **encoder_kwargs) -> None:
        assert node_url is not None
        assert "mnemonic" in encoder_kwargs or "uri" in encoder_kwargs
        super().__init__(node_url)
        if "mnemonic" in encoder_kwargs:
            self.key_pair = Keypair.create_from_mnemonic(encoder_kwargs["mnemonic"])
        elif "uri" in encoder_kwargs:
            self.key_pair = Keypair.create_from_uri(encoder_kwargs["uri"])
        
        self.__setup(node_url=node_url, path=path or f"{Path().resolve()}")

        self.service_updater = SubstrateServiceUpdaterAsService(url=node_url, **encoder_kwargs)

    def __set_or_create_directory(self, path:str):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def __set_or_create_file(self, path:str=None, extension:str=None):
        assert path is not None
        assert extension is not None
        if not os.path.exists(f"{path}.{extension}"):
            with open(f"{path}.{extension}", "w") as f:
                if extension == "json":
                    f.write("{}")
                elif extension == "txt":
                    f.write("")

    def __setup_ipfs_client(self):
        reconnection_attempts = 1
        while True:
            try:
                self.__ipfs_client = ipfshttpclient.connect(session=True)
            except ConnectionError:
                if reconnection_attempts == self.__class__.MAX_RECONNECTION_ATTEMPTS:
                    print(f"IPFS connection terminated after {reconnection_attempts} attempts.")
                    raise StorageConnectionRefusedError
                print(f"IPFS connection refused. Retrying in {self.__class__.RECONNECTION_WAIT_DURATION_SECONDS} seconds ...")
                reconnection_attempts += 1
                time.sleep(self.__class__.RECONNECTION_WAIT_DURATION_SECONDS)
                continue
            break

    def __setup(self, node_url:str=None, path:str=None):
        assert node_url is not None
        assert path is not None
        # IPFS
        self.__setup_ipfs_client()
        # directories
        self.scribe_set = set()
        substrate = SubstrateInterface(url=node_url)
        self.directory = f"{path}/{self.key_pair.ss58_address}/{substrate.chain}"
        self.data_directory = f"{self.directory}/data"
        self.sync_directory = f"{self.directory}/sync"
        # create directories if they don't exist
        self.__set_or_create_directory(self.data_directory)
        self.__set_or_create_directory(self.sync_directory)
        # create mappings.json in data if it doesn't exist
        self.__set_or_create_file(path=f"{self.data_directory}/mappings", extension="json")
        # create status.txt in sync if it doesn't exist
        self.__set_or_create_file(path=f"{self.sync_directory}/status", extension="txt")
        # create rff.txt in sync if it doesn't exist
        self.__set_or_create_file(path=f"{self.sync_directory}/rff", extension="txt")
    
    def __blake3_hash(self, data:dict=None) -> str:
        # Create a Blake3 hash object
        hasher = blake3(max_threads=blake3.AUTO)
        with open(data["content"], "rb") as f:
            counter = 0
            while True:
                counter += 1
                content = f.read(1024)
                if not content:
                    break
                hasher.update(content)
        return f"|>{self.__class__.BLAKE3}|{hasher.hexdigest()}"

    async def publish_status(self) -> str:
        service_data = {
            "status": f"{self.sync_directory}/status.txt",
            "rff": self.__ipfs_client.add(f"{self.sync_directory}/rff.txt")["Hash"],
        }

        transaction_hash = self.service_updater.encode(
            data=service_data,
            wait_for_inclusion=True,
            wait_for_finalization=False
        )
        yield transaction_hash
    
    async def periodic_publish_status(self, interval:int=10):
        while True:
            async for transaction_hash in self.publish_status():
                print(f"Published status with transaction hash: {transaction_hash}")
            await asyncio.sleep(interval)

    def kuri_registry_file_name(self, scribe:str=None) -> str:
        assert scribe is not None
        return f"{self.sync_directory}/{scribe}/kuris.json"

    def get_sync_location(self, filters:dict={}) -> str:
        return self.kuri_registry_file_name(scribe=filters["caller"][1:-1])

    def __ipfs_pubsub_subscribe(self, topic:str=None):
        assert topic is not None
        with self.__ipfs_client.pubsub.subscribe(topic) as sub:
            print(f"Subscribed to {topic}.")
            for message in sub:
                print(message)
                print(f"Received message: {message['data'].decode('utf-8')}")

    def save_kuri(self, kuri, filters:dict={}):
        # save kuri to status.txt if it doesn't exist
        kuris_in_status = []
        with open(f"{self.sync_directory}/status.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    kuris_in_status.append(line)
        print(f"{kuris_in_status = }")
        if kuri not in kuris_in_status:
            kuris_in_status.append(kuri)
            with open(f"{self.sync_directory}/status.txt", "a") as f:
                f.write(f"\n{kuri}")
        # check if kuri exists in data/mappings.json
        with open(f"{self.data_directory}/mappings.json", "r") as f:
            mappings = json.load(f)
            if kuri not in mappings:
                # if not, add it to sync/rff.txt if it doesn't exist
                kuris_in_rff = []
                with open(f"{self.sync_directory}/rff.txt", "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            kuris_in_rff.append(line)
                if kuri not in kuris_in_rff:
                    with open(f"{self.sync_directory}/rff.txt", "a") as f:
                        f.write(f"\n{kuri}")
                    # subscribe to kuri in IPFS pubsub
                    try:
                        self.__ipfs_pubsub_subscribe(topic=kuri)
                    except Exception as error:
                        print(f"Error subscribing to {kuri}: {error}")

    def sync_scribe_kuris(self,
            scribe:str=None, kuri_prefix:str=None,
            direction:str=None, start_block_number:any=None, block_count:any=None, finalized_only:bool=False
        ) -> None:
        assert scribe is not None
        direction = direction or FUTURE
        kuri_prefix = kuri_prefix or self.__class__.BLAKE3
        self.scribe_set.add(scribe)
        # create sync/scribe if it doesn't exist
        self.__set_or_create_directory(f"{self.sync_directory}/{scribe}")
        # create kuris.json in sync/scribe if it doesn't exist
        self.__set_or_create_file(path=f"{self.sync_directory}/{scribe}/kuris", extension="json")
        filters = {
            "kuri": f"^\|\>{kuri_prefix}\|.*",
            "caller": f"^{scribe}$"
        }
        self.sync(direction, start_block_number, block_count, finalized_only, filters=filters)
