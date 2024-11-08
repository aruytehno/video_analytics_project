import time

class Orchestrator:
    def __init__(self):
        self.state = "inactive"

    def set_state(self, new_state):
        valid_states = ["init_startup", "in_startup_processing", "active", "init_shutdown", "in_shutdown_processing", "inactive"]
        if new_state in valid_states:
            self.state = new_state
            print(f"State changed to: {self.state}")
        else:
            print(f"Invalid state: {new_state}")

    def run(self):
        while True:
            print(f"Current state: {self.state}")
            time.sleep(5)
