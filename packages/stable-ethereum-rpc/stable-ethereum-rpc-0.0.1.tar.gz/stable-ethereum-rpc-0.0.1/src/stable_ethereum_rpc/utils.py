from web3 import Web3
from web3.middleware import geth_poa_middleware


def create_http_provider(provider_url: str) -> Web3:
    _web3 = Web3(Web3.HTTPProvider(provider_url))
    _web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return _web3


def create_ipcp_provider(provider_url: str) -> Web3:
    _web3 = Web3(Web3.IPCProvider(provider_url))
    return _web3


def create_websocket_provider(provider_url: str) -> Web3:
    _web3 = Web3(Web3.WebsocketProvider(provider_url))
    return _web3


def create_web3_provider(provider_url: str, _type: str) -> Web3 or None:
    if _type == "http":
        return create_http_provider(provider_url)
    elif _type == "ipcp":
        return create_ipcp_provider(provider_url)
    elif _type == "websocket":
        return create_websocket_provider(provider_url)
    else:
        return None
