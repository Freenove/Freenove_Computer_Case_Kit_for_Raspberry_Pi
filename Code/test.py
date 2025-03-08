
import sys
import time
import getopt
from expansion import Expansion
from camera import Camera
from oled import OLED

def led_rgb():
    try:
        expansion_board = Expansion()
        expansion_board.set_led_mode(1)
        colors = [[255,0,0], [0,255,0], [0,0,255], [0,0,0]]
        while True:
            for color in colors:
                expansion_board.set_all_led_color(color[0], color[1], color[2])
                time.sleep(1)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        expansion_board.set_led_mode(1)
        expansion_board.set_all_led_color(0, 0, 0)
        expansion_board.end()

def led_following():
    try:
        expansion_board = Expansion()
        expansion_board.set_led_mode(2)
        colors = [[255,0,0], [0,255,0], [0,0,255]]
        expansion_board.set_all_led_color(colors[0][0], colors[0][1], colors[0][2])
        while True:
            time.sleep(1)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        expansion_board.set_led_mode(1)
        expansion_board.set_all_led_color(0, 0, 0)
        expansion_board.end()

def led_breathing():
    try:
        expansion_board = Expansion()
        expansion_board.set_led_mode(3)
        colors = [[255,0,0], [0,255,0], [0,0,255]]
        expansion_board.set_all_led_color(colors[1][0], colors[1][1], colors[1][2])
        while True:
            time.sleep(1)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        expansion_board.set_led_mode(1)
        expansion_board.set_all_led_color(0, 0, 0)
        expansion_board.end()

def led_rainbow():
    try:
        expansion_board = Expansion()
        expansion_board.set_led_mode(4)
        while True:
            time.sleep(1)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        expansion_board.set_led_mode(1)
        expansion_board.set_all_led_color(0, 0, 0)
        expansion_board.end()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["help", "camera", "oled", "fan", "led="])
    except getopt.GetoptError:
        print('Usage: test.py --camera | --oled | --fan | --led <mode:1-4>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Usage: test.py --camera | --oled | --fan | --led <mode:1-4>')
            sys.exit()
        elif opt == "--camera":
            try:
                camera = Camera()
                print("view image...")
                camera.start_image()                  
                print("Use Ctrl+C to exit...")
                while True:
                    time.sleep(1)
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
            finally:
                camera.close()
        elif opt == "--oled":
            try:
                oled = OLED()
                oled.draw_text("OLED Test!", position=(32, 15))
                oled.draw_text("www.Freenove.com", position=(15, 35))
                oled.show()
                print("Use Ctrl+C to exit...")
                while True:
                    time.sleep(1)
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
            finally:
                oled.close()
        elif opt == "--fan":
            try:
                expansion_board = Expansion()
                expansion_board.set_fan_mode(1)
                print("Use Ctrl+C to exit...")
                while True:
                    for i in range(0, 256):
                        expansion_board.set_fan_duty(i, i)
                        time.sleep(0.02)
                    for i in range(255, -1, -1):
                        expansion_board.set_fan_duty(i, i)
                        time.sleep(0.02)
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
            finally:
                expansion_board.set_fan_duty(0, 0)
                expansion_board.end()
        elif opt == "--led":
            if not arg:
                print("Usage: test.py --led <mode:1-4>")
                sys.exit(2)
            print("Use Ctrl+C to exit...")
            if arg == '1':
                led_rgb()
            elif arg == '2':
                led_following()
            elif arg == '3':
                led_breathing()
            elif arg == '4':
                led_rainbow()
            else:
                print("Usage: test.py --led <mode:1-4>")
                sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])


