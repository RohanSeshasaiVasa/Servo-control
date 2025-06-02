
from flask import Flask, request, jsonify, Response
import time
import board
import busio
from adafruit_pca9685 import PCA9685 # type: ignore

import cv2
from picamera2 import Picamera2

# ✅ Define Flask app first
app = Flask(__name__)

# ✅ Set up servo (PCA9685)
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50
SERVO_CHANNEL = 0

def angle_to_duty(angle):
    pulse_min = 500
    pulse_max = 2500
    pulse = pulse_min + (angle / 180.0) * (pulse_max - pulse_min)
    duty = int((pulse / 1000000.0) * 50 * 65535)
    return duty

@app.route('/servo', methods=['GET'])
def move_servo():
    try:
        angle = int(request.args.get('angle', 90))
        channel = int(request.args.get('channel', 0))
        duty = angle_to_duty(angle)
        pca.channels[channel].duty_cycle = duty
        time.sleep(0.4)
        pca.channels[channel].duty_cycle = 0
        return jsonify({'status': 'ok', 'angle': angle, 'channel': channel})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# ✅ Set up camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ✅ Start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
