# Ding SDK

> 钉钉企业内部应用使用的钉钉SDK，为更贴合个人编码习惯，由个人自主开发和维护的钉钉SDK的 Python 模块。

1. 安装

   ```python
   pip install dingsdk
   ```

2. 使用

   ```python
   from dingsdk import DingSDK
   
   sdk = DingSDK()
   sdk.appkey = 'your appkey'
   sdk.agentid = 'your agentid'
   sdk.appsecret = 'your appsecret'
   sdk.access_token = sdk.get_token()		# 获取企业内部应用的 AccessToken
   ```
   
3. 清洗审批实例

   ```python
   from dingsdk import InstanceCleaner
   
   instid = "approval process instance id"
   instance = sdk.get_inst_detail(instid)
   cleaner = InstanceCleaner(approval_instance)
   cleaner.cleaned_data		# 已清洗的审批实例数据
   cleaner.cleaned_formvs		# 已清洗的实例表单数据
   ```

## 版本进程

**1.0.0_2023.2.2**

- 发布钉钉接口方法十一个，见接口检索；
- 钉钉审批实例数据清洗，`InstanceCleaner()`；

## 接口检索

| 序号 | 接口描述               | 接口方法              | 发布版本 |
| ---- | ---------------------- | --------------------- | -------- |
| 1    | 内部应用Token          | `get_token()`         | `V1.0.0` |
| 2    | 获取审批模板ID         | `get_proc_id()`       | `V1.0.0` |
| 3    | 获取审批实例详情       | `get_inst_detail()`   | `V1.0.0` |
| 4    | 获取审批实例ID列表     | `get_instid_list()`   | `V1.0.0` |
| 5    | 获取审批实例附件链接   | `get_inst_file()`     | `V1.0.0` |
| 6    | 同意或拒绝审批任务     | `execute_apprtask()`  | `V1.0.0` |
| 7    | 获取在职员工UserId列表 | `get_onjob_usersid()` | `V1.0.0` |
| 8    | 获取离职员工UserId列表 | `get_dimis_usersid()` | `V1.0.0` |
| 9    | 获取用户详情           | `get_user_detail()`   | `V1.0.0` |
| 10   | 批量发送机器人单聊消息 | `send_singles_msg()`  | `V1.0.0` |
| 11   | 批量撤回机器人单聊消息 | `back_signles_msg()`  | `V1.0.0` |

