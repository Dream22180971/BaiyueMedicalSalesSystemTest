#!/usr/bin/env python3
"""
BYSMS系统接口测试运行脚本
支持多种运行模式和报告生成
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('test_runner')

def run_tests(test_type, report_format, parallel=False, timeout=None):
    """运行测试"""
    
    # 基础pytest命令
    cmd = [sys.executable, "-m", "pytest", "-v"]
    
    # 添加测试类型标记
    if test_type != "all":
        cmd.extend(["-m", test_type])
    
    # 并行执行
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # 超时设置
    if timeout:
        cmd.extend(["--timeout", str(timeout)])
    
    # 报告格式
    if report_format == "html":
        report_file = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        cmd.extend(["--html", report_file, "--self-contained-html"])
    elif report_format == "allure":
        allure_dir = "reports/allure-results"
        cmd.extend(["--alluredir", allure_dir])
    
    # 添加测试目录
    cmd.append("tests/")
    
    logger.info(f"执行命令: {' '.join(cmd)}")
    
    # 创建报告目录
    os.makedirs("reports", exist_ok=True)
    
    try:
        # 运行测试
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        
        # 输出测试结果
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        return result.returncode
    except Exception as e:
        logger.error(f"测试执行失败: {str(e)}")
        return 1

def generate_allure_report():
    """生成Allure报告"""
    if not os.path.exists("reports/allure-results"):
        logger.error("未找到Allure测试结果，请先运行测试")
        return 1
    
    allure_report_dir = f"reports/allure-report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # 检查allure命令是否可用
    try:
        subprocess.run(["allure", "--version"], check=True, capture_output=True, text=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.error("Allure命令不可用，请确保已安装Allure并添加到环境变量")
        return 1
    
    cmd = ["allure", "generate", "reports/allure-results", "-o", allure_report_dir, "--clean"]
    
    logger.info(f"生成Allure报告: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        
        # 输出结果
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode == 0:
            logger.info(f"Allure报告已生成到: {allure_report_dir}")
            logger.info(f"使用命令打开报告: allure open {allure_report_dir}")
        
        return result.returncode
    except Exception as e:
        logger.error(f"生成Allure报告失败: {str(e)}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="BYSMS系统接口测试运行器")
    parser.add_argument("--type", choices=["all", "smoke", "login", "customer", "regression"], 
                       default="all", help="测试类型")
    parser.add_argument("--report", choices=["console", "html", "allure"], 
                       default="console", help="报告格式")
    parser.add_argument("--parallel", action="store_true", help="并行执行")
    parser.add_argument("--timeout", type=int, help="测试超时时间(秒)")
    parser.add_argument("--generate-allure", action="store_true", help="生成Allure报告")
    
    args = parser.parse_args()
    
    if args.generate_allure:
        return generate_allure_report()
    
    # 运行测试
    return run_tests(
        test_type=args.type,
        report_format=args.report,
        parallel=args.parallel,
        timeout=args.timeout
    )

if __name__ == "__main__":
    sys.exit(main())