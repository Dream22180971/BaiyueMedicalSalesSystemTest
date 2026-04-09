import json
import yaml
from typing import Dict, List, Any
from faker import Faker

fake = Faker('zh_CN')

class TestDataGenerator:
    """测试数据生成器"""
    
    @staticmethod
    def generate_customer_data(count: int = 10) -> List[Dict]:
        """生成客户测试数据"""
        customers = []
        for i in range(count):
            customer = {
                'name': f"{fake.company_prefix()}{fake.company_suffix()}_{i}",
                'phonenumber': fake.phone_number(),
                'address': fake.address()
            }
            customers.append(customer)
        return customers
    
    @staticmethod
    def generate_medicine_data(count: int = 5) -> List[Dict]:
        """生成药品测试数据"""
        medicines = [
            {"name": "来适可", "sn": "LSK001", "desc": "降血脂药物"},
            {"name": "立卫克", "sn": "LWK002", "desc": "胃药"},
            {"name": "舒利迭", "sn": "SLD003", "desc": "哮喘治疗药物"},
            {"name": "拜糖平", "sn": "BTP004", "desc": "降血糖药物"},
            {"name": "络活喜", "sn": "LHX005", "desc": "降压药物"}
        ]
        
        # 如果需要的数量超过预设，生成随机药品
        if count > len(medicines):
            for i in range(len(medicines), count):
                medicine = {
                    'name': f"测试药品_{i}",
                    'sn': f"TS{i:03d}",
                    'desc': f"测试药品描述_{i}"
                }
                medicines.append(medicine)
        
        return medicines[:count]
    
    @staticmethod
    def generate_order_data(customer_id: int, medicine_ids: List[int]) -> Dict:
        """生成订单测试数据"""
        order_items = []
        for med_id in medicine_ids:
            order_items.append({
                'id': med_id,
                'amount': fake.random_int(min=1, max=100)
            })
        
        return {
            'name': f"订单_{fake.uuid4()[:8]}",
            'customerid': customer_id,
            'medicinelist': order_items
        }
    
    @staticmethod
    def save_test_data(data: Any, filename: str, format: str = 'json'):
        """保存测试数据到文件"""
        if format == 'json':
            with open(f"data/{filename}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif format == 'yaml':
            with open(f"data/{filename}.yaml", 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    
    @staticmethod
    def load_test_data(filename: str, format: str = 'json') -> Any:
        """从文件加载测试数据"""
        if format == 'json':
            with open(f"data/{filename}.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        elif format == 'yaml':
            with open(f"data/{filename}.yaml", 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)

# 预定义的测试数据
TEST_CUSTOMERS = TestDataGenerator.generate_customer_data(5)
TEST_MEDICINES = TestDataGenerator.generate_medicine_data(5)

# 边界测试数据
BOUNDARY_TEST_CASES = {
    'customer_name': [
        ('a', '12345678', '测试地址'),  # 名称过短
        ('a' * 21, '12345678', '测试地址'),  # 名称过长
        ('正常名称', '1234567', '测试地址'),  # 电话过短
        ('正常名称', '1' * 16, '测试地址'),  # 电话过长
        ('正常名称', '12345678', 'a'),  # 地址过短
        ('正常名称', '12345678', 'a' * 101),  # 地址过长
    ],
    'valid_customer': [
        ('ab', '12345678', 'ab'),  # 最小长度
        ('a' * 20, '1' * 15, 'a' * 100),  # 最大长度
    ]
}