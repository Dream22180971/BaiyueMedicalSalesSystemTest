import requests
import json
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.config import Config
from utils.logger import logger

class HTTPClient:
    """HTTP客户端封装类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = Config.BASE_URL
        self.timeout = Config.TEST_TIMEOUT
        
        # 配置重试策略
        retry_strategy = Retry(
            total=Config.MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 设置默认请求头
        self.session.headers.update(Config.HEADERS)
    
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """发送HTTP请求"""
        full_url = f"{self.base_url}{url}"
        
        # 设置超时
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        logger.debug(f"发送请求: {method} {full_url}")
        
        try:
            response = self.session.request(method, full_url, **kwargs)
            logger.debug(f"响应状态码: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {str(e)}")
            raise
    
    def get(self, url: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送GET请求"""
        return self.request('GET', url, params=params, **kwargs)
    
    def post(self, url: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送POST请求"""
        # 检查是否明确指定了Content-Type
        headers = kwargs.get('headers', {})
        if data and 'Content-Type' not in headers:
            # 默认使用JSON格式
            kwargs.setdefault('headers', {})['Content-Type'] = 'application/json'
            return self.request('POST', url, json=data, **kwargs)
        elif data and headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            # 使用form-data格式
            return self.request('POST', url, data=data, **kwargs)
        else:
            return self.request('POST', url, **kwargs)
    
    def put(self, url: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送PUT请求"""
        if data and 'Content-Type' not in kwargs.get('headers', {}):
            kwargs.setdefault('headers', {})['Content-Type'] = 'application/json'
        return self.request('PUT', url, json=data, **kwargs)
    
    def delete(self, url: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送DELETE请求"""
        if data and 'Content-Type' not in kwargs.get('headers', {}):
            kwargs.setdefault('headers', {})['Content-Type'] = 'application/json'
        return self.request('DELETE', url, json=data, **kwargs)
    
    def login(self, username: str, password: str) -> bool:
        """用户登录"""
        login_data = {
            'username': username,
            'password': password
        }
        
        # 登录接口使用form-data格式
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self.post('/api/mgr/signin', data=login_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ret') == 0:
                logger.info(f"用户 {username} 登录成功")
                return True
            else:
                logger.error(f"登录失败: {result.get('msg', '未知错误')}")
                return False
        else:
            logger.error(f"登录请求失败，状态码: {response.status_code}")
            return False
    
    def validate_response(self, response: requests.Response, expected_status: int = 200) -> Dict:
        """验证响应结果"""
        if response.status_code != expected_status:
            # 打印响应内容以便调试
            logger.error(f"响应内容: {response.text}")
            raise AssertionError(f"期望状态码 {expected_status}，实际 {response.status_code}，响应: {response.text}")
        
        try:
            result = response.json()
        except json.JSONDecodeError:
            raise AssertionError("响应不是有效的JSON格式")
        
        if result.get('ret') != 0:
            raise AssertionError(f"API返回错误: {result.get('msg', '未知错误')}")
        
        return result