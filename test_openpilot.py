#!/usr/bin/env python3
"""
Test script to verify openpilot installation and basic functionality
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, '.')

def test_imports():
    """Test basic imports"""
    print("🧪 Testing openpilot imports...")

    try:
        from common.basedir import BASEDIR
        print(f"✅ BASEDIR: {BASEDIR}")
    except Exception as e:
        print(f"❌ BASEDIR import failed: {e}")
        return False

    try:
        from common.git import get_commit
        commit = get_commit()
        print(f"✅ Git commit: {commit}")
    except Exception as e:
        print(f"❌ Git commit failed: {e}")
        return False

    try:
        import cereal.messaging
        print("✅ Cereal messaging imported")
    except Exception as e:
        print(f"❌ Cereal messaging failed: {e}")
        return False

    try:
        from tools.lib.logreader import LogReader
        print("✅ LogReader imported")
    except Exception as e:
        print(f"❌ LogReader failed: {e}")
        return False

    return True

def test_system_info():
    """Test system information"""
    print("\n🔧 System Information:")
    print(f"  Python version: {sys.version}")
    print(f"  Platform: {sys.platform}")
    print(f"  Current directory: {os.getcwd()}")
    print(f"  PYTHONPATH: {sys.path[0] if sys.path else 'Not set'}")

def test_simple_functionality():
    """Test simple functionality"""
    print("\n🚀 Testing simple functionality...")

    try:
        # Test cereal messaging
        import cereal.messaging
        services = cereal.messaging.get_services()
        print(f"✅ Found {len(services)} messaging services")

        # Show some services
        for i, service in enumerate(list(services.keys())[:5]):
            print(f"  - {service}")
        if len(services) > 5:
            print(f"  ... and {len(services) - 5} more")

    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

    return True

def main():
    """Main test function"""
    print("=" * 60)
    print("🚗 OPENPILOT INSTALLATION TEST")
    print("=" * 60)

    # Test system info
    test_system_info()

    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Check dependencies.")
        return False

    # Test functionality
    if not test_simple_functionality():
        print("\n❌ Functionality tests failed.")
        return False

    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("🎉 Openpilot is ready to use!")
    print("=" * 60)

    print("\n📋 Next steps:")
    print("1. To run the full system: python system/manager/manager.py")
    print("2. To run tools: python tools/replay/ui.py")
    print("3. To run tests: python -m pytest")
    print("4. For development: check docs/CONTRIBUTING.md")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
