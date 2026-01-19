import time
import RPi.GPIO as GPIO
from gpiozero import Servo

from .config import (
    ESC_PIN, SERVO_PIN,
    RELAY_ESC_PIN, RELAY_SERVO_PIN,
    TRIG_PIN, ECHO_PIN,
    PWM_FREQUENCY,
    ESC_NEUTRAL, ESC_MAX
)


class Hardware:
    def __init__(self):
        self.pwm_esc = None
        self.servo = None

    # -------------------------
    # Setup / Cleanup
    # -------------------------
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # ESC PWM
        GPIO.setup(ESC_PIN, GPIO.OUT)
        self.pwm_esc = GPIO.PWM(ESC_PIN, PWM_FREQUENCY)
        self.pwm_esc.start(0)

        # Relays (optional)
        if RELAY_ESC_PIN is not None:
            GPIO.setup(RELAY_ESC_PIN, GPIO.OUT)
        if RELAY_SERVO_PIN is not None:
            GPIO.setup(RELAY_SERVO_PIN, GPIO.OUT)

        # Ultrasonic (optional)
        if TRIG_PIN is not None and ECHO_PIN is not None:
            GPIO.setup(TRIG_PIN, GPIO.OUT)
            GPIO.setup(ECHO_PIN, GPIO.IN)
            GPIO.output(TRIG_PIN, GPIO.LOW)

        # Steering servo (gpiozero)
        self.servo = Servo(
            SERVO_PIN,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )

        print("[INIT] Hardware initialized.")

    def cleanup(self):
        try:
            self.stop_motor()
        except Exception:
            pass
        GPIO.cleanup()

    # -------------------------
    # ESC / Motor
    # -------------------------
    def set_throttle_duty(self, duty: float):
        duty = max(ESC_NEUTRAL, min(duty, ESC_MAX))
        self.pwm_esc.ChangeDutyCycle(duty)

    def stop_motor(self):
        self.set_throttle_duty(ESC_NEUTRAL)

    def arm_esc(self):
        """
        Basic arming sequence (may vary by ESC).
        """
        print("[ESC] Arming...")
        self.set_throttle_duty(ESC_MAX)
        time.sleep(2.0)
        self.set_throttle_duty(ESC_NEUTRAL)
        time.sleep(2.0)
        print("[ESC] Armed.")

    # -------------------------
    # Steering
    # -------------------------
    def steer(self, value: float):
        """
        gpiozero Servo value: -1.0 (left) .. 0 (center) .. +1.0 (right)
        """
        value = max(-1.0, min(value, 1.0))
        self.servo.value = value

    # -------------------------
    # Relays / Mode Switching
    # -------------------------
    def set_relays_manual(self):
        """
        Relays OFF = RC receiver controls (Layer 1).
        If you don't use relays, this does nothing.
        """
        if RELAY_ESC_PIN is not None:
            GPIO.output(RELAY_ESC_PIN, GPIO.LOW)
        if RELAY_SERVO_PIN is not None:
            GPIO.output(RELAY_SERVO_PIN, GPIO.LOW)

    def set_relays_auto(self):
        """
        Relays ON = Pi controls (Layer 2).
        If you don't use relays, this does nothing.
        """
        if RELAY_ESC_PIN is not None:
            GPIO.output(RELAY_ESC_PIN, GPIO.HIGH)
        if RELAY_SERVO_PIN is not None:
            GPIO.output(RELAY_SERVO_PIN, GPIO.HIGH)

    # -------------------------
    # Ultrasonic
    # -------------------------
    def read_distance_cm(self, timeout=0.03):
        """
        Returns distance in cm or None if sensor not enabled / timeout.
        """
        if TRIG_PIN is None or ECHO_PIN is None:
            return None

        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, GPIO.LOW)

        # Wait for echo start
        start_wait = time.time()
        while GPIO.input(ECHO_PIN) == 0:
            if time.time() - start_wait > timeout:
                return None
        start = time.time()

        # Wait for echo end
        end_wait = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            if time.time() - end_wait > timeout:
                return None
        end = time.time()

        elapsed = end - start
        return (elapsed * 34300) / 2.0

