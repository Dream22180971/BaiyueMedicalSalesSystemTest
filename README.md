# BYSMS系统接口测试框架

基于pytest+requests的BYSMS（白月销售管理系统）接口自动化测试框架。

## 项目概述

本测试框架针对BYSMS系统的API接口进行自动化测试，覆盖登录、客户管理、药品管理、订单管理等核心功能。

### 系统信息
- **被测系统**: BYSMS (白月销售管理系统)
- **测试环境**: http://127.0.0.1:8047
- **接口版本**: API v1.2

## 项目结构

```
ByhyTestSystem/
├── config/                 # 配置文件
│   ├── __init__.py
│   └── config.py          # 测试配置类
├── utils/                 # 工具类
│   ├── __init__.py
│   ├── logger.py          # 日志记录器
│   └── http_client.py     # HTTP客户端封装
├── api/                   # API业务封装
│   ├── __init__.py
│   ├── customer_api.py    # 客户管理API
│   ├── medicine_api.py    # 药品管理API
│   └── order_api.py       # 订单管理API
├── tests/                 # 测试用例
│   ├── __init__.py
│   ├── conftest.py        # pytest配置和夹具
│   ├── test_login.py      # 登录功能测试
│   ├── test_customer.py   # 客户管理测试
│   ├── test_medicine.py   # 药品管理测试
│   └── test_order.py      # 订单管理测试
├── requirements.txt       # 依赖包
├── pytest.ini            # pytest配置
├── .env.example          # 环境变量示例
├── run_tests.py          # 测试运行脚本
├── README.md             # 项目说明
└── BYSMS系统接口测试框架使用指导手册.md  # 使用指导手册
```

## 功能特性

### 测试覆盖范围
- ✅ 登录认证测试
- ✅ 客户管理测试（增删改查、搜索、分页）
- ✅ 药品管理测试（增删改查、搜索、分页）
- ✅ 订单管理测试（增删改查、搜索、分页）

### 框架特性
- **分层架构**: 配置层、工具层、业务层、测试层分离
- **数据驱动**: 支持Faker生成测试数据，边界值测试
- **自动清理**: 测试数据自动创建和清理
- **重试机制**: 网络请求自动重试
- **详细日志**: 完整的测试执行日志
- **多种报告**: 支持HTML、Allure等多种报告格式
- **并行执行**: 支持多进程并行测试

## 快速开始

### 1. 使用指导手册

项目根目录下提供了详细的使用指导手册：
- **BYSMS系统接口测试框架使用指导手册.md**：包含完整的测试框架使用说明、运行方法、问题解决等内容

### 2. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd ByhyTestSystem

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，配置测试环境信息
# BASE_URL=http://127.0.0.1:8047
# ADMIN_USERNAME=byhy
# ADMIN_PASSWORD=88888888
```

### 3. 运行测试

```bash
# 运行所有测试
python run_tests.py

# 运行冒烟测试
python run_tests.py --type smoke

# 运行客户管理测试
python run_tests.py --type customer

# 并行执行测试
python run_tests.py --parallel

# 生成HTML报告
python run_tests.py --report html

# 生成Allure报告
python run_tests.py --report allure
python run_tests.py --generate-allure
```

### 4. 使用pytest直接运行

```bash
# 运行所有测试
pytest

# 运行标记为smoke的测试
pytest -m smoke

# 运行特定模块的测试
pytest tests/test_customer.py

# 生成HTML报告
pytest --html=reports/report.html --self-contained-html

# 并行执行
pytest -n auto
```

## 测试用例设计

### 登录测试 (test_login.py)
- 正常登录成功
- 错误密码登录失败
- 错误用户名登录失败
- 空凭证登录失败
- 特殊字符登录失败
- 超长凭证登录失败
- 响应格式验证
- 会话保持测试

### 客户管理测试 (test_customer.py)
- 客户列表获取
- 添加客户成功/失败
- 修改客户信息
- 删除客户
- 分页功能测试
- 搜索功能测试
- 字段验证测试
- 边界值测试

### 药品管理测试 (test_medicine.py)
- 药品列表获取
- 添加药品成功/失败
- 修改药品信息
- 删除药品
- 分页功能测试
- 搜索功能测试
- 字段验证测试
- 边界值测试

### 订单管理测试 (test_order.py)
- 订单列表获取
- 添加订单成功/失败
- 删除订单
- 分页功能测试
- 订单存在性检查
- 字段验证测试

## 测试数据管理

框架使用pytest fixtures和Faker库动态生成测试数据：

### 1. 测试数据生成
- 使用Faker库生成真实的测试数据
- 测试数据自动创建和清理
- 确保测试数据的唯一性

### 2. Fixtures管理
在`conftest.py`中定义了多个fixtures：
- `test_customer_data`: 生成客户测试数据
- `test_medicine_data`: 生成药品测试数据
- `test_order_data`: 生成订单测试数据
- `created_customer`: 创建测试客户并自动清理
- `created_medicine`: 创建测试药品并自动清理
- `created_order`: 创建测试订单并自动清理

### 3. 数据隔离
- 每个测试用例使用独立的测试数据
- 测试结束后自动清理测试数据
- 避免测试数据之间的干扰

## 配置说明

### 环境变量 (.env)
```ini
# 基础配置
BASE_URL=http://127.0.0.1:8047
API_PREFIX=/api/mgr

# 管理员账号
ADMIN_USERNAME=byhy
ADMIN_PASSWORD=88888888

# 测试配置
TEST_TIMEOUT=30
MAX_RETRIES=3
LOG_LEVEL=INFO
```

### pytest配置 (pytest.ini)
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers -n auto
markers =
    smoke: 冒烟测试
    regression: 回归测试
    api: API接口测试
    customer: 客户管理测试
    medicine: 药品管理测试
    order: 订单管理测试
    login: 登录测试
filterwarnings =
    ignore::DeprecationWarning
```

## CI/CD集成

### GitHub Actions 示例
```yaml
name: BYSMS API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python run_tests.py --parallel --report html
    
    - name: Upload test results
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: reports/
```

## 测试报告

### HTML报告
![HTML报告示例](docs/html-report.png)

### Allure报告
```bash
# 生成Allure报告
allure generate reports/allure-results -o reports/allure-report --clean

# 打开报告
allure open reports/allure-report
```

## 故障排除

### 常见问题

1. **连接被拒绝**
   - 检查BASE_URL配置是否正确
   - 确认被测系统是否启动

2. **登录失败**
   - 检查ADMIN_USERNAME和ADMIN_PASSWORD
   - 确认账号没有被锁定

3. **测试数据冲突**
   - 框架会自动清理测试数据
   - 如遇冲突，可手动清理测试环境

### 调试模式
```bash
# 设置详细日志
LOG_LEVEL=DEBUG pytest -v

# 查看请求详情
# 在utils/http_client.py中启用详细日志
```

## 扩展开发

### 添加新的API模块
1. 在`api/`目录下创建新的API类
2. 实现对应的CRUD操作方法
3. 在`tests/`目录下创建测试用例
4. 在`conftest.py`中添加对应的fixture

### 添加新的测试类型
1. 在`pytest.ini`中注册新的marker
2. 在测试用例中使用对应的marker装饰器
3. 在`run_tests.py`中添加对应的测试类型

## 贡献指南

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证。

## 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your-email@example.com]
- 项目地址: [GitHub Repository URL]

---

## 版本来源

本测试框架基于白月黑羽的 BYSMS 系统需求文档：
[BYSMS系统 需求1.0 - 白月黑羽](https://www.byhy.net/py/django/req_1/)

**说明**：此项目仅为演示分享，用于学习和交流接口测试框架的设计与实现。

**注意**: 请确保在运行测试前，BYSMS系统已正确部署并运行在指定端口。