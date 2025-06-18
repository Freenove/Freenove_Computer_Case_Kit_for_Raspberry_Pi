
# Thanks to @ricardodemauro for the code modifications.
## This is a rewrite of the application.py with:
## native method instead of syscall
## no threading (less cpu usage)
## ached the cooling_fan path
## some python optimizations
## It uses less memory and less cpu time

import os
import sys
import time
import psutil
import atexit
import signal
import threading
import datetime

from oled import OLED
from expansion import Expansion

class Pi_Monitor:
    __slots__ = ['oled', 'expansion', 'font_size', 'cleanup_done', 
                 'stop_event', '_fan_pwm_path', '_format_strings']

    def __init__(self):
        # Initialize OLED and Expansion objects
        self.oled = None
        self.expansion = None
        self.font_size = 12
        self.cleanup_done = False
        self.stop_event = threading.Event()  # Keep for signal handling
        
        # Cache hwmon path lookup for performance
        self._fan_pwm_path = None
        
        # Pre-allocate format strings
        self._format_strings = {
            'cpu': "CPU: {}%",
            'mem': "MEM: {}%", 
            'disk': "DISK: {}%",
            'date': "Date: {}",
            'week': "Week: {}",
            'time': "TIME: {}",
            'pi_temp': "PI TEMP: {}C",
            'pc_temp': "PC TEMP: {}C",
            'fan_mode': "FAN Mode: {}",
            'fan_duty': "FAN Duty: {}%",
            'led_mode': "LED Mode: {}"
        }

        try:
            self.oled = OLED()
        except Exception as e:
            sys.exit(1)

        try:
            self.expansion = Expansion()
            self.expansion.set_led_mode(4)
            self.expansion.set_all_led_color(255, 0, 0)
            self.expansion.set_fan_mode(1)
        except Exception as e:
            sys.exit(1)

        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)
        
        # Initialize fan PWM path cache
        self._find_fan_pwm_path()

    def _find_fan_pwm_path(self):
        """Cache the fan PWM path to avoid repeated directory lookups"""
        try:
            base_path = '/sys/devices/platform/cooling_fan/hwmon/'
            hwmon_dirs = [d for d in os.listdir(base_path) if d.startswith('hwmon')]
            if hwmon_dirs:
                self._fan_pwm_path = os.path.join(base_path, hwmon_dirs[0], 'pwm1')
        except Exception:
            self._fan_pwm_path = None

    def get_raspberry_fan_pwm(self, max_retries=3, retry_delay=0.1):
        """Get fan PWM using cached path and direct file read instead of subprocess"""
        for attempt in range(max_retries + 1):
            try:
                # Use cached path if available
                if self._fan_pwm_path:
                    fan_input_path = self._fan_pwm_path
                else:
                    base_path = '/sys/devices/platform/cooling_fan/hwmon/'
                    hwmon_dirs = [d for d in os.listdir(base_path) if d.startswith('hwmon')]
                    if not hwmon_dirs:
                        raise FileNotFoundError("No hwmon directory found")
                    fan_input_path = os.path.join(base_path, hwmon_dirs[0], 'pwm1')
                
                # Direct file read instead of subprocess
                with open(fan_input_path, 'r') as f:
                    pwm_value = int(f.read().strip())
                    return max(0, min(255, pwm_value))  # Clamp between 0-255
                    
            except (OSError, ValueError) as e:
                if attempt < max_retries:
                    time.sleep(retry_delay)
                else:
                    return -1
            except Exception:
                return -1
        return -1

    def get_raspberry_cpu_usage(self):
        """Get the CPU usage percentage"""
        try:
            return psutil.cpu_percent(interval=0)
        except Exception:
            return 0

    def get_raspberry_memory_usage(self):
        """Get the memory usage percentage"""
        try:
            memory = psutil.virtual_memory()
            return memory.percent
        except Exception:
            return 0

    def get_raspberry_disk_usage(self, path='/'):
        """Get the disk usage percentage for the specified path"""
        try:
            disk_usage = psutil.disk_usage(path)
            return disk_usage.percent
        except Exception:
            return 0

    def get_raspberry_date(self):
        """Get the current date in YYYY-MM-DD format using native Python datetime"""
        try:
            return datetime.date.today().strftime('%Y-%m-%d')
        except Exception:
            return "1990-1-1"

    def get_raspberry_weekday(self):
        """Get the current weekday name using native Python datetime"""
        try:
            return datetime.date.today().strftime('%A')
        except Exception:
            return "Error"

    def get_raspberry_time(self):
        """Get the current time in HH:MM:SS format using native Python datetime"""
        try:
            return datetime.datetime.now().strftime('%H:%M:%S')
        except Exception:
            return '0:0:0'

    def get_raspberry_cpu_temperature(self):
        """Get the CPU temperature in Celsius using direct file read"""
        try:
            with open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r') as f:
                temp_raw = int(f.read().strip())
                return temp_raw / 1000.0
        except Exception:
            return 0

    def get_computer_temperature(self):
        # Get the computer temperature using Expansion object
        try:
            return self.expansion.get_temp()
        except Exception as e:
            return 0

    def get_computer_fan_mode(self):
        # Get the computer fan mode using Expansion object
        try:
            return self.expansion.get_fan_mode()
        except Exception as e:
            return 0

    def get_computer_fan_duty(self):
        # Get the computer fan duty cycle using Expansion object
        try:
            return self.expansion.get_fan0_duty()
        except Exception as e:
            return 0

    def get_computer_led_mode(self):
        # Get the computer LED mode using Expansion object
        try:
            return self.expansion.get_led_mode()
        except Exception as e:
            return 0

    def cleanup(self):
        # Perform cleanup operations
        if self.cleanup_done:
            return
        self.cleanup_done = True
        try:
            if self.oled:
                self.oled.close()
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.set_led_mode(1)
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.set_all_led_color(0, 0, 0)
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.set_fan_mode(0)
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.set_fan_frequency(50)
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.set_fan_duty(0, 0)
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.end()
        except Exception as e:
            pass

    def handle_signal(self, signum, frame):
        # Handle signal to stop the application
        self.stop_event.set()
        self.cleanup()
        sys.exit(0)

    def run_monitor_loop(self):
        """Main monitoring loop - single-threaded infinite loop for both OLED display and fan control"""
        last_fan_pwm = 0
        last_fan_pwm_limit = 0
        temp_threshold_high = 170
        temp_threshold_low = 130
        max_pwm = 255
        min_pwm = 0
        oled_counter = 0  # Counter to control OLED update frequency
        oled_screen = 0   # Which screen to show (0, 1, or 2)
        
        while not self.stop_event.is_set():
            # Fan control logic (runs every iteration - every 1 second)
            current_cpu_temp = self.get_raspberry_cpu_temperature()
            current_fan_pwm = self.get_raspberry_fan_pwm()
            
            # Use single print statement to reduce I/O
            print(f"CPU TEMP: {current_cpu_temp}C, FAN PWM: {current_fan_pwm}")
            
            if current_fan_pwm != -1:
                if last_fan_pwm_limit == 0 and current_fan_pwm > temp_threshold_high:
                    last_fan_pwm = max_pwm
                    self.expansion.set_fan_duty(last_fan_pwm, last_fan_pwm)
                    last_fan_pwm_limit = 1
                elif last_fan_pwm_limit == 1 and current_fan_pwm < temp_threshold_low:
                    last_fan_pwm = min_pwm
                    self.expansion.set_fan_duty(last_fan_pwm, last_fan_pwm)
                    last_fan_pwm_limit = 0
            
            # OLED update logic (runs every 3 seconds)
            if oled_counter % 3 == 0:
                self.oled.clear()
                if oled_screen == 0:
                    # Screen 1: System Parameters
                    self.oled.draw_text("PI Parameters", position=(0, 0), font_size=self.font_size)
                    self.oled.draw_text(self._format_strings['cpu'].format(self.get_raspberry_cpu_usage()), position=(0, 16), font_size=self.font_size)
                    self.oled.draw_text(self._format_strings['mem'].format(self.get_raspberry_memory_usage()), position=(0, 32), font_size=self.font_size)
                    self.oled.draw_text(self._format_strings['disk'].format(self.get_raspberry_disk_usage()), position=(0, 48), font_size=self.font_size)
                elif oled_screen == 1:
                    # Screen 2: Date/Time/LED
                    self.oled.draw_text(self._format_strings['date'].format(self.get_raspberry_date()), position=(0, 0), font_size=self.font_size)
                    self.oled.draw_text(self._format_strings['week'].format(self.get_raspberry_weekday()), position=(0, 16), font_size=self.font_size)
                    self.oled.draw_text(self._format_strings['time'].format(self.get_raspberry_time()), position=(0, 32), font_size=self.font_size)
                    self.oled.draw_text(self._format_strings['led_mode'].format(self.get_computer_led_mode()), position=(0, 48), font_size=self.font_size)
                else:  # oled_screen == 2
                    # Screen 3: Temperature/Fan
                    self.oled.draw_text(self._format_strings['pi_temp'].format(current_cpu_temp), position=(0, 0), font_size=self.font_size)
                    self.oled.draw_text(self._format_strings['pc_temp'].format(self.get_computer_temperature()), position=(0, 16), font_size=self.font_size)
                    self.oled.draw_text(self._format_strings['fan_mode'].format(self.get_computer_fan_mode()), position=(0, 32), font_size=self.font_size)
                    self.oled.draw_text(self._format_strings['fan_duty'].format(int(float(self.get_computer_fan_duty()/255.0)*100)), position=(0, 48), font_size=self.font_size)
                
                self.oled.show()
                oled_screen = (oled_screen + 1) % 3  # Cycle through screens 0, 1, 2
            
            oled_counter += 1
            time.sleep(1)  # Base interval of 1 second

if __name__ == "__main__":
    pi_monitor = None

    try:
        time.sleep(1)

        pi_monitor = Pi_Monitor()
        # Use simple infinite loop instead of threading
        pi_monitor.run_monitor_loop()

    except KeyboardInterrupt:
        print("\nShutdown requested by user (Ctrl+C)")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if pi_monitor is not None:
            pi_monitor.stop_event.set()
            pi_monitor.cleanup()
        print("Monitor stopped.")
