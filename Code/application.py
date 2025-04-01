import os
import sys
import time
import subprocess
import psutil
import atexit
import signal
import errno
import threading

from oled import OLED
from expansion import Expansion

class Pi_Control:

    def __init__(self):
        # Initialize OLED and Expansion objects
        self.oled = None
        self.expansion = None
        self.font_size = 12
        self.cleanup_done = False
        self.data_lock = threading.Lock()
        self.stop_event = threading.Event()

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

        atexit.register(self.cleanup)  # Register the cleanup function to be called when the script exits
        # Register signal handlers for SIGTERM and SIGINT
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)

    def get_raspberry_fan_pwm(self, max_retries=3, retry_delay=0.1):
        # Get the fan PWM value with retry mechanism
        for attempt in range(max_retries + 1):
            try:
                base_path = '/sys/devices/platform/cooling_fan/hwmon/'
                hwmon_dirs = [d for d in os.listdir(base_path) if d.startswith('hwmon')]
                if not hwmon_dirs:
                    raise FileNotFoundError("No hwmon directory found in /sys/devices/platform/cooling_fan/hwmon/")
                hwmon_dir = hwmon_dirs[0]
                fan_input_path = os.path.join(base_path, hwmon_dir, 'pwm1')

                result = subprocess.run(['cat', fan_input_path],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)
                if result.returncode == 0:
                    pwm_value = int(result.stdout.strip())
                    if pwm_value > 0:
                        pwm_value = 255
                    elif pwm_value < 0:
                        pwm_value = 0
                    return pwm_value
                else:
                    return -1
            except OSError as e:
                if e.errno == errno.EAGAIN and attempt < max_retries:
                    time.sleep(retry_delay)
                else:
                    return -1
            except Exception as e:
                return -1

    def get_raspberry_cpu_usage(self):
        # Get the CPU usage percentage
        try:
            return psutil.cpu_percent(interval=0)
        except Exception as e:
            return 0

    def get_raspberry_memory_usage(self):
        # Get the memory usage percentage
        try:
            memory = psutil.virtual_memory()
            return memory.percent
        except Exception as e:
            return 0

    def get_raspberry_disk_usage(self, path='/'):
        # Get the disk usage percentage for the specified path
        try:
            disk_usage = psutil.disk_usage(path)
            return disk_usage.percent
        except Exception as e:
            return 0

    def get_raspberry_date(self):
        # Get the current date in YYYY-MM-DD format
        try:
            result = subprocess.run(['date', '+%Y-%m-%d'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "1990-1-1"
        except Exception as e:
            return "1990-1-1"

    def get_raspberry_weekday(self):
        # Get the current weekday name
        try:
            result = subprocess.run(['date', '+%A'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "Error"
        except Exception as e:
            return "Error"

    def get_raspberry_time(self):
        # Get the current time in HH:MM:SS format
        try:
            result = subprocess.run(['date', '+%H:%M:%S'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return '0:0:0'
        except Exception as e:
            return '0:0:0'

    def get_raspberry_cpu_temperature(self):
        # Get the CPU temperature in Celsius
        try:
            result = subprocess.run(['cat', '/sys/devices/virtual/thermal/thermal_zone0/temp'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            if result.returncode == 0:
                temp_raw = int(result.stdout.strip())
                return temp_raw / 1000.0
            else:
                return 0
        except Exception as e:
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

    def threading_oled(self):
        # Thread function to update OLED display
        while not self.stop_event.is_set():
            with self.data_lock:
                self.oled.clear()
                self.oled.draw_text("PI Parameters", position=(0, 0), font_size=self.font_size)
                self.oled.draw_text(f"CPU: {self.get_raspberry_cpu_usage()}%", position=(0, 16), font_size=self.font_size)
                self.oled.draw_text(f"MEM: {self.get_raspberry_memory_usage()}%", position=(0, 32), font_size=self.font_size)
                self.oled.draw_text(f"DISK: {self.get_raspberry_disk_usage()}%", position=(0, 48), font_size=self.font_size)
                self.oled.show()
            time.sleep(3)
            with self.data_lock:
                self.oled.clear()
                self.oled.draw_text(f"Date: {self.get_raspberry_date()}", position=(0, 0), font_size=self.font_size)
                self.oled.draw_text(f"Week: {self.get_raspberry_weekday()}", position=(0, 16), font_size=self.font_size)
                self.oled.draw_text(f"TIME: {self.get_raspberry_time()}", position=(0, 32), font_size=self.font_size)
                self.oled.draw_text(f"LED Mode: {self.get_computer_led_mode()}", position=(0, 48), font_size=self.font_size)
                self.oled.show()
            time.sleep(3)
            with self.data_lock:
                self.oled.clear()
                self.oled.draw_text(f"PI TEMP: {self.get_raspberry_cpu_temperature()}C", position=(0, 0), font_size=self.font_size)
                self.oled.draw_text(f"PC TEMP: {self.get_computer_temperature()}C", position=(0, 16), font_size=self.font_size)
                self.oled.draw_text(f"FAN Mode: {self.get_computer_fan_mode()}", position=(0, 32), font_size=self.font_size)
                self.oled.draw_text(f"FAN Duty: {int(float(self.get_computer_fan_duty()/255.0)*100)}%", position=(0, 48), font_size=self.font_size)
                self.oled.show()
            time.sleep(3)

    def threading_fan(self):
        # Thread function to control the fan
        last_fan_pwm = 0
        while not self.stop_event.is_set():
            with self.data_lock:
                current_fan_pwm = self.get_raspberry_fan_pwm()
                if current_fan_pwm != -1 and current_fan_pwm != last_fan_pwm:
                    last_fan_pwm = current_fan_pwm
                    #print(f"FAN PWM: {last_fan_pwm}")
                    self.expansion.set_fan_duty(last_fan_pwm, last_fan_pwm)
            time.sleep(0.01)

if __name__ == "__main__":
    pi_control = None
    oled_thread = None
    fan_thread = None

    try:
        time.sleep(1)

        pi_control = Pi_Control()
        oled_thread = threading.Thread(target=pi_control.threading_oled, name="OLED_Thread")
        fan_thread = threading.Thread(target=pi_control.threading_fan, name="Fan_Thread")

        oled_thread.start()
        fan_thread.start()

        while not pi_control.stop_event.is_set():
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass
    finally:
        if pi_control is not None:
            pi_control.stop_event.set()
            pi_control.cleanup()
            if oled_thread is not None and oled_thread.is_alive():
                oled_thread.join()
            if fan_thread is not None and fan_thread.is_alive():
                fan_thread.join()