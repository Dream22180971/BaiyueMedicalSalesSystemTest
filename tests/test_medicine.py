import pytest
from faker import Faker

class TestMedicine:
    """药品管理功能测试"""
    
    @pytest.mark.medicine
    @pytest.mark.smoke
    def test_list_medicines(self, medicine_api):
        """测试获取药品列表"""
        medicines = medicine_api.list_medicines()
        
        assert isinstance(medicines, list)
        # 验证返回的药品数据结构
        if medicines:
            medicine = medicines[0]
            assert 'id' in medicine
            assert 'name' in medicine
            assert 'sn' in medicine
            assert 'desc' in medicine
    
    @pytest.mark.medicine
    def test_add_medicine_success(self, medicine_api, test_medicine_data):
        """测试添加药品成功"""
        medicine_id = medicine_api.add_medicine(**test_medicine_data)
        
        assert isinstance(medicine_id, int)
        assert medicine_id > 0
        
        # 验证药品确实被添加
        medicine = medicine_api.get_medicine_by_id(medicine_id)
        assert medicine is not None
        assert medicine['name'] == test_medicine_data['name']
        assert medicine['sn'] == test_medicine_data['sn']
        assert medicine['desc'] == test_medicine_data['desc']
    
    @pytest.mark.medicine
    def test_add_medicine_with_existing_sn(self, medicine_api, created_medicine, test_medicine_data):
        """测试添加重复编号药品失败"""
        # 使用已存在的药品编号
        existing_medicine = medicine_api.get_medicine_by_id(created_medicine)
        
        with pytest.raises(AssertionError) as exc_info:
            medicine_api.add_medicine(
                name=test_medicine_data['name'],
                sn=existing_medicine['sn'],
                desc=test_medicine_data['desc']
            )
        
        assert "药品编号已经存在" in str(exc_info.value)
    
    @pytest.mark.medicine
    def test_add_medicine_with_invalid_data(self, medicine_api):
        """测试添加药品时数据验证"""
        # 名称过短
        with pytest.raises(ValueError) as exc_info:
            medicine_api.add_medicine("a", "SN001", "测试药品")
        assert "药品名称长度必须在2-50个字符之间" in str(exc_info.value)
        
        # 名称过长
        with pytest.raises(ValueError) as exc_info:
            medicine_api.add_medicine("a" * 51, "SN001", "测试药品")
        assert "药品名称长度必须在2-50个字符之间" in str(exc_info.value)
        
        # 编号过短
        with pytest.raises(ValueError) as exc_info:
            medicine_api.add_medicine("测试药品", "SN", "测试药品")
        assert "药品编号长度必须在3-20个字符之间" in str(exc_info.value)
        
        # 编号过长
        with pytest.raises(ValueError) as exc_info:
            medicine_api.add_medicine("测试药品", "S" * 21, "测试药品")
        assert "药品编号长度必须在3-20个字符之间" in str(exc_info.value)
        
        # 描述过短
        with pytest.raises(ValueError) as exc_info:
            medicine_api.add_medicine("测试药品", "SN001", "a")
        assert "药品描述长度必须在2-200个字符之间" in str(exc_info.value)
        
        # 描述过长
        with pytest.raises(ValueError) as exc_info:
            medicine_api.add_medicine("测试药品", "SN001", "a" * 201)
        assert "药品描述长度必须在2-200个字符之间" in str(exc_info.value)
    
    @pytest.mark.medicine
    def test_modify_medicine_success(self, medicine_api, created_medicine, faker):
        """测试修改药品信息成功"""
        new_data = {
            'name': f"修改药品_{int(faker.unix_time())}",
            'sn': f"SN{faker.unique.random_int(100, 999)}",
            'desc': faker.sentence()
        }
        
        success = medicine_api.modify_medicine(created_medicine, **new_data)
        assert success is True
        
        # 验证修改结果
        medicine = medicine_api.get_medicine_by_id(created_medicine)
        assert medicine['name'] == new_data['name']
        assert medicine['sn'] == new_data['sn']
        assert medicine['desc'] == new_data['desc']
    
    @pytest.mark.medicine
    def test_modify_nonexistent_medicine(self, medicine_api):
        """测试修改不存在的药品"""
        nonexistent_id = 999999
        
        with pytest.raises(AssertionError) as exc_info:
            medicine_api.modify_medicine(
                nonexistent_id, 
                "不存在的药品", 
                "SN999", 
                "测试药品"
            )
        
        # 应该返回错误信息
        assert exc_info.value is not None
    
    @pytest.mark.medicine
    def test_delete_medicine_success(self, medicine_api, test_medicine_data):
        """测试删除药品成功"""
        # 先添加一个药品
        medicine_id = medicine_api.add_medicine(**test_medicine_data)
        
        # 删除药品
        success = medicine_api.delete_medicine(medicine_id)
        assert success is True
        
        # 验证药品已被删除
        medicine = medicine_api.get_medicine_by_id(medicine_id)
        assert medicine is None
    
    @pytest.mark.medicine
    def test_delete_nonexistent_medicine(self, medicine_api):
        """测试删除不存在的药品"""
        nonexistent_id = 999999
        
        with pytest.raises(AssertionError) as exc_info:
            medicine_api.delete_medicine(nonexistent_id)
        
        # 应该返回错误信息
        assert exc_info.value is not None
    
    @pytest.mark.medicine
    def test_medicine_pagination(self, medicine_api):
        """测试药品列表分页功能"""
        # 获取第一页
        page1 = medicine_api.list_medicines(page_size=5, page_num=1)
        
        # 获取第二页
        page2 = medicine_api.list_medicines(page_size=5, page_num=2)
        
        # 验证分页功能正常
        assert isinstance(page1, list)
        assert isinstance(page2, list)
    
    @pytest.mark.medicine
    def test_medicine_search(self, medicine_api, created_medicine):
        """测试药品搜索功能"""
        # 获取测试药品信息
        test_medicine = medicine_api.get_medicine_by_id(created_medicine)
        
        # 使用药品名称搜索
        medicines = medicine_api.list_medicines(keywords=test_medicine['name'])
        
        # 验证搜索结果包含测试药品
        found = False
        for medicine in medicines:
            if medicine['id'] == created_medicine:
                found = True
                break
        
        assert found is True
    
    @pytest.mark.medicine
    def test_medicine_field_validation(self, medicine_api):
        """测试药品字段验证"""
        import time
        import uuid
        
        # 生成唯一的药品编号前缀
        timestamp = str(int(time.time()))[-6:]
        uuid_part = uuid.uuid4().hex[:3]
        unique_prefix = f"SN_{timestamp}_{uuid_part}"
        
        # 测试各种边界情况
        test_cases = [
            # (name, sn, desc, should_fail)
            ("测试药品", f"{unique_prefix}", "正常药品", False),
            ("ab", f"{unique_prefix}1", "ab", False),  # 最小长度
            ("a" * 50, f"{unique_prefix}2", "a" * 200, False),  # 最大长度
            ("a", f"{unique_prefix}3", "正常药品", True),  # 名称过短
            ("a" * 51, f"{unique_prefix}4", "正常药品", True),  # 名称过长
            ("测试药品", "SN", "正常药品", True),  # 编号过短
            ("测试药品", "S" * 21, "正常药品", True),  # 编号过长
            ("测试药品", f"{unique_prefix}5", "a", True),  # 描述过短
            ("测试药品", f"{unique_prefix}6", "a" * 201, True),  # 描述过长
        ]
        
        for name, sn, desc, should_fail in test_cases:
            if should_fail:
                with pytest.raises((ValueError, AssertionError)):
                    medicine_api.add_medicine(name, sn, desc)
            else:
                try:
                    medicine_id = medicine_api.add_medicine(name, sn, desc)
                    # 清理测试数据
                    medicine_api.delete_medicine(medicine_id)
                except Exception:
                    pytest.fail(f"有效数据测试失败: {name}, {sn}, {desc}")
