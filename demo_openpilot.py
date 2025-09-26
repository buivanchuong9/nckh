#!/usr/bin/env python3
"""
Demo script to show openpilot functionality
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, '.')

try:
    # Import basic openpilot modules
    from cereal import messaging
    from common.basedir import BASEDIR
    from common.util import get_git_commit
    from tools.lib.logreader import LogReader

    print("=" * 50)
    print("🚗 OPENPILOT DEMO 🚗")
    print("=" * 50)
    print(f"Base directory: {BASEDIR}")
    print(f"Git commit: {get_git_commit()}")
    print()

    # Show available messaging services
    print("📡 Available messaging services:")
    services = messaging.get_services()
    for service in list(services.keys())[:10]:  # Show first 10
        print(f"  - {service}")
    if len(services) > 10:
        print(f"  ... and {len(services) - 10} more services")
    print()

    # Show some system information
    print("🔧 System Information:")
    print(f"  Python version: {sys.version}")
    print(f"  Platform: {sys.platform}")
    print(f"  Current working directory: {os.getcwd()}")
    print()

    print("✅ Openpilot is successfully imported and ready to use!")
    print("   This is a basic demo. To run the full system, you would need:")
    print("   - Supported hardware (comma 3X device)")
    print("   - Supported vehicle")
    print("   - Proper CAN bus connection")
    print("   - Camera hardware")
    print()
    print("🎯 For full functionality, visit: https://comma.ai/shop")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Some dependencies might be missing. Try installing them with:")
    print("pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")
    print("There was an error running the demo.")

if __name__ == "__main__":
    print("\n🎉 Demo completed!")
