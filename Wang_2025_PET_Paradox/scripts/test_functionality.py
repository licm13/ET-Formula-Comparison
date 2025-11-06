#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to verify all Wang_2025_PET_Paradox functionality."""

import os
import sys

def test_imports():
    """Test that all modules can be imported."""
    try:
        from paradoxes_pet.data import generate_synthetic_monthly
        from paradoxes_pet.pet import pm_rc_pet_mm_day, pm_rc_pet_yang_mm_day, pm_rc_pet_jarvis_mm_day
        from paradoxes_pet.indices import annual_aridity_index, toy_pdsi_like, drought_extent_and_frequency
        from paradoxes_pet.plotting import set_cn_en_fonts
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_data_generation():
    """Test synthetic data generation."""
    try:
        from paradoxes_pet.data import generate_synthetic_monthly
        df = generate_synthetic_monthly(seed=42)
        assert len(df) > 0
        assert "P_mm" in df.columns
        assert "Ta_C" in df.columns
        print("✅ Data generation successful")
        return True
    except Exception as e:
        print(f"❌ Data generation failed: {e}")
        return False

def test_pet_calculations():
    """Test PET calculations."""
    try:
        from paradoxes_pet.data import generate_synthetic_monthly
        from paradoxes_pet.pet import pm_rc_pet_mm_day
        
        df = generate_synthetic_monthly(seed=42)
        pet = pm_rc_pet_mm_day(df["Ta_C"], df["Rn_star_MJ_m2_day"], df["VPD_kPa"], df["WS2_m_s"])
        assert len(pet) == len(df)
        assert all(pet > 0)  # PET should be positive
        print("✅ PET calculations successful")
        return True
    except Exception as e:
        print(f"❌ PET calculations failed: {e}")
        return False

def test_font_setup():
    """Test font configuration."""
    try:
        from paradoxes_pet.plotting import set_cn_en_fonts
        font_name = set_cn_en_fonts()
        print(f"✅ Font setup successful: {font_name}")
        return True
    except Exception as e:
        print(f"❌ Font setup failed: {e}")
        return False

def main():
    print("Testing Wang_2025_PET_Paradox package functionality...")
    print("=" * 60)
    
    tests = [
        ("Import test", test_imports),
        ("Data generation test", test_data_generation), 
        ("PET calculations test", test_pet_calculations),
        ("Font setup test", test_font_setup)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
    
    print("=" * 60)
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! Package is fully functional.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()