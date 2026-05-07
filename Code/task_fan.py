from api_expansion import Expansion
from api_systemInfo import SystemInformation
from api_json import ConfigManager
import atexit
import signal
import time
import sys

class FAN_TASK:

    def __init__(self):
        self.expansion = None
        self.system_info = None
        self.board_type = None
        self.running = True

        try:
            self.expansion = Expansion()
            self.board_type = self.expansion.get_board_type()
        except Exception as e:
            sys.exit(1)

        try:
            self.system_info = SystemInformation()
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

        self.running = False

        if signum is not None:
            pass

    def _load_fan_config(self):
        config = ConfigManager()
        fan_cfg = config.get_section('Fan')
        return {
            'low_threshold':  fan_cfg.get('mode2_low_temp_threshold', 30),
            'high_threshold': fan_cfg.get('mode2_high_temp_threshold', 50),
            'schmitt':        fan_cfg.get('mode2_temp_schmitt', 3),
            'low_speed':      fan_cfg.get('mode2_low_speed', 75),
            'middle_speed':   fan_cfg.get('mode2_middle_speed', 125),
            'high_speed':     fan_cfg.get('mode2_high_speed', 175),
        }

    def _get_cpu_temp(self):
        try:
            return self.system_info.get_raspberry_pi_cpu_temperature()
        except Exception:
            return 0.0

    def _get_case_temp(self):
        try:
            return self.expansion.get_temp()
        except Exception:
            return 0.0

    def _set_fan_duty(self, duty):
        if self.board_type == "FNK0100":
            self.expansion.set_fan_duty(duty, duty)
        elif self.board_type == "FNK0107":
            self.expansion.set_fan_duty(duty, duty, duty)

    def run_fan_loop(self):
        """Follow Case: software Schmitt-trigger control using max(cpu_temp, case_temp)."""
        self.expansion.set_fan_mode(1)   # Manual — duty set by this loop
        if self.board_type == "FNK0107":
            self.expansion.set_fan_frequency(50000)
            self.expansion.set_fan_power_switch(1)
        elif self.board_type == "FNK0100":
            self.expansion.set_fan_frequency(50)

        cfg = self._load_fan_config()
        low_threshold  = cfg['low_threshold']
        high_threshold = cfg['high_threshold']
        schmitt        = cfg['schmitt']
        low_speed      = cfg['low_speed']
        middle_speed   = cfg['middle_speed']
        high_speed     = cfg['high_speed']

        current_speed = 0  # Start in STOPPED state
        self._set_fan_duty(current_speed)

        try:
            while self.running:
                temp = max(self._get_cpu_temp(), self._get_case_temp())

                if current_speed == high_speed:
                    if temp < high_threshold:
                        current_speed = middle_speed
                elif current_speed == middle_speed:
                    if temp >= high_threshold:
                        current_speed = high_speed
                    elif temp < low_threshold:
                        current_speed = low_speed
                elif current_speed == low_speed:
                    if temp >= low_threshold:
                        current_speed = middle_speed
                    elif temp < low_threshold - schmitt:
                        current_speed = 0
                else:  # STOPPED (0)
                    if temp >= low_threshold:
                        current_speed = middle_speed  # skip LOW on heating

                self._set_fan_duty(current_speed)
                time.sleep(5)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    fan_task = None
    try:
        fan_task = FAN_TASK()
        fan_task.run_fan_loop()
    except KeyboardInterrupt:
        print("\nShutdown requested by user (Ctrl+C)")
    except Exception as e:
        print(f"Unexpected error: {e}")
