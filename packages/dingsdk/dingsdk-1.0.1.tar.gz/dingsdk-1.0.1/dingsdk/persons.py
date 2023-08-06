"""
智能人事
https://open.dingtalk.com/document/orgapp/intelligent-personnel-call-description
"""
from .core import Abstract


class Personnel(Abstract):
    
    def get_onjob_usersid(self, status:str='') -> list:
        """获取在职员工UserId列表
        """
        kwargs = {
            'url': 'smartwork/hrm/employee/queryonjob',
            'params': {'access_token': self.access_token},
            'data': {"status_list": status, "size": 50, "offset": 0}
        }
        result = self.post1(**kwargs).get('result', {})
        kwargs['pms']['offset'] = result.get('next_cursor', 0)
        
        while kwargs['pms']['offset'] > 0:
            res = self.post1(**kwargs).get('result', {})
            kwargs['pms']['offset'] = res.get('next_cursor', 0)
            result['data_list'].extend(res.get('data_list',[]))
        
        return result.get('data_list', [])
    
    def get_dimis_usersid(self) -> list:
        """获取离职员工UserId列表
        """
        kwargs = {
            'pms': {"offset":0, "size":50},
            'params': {'access_token': self.access_token},
            'data': 'smartwork/hrm/employee/querydimission',
        }
        result = self.post1(**kwargs).get('result', {})
        kwargs['pms']['offset'] = result.get('next_cursor', 0)
        
        while kwargs['pms']['offset'] > 0:
            res = self.post1(**kwargs).get('result', {})
            kwargs['pms']['offset'] = res.get('next_cursor', 0)
            result['data_list'].extend(res.get('data_list',[]))
        
        return result.get('data_list', [])
    