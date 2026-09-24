Run a complete API regression suite with one command using pytest and requests. / 基于 pytest + requests，一条命令跑完整套 API 回归测试。

<!-- README-V2-BILINGUAL -->

# BaiyueMedicalSalesSystemTest

> **EN:** Run a complete API regression suite with one command using pytest and requests.  
> **中文：** 基于 pytest + requests，一条命令跑完整套 API 回归测试。

## Demo / 演示

CLI/test-report demo GIF is not yet stored in this repo. / 当前仓库尚未存放 CLI 或测试报告 GIF。

## Quick Start / 5 分钟快速开始

```bash
git clone https://github.com/Dream22180971/BaiyueMedicalSalesSystemTest.git
cd BaiyueMedicalSalesSystemTest
python -m venv venv
pip install -r requirements.txt
python run_tests.py
```

> **EN:** The commands above are intentionally kept short: clone, install, run. Project-specific configuration and advanced usage stay in the detailed documentation below.  
> **中文：** 上面的命令刻意保持最短路径：克隆、安装、运行。项目特定配置与高级用法继续保留在下方详细文档中。

## Why this project / 为什么做这个项目

**EN:** This repository is built around one concrete problem and aims to be understandable, runnable and useful before becoming complex.

**中文：** 这个仓库围绕一个明确问题构建，优先做到易理解、能运行、真正有用，再逐步增加复杂能力。

---

<!-- ORIGINAL-DOCS -->
# BYSMS 接口自动化测试框架

> 一行命令跑完所有 API 测试——基于 pytest + requests，自动清理数据，支持并行和多种报告。

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python)](https://python.org)
[![pytest](https://img.shields.io/badge/pytest-7.x-0A9EDC?style=flat)](https://pytest.org)

---

## 目录

- [它是什么](#它是什么)
- [为什么做](#为什么做)
- [核心功能](#核心功能)
- [快速开始](#快速开始)
- [测试覆盖](#测试覆盖)
- [技术架构](#技术架构)
- [FAQ](#faq)
- [谁适合用](#谁适合用)
- [关于我](#关于我)

---

## 它是什么

一个**销售管理系统 API 自动化测试框架**，帮你做三件事：

1. **自动测接口**：登录、客户管理、药品管理、订单管理，全部覆盖
2. **自动清理数据**：测试完自动删掉创建的数据，不影响环境
3. **多种报告**：HTML 报告、Allure 报告、并行执行，一行命令搞定

不需要手动写测试脚本，框架已经帮你搭好了分层架构。

---

## 为什么做

手工测 API 接口太累了——每次发版都要手动测一遍登录、CRUD、分页、搜索，重复劳动而且容易漏。

写测试脚本又太麻烦——每个项目都要从零搭框架、封装 HTTP 请求、处理登录态、管理测试数据。

这个框架的思路：**把重复的活交给机器**。你只需要维护测试用例，框架帮你跑、帮你清理、帮你出报告。

---

## 核心功能

| 你能做什么 | 说明 |
|-----------|------|
| **一键运行** | `python run_tests.py` 跑完所有接口测试 |
| **按类型跑** | 冒烟测试、客户管理、药品管理、订单管理，单独跑 |
| **并行执行** | `--parallel` 多进程并行，加快速度 |
| **自动清理** | 测试数据自动创建和清理，不影响环境 |
| **多种报告** | HTML / Allure / 控制台，按需选择 |
| **数据驱动** | Faker 生成测试数据，边界值自动覆盖 |

---

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/Dream22180971/BaiyueMedicalSalesSystem.git
cd BaiyueMedicalSalesSystem

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate  # Linux/Mac

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env，填入测试环境地址和账号

# 5. 跑测试
python run_tests.py
```

### 常用命令

```bash
# 冒烟测试
python run_tests.py --type smoke

# 只跑客户管理
python run_tests.py --type customer

# 并行执行
python run_tests.py --parallel

# 生成 HTML 报告
python run_tests.py --report html

# 生成 Allure 报告
python run_tests.py --report allure
```

---

## 测试覆盖

| 模块 | 测试内容 |
|------|----------|
| **登录** | 正常登录、错误密码、空凭证、特殊字符、超长凭证、会话保持 |
| **客户管理** | 增删改查、搜索、分页、字段验证、边界值 |
| **药品管理** | 增删改查、搜索、分页、字段验证、边界值 |
| **订单管理** | 增删改查、搜索、分页、字段验证、订单存在性检查 |

---

## 技术架构

```
┌──────────────────────────────────┐
│     测试运行层                    │
│  pytest · run_tests.py           │
├──────────────────────────────────┤
│     业务封装层 (api/)             │
│  customer_api · medicine_api     │
│  order_api                       │
├──────────────────────────────────┤
│     工具层 (utils/)              │
│  http_client · logger            │
├──────────────────────────────────┤
│     配置层 (config/)             │
│  .env · config.py                │
├──────────────────────────────────┤
│     被测系统                     │
│  BYSMS (白月销售管理系统)         │
└──────────────────────────────────┘
```

**分层设计**：配置层 → 工具层 → 业务层 → 测试层，每层职责清晰，加新接口只需加一层。

---

## FAQ

**Q: 被测系统从哪来？**
A: 基于白月黑羽的 BYSMS 系统，需要自行部署到本地 8047 端口。

**Q: 测试数据会冲突吗？**
A: 不会。框架使用 pytest fixtures 动态生成数据，测试结束后自动清理。

**Q: 怎么加新接口测试？**
A: 在 `api/` 目录加 API 类，在 `tests/` 目录加测试用例，在 `conftest.py` 加 fixture。

**Q: 支持 CI/CD 吗？**
A: 支持。README 中有 GitHub Actions 示例，也可以集成到 Jenkins 等平台。

---

## 谁适合用

- **测试工程师**：学习接口自动化框架的设计与实现
- **Python 学习者**：pytest + requests + fixtures 的实战案例
- **正在做毕设的学生**：自动化测试方向的参考项目
- **想搭测试框架的人**：直接拿去改，省掉从零搭建的时间

---

## 关于我

我是**肖恩沃尔特**（Sean Walter），一个从测试工程师正在转型为 AI 独立开发者的程序员。

这个框架是我做接口测试时的产物——与其每次手动测，不如搭个框架让机器跑。

- GitHub: [Dream22180971](https://github.com/Dream22180971)
- Twitter/X: [@sean_walter0717](https://x.com/sean_walter0717)
- 博客: [seanwalter.top](https://seanwalter.top)

---

## License

[MIT](./LICENSE)
