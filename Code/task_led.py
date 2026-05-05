from api_expansion import Expansion
from power_state import get_power_reading

import atexit
import json
import os
import signal
import socket
import time
import sys

_COLOR_LOW  = (0, 206, 209)   # water blue at low power
_COLOR_HIGH = (255, 0, 0)     # red at high power
_LOW_WATTS  = 2000
_HIGH_WATTS = 4800

# app_config.json LED.mode values (matches app_ui_led.py radio button order)
_MODE_RAINBOW   = 0
_MODE_BREATHING = 1
_MODE_FOLLOW    = 2
_MODE_MANUAL    = 3  # power-based color (replaces static single color)
_MODE_CUSTOM    = 4  # same power-based logic (task_led.py custom mode)
_MODE_CLOSE     = 5

# Hardware set_led_mode() values from api_expansion comment:
# 0: close, 1: RGB, 2: Following, 3: Breathing, 4: Rainbow
_HW_CLOSE     = 0
_HW_RGB       = 1
_HW_FOLLOWING = 2
_HW_BREATHING = 3
_HW_RAINBOW   = 4

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_config.json')


def _is_network_connected():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('10.255.255.255', 1))
            return s.getsockname()[0] != '0.0.0.0'
    except OSError:
        return False


def _read_config():
    try:
        with open(_CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def _power_to_color(watts):
    if watts is None or watts <= _LOW_WATTS:
        return _COLOR_LOW
    if watts >= _HIGH_WATTS:
        return _COLOR_HIGH
    t = (watts - _LOW_WATTS) / (_HIGH_WATTS - _LOW_WATTS)
    r = int(_COLOR_LOW[0] + t * (_COLOR_HIGH[0] - _COLOR_LOW[0]))
    g = int(_COLOR_LOW[1] + t * (_COLOR_HIGH[1] - _COLOR_LOW[1]))
    b = int(_COLOR_LOW[2] + t * (_COLOR_HIGH[2] - _COLOR_LOW[2]))
    return (r, g, b)


def _rainbow_step(pos):
    pos = pos % 255
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


class LED_TASK:

    def __init__(self):
        self.expansion = None
        self.running = True

        try:
            self.expansion = Expansion()
        except Exception as e:
            sys.exit(1)

        atexit.register(self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)

    def handle_signal(self, signum=None, frame=None):
        try:
            if self.expansion:
                self.expansion.set_led_mode(_HW_CLOSE)
        except Exception as e:
            print(e)
        try:
            if self.expansion:
                self.expansion.set_all_led_color(0, 0, 0)
        except Exception as e:
            print(e)
        try:
            if self.expansion:
                self.expansion.end()
        except Exception as e:
            print(e)
        self.running = False

    def run_led_loop(self):
        """Main loop: reads LED.mode from app_config.json every 3 s and dispatches accordingly.

        mode 0 (Rainbow)  → software rainbow wheel (original show_wheel_color behavior)
        mode 1 (Breathing)→ hardware breathing with configured color
        mode 2 (Follow)   → hardware following with configured color
        mode 3 (Manual)   → power-based dynamic color (custom: water-blue→red by wattage)
        mode 4 (Custom)   → same power-based logic as mode 3
        mode 5 (Close)    → LEDs off
        """
        config = _read_config()
        last_config_read = time.monotonic()

        # power-mode state
        blink_on = False
        online = True
        power_r, power_g, power_b = _COLOR_LOW
        last_power_check = 0.0

        # rainbow state
        rainbow_pos = 0

        # track hardware mode to avoid redundant set_led_mode calls
        hw_mode = None

        try:
            while self.running:
                now = time.monotonic()

                if now - last_config_read >= 3.0:
                    config = _read_config()
                    last_config_read = now

                led_cfg = config.get('LED', {})
                mode = led_cfg.get('mode', _MODE_MANUAL)

                if mode == _MODE_RAINBOW:
                    r, g, b = _rainbow_step(rainbow_pos)
                    if hw_mode != _HW_RGB:
                        self.expansion.set_led_mode(_HW_RGB)
                        hw_mode = _HW_RGB
                    self.expansion.set_all_led_color(r, g, b)
                    rainbow_pos = (rainbow_pos + 1) % 255
                    time.sleep(0.05)

                elif mode == _MODE_BREATHING:
                    r = led_cfg.get('red_value', 0)
                    g = led_cfg.get('green_value', 0)
                    b = led_cfg.get('blue_value', 255)
                    if hw_mode != _HW_BREATHING:
                        self.expansion.set_led_mode(_HW_BREATHING)
                        self.expansion.set_all_led_color(r, g, b)
                        hw_mode = _HW_BREATHING
                    time.sleep(0.5)

                elif mode == _MODE_FOLLOW:
                    r = led_cfg.get('red_value', 0)
                    g = led_cfg.get('green_value', 0)
                    b = led_cfg.get('blue_value', 255)
                    if hw_mode != _HW_FOLLOWING:
                        self.expansion.set_led_mode(_HW_FOLLOWING)
                        self.expansion.set_all_led_color(r, g, b)
                        hw_mode = _HW_FOLLOWING
                    time.sleep(0.5)

                elif mode in (_MODE_MANUAL, _MODE_CUSTOM):
                    if hw_mode != _HW_RGB:
                        self.expansion.set_led_mode(_HW_RGB)
                        hw_mode = _HW_RGB

                    if now - last_power_check >= 3.0:
                        last_power_check = now
                        online = _is_network_connected()
                        if online:
                            watts = get_power_reading()
                            power_r, power_g, power_b = _power_to_color(watts)
                            blink_on = False
                            self.expansion.set_all_led_color(power_r, power_g, power_b)

                    if not online:
                        blink_on = not blink_on
                        br, bg, bb = (255, 0, 0) if blink_on else (0, 0, 0)
                        self.expansion.set_all_led_color(br, bg, bb)

                    time.sleep(0.5)

                elif mode == _MODE_CLOSE:
                    if hw_mode != _HW_CLOSE:
                        self.expansion.set_led_mode(_HW_CLOSE)
                        hw_mode = _HW_CLOSE
                    time.sleep(0.5)

                else:
                    time.sleep(0.5)

        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    led_task = None
    try:
        led_task = LED_TASK()
        led_task.run_led_loop()
    except KeyboardInterrupt:
        print("\nShutdown requested by user (Ctrl+C)")
    except Exception as e:
        print(f"Unexpected error: {e}")
