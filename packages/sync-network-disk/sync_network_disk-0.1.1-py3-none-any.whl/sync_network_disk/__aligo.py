import aligo
from typing import List
from aligo import BatchRequest, BatchSubRequest

class Aligo(aligo.Aligo):
    V3_FILE_DELETE = '/v3/file/delete'

    def delete_file(self, file_id: str, drive_id: str = None) -> bool:
        """删除文件"""
        drive_id = drive_id or self.default_drive_id
        response = self._post(self.V3_FILE_DELETE, body={
            'drive_id': drive_id,
            'file_id': file_id
        })
        return response.status_code == 204

    def batch_delete_files(self, file_id_list: List[str], drive_id: str = None):
        """批量删除文件"""
        drive_id = drive_id or self.default_drive_id
        result = self.batch_request(BatchRequest(
            requests=[BatchSubRequest(
                id=file_id,
                url='/file/delete',
                body={
                    'drive_id': drive_id,
                    'file_id': file_id
                }
            ) for file_id in file_id_list]
        ), dict)
        return list(result)