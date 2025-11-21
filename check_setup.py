"""
Setup Checker Script
Run this to verify your setup before running the application.
"""
import sys

def check_setup():
    print("═" * 60)
    print("   Movie & TV Shows Browser - Setup Checker")
    print("═" * 60)
    print()
    
    # Check Python version
    print("✓ Checking Python version...")
    if sys.version_info >= (3, 7):
        print(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor} (OK)")
    else:
        print(f"  ✗ Python {sys.version_info.major}.{sys.version_info.minor} (Need 3.7+)")
        return False
    print()
    
    # Check dependencies
    print("✓ Checking dependencies...")
    dependencies = {
        'requests': 'requests',
        'PIL': 'Pillow',
        'tkinter': 'tkinter (built-in)'
    }
    
    missing = []
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    print()
    
    if missing:
        print("⚠ Missing packages detected!")
        print(f"  Run: pip install {' '.join([p for p in missing if 'built-in' not in p])}")
        print()
    
    # Check config file
    print("✓ Checking configuration...")
    try:
        from config import TMDB_API_KEY
        if TMDB_API_KEY == "YOUR_TMDB_API_KEY_HERE":
            print("  ⚠ TMDb API key not configured")
            print("  → Edit config.py and add your API key")
            print("  → Get it from: https://www.themoviedb.org/settings/api")
        else:
            print("  ✓ API key configured")
    except Exception as e:
        print(f"  ✗ Error reading config: {e}")
    print()
    
    # Check database module
    print("✓ Checking database...")
    try:
        from database.db import create_users_table
        print("  ✓ Database module OK")
    except Exception as e:
        print(f"  ✗ Database error: {e}")
    print()
    
    # Summary
    print("═" * 60)
    if not missing and TMDB_API_KEY != "YOUR_TMDB_API_KEY_HERE":
        print("✅ Setup complete! Run: python login.py")
    else:
        print("⚠ Please complete the setup steps above")
    print("═" * 60)

if __name__ == "__main__":
    check_setup()
