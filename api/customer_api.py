from typing import Dict, List, Optional
from utils.http_client import HTTPClient
from config.config import Config
from utils.logger import logger

class CustomerAPI:
    """客户管理API封装"""
    
    def __init__(self, client: HTTPClient):
        self.client = client
        self.base_url = Config.CUSTOMER_URL
    
    def list_customers(self, page_size: int = 10, page_num: int = 1, keywords: str = "") -> List[Dict]:
        """获取客户列表"""
        params = {
            'action': 'list_customer',
            'pagesize': page_size,
            'pagenum': page_num,
            'keywords': keywords
        }
        
        response = self.client.get('/api/mgr/customers', params=params)
        result = self.client.validate_response(response)
        
        customers = result.get('retlist', [])
        logger.info(f"获取到 {len(customers)} 个客户")
        return customers
    
    def add_customer(self, name: str, phonenumber: str, address: str) -> int:
        """添加客户"""
        # 验证字段长度
        self._validate_customer_data(name, phonenumber, address)
        
        # 检查客户名是否已存在
        if self.customer_exists(name):
            raise AssertionError("客户名已经存在")
        
        data = {
            'action': 'add_customer',
            'data': {
                'name': name,
                'phonenumber': phonenumber,
                'address': address
            }
        }
        
        response = self.client.post('/api/mgr/customers', data=data)
        result = self.client.validate_response(response)
        
        customer_id = result.get('id')
        logger.info(f"添加客户成功，ID: {customer_id}")
        return customer_id
    
    def modify_customer(self, customer_id: int, name: str, phonenumber: str, address: str) -> bool:
        """修改客户信息"""
        data = {
            'action': 'modify_customer',
            'id': customer_id,
            'newdata': {
                'name': name,
                'phonenumber': phonenumber,
                'address': address
            }
        }
        
        # 验证字段长度
        self._validate_customer_data(name, phonenumber, address)
        
        response = self.client.put('/api/mgr/customers', data=data)
        self.client.validate_response(response)
        
        logger.info(f"修改客户 {customer_id} 信息成功")
        return True
    
    def delete_customer(self, customer_id: int) -> bool:
        """删除客户"""
        # 先检查客户是否存在
        if not self.get_customer_by_id(customer_id):
            raise AssertionError(f"客户 {customer_id} 不存在")
        
        data = {
            'action': 'del_customer',
            'id': customer_id
        }
        
        response = self.client.delete('/api/mgr/customers', data=data)
        self.client.validate_response(response)
        
        logger.info(f"删除客户 {customer_id} 成功")
        return True
    
    def get_customer_by_id(self, customer_id: int) -> Optional[Dict]:
        """根据ID获取客户信息"""
        customers = self.list_customers()
        for customer in customers:
            if customer.get('id') == customer_id:
                return customer
        return None
    
    def customer_exists(self, name: str) -> bool:
        """检查客户是否存在"""
        customers = self.list_customers(keywords=name)
        for customer in customers:
            if customer.get('name') == name:
                return True
        return False
    
    def _validate_customer_data(self, name: str, phonenumber: str, address: str):
        """验证客户数据格式"""
        if len(name) < 2 or len(name) > 20:
            raise ValueError("客户名长度必须在2-20个字符之间")
        
        if len(phonenumber) < 8 or len(phonenumber) > 15:
            raise ValueError("电话号码长度必须在8-15个字符之间")
        
        if len(address) < 2 or len(address) > 100:
            raise ValueError("地址长度必须在2-100个字符之间")