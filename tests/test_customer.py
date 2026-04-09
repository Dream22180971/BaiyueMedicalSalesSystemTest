import pytest
from faker import Faker

class TestCustomer:
    """客户管理功能测试"""
    
    @pytest.mark.customer
    @pytest.mark.smoke
    def test_list_customers(self, customer_api):
        """测试获取客户列表"""
        customers = customer_api.list_customers()
        
        assert isinstance(customers, list)
        # 验证返回的客户数据结构
        if customers:
            customer = customers[0]
            assert 'id' in customer
            assert 'name' in customer
            assert 'phonenumber' in customer
            assert 'address' in customer
    
    @pytest.mark.customer
    def test_add_customer_success(self, customer_api, test_customer_data):
        """测试添加客户成功"""
        customer_id = customer_api.add_customer(**test_customer_data)
        
        assert isinstance(customer_id, int)
        assert customer_id > 0
        
        # 验证客户确实被添加
        customer = customer_api.get_customer_by_id(customer_id)
        assert customer is not None
        assert customer['name'] == test_customer_data['name']
        assert customer['phonenumber'] == test_customer_data['phonenumber']
        assert customer['address'] == test_customer_data['address']
    
    @pytest.mark.customer
    def test_add_customer_with_existing_name(self, customer_api, created_customer, test_customer_data):
        """测试添加同名客户失败"""
        # 使用已存在的客户名
        existing_customer = customer_api.get_customer_by_id(created_customer)
        
        with pytest.raises(AssertionError) as exc_info:
            customer_api.add_customer(
                name=existing_customer['name'],
                phonenumber=test_customer_data['phonenumber'],
                address=test_customer_data['address']
            )
        
        assert "客户名已经存在" in str(exc_info.value)
    
    @pytest.mark.customer
    def test_add_customer_with_invalid_data(self, customer_api):
        """测试添加客户时数据验证"""
        # 名称过短
        with pytest.raises(ValueError) as exc_info:
            customer_api.add_customer("a", "12345678", "测试地址")
        assert "客户名长度必须在2-20个字符之间" in str(exc_info.value)
        
        # 名称过长
        with pytest.raises(ValueError) as exc_info:
            customer_api.add_customer("a" * 21, "12345678", "测试地址")
        assert "客户名长度必须在2-20个字符之间" in str(exc_info.value)
        
        # 电话号码过短
        with pytest.raises(ValueError) as exc_info:
            customer_api.add_customer("测试客户", "1234567", "测试地址")
        assert "电话号码长度必须在8-15个字符之间" in str(exc_info.value)
        
        # 电话号码过长
        with pytest.raises(ValueError) as exc_info:
            customer_api.add_customer("测试客户", "1" * 16, "测试地址")
        assert "电话号码长度必须在8-15个字符之间" in str(exc_info.value)
        
        # 地址过短
        with pytest.raises(ValueError) as exc_info:
            customer_api.add_customer("测试客户", "12345678", "a")
        assert "地址长度必须在2-100个字符之间" in str(exc_info.value)
        
        # 地址过长
        with pytest.raises(ValueError) as exc_info:
            customer_api.add_customer("测试客户", "12345678", "a" * 101)
        assert "地址长度必须在2-100个字符之间" in str(exc_info.value)
    
    @pytest.mark.customer
    def test_modify_customer_success(self, customer_api, created_customer, faker):
        """测试修改客户信息成功"""
        new_data = {
            'name': f"修改客户_{int(faker.unix_time())}",
            'phonenumber': faker.phone_number(),
            'address': faker.address()
        }
        
        success = customer_api.modify_customer(created_customer, **new_data)
        assert success is True
        
        # 验证修改结果
        customer = customer_api.get_customer_by_id(created_customer)
        assert customer['name'] == new_data['name']
        assert customer['phonenumber'] == new_data['phonenumber']
        assert customer['address'] == new_data['address']
    
    @pytest.mark.customer
    def test_modify_nonexistent_customer(self, customer_api):
        """测试修改不存在的客户"""
        nonexistent_id = 999999
        
        with pytest.raises(AssertionError) as exc_info:
            customer_api.modify_customer(
                nonexistent_id, 
                "不存在的客户", 
                "12345678", 
                "测试地址"
            )
        
        # 应该返回错误信息
        assert exc_info.value is not None
    
    @pytest.mark.customer
    def test_delete_customer_success(self, customer_api, test_customer_data):
        """测试删除客户成功"""
        # 先添加一个客户
        customer_id = customer_api.add_customer(**test_customer_data)
        
        # 删除客户
        success = customer_api.delete_customer(customer_id)
        assert success is True
        
        # 验证客户已被删除
        customer = customer_api.get_customer_by_id(customer_id)
        assert customer is None
    
    @pytest.mark.customer
    def test_delete_nonexistent_customer(self, customer_api):
        """测试删除不存在的客户"""
        nonexistent_id = 999999
        
        with pytest.raises(AssertionError) as exc_info:
            customer_api.delete_customer(nonexistent_id)
        
        # 应该返回错误信息
        assert exc_info.value is not None
    
    @pytest.mark.customer
    def test_customer_pagination(self, customer_api):
        """测试客户列表分页功能"""
        # 获取第一页
        page1 = customer_api.list_customers(page_size=5, page_num=1)
        
        # 获取第二页
        page2 = customer_api.list_customers(page_size=5, page_num=2)
        
        # 验证分页功能正常
        assert isinstance(page1, list)
        assert isinstance(page2, list)
    
    @pytest.mark.customer
    def test_customer_search(self, customer_api, created_customer):
        """测试客户搜索功能"""
        # 获取测试客户信息
        test_customer = customer_api.get_customer_by_id(created_customer)
        
        # 使用客户名搜索
        customers = customer_api.list_customers(keywords=test_customer['name'])
        
        # 验证搜索结果包含测试客户
        found = False
        for customer in customers:
            if customer['id'] == created_customer:
                found = True
                break
        
        assert found is True
    
    @pytest.mark.customer
    def test_customer_field_validation(self, customer_api):
        """测试客户字段验证"""
        import time
        import uuid
        
        # 生成唯一的客户名前缀（确保长度不超过限制）
        timestamp = str(int(time.time()))[-6:]
        uuid_part = uuid.uuid4().hex[:3]
        unique_prefix = f"测_{timestamp}_{uuid_part}"
        
        # 测试各种边界情况
        test_cases = [
            # (name, phonenumber, address, should_fail)
            (f"{unique_prefix}", "13800138000", "正常地址", False),
            ("ab", "12345678", "ab", False),  # 最小长度
            ("a" * 20, "1" * 15, "a" * 100, False),  # 最大长度
            ("a", "12345678", "正常地址", True),  # 名称过短
            ("a" * 21, "12345678", "正常地址", True),  # 名称过长
            (f"{unique_prefix}1", "1234567", "正常地址", True),  # 电话过短
            (f"{unique_prefix}2", "1" * 16, "正常地址", True),  # 电话过长
            (f"{unique_prefix}3", "12345678", "a", True),  # 地址过短
            (f"{unique_prefix}4", "12345678", "a" * 101, True),  # 地址过长
        ]
        
        for name, phone, address, should_fail in test_cases:
            if should_fail:
                with pytest.raises((ValueError, AssertionError)):
                    customer_api.add_customer(name, phone, address)
            else:
                try:
                    customer_id = customer_api.add_customer(name, phone, address)
                    # 清理测试数据
                    customer_api.delete_customer(customer_id)
                except Exception:
                    pytest.fail(f"有效数据测试失败: {name}, {phone}, {address}")