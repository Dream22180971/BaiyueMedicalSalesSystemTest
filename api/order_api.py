from typing import Dict, List, Optional
from utils.http_client import HTTPClient
from config.config import Config
from utils.logger import logger

class OrderAPI:
    """订单管理API封装"""
    
    def __init__(self, client: HTTPClient):
        self.client = client
        self.base_url = Config.ORDER_URL
    
    def list_orders(self, page_size: int = 10, page_num: int = 1, keywords: str = "") -> List[Dict]:
        """获取订单列表"""
        params = {
            'action': 'list_order',
            'pagesize': page_size,
            'pagenum': page_num,
            'keywords': keywords
        }
        
        response = self.client.get('/api/mgr/orders', params=params)
        result = self.client.validate_response(response)
        
        orders = result.get('retlist', [])
        logger.info(f"获取到 {len(orders)} 个订单")
        return orders
    
    def add_order(self, customer_id: int, medicine_list: List[Dict]) -> int:
        """添加订单"""
        # 验证参数
        if not customer_id or not medicine_list:
            raise ValueError("客户ID和药品列表不能为空")
        
        import time
        # 生成订单名称
        order_name = f"订单_{int(time.time())}"
        
        data = {
            'action': 'add_order',
            'data': {
                'name': order_name,
                'customerid': customer_id,
                'medicinelist': medicine_list
            }
        }
        
        response = self.client.post('/api/mgr/orders', data=data)
        result = self.client.validate_response(response)
        
        order_id = result.get('id')
        logger.info(f"添加订单成功，ID: {order_id}")
        return order_id
    
    def delete_order(self, order_id: int) -> bool:
        """删除订单"""
        # 先检查订单是否存在
        if not self.get_order_by_id(order_id):
            raise AssertionError(f"订单 {order_id} 不存在")
        
        data = {
            'action': 'delete_order',
            'id': order_id
        }
        
        response = self.client.delete('/api/mgr/orders', data=data)
        self.client.validate_response(response)
        
        logger.info(f"删除订单 {order_id} 成功")
        return True
    
    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        """根据ID获取订单信息"""
        orders = self.list_orders()
        for order in orders:
            if order.get('id') == order_id:
                return order
        return None
    
    def order_exists(self, order_id: int) -> bool:
        """检查订单是否存在"""
        orders = self.list_orders()
        for order in orders:
            if order.get('id') == order_id:
                return True
        return False
