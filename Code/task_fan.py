from api_expansion import Expansion
import atexit
import signal
import time
import sys

class FAN_TASK:

    def __init__(self):
        self.expansion = None
        self.board_type = None
        self.running = True  # Add flag to control main loop

        try:
            self.expansion = Expansion()                            # Initialize Expansion object
            self.board_type = self.expansion.get_board_type()
        except Exception as e:
            sys.exit(1)

        atexit.register(self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)

    def handle_signal(self, signum=None, frame=None):
        try:
            if self.expansion:
                self.expansion.set_fan_mode(0)
        except Exception as e:
            print(e)
        try:
            if self.expansion:
                if self.board_type == "FNK0100":
                    self.expansion.set_fan_duty(0, 0)
                elif self.board_type == "FNK0107":
                    self.expansion.set_fan_duty(0, 0, 0)
        except Exception as e:
            print(e)
        try:
            if self.expansion:
                self.expansion.end()
        except Exception as e:
            print(e)
        
        # Set running flag to False to exit main loop
        self.running = False
        
        # Only exit if called from signal handler (not from atexit)
        if signum is not None:
            pass

    def run_fan_loop(self):
        """Main monitoring loop - single-threaded infinite loop for both OLED display and fan control"""
        self.expansion.set_fan_mode(1)
        self.expansion.set_fan_frequency(50000) 
        if self.board_type == "FNK0100":
            self.expansion.set_fan_temp_mode_threshold(50, 100)
        elif self.board_type == "FNK0107":
            self.expansion.set_fan_temp_mode_threshold(50, 100, 3)
            self.expansion.set_fan_temp_mode_speed(75, 125, 175)
            self.expansion.set_fan_pi_following(0, 100)
            self.expansion.set_fan_power_switch(1)

        try:
            while self.running:
                for i in range(0,255,1):
                    if not self.running:
                        break
                    if self.board_type == "FNK0100":
                        self.expansion.set_fan_duty(i, i)
                    elif self.board_type == "FNK0107":
                        self.expansion.set_fan_duty(i, i, i)
                    time.sleep(0.01)
                if not self.running:
                    break
                for i in range(255,0,-1):
                    if not self.running:
                        break
                    if self.board_type == "FNK0100":
                        self.expansion.set_fan_duty(i, i)
                    elif self.board_type == "FNK0107":
                        self.expansion.set_fan_duty(i, i, i)
                    time.sleep(0.01)
        except KeyboardInterrupt:
            # This will be caught by the signal handlers
            pass

if __name__ == "__main__":
    fan_task= None
    try:
        fan_task = FAN_TASK()
        fan_task.run_fan_loop()
    except KeyboardInterrupt:
        print("\nShutdown requested by user (Ctrl+C)")
    except Exception as e:
        print(f"Unexpected error: {e}")