from flask import Flask, request, jsonify, Response
import time
import board
import busio
from adafruit_pca9685 import PCA9685  # type: ignore

import cv2
from picamera2 import Picamera2

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Set up I2C and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Standard for servos

# ✅ Utility function to convert angle to duty cycle
def angle_to_duty(angle):
    pulse_min = 500     # in microseconds
    pulse_max = 2500    # in microseconds
    pulse = pulse_min + (angle / 180.0) * (pulse_max - pulse_min)
    duty = int((pulse / 1000000.0) * 50 * 65535)  # Convert to 16-bit duty cycle
    return duty

# ✅ Servo control endpoint
@app.route('/servo', methods=['GET'])
def move_servo():
    try:
        angle = int(request.args.get('angle', 90))
        channel = int(request.args.get('channel', 0))

        if not (0 <= channel <= 15):
            return jsonify({'status': 'error', 'message': f'Invalid channel: {channel}'})

        duty = angle_to_duty(angle)
        print(f"[INFO] Moving servo on channel {channel} to angle {angle} (duty: {duty})")

        pca.channels[channel].duty_cycle = duty
        time.sleep(0.4)  # Let the servo reach the position
        pca.channels[channel].duty_cycle = 0  # Optional: stop signal

        return jsonify({'status': 'ok', 'angle': angle, 'channel': channel})
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'status': 'error', 'message': str(e)})

# ✅ Set up camera (Picamera2 + OpenCV)
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

# ✅ Video stream generator
def generate_frames():
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# ✅ Video feed endpoint
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ✅ Start Flask server
if __name__ == '__main__':
    print("[INFO] Starting servo & camera server on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)
