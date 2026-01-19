"""
RC Car Raspberry Pi - Configuration

Put all tunable parameters and GPIO pin assignments here.
No loops or hardware setup in this file.
"""

# =========================
# GPIO PIN ASSIGNMENTS
# =========================
ESC_PIN = 21
SERVO_PIN = 18

# Optional relays (set to None if not using)
RELAY_ESC_PIN = 23
RELAY_SERVO_PIN = 24

# Optional ultrasonic sensor (set to None if not using)
TRIG_PIN = 5
ECHO_PIN = 6

# =========================
# PWM SETTINGS
# =========================
PWM_FREQUENCY = 50  # 50Hz for most ESCs/servos

# ESC duty-cycle tuning (you MUST calibrate these for your ESC)
ESC_NEUTRAL = 7.5       # stop/neutral
ESC_SAFE_FORWARD = 8.0  # mild forward speed
ESC_MAX = 8.5           # cap speed for safety (do not exceed 10 on most ESCs)

# =========================
# STEERING
# =========================
# gpiozero Servo uses -1.0..1.0 value
STEER_CENTER = 0.0
STEER_LEFT = -0.6
STEER_RIGHT = 0.6

# =========================
# AUTONOMOUS SAFETY
# =========================
OBSTACLE_STOP_CM = 20.0

# Loop timing
KEY_TIMEOUT = 0.05
CONTROL_DELAY = 0.02

# Controls
EMERGENCY_STOP_KEY = " "   # spacebar
QUIT_KEY = "q"
MANUAL_KEY = "m"

