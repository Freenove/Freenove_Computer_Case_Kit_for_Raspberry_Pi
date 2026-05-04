from api_expansion import Expansion
from power_state import get_power_reading

import atexit
import signal
import socket
import time
import sys

_COLOR_LOW  = (0, 206, 209)   # water blue at low power
_COLOR_HIGH = (255, 0, 0)     # red at high power
_LOW_WATTS  = 2000
_HIGH_WATTS = 4800


def _is_network_connected():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('10.255.255.255', 1))
            return s.getsockname()[0] != '0.0.0.0'
    except OSError:
        return False


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
                self.expansion.set_led_mode(0)
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
        """Power-based dynamic LED color: water-blue (low) to red (high), blinks red when offline."""
        self.expansion.set_led_mode(1)  # Static RGB mode
        r, g, b = _COLOR_LOW
        self.expansion.set_all_led_color(r, g, b)

        tick = 0
        blink_on = False
        online = True
        try:
            while self.running:
                # Every 3 seconds (6 ticks × 0.5 s): refresh network status and power color
                if tick % 6 == 0:
                    online = _is_network_connected()
                    if online:
                        watts = get_power_reading()
                        r, g, b = _power_to_color(watts)
                        blink_on = False
                        self.expansion.set_all_led_color(r, g, b)

                # Every 0.5 s: toggle blink when offline
                if not online:
                    blink_on = not blink_on
                    br, bg, bb = (255, 0, 0) if blink_on else (0, 0, 0)
                    self.expansion.set_all_led_color(br, bg, bb)

                tick += 1
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
