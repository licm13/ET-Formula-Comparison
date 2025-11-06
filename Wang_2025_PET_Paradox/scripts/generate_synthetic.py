
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate synthetic monthly climate data and save to CSV.
生成合成月尺度气候数据并保存为 CSV。
"""
import os
from paradoxes_pet.data import generate_synthetic_monthly

def main():
    df = generate_synthetic_monthly(seed=42)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/synthetic_climate.csv")
    print("Saved -> data/synthetic_climate.csv")

if __name__ == "__main__":
    main()
