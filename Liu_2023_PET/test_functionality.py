#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to verify all Liu_2023_PET functionality."""

import math
import os

def test_imports():
    """Test that all modules can be imported."""
    try:
        from ep_veg import ep_pm_rc, ep_yang, ep_veg
        from ep_veg import estimate_g1, estimate_Aww
        from ep_veg.budyko import budyko_evaporation, budyko_runoff
        from ep_veg.parameters import psychrometric_constant_kpa_per_C, latent_heat_MJ_per_kg
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_calculations():
    """Test basic EP calculations."""
    try:
        from ep_veg import ep_pm_rc, ep_yang, ep_veg
        from ep_veg import estimate_g1, estimate_Aww
        
        # Test parameters
        T=20; Rn=15; U2=2; VPD=1.5; LAI=3.0; Ca=420
        
        # Parameter estimates
        g1 = estimate_g1(T_C_mean_above0=15.0, MI=1.0, log_base="ln")
        Aww = estimate_Aww(Ca_ppm=Ca)
        
        # EP calculations
        eto = ep_pm_rc(T, Rn, U2, VPD)
        epy = ep_yang(T, Rn, U2, VPD, Ca_ppm=Ca)
        epv = ep_veg(T, Rn, U2, VPD, LAI, Ca, Aww_μmol_m2_s=Aww, g1_kPa05=g1)
        
        # Verify results
        assert eto > 0 and epy > 0 and epv > 0
        assert math.isfinite(eto) and math.isfinite(epy) and math.isfinite(epv)
        assert g1 > 0 and Aww > 0
        
        print(f"✅ Basic calculations successful (ETo: {eto:.2f}, EPy: {epy:.2f}, EPv: {epv:.2f})")
        return True
    except Exception as e:
        print(f"❌ Basic calculations failed: {e}")
        return False

def test_budyko_functionality():
    """Test Budyko framework functionality."""
    try:
        from ep_veg.budyko import budyko_evaporation, budyko_runoff
        
        # Test with synthetic values
        P = 100.0  # mm/d precipitation
        EP = 80.0  # mm/d potential evapotranspiration
        n = 1.9    # Budyko parameter
        
        E = budyko_evaporation(P, EP, n=n)
        Q = budyko_runoff(P, EP, n=n)
        
        # Verify water balance: P = E + Q
        assert abs(P - (E + Q)) < 1e-6
        assert E > 0 and Q > 0
        
        print(f"✅ Budyko functionality successful (E: {E:.2f}, Q: {Q:.2f})")
        return True
    except Exception as e:
        print(f"❌ Budyko functionality failed: {e}")
        return False

def test_parameter_functions():
    """Test parameter calculation functions."""
    try:
        from ep_veg.parameters import psychrometric_constant_kpa_per_C, latent_heat_MJ_per_kg
        
        # Test psychrometric constant
        gamma = psychrometric_constant_kpa_per_C(P_kPa=101.3)
        assert gamma > 0
        
        # Test latent heat
        lambda_val = latent_heat_MJ_per_kg(T_C=20.0)
        assert lambda_val > 0
        
        print(f"✅ Parameter functions successful (γ: {gamma:.4f}, λ: {lambda_val:.2f})")
        return True
    except Exception as e:
        print(f"❌ Parameter functions failed: {e}")
        return False

def test_example_script():
    """Test the example script execution."""
    try:
        import subprocess
        import sys
        
        # Change to examples directory and run script
        os.chdir("examples")
        result = subprocess.run([sys.executable, "run_quick_demo.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            # Check if files were created
            os.chdir("..")
            if (os.path.exists("figures/ep_models_timeseries.png") and 
                os.path.exists("figures/runoff_timeseries.png") and
                os.path.exists("figures/synthetic_daily_dataset.csv")):
                print("✅ Example script successful")
                return True
            else:
                print("❌ Example script ran but didn't create expected files")
                return False
        else:
            print(f"❌ Example script failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Example script test failed: {e}")
        return False

def main():
    print("Testing Liu_2023_PET (ep_veg) package functionality...")
    print("=" * 60)
    
    tests = [
        ("Import test", test_imports),
        ("Basic calculations test", test_basic_calculations),
        ("Budyko functionality test", test_budyko_functionality),
        ("Parameter functions test", test_parameter_functions),
        ("Example script test", test_example_script)
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