import time

from .config import (
    ESC_NEUTRAL, ESC_SAFE_FORWARD,
    STEER_CENTER, STEER_LEFT, STEER_RIGHT,
    OBSTACLE_STOP_CM,
    KEY_TIMEOUT, CONTROL_DELAY,
    EMERGENCY_STOP_KEY, QUIT_KEY, MANUAL_KEY,
)
from .keyboard_io import setup_keyboard, restore_keyboard, get_key


class Controller:
    def __init__(self, hw):
        self.hw = hw
        self.mode = "MANUAL"  # MANUAL or AUTO

    def set_manual(self):
        self.mode = "MANUAL"
        self.hw.set_relays_manual()
        self.hw.stop_motor()
        self.hw.steer(STEER_CENTER)
        print("[MODE] Manual (RC transmitter controls).")

    def set_auto(self):
        self.mode = "AUTO"
        self.hw.set_relays_auto()
        self.hw.arm_esc()
        self.hw.stop_motor()
        self.hw.steer(STEER_CENTER)
        print("[MODE] Auto (Pi controls).")

    def autonomous_loop(self):
        print("\n[Auto] Controls: W forward | S stop | A left | D right | Space emergency stop | M manual | Q quit\n")

        current_duty = ESC_NEUTRAL
        self.hw.stop_motor()
        self.hw.steer(STEER_CENTER)

        fd, old = setup_keyboard()
        try:
            while self.mode == "AUTO":
                # Safety: obstacle stop
                dist = self.hw.read_distance_cm()
                if dist is not None and dist < OBSTACLE_STOP_CM:
                    print(f"[SAFE] Obstacle at {dist:.1f} cm -> STOP")
                    self.hw.stop_motor()
                    current_duty = ESC_NEUTRAL
                else:
                    self.hw.set_throttle_duty(current_duty)

                key = get_key(timeout=KEY_TIMEOUT)
                if key:
                    key = key.lower()

                    if key == "w":
                        current_duty = ESC_SAFE_FORWARD
                        print("[Key] W -> forward")

                    elif key == "s":
                        current_duty = ESC_NEUTRAL
                        self.hw.stop_motor()
                        print("[Key] S -> stop")

                    elif key == "a":
                        self.hw.steer(STEER_LEFT)
                        print("[Key] A -> left")

                    elif key == "d":
                        self.hw.steer(STEER_RIGHT)
                        print("[Key] D -> right")

                    elif key == EMERGENCY_STOP_KEY:
                        current_duty = ESC_NEUTRAL
                        self.hw.stop_motor()
                        self.hw.steer(STEER_CENTER)
                        print("[Key] Space -> emergency stop + center")

                    elif key == MANUAL_KEY:
                        print("[Key] M -> switch to manual")
                        self.set_manual()
                        break

                    elif key == QUIT_KEY:
                        print("[Key] Q -> quit")
                        self.hw.stop_motor()
                        return

                time.sleep(CONTROL_DELAY)

        except KeyboardInterrupt:
            print("\n[Auto] KeyboardInterrupt -> stop motor")
            self.hw.stop_motor()

        finally:
            restore_keyboard(fd, old)

