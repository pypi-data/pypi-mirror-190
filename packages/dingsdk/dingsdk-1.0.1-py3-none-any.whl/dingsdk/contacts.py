"""
通讯录管理
https://open.dingtalk.com/document/orgapp/contacts-overview
"""
from .core import Abstract


class Contacts(Abstract):
    
    def get_user_detail(self, userid:str) -> dict:
        """获取用户详情
        """
        kwargs = {
            'url': 'topapi/v2/user/get',
            'params': {'access_token': self.access_token},
            'data': {"language": "zh_CN", "userid": userid},
        }
        return self.post1(**kwargs).get('result', {})
    