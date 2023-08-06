"""
OA审批
https://open.dingtalk.com/document/orgapp/workflow-overview
"""
import json

from .core import Abstract


class Approval(Abstract):
    
    def get_proc_id(self, name:str) -> str:
        """获取审批模板ID
        """
        kwargs = {
            'data': {'name': name},
            'url': 'process/get_by_name',
            'params': {'access_token': self.access_token},
        }
        return self.post1(**kwargs).get('process_code', '')
    
    def get_inst_detail(self, instid:str) -> dict:
        """获取审批实例详情
        """
        kwargs = {
            'token': self.access_token,
            'pms': {'processInstanceId': instid},
            'url': 'v1.0/workflow/processInstances'
        }
        return self.get2(**kwargs).get('result', {})
    
    def get_instid_list(self, procid:str, st:int,
        et:int=None, usersid:list=[], status:list=[]) -> list:
        """获取审批实例ID列表
        """
        status = status if isinstance(status, list) else []
        usersid = usersid if isinstance(usersid, list) else []
        
        kwargs = {
            'token': self.access_token,
            'url': 'v1.0/workflow/processes/instanceIds/query',
            'data': {
                'processCode': procid, 'startTime': st,
                'userIds': usersid, 'statuses': status,
                'endTime': et, 'nextToken': 0, 'maxResults':20
            }
        }
        result = self.post2(**kwargs).get('result', {})
        kwargs['pms']['nextToken'] = result.get('nextToken', 0)
        
        # 当 nextToken > 500 时，会引发异常
        while kwargs['pms']['nextToken'] > 0:
            res = self.post2(**kwargs).get('result',{})
            result['list'].extend(res.get('list', []))
            kwargs['pms']['nextToken'] = res.get('nextToken', 0)
        
        return result.get('list', [])
    
    def get_inst_file(self, instid:str, fileid:str) -> str:
        """获取实例附件链接
        """
        kwargs = {
            'token': self.access_token,
            'data': {'processInstanceId': instid, 'fileId': fileid},
            'url': 'v1.0/workflow/processInstances/spaces/files/urls/download'
        }
        return self.post2(**kwargs).get('result', {}).get('downloadUri', '')
    
    def execute_apprtask(self, instid:str, userid:str, taskid:str,
                         agree:bool=True, remark:str=None) -> bool:
        """同意或拒绝审批任务
        """
        result = 'agree' if agree == True else 'refuse'
        kwargs = {
            'token': self.access_token,
            'url': 'v1.0/workflow/processInstances/execute',
            'data': {"remark":remark, "result":result, "taskId": taskid,
                     "actionerUserId": userid, "processInstanceId": instid},
        }
        return self.post2(**kwargs).get('result', False)


class InstanceCleaner:
    """审批实例数据清洗
    
    Note:
        - 所有字段名保持不变，与文档一致
        - 将 status、result 的值替换成中文
        - 参考钉钉服务端API文档【获取单个审批实例详情 2023-01-18】

    Example:
    
    ```python
    cleaner = InstanceCleaner(data=instance_data)
    cleaner.cleaned_data    # 已清洗的实例数据, Dict(List(String, Array Object))
    cleaner.cleaned_taskvs    # 已清洗的任务数据, List(Dict)
    cleaner.cleaned_histvs    # 已清洗的历史数据, List(Dict)
    cleaner.cleaned_formvs    # 已清洗的表单数据, List(Dict(FieldName, FieldValue))
    ```
    """
    
    def __init__(self, data: dict) -> None:
        self._cleaned_data = self._clean(data)
    
    def _clean(self, data:dict) -> dict:
        data['tasks'] = parse_taskvs(data['tasks'])
        
        data['operationRecords'] = \
            parse_histvs(data['operationRecords'])
        
        data['formComponentValues'] = \
            parse_formvs(data['formComponentValues'])
        
        data['result'] = get_result_cn(data['result'])
        data['status'] = get_status_cn(data['status'])
        return data
    
    @property
    def cleaned_data(self) -> dict:
        return self._cleaned_data
    
    @property
    def cleaned_result(self) -> str:
        return self._cleaned_data['result']
    
    @property
    def cleaned_status(self) -> str:
        return self._cleaned_data['status']
        
    @property
    def cleaned_taskvs(self) -> list:
        return self._cleaned_data['tasks']
    
    @property
    def cleaned_histvs(self) -> list:
        return self._cleaned_data['operationRecords']
    
    @property
    def cleaned_formvs(self) -> list:
        return self._cleaned_data['formComponentValues']


get_result_cn = lambda v: {
    "AGREE": "同意", "REFUSE": "拒绝",
    "NONE": "未处理", "REDIRECTED": "转交"
}.get(v.upper(), v.upper())


get_status_cn = lambda v: {
    "NEW": "新创建", "PAUSED": "暂停",
    "CANCELED": "取消", "COMPLETED": "完成",
    "RUNNING": "审批中", "TERMINATED": "终止"
}.get(v.upper(), v.upper())


get_histvs_type_cn = lambda v: {
    "ADD_REMARK": "添加评论", "FINISH_PROCESS_INSTANCE": "结束流程实例",
    "REDIRECT_TASK": "转交任务", "START_PROCESS_INSTANCE": "发起流程实例",
    "REDIRECT_PROCESS": "审批退回", "EXECUTE_TASK_AGENT": "代理人执行任务",
    "APPEND_TASK_BEFORE": "前加签任务", 'EXECUTE_TASK_AUTO': '自动执行任务',
    "APPEND_TASK_AFTER": "后加签任务", "EXECUTE_TASK_NORMAL": "正常执行任务",
    "PROCESS_CC": "抄送", "TERMINATE_PROCESS_INSTANCE": "终止(撤销)流程实例",
}.get(v.upper(), v.upper())


def parse_taskvs(datas:list) -> list:
    """清洗审批任务
    """
    if isinstance(datas, str):
        datas = json.loads(datas)
        
    if not isinstance(datas, list):
        return datas
    
    return list(map(parse_taskvalue, datas))


def parse_taskvalue(data:dict) -> dict:
    result = 'result' if 'result' in data else 'task_result'
    status = 'status' if 'status' in data else 'task_status'
    return {
        **data,
        result: get_result_cn(data[result]),
        status: get_status_cn(data[status])
    }


def parse_histvs(datas:list) -> list:
    """清洗审批记录
    """
    if isinstance(datas, str):
        datas = json.loads(datas)
    
    if not isinstance(datas, list):
        return datas
    
    return list(map(parse_histvalue, datas))


def parse_histvalue(data:dict) -> dict:
    type_ = 'type' if 'type' in data else 'operation_type'
    result = 'result' if 'result' in data else 'operation_result'
    
    return {
        **data,
        result: get_result_cn(data[result]),
        type_: get_histvs_type_cn(data[type_])
    }


def parse_formvs(datas:list) -> list:
    """整个表单清洗
    """
    if isinstance(datas, str):
        datas = json.loads(datas)

    if not isinstance(datas, list):
        return datas
    
    # 不能返回 Dict, 因表单字段名可能不唯一
    # return {k: v for data in datas \
    #     for k,v in clean_default(data).items()}
    return list(map(parse_formvalue, datas))


def parse_formvalue(data:dict) -> dict:
    """单个表单字段清洗

    字段类型支持：
        - 说明 `TextNote`
        - 文本 `TextField`
        - 表单 `TableField`
        - 金额 `MoneyField`
        - 关联 `RelateField`
        - 日期 `DDDateField`
        - 图片 `DDPhotoField`
        - 附件 `DDAttachment`
        - 文本 `TextareaField`
        - 选项 `DDSelectField`
    """

    name = data.get('name')
    value = data.get('value')
    type_ = data.get('componentType' if \
        'componentType' in data else 'component_type')
    
    if not (name or value or type_):
        return data

    if type_ == 'TextNote':
        name = '说明'

    elif type_ in 'DDAttachment DDPhotoField':
        if isinstance(value, str):
            value = json.loads(value)

    elif type_ == 'TableField':
        if isinstance(value, str):
            value = json.loads(value)
        
        if isinstance(value, list):
            value = [{row.get('label'): row.get('value')}\
                for v in value for row in v['rowValue']]

    return {name: value}
