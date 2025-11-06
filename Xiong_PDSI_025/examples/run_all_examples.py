#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行所有示例脚本并生成图片 / Run all example scripts and generate figures
"""
import subprocess
import sys
import os

def run_script(script_name):
    """运行单个示例脚本"""
    print(f"运行 {script_name}...")
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {script_name} 运行成功")
        else:
            print(f"❌ {script_name} 运行失败:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ 运行 {script_name} 时出错: {e}")

def main():
    print("开始运行所有 PDSI 示例脚本...")
    print("=" * 50)
    
    # 运行示例脚本
    scripts = [
        "01_quickstart_synthetic.py",
        "02_spatial_timeseries_and_trends.py"
    ]
    
    for script in scripts:
        if os.path.exists(script):
            run_script(script)
        else:
            print(f"⚠️  脚本 {script} 不存在")
    
    print("=" * 50)
    print("检查生成的图片...")
    
    # 检查生成的图片
    expected_files = [
        "figures/example_timeseries.png",
        "figures/example_map_mean.png", 
        "figures/example_trend.png",
        "figures/example_corr.png"
    ]
    
    for file_path in expected_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 已生成")
        else:
            print(f"❌ {file_path} 未找到")
    
    print("=" * 50)
    print("所有示例脚本运行完成!")

if __name__ == "__main__":
    main()