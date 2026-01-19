from .hardware import Hardware
from .control import Controller


def main():
    hw = Hardware()
    hw.setup()

    controller = Controller(hw)
    controller.set_manual()

    try:
        while True:
            print("\n==============================")
            print(" RC CAR CONTROL MENU")
            print("==============================")
            print(f"Current mode: {controller.mode}")
            print("1) Manual RC Control")
            print("2) Autonomous Pi Control (WASD + Safety)")
            print("q) Quit")

            choice = input("Select option: ").strip().lower()

            if choice == "1":
                controller.set_manual()
                input("Manual mode active. Press Enter to return to menu...")

            elif choice == "2":
                controller.set_auto()
                controller.autonomous_loop()

            elif choice == "q":
                print("Exiting...")
                break

            else:
                print("Invalid selection.")

    finally:
        print("[CLEANUP] Stopping and cleaning GPIO.")
        hw.cleanup()

