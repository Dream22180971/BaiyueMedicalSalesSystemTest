# BYSMS 系统接口测试框架使用指导手册

## 版本来源

本测试框架基于白月黑羽的 BYSMS 系统需求文档：
[BYSMS系统 需求1.0 - 白月黑羽](https://www.byhy.net/py/django/req_1/)

**说明**：此项目仅为演示分享，用于学习和交流接口测试框架的设计与实现。

## 1. 环境准备

### 1.1 系统要求
- Windows 10/11 操作系统
- Python 3.8 及以上版本
- BYSMS 系统服务（运行在 http://127.0.0.1:8047）

### 1.2 安装依赖
1. 打开命令提示符（CMD）或 PowerShell
2. 切换到项目目录：
   ```
   cd d:\MyCodingProject\ByhyTestSystem
   ```
3. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```

## 2. 测试框架结构

```
ByhyTestSystem/
├── api/                # API 封装模块
│   ├── customer_api.py # 客户管理 API
│   ├── medicine_api.py # 药品管理 API
│   └── order_api.py    # 订单管理 API
├── config/             # 配置文件
│   └── config.py       # 测试配置
├── tests/              # 测试用例
│   ├── conftest.py     # 测试 fixtures
│   ├── test_customer.py # 客户管理测试
│   ├── test_medicine.py # 药品管理测试
│   ├── test_order.py   # 订单管理测试
│   └── test_login.py   # 登录测试
├── utils/              # 工具模块
│   ├── http_client.py  # HTTP 客户端
│   └── logger.py       # 日志工具
├── pytest.ini          # pytest 配置文件
├── requirements.txt    # 依赖包列表
└── run_tests.py        # 测试运行脚本
```

## 3. 运行测试

### 3.1 运行完整测试套件
```
python -m pytest -v
```

### 3.2 运行特定模块测试
- 运行登录测试：
  ```
python -m pytest tests/test_login.py -v
  ```
- 运行客户管理测试：
  ```
python -m pytest tests/test_customer.py -v
  ```
- 运行药品管理测试：
  ```
python -m pytest tests/test_medicine.py -v
  ```
- 运行订单管理测试：
  ```
python -m pytest tests/test_order.py -v
  ```

### 3.3 使用标记运行测试
- 运行冒烟测试：
  ```
python -m pytest -m smoke -v
  ```
- 运行回归测试：
  ```
python -m pytest -m regression -v
  ```
- 运行 API 测试：
  ```
python -m pytest -m api -v
  ```

### 3.4 使用运行脚本
1. 运行冒烟测试并生成 HTML 报告：
   ```
python run_tests.py --type smoke --report html
   ```
2. 运行所有测试并生成 Allure 报告：
   ```
python run_tests.py --type all --report allure
   ```

## 4. 测试结果分析

### 4.1 命令行输出
- 绿色 `PASSED` 表示测试通过
- 红色 `FAILED` 表示测试失败
- 黄色 `ERROR` 表示测试错误

### 4.2 HTML 报告
- 生成位置：`reports/` 目录
- 打开方式：用浏览器打开 `reports/report_*.html` 文件

### 4.3 Allure 报告
1. 生成报告文件：
   ```
python run_tests.py --type all --report allure
   ```
2. 启动 Allure 服务：
   ```
allure serve reports/allure-results
   ```
3. 在浏览器中查看报告

## 5. 测试数据管理

- 测试数据由 `conftest.py` 中的 fixtures 自动生成
- 测试结束后会自动清理测试数据
- 无需手动管理测试数据

## 6. 常见问题解决

### 6.1 测试失败
- 检查 BYSMS 系统是否正常运行
- 检查网络连接是否正常
- 查看测试日志了解具体失败原因

### 6.2 依赖包安装失败
- 确保 pip 版本是最新的：`pip install --upgrade pip`
- 检查网络连接是否正常
- 尝试使用国内镜像源：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

### 6.3 端口占用
- 确保 BYSMS 系统运行在 8047 端口
- 检查是否有其他程序占用 8047 端口

## 7. 测试用例编写指南

### 7.1 新增测试用例
1. 在 `tests/` 目录下创建新的测试文件，命名为 `test_*.py`
2. 继承 `Test*` 类
3. 使用 `@pytest.mark` 标记测试类型
4. 使用 fixtures 获取测试数据和 API 实例

### 7.2 测试用例结构
```python
import pytest

class TestExample:
    @pytest.mark.smoke
    def test_example(self, api_instance):
        # 测试步骤
        # 断言
        pass
```

## 8. 注意事项

1. 确保 BYSMS 系统在测试前已启动
2. 测试过程中不要手动操作 BYSMS 系统
3. 测试完成后检查测试数据是否已清理
4. 定期更新测试用例以适应系统变化

## 9. 联系支持

如果遇到问题，请联系测试团队或查看项目文档。

---

本指导手册旨在帮助新人快速上手 BYSMS 系统的接口测试框架，随着系统的演进，本手册会不断更新。