import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """测试配置类"""
    
    # 基础配置
    BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8047')
    API_PREFIX = os.getenv('API_PREFIX', '/api/mgr')
    
    # 认证信息
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    
    # 测试配置
    TEST_TIMEOUT = int(os.getenv('TEST_TIMEOUT', '30'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # API端点
    LOGIN_URL = f"{BASE_URL}{API_PREFIX}/signin"
    CUSTOMER_URL = f"{BASE_URL}{API_PREFIX}/customers"
    MEDICINE_URL = f"{BASE_URL}{API_PREFIX}/medicines"
    ORDER_URL = f"{BASE_URL}{API_PREFIX}/orders"
    
    # 请求头
    HEADERS = {
        'Content-Type': 'application/json',
        'User-Agent': 'BYSMS-Test-Framework/1.0'
    }
    
    @classmethod
    def validate_config(cls):
        """验证配置是否完整"""
        required_vars = ['BASE_URL', 'ADMIN_USERNAME', 'ADMIN_PASSWORD']
        missing = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing.append(var)
        
        if missing:
            raise ValueError(f"缺少必要的环境变量: {', '.join(missing)}")
        
        return True