#!/usr/bin/env python3
"""
Simple test script for openpilot
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, '.')

def test_basic_imports():
    """Test basic imports without complex dependencies"""
    print("🧪 Testing basic openpilot imports...")

    try:
        from common.basedir import BASEDIR
        print(f"✅ BASEDIR: {BASEDIR}")
    except Exception as e:
        print(f"❌ BASEDIR failed: {e}")
        return False

    try:
        import cereal.messaging
        print("✅ Cereal messaging imported")

        # Try to get services
        services = cereal.messaging.get_services()
        print(f"✅ Found {len(services)} messaging services")

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

def test_simple_functionality():
    """Test simple functionality"""
    print("\n🚀 Testing simple functionality...")

    try:
        # Test cereal messaging
        import cereal.messaging
        services = cereal.messaging.get_services()

        print("📡 Available services:")
        for i, service in enumerate(list(services.keys())[:10]):
            print(f"  {i+1}. {service}")
        if len(services) > 10:
            print(f"  ... and {len(services) - 10} more services")

        return True

    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("🚗 OPENPILOT SIMPLE TEST")
    print("=" * 50)

    print(f"🔧 Python version: {sys.version.split()[0]}")
    print(f"🔧 Platform: {sys.platform}")
    print(f"🔧 Current directory: {os.getcwd()}")

    # Test basic imports
    if not test_basic_imports():
        print("\n❌ Basic import tests failed.")
        return False

    # Test functionality
    if not test_simple_functionality():
        print("\n❌ Functionality tests failed.")
        return False

    print("\n" + "=" * 50)
    print("✅ BASIC TESTS PASSED!")
    print("🎉 Openpilot core is working!")
    print("=" * 50)

    print("\n📋 Next steps to run full system:")
    print("1. Build system: cd system/manager && python build.py")
    print("2. Run manager: cd system/manager && python manager.py")
    print("3. Or use launcher: ./launch_openpilot.sh")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
