#!/usr/bin/env python3
"""
One-command launcher for Simple Alert System
Automatically installs dependencies and starts the system
"""

import subprocess
import sys
import os
import argparse

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")

    dependencies = [
        "opencv-python",
        "numpy",
        "pyzmq",
        "pycapnp",
        "tqdm",
        "zstandard"
    ]

    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {dep}")
            return False

    return True

def check_camera_connection():
    """Check if camera is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            return True
        else:
            return False
    except:
        return False

def show_phone_camera_instructions():
    """Show instructions for connecting phone camera"""
    print("\n" + "="*60)
    print("📱 PHONE CAMERA CONNECTION INSTRUCTIONS")
    print("="*60)
    print("To use your phone as a camera:")
    print()
    print("1. Install IP Webcam app on your phone:")
    print("   • Android: IP Webcam (by Pavel Khlebovich)")
    print("   • iOS: EpocCam or similar IP camera app")
    print()
    print("2. Connect phone and computer to same WiFi network")
    print()
    print("3. Start the IP camera app on your phone")
    print()
    print("4. Note the IP address shown in the app (e.g., 192.168.1.100:8080)")
    print()
    print("5. Edit the camera source in the script:")
    print("   Change source=0 to source='http://YOUR_PHONE_IP:8080/video'")
    print()
    print("6. Run the system again")
    print("="*60)

def main():
    """Main launcher function"""
    print("🚗 SIMPLE ALERT SYSTEM LAUNCHER")
    print("=" * 40)

    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required. Current version:", sys.version)
        return

    print(f"✅ Python version: {sys.version.split()[0]}")

    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return

    # Check camera
    print("\n📷 Checking camera connection...")
    if check_camera_connection():
        print("✅ Camera detected")
    else:
        print("⚠️ No camera detected")
        show_phone_camera_instructions()
        response = input("\nContinue anyway? (y/n): ").lower()
        if response != 'y':
            return

    # CLI args
    parser = argparse.ArgumentParser(description="Launch Simple Alert System")
    parser.add_argument("--source", default="0", help="Camera source: 0 for webcam or http://IP:PORT/video for IP Webcam")
    parser.add_argument("--no-lanes", action="store_true", help="Disable lane overlay drawing")
    parser.add_argument("--no-motion", action="store_true", help="Disable motion alerts")
    args = parser.parse_args()

    # Add current directory to Python path
    sys.path.insert(0, os.getcwd())

    print("\n🚀 Starting Simple Alert System...")
    print("💡 Press 'q' to quit, 's' to save screenshot")
    print("⚠️ This system provides alerts only - NO autonomous driving")

    try:
        # Import and run the alert system
        from simple_alert_system import SimpleAlertSystem

        system = SimpleAlertSystem(
            source=args.source,
            draw_lanes=not args.no_lanes,
            detect_motion=not args.no_motion,
        )
        system.run()

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure simple_alert_system.py is in the same directory")
    except Exception as e:
        print(f"❌ Error starting system: {e}")
        print("Please check your camera connection and try again")

if __name__ == "__main__":
    main()
