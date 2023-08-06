"""
文件存储
https://open.dingtalk.com/document/orgapp/dingtalk-storage-overview
"""
import os

from .core import Abstract


class CouldStore(Abstract):
    
    def _upload_media(self, file:'FileItem') -> str:
        """上传媒体文件
        """
        kwargs = {
            'url': 'media/upload',
            'data': {'type': file.file_type},
            'files': {'media': file.from_data},
            'params': {'access_token': self.access_token}
        }
        return self.post1(**kwargs).get('media_id', '')
    
    def load_file(self, filepath:str) -> 'FileItem':
        return FileItem(filepath)


class FileItem:
    
    def __init__(self, filepath:str) -> None:
        self._fp = filepath
        self._fn = os.path.split(filepath)[1]
        self._ext = os.path.splitext(filepath)[0]

    @property
    def from_data(self) -> tuple:
        return (self._fn, open(self._fp, 'rb'),
                f'application/{self.file_type}')

    @property
    def file_type(self) -> str:
        # if self._ext in ('mp4',):
        #     return 'video'
        # elif self._ext in ('amr', 'mp3', 'wav'):
        #     return 'voice'
        # elif self._ext in ('.jpg', '.png', '.gif', '.bmp'):
        #     return 'image'
        
        return 'file'
    
    @property
    def file_size(self) -> str:
        return 0
