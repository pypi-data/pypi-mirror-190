import httpx
import requests

requests.Request
requests.get

class ClientV1(httpx.Client):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs,
            base_url='https://oapi.dingtalk.com/')
    
    def request(self, *args, **kwargs) -> dict:
        response = super().request(*args, **kwargs).json()
        if response.get('errcode') == 0: return response
        raise DingTalkSDKError({'url':args[1], **response})
    
    def get(self, url, pms, *args, **kwargs) -> dict:
        kwargs.update(url=url, params=pms)
        return super().get(*args, **kwargs)
    
    def post(self, url, data, *args, **kwargs) -> dict:
        kwargs.update(url=url, data=data)
        return super().post(*args, **kwargs)


class ClientV2(httpx.Client):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs,
            base_url='https://api.dingtalk.com/')
        
    def request(self, *args, **kwargs) -> dict:
        kwargs.update(headers={
            'Host': 'api.dingtalk.com',
            'Content-Type': 'application/json',
            'x-acs-dingtalk-access-token': kwargs.pop('auth')
        })
        response = super().request(*args, **kwargs)
        if response.is_success: return response.json()
        raise DingTalkSDKError({'url': args[1], **response.json()})

    def get(self, url, token, pms, *args, **kwargs) -> dict:
        kwargs.update(url=url, params=pms, auth=token)
        return super().get(*args, **kwargs)

    def post(self, url, token, data, *args, **kwargs) -> dict:
        kwargs.update(url=url, json=data, auth=token)
        return super().post(*args, **kwargs)


class DingTalkSDKError(Exception):
    pass


get1 = ClientV1().get
get2 = ClientV2().get
post1 = ClientV1().post
post2 = ClientV2().post


class Abstract:
    get1  = get1
    get2  = get2
    post1 = post1
    post2 = post2
    
    appkey = None
    agentid = None
    appsecret = None
    access_token = None


