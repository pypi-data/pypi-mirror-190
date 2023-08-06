"""
钉钉机器人
https://open.dingtalk.com/document/orgapp/robot-overview
"""

import json

from .core import Abstract


class Chatbot(Abstract):
    
    def send_singles_msg(self, usersid:list, msgkey:str, msgpms:dict) -> dict:
        """批量发送单聊消息
        """
        kwargs = {
            'token': self.access_token,
            'url': 'v1.0/robot/oToMessages/batchSend',
            'data': {"robotCode" :self.appkey, "userIds": usersid,
                "msgKey": msgkey, "msgParam": json.dumps(msgpms)}
        }
        return self.post2(**kwargs)
    
    def back_signles_msg(self, tasksid:list) -> dict:
        """批量撤回单聊消息
        """
        kwargs = {
            'token': self.access_token,
            'url': 'v1.0/robot/otoMessages/batchRecall',
            'data': {'robotCode': self.appkey, 'processQueryKeys': tasksid}
        }
        return self.post2(**kwargs)
