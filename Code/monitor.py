import os
import sys
import time
import subprocess
import psutil
import atexit
import signal
import errno
import threading
import datetime

from oled import OLED
from expansion import Expansion

class Pi_Monitor:
    __slots__ = ['oled', 'expansion', 'font_size', 'cleanup_done', 'data_lock', 
                 'stop_event', '_fan_pwm_path', '_format_strings']

    def __init__(self):
        # Initialize OLED and Expansion objects
        self.oled = None
        self.expansion = None
        self.font_size = 12
        self.cleanup_done = False
        self.data_lock = threading.Lock()
        self.stop_event = threading.Event()
        
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
                    if pwm_value > 255:
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

    def get_raspberry_fan_pwm_v2(self, max_retries=3, retry_delay=0.1):
        """Optimized version using cached path and direct file read instead of subprocess"""
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
        # Get the CPU usage percentage
        try:
            return psutil.cpu_percent(interval=0)
        except Exception as e:
            return 0

    def get_raspberry_cpu_usage_v2(self):
        """Optimized version without caching"""
        try:
            return psutil.cpu_percent(interval=0)
        except Exception:
            return 0

    def get_raspberry_memory_usage(self):
        # Get the memory usage percentage
        try:
            memory = psutil.virtual_memory()
            return memory.percent
        except Exception as e:
            return 0

    def get_raspberry_memory_usage_v2(self):
        """Optimized version without caching"""
        try:
            memory = psutil.virtual_memory()
            return memory.percent
        except Exception:
            return 0

    def get_raspberry_disk_usage(self, path='/'):
        # Get the disk usage percentage for the specified path
        try:
            disk_usage = psutil.disk_usage(path)
            return disk_usage.percent
        except Exception as e:
            return 0

    def get_raspberry_disk_usage_v2(self, path='/'):
        """Optimized version without caching"""
        try:
            disk_usage = psutil.disk_usage(path)
            return disk_usage.percent
        except Exception:
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

    def get_raspberry_date_v2(self):
        """Optimized version using native Python datetime instead of subprocess"""
        try:
            return datetime.date.today().strftime('%Y-%m-%d')
        except Exception:
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
        
    def get_raspberry_weekday_v2(self):
        """Optimized version using native Python datetime instead of subprocess"""
        try:
            return datetime.date.today().strftime('%A')
        except Exception:
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
        
    def get_raspberry_time_v2(self):
        """Optimized version using native Python datetime instead of subprocess"""
        try:
            return datetime.datetime.now().strftime('%H:%M:%S')
        except Exception:
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

    def get_raspberry_cpu_temperature_v2(self):
        """Optimized version using direct file read instead of subprocess"""
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

    def threading_oled_v2(self):
        """Optimized OLED thread function with reduced lock contention and using v2 methods"""
        while not self.stop_event.is_set():
            # Pre-collect all data outside the lock to minimize lock time
            data_sets = [
                {
                    'title': "PI Parameters",
                    'lines': [
                        self._format_strings['cpu'].format(self.get_raspberry_cpu_usage_v2()),
                        self._format_strings['mem'].format(self.get_raspberry_memory_usage_v2()),
                        self._format_strings['disk'].format(self.get_raspberry_disk_usage_v2())
                    ]
                },
                {
                    'title': self._format_strings['date'].format(self.get_raspberry_date_v2()),
                    'lines': [
                        self._format_strings['week'].format(self.get_raspberry_weekday_v2()),
                        self._format_strings['time'].format(self.get_raspberry_time_v2()),
                        self._format_strings['led_mode'].format(self.get_computer_led_mode())
                    ]
                },
                {
                    'title': self._format_strings['pi_temp'].format(self.get_raspberry_cpu_temperature_v2()),
                    'lines': [
                        self._format_strings['pc_temp'].format(self.get_computer_temperature()),
                        self._format_strings['fan_mode'].format(self.get_computer_fan_mode()),
                        self._format_strings['fan_duty'].format(int(float(self.get_computer_fan_duty()/255.0)*100))
                    ]
                }
            ]
            
            # Quick display update with minimal lock time
            for data_set in data_sets:
                if self.stop_event.is_set():
                    break
                    
                with self.data_lock:
                    self.oled.clear()
                    self.oled.draw_text(data_set['title'], position=(0, 0), font_size=self.font_size)
                    for i, line in enumerate(data_set['lines']):
                        self.oled.draw_text(line, position=(0, 16 + i*16), font_size=self.font_size)
                    self.oled.show()
                
                time.sleep(3)

    def threading_fan_limit(self):
        # Thread function to limit the fan speed
        last_fan_pwm = 0
        last_fan_pwm_limit = 0
        while not self.stop_event.is_set():
            with self.data_lock:
                current_cpu_temp = self.get_raspberry_cpu_temperature()
                current_fan_pwm = self.get_raspberry_fan_pwm()
                print(f"CPU TEMP: {current_cpu_temp}C")
                print(f"FAN PWM: {current_fan_pwm}")
                if current_fan_pwm != -1:
                    if last_fan_pwm_limit == 0:
                        if current_fan_pwm > 170:
                            last_fan_pwm = 255
                            self.expansion.set_fan_duty(last_fan_pwm, last_fan_pwm)
                            last_fan_pwm_limit = 1
                    elif last_fan_pwm_limit == 1:
                        if current_fan_pwm < 130:
                            last_fan_pwm = 0
                            self.expansion.set_fan_duty(last_fan_pwm, last_fan_pwm)
                            last_fan_pwm_limit = 0
            time.sleep(1)

    def threading_fan_limit_v2(self):
        """Optimized fan limit thread function with reduced I/O and better variable management"""
        last_fan_pwm = 0
        last_fan_pwm_limit = 0
        temp_threshold_high = 170
        temp_threshold_low = 130
        max_pwm = 255
        min_pwm = 0
        
        while not self.stop_event.is_set():
            with self.data_lock:
                current_cpu_temp = self.get_raspberry_cpu_temperature_v2()
                current_fan_pwm = self.get_raspberry_fan_pwm_v2()
                
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
            
            time.sleep(1)

if __name__ == "__main__":
    pi_monitor = None
    oled_thread = None
    fan_thread = None

    try:
        time.sleep(1)

        pi_monitor = Pi_Monitor()
        oled_thread = threading.Thread(target=pi_monitor.threading_oled, name="OLED_Thread")
        fan_thread = threading.Thread(target=pi_monitor.threading_fan_limit, name="Fan_Thread")

        oled_thread.start()
        fan_thread.start()

        while not pi_monitor.stop_event.is_set():
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass
    finally:
        if pi_monitor is not None:
            pi_monitor.stop_event.set()
            pi_monitor.cleanup()
            if oled_thread is not None and oled_thread.is_alive():
                oled_thread.join()
            if fan_thread is not None and fan_thread.is_alive():
                fan_thread.join()
