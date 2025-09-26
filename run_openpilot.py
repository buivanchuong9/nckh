#!/usr/bin/env python3
"""
Simple launcher for openpilot tools and components
"""

import sys
import os
import subprocess

# Add current directory to Python path
sys.path.insert(0, '.')

def setup_environment():
    """Setup environment variables"""
    os.environ['PYTHONPATH'] = os.getcwd()
    print(f"✅ PYTHONPATH set to: {os.getcwd()}")

def show_menu():
    """Show available options"""
    print("=" * 60)
    print("🚗 OPENPILOT LAUNCHER")
    print("=" * 60)
    print("Available options:")
    print()
    print("1. 🧪 Run tests")
    print("2. 📊 Run log reader tools")
    print("3. 🎮 Run simulation")
    print("4. 🔧 Run system manager (advanced)")
    print("5. 📱 Run phone camera demo")
    print("6. 🚀 Run simple alert system")
    print("7. ❌ Exit")
    print()

def run_tests():
    """Run openpilot tests"""
    print("🧪 Running openpilot tests...")
    try:
        result = subprocess.run([sys.executable, "simple_test.py"],
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"❌ Test failed: {e}")

def run_log_tools():
    """Run log reader tools"""
    print("📊 Running log reader tools...")
    try:
        # Try to run a simple log reader demo
        code = """
import sys
sys.path.insert(0, '.')
from tools.lib.logreader import LogReader
print('✅ LogReader is working!')
print('📋 LogReader can be used to read openpilot log files')
print('💡 Example: LogReader(path_to_log_file)')
"""
        exec(code)
    except Exception as e:
        print(f"❌ Log tools failed: {e}")

def run_simulation():
    """Run simulation"""
    print("🎮 Running simulation...")
    try:
        if os.path.exists("tools/sim/run_bridge.py"):
            print("🎯 Starting simulation bridge...")
            print("💡 This will start a simulated driving environment")
            # For now, just show info
            print("📋 Simulation files found:")
            print("  - tools/sim/run_bridge.py")
            print("  - tools/sim/lib/")
            print("💡 To run full simulation, use: python tools/sim/run_bridge.py")
        else:
            print("❌ Simulation files not found")
    except Exception as e:
        print(f"❌ Simulation failed: {e}")

def run_system_manager():
    """Run system manager (advanced)"""
    print("🔧 System manager requires:")
    print("  - Hardware support (comma device)")
    print("  - Proper build environment")
    print("  - System-level permissions")
    print()
    print("⚠️ This is for advanced users only")
    print("💡 For development, use simulation instead")

def run_phone_camera_demo():
    """Run phone camera demo"""
    print("📱 Running phone camera demo...")
    try:
        if os.path.exists("simple_alert_system.py"):
            subprocess.run([sys.executable, "simple_alert_system.py"])
        else:
            print("❌ Phone camera demo not found")
    except Exception as e:
        print(f"❌ Phone camera demo failed: {e}")

def run_simple_alert():
    """Run simple alert system"""
    print("🚀 Running simple alert system...")
    try:
        if os.path.exists("start_alert_system.py"):
            subprocess.run([sys.executable, "start_alert_system.py"])
        else:
            print("❌ Simple alert system not found")
    except Exception as e:
        print(f"❌ Simple alert system failed: {e}")

def main():
    """Main launcher function"""
    setup_environment()

    while True:
        show_menu()
        try:
            choice = input("Enter your choice (1-7): ").strip()

            if choice == '1':
                run_tests()
            elif choice == '2':
                run_log_tools()
            elif choice == '3':
                run_simulation()
            elif choice == '4':
                run_system_manager()
            elif choice == '5':
                run_phone_camera_demo()
            elif choice == '6':
                run_simple_alert()
            elif choice == '7':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-7.")

            input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
