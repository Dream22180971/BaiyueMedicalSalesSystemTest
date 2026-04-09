import pytest
import time
from faker import Faker
from utils.http_client import HTTPClient
from api.customer_api import CustomerAPI
from api.medicine_api import MedicineAPI
from api.order_api import OrderAPI
from config.config import Config
from utils.logger import logger

fake = Faker('zh_CN')

@pytest.fixture(scope="session")
def http_client():
    """全局HTTP客户端"""
    client = HTTPClient()
    
    # 验证配置
    Config.validate_config()
    
    yield client
    
    # 测试结束后清理
    client.session.close()

@pytest.fixture(scope="function")
def authenticated_client(http_client):
    """已认证的HTTP客户端"""
    # 登录系统
    success = http_client.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
    if not success:
        pytest.fail("管理员登录失败，无法执行测试")
    
    yield http_client
    
    # 测试结束后可以执行清理操作

@pytest.fixture(scope="function")
def customer_api(authenticated_client):
    """客户管理API实例"""
    return CustomerAPI(authenticated_client)

@pytest.fixture(scope="function")
def medicine_api(authenticated_client):
    """药品管理API实例"""
    return MedicineAPI(authenticated_client)

@pytest.fixture(scope="function")
def order_api(authenticated_client):
    """订单管理API实例"""
    return OrderAPI(authenticated_client)

@pytest.fixture(scope="function")
def test_customer_data():
    """测试客户数据"""
    import uuid
    # 确保客户名长度不超过20个字符
    timestamp = str(int(time.time()))[-6:]
    uuid_part = uuid.uuid4().hex[:4]
    return {
        'name': f"客_{timestamp}_{uuid_part}",
        'phonenumber': fake.phone_number(),
        'address': fake.address()
    }

@pytest.fixture(scope="function")
def created_customer(customer_api, test_customer_data):
    """创建测试客户并返回ID，测试结束后自动清理"""
    customer_id = customer_api.add_customer(**test_customer_data)
    
    yield customer_id
    
    # 测试结束后删除客户
    try:
        customer_api.delete_customer(customer_id)
        logger.info(f"清理测试客户: {customer_id}")
    except Exception as e:
        logger.warning(f"清理客户失败: {str(e)}")

@pytest.fixture(scope="function")
def test_medicine_data():
    """测试药品数据"""
    import uuid
    # 确保药品编号长度符合要求
    timestamp = str(int(time.time()))[-6:]
    uuid_part = uuid.uuid4().hex[:4]
    return {
        'name': f"测试药品_{timestamp}",
        'sn': f"SN_{timestamp}_{uuid_part}",
        'desc': fake.sentence()
    }

@pytest.fixture(scope="function")
def created_medicine(medicine_api, test_medicine_data):
    """创建测试药品并返回ID，测试结束后自动清理"""
    medicine_id = medicine_api.add_medicine(**test_medicine_data)
    
    yield medicine_id
    
    # 测试结束后删除药品
    try:
        medicine_api.delete_medicine(medicine_id)
        logger.info(f"清理测试药品: {medicine_id}")
    except Exception as e:
        logger.warning(f"清理药品失败: {str(e)}")

@pytest.fixture(scope="function")
def test_order_data(created_customer, created_medicine):
    """测试订单数据"""
    return {
        'customer_id': created_customer,
        'medicine_list': [
            {
                'id': created_medicine,
                'amount': '1'
            }
        ]
    }

@pytest.fixture(scope="function")
def created_order(order_api, test_order_data):
    """创建测试订单并返回ID，测试结束后自动清理"""
    order_id = order_api.add_order(**test_order_data)
    
    yield order_id
    
    # 测试结束后删除订单
    try:
        order_api.delete_order(order_id)
        logger.info(f"清理测试订单: {order_id}")
    except Exception as e:
        logger.warning(f"清理订单失败: {str(e)}")

@pytest.fixture(scope="session")
def faker():
    """Faker实例"""
    return fake

# 钩子函数
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """获取测试结果"""
    outcome = yield
    rep = outcome.get_result()
    
    # 设置测试结果属性
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="function", autouse=True)
def test_logging(request):
    """自动记录测试开始和结束"""
    logger.info(f"开始测试: {request.node.name}")
    
    yield
    
    # 检查测试结果
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        logger.error(f"测试失败: {request.node.name}")
    else:
        logger.info(f"测试完成: {request.node.name}")