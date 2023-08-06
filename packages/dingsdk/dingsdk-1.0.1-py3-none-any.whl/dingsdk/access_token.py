from .core import Abstract


class AccessToken(Abstract):
    
    def get_token(self) -> str:
        """获取企业内部应用的 AccessToken
        """
        return super().get1('gettoken', {
            'appkey': self.appkey,
            'appsecret': self.appsecret
        }).get('access_token', '')
