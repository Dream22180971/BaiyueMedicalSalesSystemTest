import pytest
from config.config import Config
from utils.http_client import HTTPClient

class TestLogin:
    """登录功能测试"""
    
    @pytest.mark.login
    @pytest.mark.smoke
    def test_login_success(self, http_client):
        """测试管理员登录成功"""
        success = http_client.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
        assert success is True
    
    @pytest.mark.login
    def test_login_with_wrong_password(self, http_client):
        """测试错误密码登录失败"""
        success = http_client.login(Config.ADMIN_USERNAME, "wrong_password")
        assert success is False
    
    @pytest.mark.login
    def test_login_with_wrong_username(self, http_client):
        """测试错误用户名登录失败"""
        success = http_client.login("wrong_username", Config.ADMIN_PASSWORD)
        assert success is False
    
    @pytest.mark.login
    def test_login_with_empty_credentials(self, http_client):
        """测试空用户名和密码登录失败"""
        success = http_client.login("", "")
        assert success is False
    
    @pytest.mark.login
    def test_login_with_special_characters(self, http_client):
        """测试特殊字符登录失败"""
        success = http_client.login("admin@#$", "pass@#$")
        assert success is False
    
    @pytest.mark.login
    def test_login_with_long_credentials(self, http_client):
        """测试超长用户名密码登录失败"""
        long_username = "a" * 100
        long_password = "b" * 100
        success = http_client.login(long_username, long_password)
        assert success is False
    
    @pytest.mark.login
    def test_login_response_format(self, http_client):
        """测试登录响应格式"""
        # 正确登录
        login_data = {
            'username': Config.ADMIN_USERNAME,
            'password': Config.ADMIN_PASSWORD
        }
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = http_client.post(Config.API_PREFIX + '/signin', 
                                  data=login_data, headers=headers)
        
        assert response.status_code == 200
        result = response.json()
        assert 'ret' in result
        assert result['ret'] == 0
        
        # 错误登录
        login_data['password'] = 'wrong'
        response = http_client.post(Config.API_PREFIX + '/signin', 
                                  data=login_data, headers=headers)
        
        assert response.status_code == 200
        result = response.json()
        assert 'ret' in result
        assert result['ret'] != 0
        assert 'msg' in result
    
    @pytest.mark.login
    def test_session_persistence(self, http_client):
        """测试会话保持"""
        # 先登录
        success = http_client.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
        assert success is True
        
        # 使用同一个客户端访问需要认证的接口
        # 这里可以测试客户列表接口
        params = {
            'action': 'list_customer',
            'pagesize': 5,
            'pagenum': 1
        }
        
        response = http_client.get(Config.API_PREFIX + '/customers', params=params)
        assert response.status_code == 200
        
        result = response.json()
        assert 'ret' in result
        # 如果未登录，应该返回错误，这里期望成功
        assert result['ret'] == 0