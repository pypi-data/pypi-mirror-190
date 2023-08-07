import time
import timeit
from web3 import Web3
from stable_ethereum_rpc.config import AppConfig


class Web3Measure:
    def __init__(self, chain_id: int, max_timestamp: int = None):
        self.chain_id = chain_id
        if max_timestamp:
            self.max_timestamp = max_timestamp
        else:
            self.max_timestamp = AppConfig.DEFAULT_NETWORK[chain_id]["maxTimestamp"]

    def _timestamp(self, web3: Web3):
        start_time = timeit.default_timer()
        _block_data = web3.eth.get_block("latest")
        end_time = timeit.default_timer()
        _timestamp = _block_data["timestamp"]
        current_timestamp = time.time()
        distance = current_timestamp - _timestamp
        time_to_run = end_time - start_time
        return {
            "result": distance * time_to_run,
            "distance": distance,
            "time": time_to_run,
            "isOk": 0 <= distance <= self.max_timestamp,
        }

    def test_web3(self, web3: Web3):
        raw_result = self._timestamp(web3)
        return raw_result
