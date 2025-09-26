#!/usr/bin/env python3
"""
Simple Alert System - Simplified version of openpilot for alerts only
Connects to phone camera and provides basic road monitoring
"""

import cv2
import numpy as np
import time
import threading
import sys
import os
import argparse
from typing import Union
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, '.')

class SimpleAlertSystem:
    def __init__(self, source: Union[int, str] = 0, draw_lanes: bool = True, detect_motion: bool = True):
        self.camera = None
        self.running = False
        self.alerts = []
        self.frame_count = 0
        self.source: Union[int, str] = source
        self.draw_lanes: bool = draw_lanes
        self.detect_motion: bool = detect_motion

    def connect_camera(self, source: Union[int, str, None] = None):
        """Connect to camera (0 for webcam, or IP for phone camera)"""
        try:
            cam_source: Union[int, str] = self.source if source is None else source

            # Convert numeric strings like "0" to int for local webcam
            if isinstance(cam_source, str) and cam_source.isdigit():
                cam_source = int(cam_source)

            self.camera = cv2.VideoCapture(cam_source)
            if not self.camera.isOpened():
                raise Exception("Cannot open camera")

            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)

            # Optimize for IP streams
            if isinstance(cam_source, str) and cam_source.startswith("http"):
                try:
                    self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                except Exception:
                    pass
                try:
                    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                    self.camera.set(cv2.CAP_PROP_FOURCC, fourcc)
                except Exception:
                    pass

            print(f"✅ Camera connected successfully!")
            return True
        except Exception as e:
            print(f"❌ Camera connection failed: {e}")
            return False

    def _compute_lane_lines(self, frame):
        """Compute lane lines using Canny + Hough and return segmented lines."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50,
                                minLineLength=50, maxLineGap=10)
        return lines

    def detect_lane_departure(self, frame):
        """Simple lane departure detection"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Edge detection
            edges = cv2.Canny(blurred, 50, 150)

            # Detect lines using Hough transform
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50,
                                  minLineLength=50, maxLineGap=10)

            if lines is not None:
                left_lines = []
                right_lines = []

                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 0

                    # Classify lines as left or right based on slope
                    if slope < -0.3:  # Left lane
                        left_lines.append(line[0])
                    elif slope > 0.3:  # Right lane
                        right_lines.append(line[0])

                # Check for lane departure
                height, width = frame.shape[:2]
                center_x = width // 2

                # Simple alert logic
                if len(left_lines) > 0 and len(right_lines) > 0:
                    # Calculate average line positions
                    left_avg = np.mean([line[0] + line[2] for line in left_lines]) / 2
                    right_avg = np.mean([line[0] + line[2] for line in right_lines]) / 2

                    # Check if car is drifting
                    if center_x - left_avg < 50:  # Too close to left lane
                        return "LEFT_LANE_DEPARTURE"
                    elif right_avg - center_x < 50:  # Too close to right lane
                        return "RIGHT_LANE_DEPARTURE"

            return None
        except Exception as e:
            print(f"Lane detection error: {e}")
            return None

    def draw_lane_overlay(self, frame):
        """Draw lane line overlays if detected."""
        if not self.draw_lanes:
            return
        try:
            lines = self._compute_lane_lines(frame)
            if lines is None:
                return
            overlay = frame.copy()
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(overlay, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Blend overlay
            cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        except Exception:
            pass

    def detect_objects(self, frame):
        """Simple object detection for basic alerts"""
        try:
            # Convert to grayscale for motion detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Simple motion detection using frame differencing
            if not hasattr(self, 'prev_frame'):
                self.prev_frame = gray
                return None

            # Calculate frame difference
            diff = cv2.absdiff(self.prev_frame, gray)
            thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]

            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Check for significant motion (potential obstacles)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Threshold for significant motion
                    return "MOTION_DETECTED"

            self.prev_frame = gray
            return None
        except Exception as e:
            print(f"Object detection error: {e}")
            return None

    def play_alert_sound(self, alert_type):
        """Play alert sound (simple beep)"""
        try:
            import winsound
            # Run beep in a background thread to avoid blocking UI
            def _beep(freq, dur):
                try:
                    winsound.Beep(freq, dur)
                except Exception:
                    pass
            if alert_type == "LEFT_LANE_DEPARTURE":
                threading.Thread(target=_beep, args=(800, 200), daemon=True).start()
            elif alert_type == "RIGHT_LANE_DEPARTURE":
                threading.Thread(target=_beep, args=(600, 200), daemon=True).start()
            elif alert_type == "MOTION_DETECTED":
                threading.Thread(target=_beep, args=(1000, 100), daemon=True).start()
        except ImportError:
            print("🔊 BEEP! Alert detected")

    def show_alert_info(self, frame, alert_type):
        """Display alert information on frame"""
        height, width = frame.shape[:2]

        # Alert colors
        colors = {
            "LEFT_LANE_DEPARTURE": (0, 0, 255),    # Red
            "RIGHT_LANE_DEPARTURE": (0, 0, 255),   # Red
            "MOTION_DETECTED": (0, 255, 255)       # Yellow
        }

        # Alert messages
        messages = {
            "LEFT_LANE_DEPARTURE": "⚠️ LEFT LANE DEPARTURE",
            "RIGHT_LANE_DEPARTURE": "⚠️ RIGHT LANE DEPARTURE",
            "MOTION_DETECTED": "⚠️ MOTION DETECTED"
        }

        color = colors.get(alert_type, (255, 255, 255))
        message = messages.get(alert_type, "⚠️ ALERT")

        # Draw alert box
        cv2.rectangle(frame, (10, 10), (width - 10, 80), color, -1)
        cv2.putText(frame, message, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, timestamp, (20, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    def run(self):
        """Main loop"""
        print("🚗 Starting Simple Alert System...")
        print("📱 To connect phone camera, use IP camera app and set source to phone's IP")
        print("💡 Press 'q' to quit, 's' to save screenshot")

        if not self.connect_camera():
            print("❌ Cannot connect to camera. Exiting...")
            return

        self.running = True
        last_alert_time = 0

        try:
            # Improve window handling on Windows
            try:
                cv2.setNumThreads(1)
            except Exception:
                pass
            cv2.namedWindow('Simple Alert System', cv2.WINDOW_NORMAL)

            while self.running:
                ret, frame = self.camera.read()
                if not ret:
                    print("❌ Cannot read from camera")
                    break

                self.frame_count += 1
                current_time = time.time()

                # Detect alerts every few frames to avoid spam
                if self.frame_count % 10 == 0:
                    # Lane departure detection
                    lane_alert = self.detect_lane_departure(frame)
                    if lane_alert and (current_time - last_alert_time) > 2:  # 2 second cooldown
                        self.alerts.append(lane_alert)
                        self.play_alert_sound(lane_alert)
                        self.show_alert_info(frame, lane_alert)
                        last_alert_time = current_time
                        print(f"🚨 {lane_alert} detected!")

                # Object detection
                if self.detect_motion:
                    object_alert = self.detect_objects(frame)
                    if object_alert and (current_time - last_alert_time) > 1:  # 1 second cooldown
                        self.alerts.append(object_alert)
                        self.play_alert_sound(object_alert)
                        self.show_alert_info(frame, object_alert)
                        last_alert_time = current_time
                        print(f"🚨 {object_alert} detected!")

                # Optionally draw lanes on the frame
                self.draw_lane_overlay(frame)

                # Show frame info
                height, width = frame.shape[:2]
                cv2.putText(frame, f"Frame: {self.frame_count}", (10, height - 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, f"Alerts: {len(self.alerts)}", (10, height - 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                # Display frame
                # Resize for stability/perf on some Windows setups
                try:
                    display = cv2.resize(frame, (960, int(960 * height / max(width, 1))))
                except Exception:
                    display = frame
                cv2.imshow('Simple Alert System', display)

                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save screenshot
                    filename = f"alert_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"📸 Screenshot saved: {filename}")

        except KeyboardInterrupt:
            print("\n⏹️ Stopping system...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        print(f"📊 Total alerts detected: {len(self.alerts)}")
        print("👋 Simple Alert System stopped")

def main():
    """Main function"""
    print("=" * 60)
    print("🚗 SIMPLE ALERT SYSTEM - OpenPilot Simplified")
    print("=" * 60)
    print("🎯 Features:")
    print("   • Lane departure detection")
    print("   • Motion/object detection")
    print("   • Audio alerts")
    print("   • Phone camera support")
    print("   • Screenshot capability")
    print()

    # CLI arguments
    parser = argparse.ArgumentParser(description="Simple Alert System (no self-driving)")
    parser.add_argument("--source", default="0", help="Camera source: 0 for webcam or http://IP:PORT/video for IP Webcam")
    parser.add_argument("--no-lanes", action="store_true", help="Disable lane overlay drawing")
    parser.add_argument("--no-motion", action="store_true", help="Disable motion alerts")
    args = parser.parse_args()

    # Check if OpenCV is available
    try:
        import cv2  # noqa: F401
        print("✅ OpenCV detected")
    except ImportError:
        print("❌ OpenCV not found. Installing...")
        os.system("pip install opencv-python")
        print("✅ OpenCV installed. Please restart the script.")
        return

    # Create and run the alert system
    system = SimpleAlertSystem(
        source=args.source,
        draw_lanes=not args.no_lanes,
        detect_motion=not args.no_motion,
    )
    system.run()

if __name__ == "__main__":
    main()
