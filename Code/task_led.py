from api_expansion import Expansion

import atexit
import signal
import time
import sys

class LED_TASK:

    def __init__(self):
        self.expansion = None
        self.running = True  # Add flag to control main loop

        try:
            self.expansion = Expansion()                            # Initialize Expansion object
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
        
        # Set running flag to False to exit main loop
        self.running = False

    def show_single_color(self):
        """Main monitoring loop - single-threaded infinite loop for both OLED display and fan control"""
        rainbow_colors = [
            (255, 0, 0),    # 红色 (Red)
            (0, 255, 0),    # 绿色 (Green)
            (0, 0, 255),    # 蓝色 (Blue)
            (255, 255, 0),  # 黄色 (Yellow)
            (75, 0, 130),   # 靛蓝 (Indigo)
            (0, 255, 255),  # 青色 (Cyan)
            (255, 165, 0),  # 橙色 (Orange)
            (128, 0, 128),  # 紫色 (Purple)
            (255, 192, 203),# 粉色 (Pink)
            (0, 128, 128),  # 青绿色 (Teal)
            (64, 0, 128),   # 暗紫色 (Purple)
            (255, 0, 255),  # 洋红 (Magenta)
        ]
        r,g,b = rainbow_colors[0]
        self.expansion.set_led_mode(1)
        self.expansion.set_all_led_color(r,g,b)
        try:
            while self.running:
                for i in range(len(rainbow_colors)):
                    if not self.running:
                        break
                    r,g,b = rainbow_colors[i]
                    self.expansion.set_all_led_color(r,g,b)
                    time.sleep(0.5)
        except KeyboardInterrupt:
            # This will be caught by the signal handlers
            pass

    def wheel(self, pos):
        wheel_pos = pos % 255
        if wheel_pos < 85:
            r = 255 - wheel_pos * 3
            g = wheel_pos * 3
            b = 0
            return (r, g, b)
        if wheel_pos < 170:
            wheel_pos -= 85
            r = 0
            g = 255 - wheel_pos * 3
            b = wheel_pos * 3
            return (r, g, b)
        wheel_pos -= 170
        r = wheel_pos * 3
        g = 0
        b = 255 - wheel_pos * 3
        return (r, g, b)

    def show_wheel_color(self):
        '''显示彩虹色'''
        self.expansion.set_led_mode(1)
        try:
            while self.running:
                for i in range(255):
                    if not self.running:
                        break
                    r,g,b = self.wheel(i)
                    self.expansion.set_all_led_color(r,g,b)
                    time.sleep(0.05)
        except KeyboardInterrupt:
            # This will be caught by the signal handlers
            pass


    def run_led_loop(self):
        """Main monitoring loop - single-threaded infinite loop for both OLED display and fan control"""
        #self.show_single_color()
        self.show_wheel_color()


if __name__ == "__main__":
    led_task= None
    try:
        led_task = LED_TASK()

        # Use simple infinite loop instead of threading
        led_task.run_led_loop()

    except KeyboardInterrupt:
        print("\nShutdown requested by user (Ctrl+C)")
    except Exception as e:
        print(f"Unexpected error: {e}")