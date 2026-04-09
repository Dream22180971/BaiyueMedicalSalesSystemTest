from typing import Dict, List, Optional
from utils.http_client import HTTPClient
from config.config import Config
from utils.logger import logger

class MedicineAPI:
    """药品管理API封装"""
    
    def __init__(self, client: HTTPClient):
        self.client = client
        self.base_url = Config.MEDICINE_URL
    
    def list_medicines(self, page_size: int = 10, page_num: int = 1, keywords: str = "") -> List[Dict]:
        """获取药品列表"""
        params = {
            'action': 'list_medicine',
            'pagesize': page_size,
            'pagenum': page_num,
            'keywords': keywords
        }
        
        response = self.client.get('/api/mgr/medicines', params=params)
        result = self.client.validate_response(response)
        
        medicines = result.get('retlist', [])
        logger.info(f"获取到 {len(medicines)} 个药品")
        return medicines
    
    def add_medicine(self, name: str, sn: str, desc: str) -> int:
        """添加药品"""
        # 验证字段长度
        self._validate_medicine_data(name, sn, desc)
        
        # 检查药品是否已存在
        if self.medicine_exists(sn):
            raise AssertionError("药品编号已经存在")
        
        data = {
            'action': 'add_medicine',
            'data': {
                'name': name,
                'sn': sn,
                'desc': desc
            }
        }
        
        response = self.client.post('/api/mgr/medicines', data=data)
        result = self.client.validate_response(response)
        
        medicine_id = result.get('id')
        logger.info(f"添加药品成功，ID: {medicine_id}")
        return medicine_id
    
    def modify_medicine(self, medicine_id: int, name: str, sn: str, desc: str) -> bool:
        """修改药品信息"""
        data = {
            'action': 'modify_medicine',
            'id': medicine_id,
            'newdata': {
                'name': name,
                'sn': sn,
                'desc': desc
            }
        }
        
        # 验证字段长度
        self._validate_medicine_data(name, sn, desc)
        
        response = self.client.put('/api/mgr/medicines', data=data)
        self.client.validate_response(response)
        
        logger.info(f"修改药品 {medicine_id} 信息成功")
        return True
    
    def delete_medicine(self, medicine_id: int) -> bool:
        """删除药品"""
        # 先检查药品是否存在
        if not self.get_medicine_by_id(medicine_id):
            raise AssertionError(f"药品 {medicine_id} 不存在")
        
        data = {
            'action': 'del_medicine',
            'id': medicine_id
        }
        
        response = self.client.delete('/api/mgr/medicines', data=data)
        self.client.validate_response(response)
        
        logger.info(f"删除药品 {medicine_id} 成功")
        return True
    
    def get_medicine_by_id(self, medicine_id: int) -> Optional[Dict]:
        """根据ID获取药品信息"""
        medicines = self.list_medicines()
        for medicine in medicines:
            if medicine.get('id') == medicine_id:
                return medicine
        return None
    
    def medicine_exists(self, sn: str) -> bool:
        """检查药品是否存在"""
        # 遍历所有药品，不依赖搜索功能
        medicines = self.list_medicines()
        for medicine in medicines:
            if medicine.get('sn') == sn:
                return True
        return False
    
    def _validate_medicine_data(self, name: str, sn: str, desc: str):
        """验证药品数据格式"""
        if len(name) < 2 or len(name) > 50:
            raise ValueError("药品名称长度必须在2-50个字符之间")
        
        if len(sn) < 3 or len(sn) > 20:
            raise ValueError("药品编号长度必须在3-20个字符之间")
        
        if len(desc) < 2 or len(desc) > 200:
            raise ValueError("药品描述长度必须在2-200个字符之间")
