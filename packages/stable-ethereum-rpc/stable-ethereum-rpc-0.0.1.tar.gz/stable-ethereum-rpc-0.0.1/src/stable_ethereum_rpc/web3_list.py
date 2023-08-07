from web3 import Web3

from stable_ethereum_rpc.utils import create_web3_provider
from stable_ethereum_rpc.web3_measure import Web3Measure


class Web3Entity:
    def __init__(self, web3: Web3, rpc_str: str, _type: str, chain_id: int):
        self.web3 = web3
        self.rpc = rpc_str
        self.type = _type
        self.chain_id = chain_id


class Web3List:
    def __init__(self, web3_list: list, chain_id: int, max_timestamp: int):
        self.chain_id = chain_id
        self._list: {str: Web3Entity} = {}
        for _web3 in web3_list:
            self.add_web3(_web3["url"], _web3["type"])
        self._measure = Web3Measure(chain_id, max_timestamp)

    def get_sufficient_web3(self, **kwargs) -> Web3Entity or None:
        web3_keys = list(self._list.keys())
        _len = len(web3_keys)
        start_index = kwargs.get("start_index")
        web3_param_url = kwargs.get("web3")
        web3_callback_func = kwargs.get("func")
        if web3_param_url:
            start_index = web3_keys.index(web3_param_url)
        elif start_index is None or start_index >= _len:
            start_index = 0
        counter = start_index
        check = True
        result = self._list[web3_keys[start_index]]
        while check:
            web3_url = web3_keys[counter]
            web3_entity = self._list[web3_url]
            _measure_param = self._measure.test_web3(web3_entity.web3)
            if web3_callback_func:
                if callable(web3_callback_func):
                    web3_callback_func(web3_entity, _measure_param)
            if _measure_param["isOk"]:
                result = web3_entity
                check = False
            else:
                if counter < _len - 1:
                    counter = counter + 1
                else:
                    counter = 0
                if counter == start_index:
                    check = False
                    result = None
        return result

    def get_best_stable_web3(self, **kwargs) -> Web3Entity:
        web3_callback_func = kwargs.get("func")
        web3_value = list(self._list.values())
        _result = web3_value[0]
        __temp_result = self._measure.test_web3(web3_value[0].web3)
        _measure_param = __temp_result["result"]
        if web3_callback_func:
            if callable(web3_callback_func):
                web3_callback_func(web3_value[0], __temp_result)
        for web3_item in web3_value[1:]:
            temp_measure = self._measure.test_web3(web3_item.web3)
            if web3_callback_func:
                if callable(web3_callback_func):
                    web3_callback_func(web3_item, temp_measure)
            if temp_measure["isOk"]:
                if temp_measure["result"] < _measure_param:
                    _result = web3_item
                    _measure_param = temp_measure["result"]
        return _result

    def add_web3(self, provider_url: str, _type: str, upsert=False) -> bool:
        is_already_exists = provider_url in self._list
        if upsert or (not is_already_exists):
            provider_web3 = create_web3_provider(provider_url, _type)
            self._list[provider_url] = Web3Entity(provider_web3, provider_url, _type, self.chain_id)
            return True
        else:
            current_entity = self._list[provider_url]
            current_type = current_entity.type
            if current_type == _type:
                return False
            else:
                provider_web3 = create_web3_provider(provider_url, _type)
                self._list[provider_url] = Web3Entity(provider_web3, provider_url, _type, self.chain_id)

    def remove_web3(self, provider_url: str) -> bool:
        if provider_url in self._list:
            del self._list[provider_url]
            return True
        else:
            return False
