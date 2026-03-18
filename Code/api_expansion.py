import smbus
import time

class I2CController:
    def __init__(self, bus_number=1, address=0x21):
        self.bus_number = bus_number
        self.address = address
        self._bus = None
    
    @property
    def bus(self):
        if self._bus is None:
            self._bus = smbus.SMBus(self.bus_number)
        return self._bus
    
    def check_device_exists(self, address=None):
        if address is None:
            address = self.address
        try:
            self.bus.read_byte(address)
            return True
        except IOError:
            return False
        except Exception:
            return False


    def write(self, reg, values):
        try:
            if isinstance(values, list):
                self.bus.write_i2c_block_data(self.address, reg, values)
            else:
                self.bus.write_byte_data(self.address, reg, values)
        except IOError as e:
            pass
    
    def read(self, reg, length=1):
        try:
            if length == 1:
                return self.bus.read_byte_data(self.address, reg)
            else:
                return self.bus.read_i2c_block_data(self.address, reg, length)
        except Exception as e:
            if length == 1:
                return 0
            else:
                return [0] * length
    
    def close(self):
        if self._bus is not None:
            self._bus.close()
            self._bus = None

class FNK0100:
    REG_LED_SPECIFIED     = 0x01
    REG_LED_ALL           = 0x02
    REG_LED_MODE          = 0x03
    REG_FAN_MODE          = 0x04
    REG_FAN_FREQUENCY     = 0x05
    REG_FAN_DUTY          = 0x06
    REG_FAN_THRESHOLD     = 0x07
    REG_POWER_ON_CHECK    = 0x08
    
    REG_LED_SPECIFIED_READ = 0xf4
    REG_LED_ALL_READ      = 0xf5
    REG_LED_MODE_READ     = 0xf6
    REG_FAN_MODE_READ     = 0xf7
    REG_FAN_FREQUENCY_READ = 0xf8
    REG_FAN0_DUTY_READ    = 0xf9
    REG_FAN1_DUTY_READ    = 0xfa
    REG_FAN_THRESHOLD_READ = 0xfb
    REG_TEMP_READ         = 0xfc
    
    def __init__(self, i2c_controller):
        self.i2c = i2c_controller
    
    # 设置开机检查
    def set_power_on_check(self, state):
        self.i2c.write(self.REG_POWER_ON_CHECK, state)

    # 获取温度方法
    def get_temp(self):
        return self.i2c.read(self.REG_TEMP_READ)

    # 风扇控制方法
    def set_fan_mode(self, mode):
        self.i2c.write(self.REG_FAN_MODE, mode)
    def set_fan_frequency(self, freq):
        frequency = [
            (freq >> 24) & 0xFF,
            (freq >> 16) & 0xFF,
            (freq >> 8) & 0xFF,
            freq & 0xFF
        ]
        self.i2c.write(self.REG_FAN_FREQUENCY, frequency)
    def set_fan_duty(self, duty0, duty1):
        duty = [duty0, duty1]
        self.i2c.write(self.REG_FAN_DUTY, duty)
    def set_fan_temp_mode_threshold(self, low_threshold, high_threshold):
        threshold = [low_threshold, high_threshold]
        self.i2c.write(self.REG_FAN_THRESHOLD, threshold)
    def get_fan_mode(self):
        return self.i2c.read(self.REG_FAN_MODE_READ)
    def get_fan_frequency(self):
        arr = self.i2c.read(self.REG_FAN_FREQUENCY_READ, 4)
        freq = (arr[0] << 24) | (arr[1] << 16) | (arr[2] << 8) | arr[3]
        return freq
    def get_fan0_duty(self):
        return self.i2c.read(self.REG_FAN0_DUTY_READ)
    def get_fan1_duty(self):
        return self.i2c.read(self.REG_FAN1_DUTY_READ)
    def get_fan_duty(self):
        duty0 = self.get_fan0_duty()
        duty1 = self.get_fan1_duty()
        return [duty0, duty1]
    def get_fan_threshold(self):
        return self.i2c.read(self.REG_FAN_THRESHOLD_READ, 2)

    # 彩灯控制方法
    def set_led_color(self, led_id, r, g, b):
        cmd = [led_id, r, g, b]
        self.i2c.write(self.REG_LED_SPECIFIED, cmd)
    def set_all_led_color(self, r, g, b):
        cmd = [r, g, b]
        self.i2c.write(self.REG_LED_ALL, cmd)
    def set_led_mode(self, mode):
        self.i2c.write(self.REG_LED_MODE, mode)
    def get_led_color(self, led_id):
        self.i2c.write(self.REG_LED_SPECIFIED, led_id)
        return self.i2c.read(self.REG_LED_SPECIFIED_READ, 3)
    def get_all_led_color(self):
        return self.i2c.read(self.REG_LED_ALL_READ, 12)  # FNK0100 版本返回12字节
    def get_led_mode(self):
        return self.i2c.read(self.REG_LED_MODE_READ)

class FNK0107:
    REG_LED_SPECIFIED       = 0x01
    REG_LED_ALL             = 0x02
    REG_LED_MODE            = 0x03
    REG_FAN_MODE            = 0x04
    REG_FAN_FREQUENCY       = 0x05
    REG_FAN_DUTY            = 0x06
    REG_FAN_THRESHOLD       = 0x07
    REG_POWER_ON_CHECK      = 0x08
    REG_FAN_TEMP_MODE_SPEED = 0x09
    REG_FAN_POWER_SWITCH    = 0x0a
    REG_FAN_PI_FOLLOWING    = 0x0b

    REG_LED_SPECIFIED_READ      = 0xf4
    REG_LED_ALL_READ            = 0xf5
    REG_LED_MODE_READ           = 0xf6
    REG_FAN_MODE_READ           = 0xf7
    REG_FAN_FREQUENCY_READ      = 0xf8
    REG_FAN_DUTY_READ           = 0xf9
    REG_FAN_PI_FOLLOWING_READ   = 0xfa
    REG_FAN_THRESHOLD_READ      = 0xfb
    REG_TEMP_READ               = 0xfc
    REG_FAN_POWER_SWITCH_READ   = 0xf0
    REG_FAN_TEMP_MODE_SPEED_READ = 0xf1
    REG_MOTOR_SPEED_READ        = 0xf2

    def __init__(self, i2c_controller):
        self.i2c = i2c_controller

    # 设置开机检查
    def set_power_on_check(self, state):
        self.i2c.write(self.REG_POWER_ON_CHECK, state)

    # 获取温度方法
    def get_temp(self):
        return self.i2c.read(self.REG_TEMP_READ)

    # 风扇控制方法
    def set_fan_mode(self, mode):
        self.i2c.write(self.REG_FAN_MODE, mode)
    def set_fan_frequency(self, freq):
        frequency = [
            freq & 0xFF,
            (freq >> 8) & 0xFF,
            (freq >> 16) & 0xFF,
            (freq >> 24) & 0xFF
        ]
        self.i2c.write(self.REG_FAN_FREQUENCY, frequency)
    def set_fan_duty(self, duty0, duty1, duty2):
        duty = [duty0, duty1, duty2]
        self.i2c.write(self.REG_FAN_DUTY, duty)
    def set_fan_temp_mode_threshold(self, low_threshold, high_threshold, schmitt=3):
        cmd = [low_threshold, high_threshold, schmitt]
        self.i2c.write(self.REG_FAN_THRESHOLD, cmd)
    def set_fan_temp_mode_speed(self, low_speed, mid_speed, high_speed):
        cmd = [low_speed, mid_speed, high_speed]
        self.i2c.write(self.REG_FAN_TEMP_MODE_SPEED, cmd)
    def set_fan_power_switch(self, state):
        self.i2c.write(self.REG_FAN_POWER_SWITCH, state)
    def set_fan_pi_following(self, min_duty, max_duty):
        cmd = [min_duty, max_duty]
        self.i2c.write(self.REG_FAN_PI_FOLLOWING, cmd)
    def get_fan_mode(self):
        return self.i2c.read(self.REG_FAN_MODE_READ)
    def get_fan_frequency(self):
        arr = self.i2c.read(self.REG_FAN_FREQUENCY_READ, 4)
        freq = (arr[3] << 24) | (arr[2] << 16) | (arr[1] << 8) | arr[0]
        return freq
    def get_fan_duty(self):
        return self.i2c.read(self.REG_FAN_DUTY_READ, 3)
    def get_fan_threshold(self):
        return self.i2c.read(self.REG_FAN_THRESHOLD_READ, 3)
    def get_fan_power_switch(self):
        return self.i2c.read(self.REG_FAN_POWER_SWITCH_READ)
    def get_fan_temp_mode_speed(self):
        return self.i2c.read(self.REG_FAN_TEMP_MODE_SPEED_READ, 3)
    def get_motor_speed(self):
        buf = self.i2c.read(self.REG_MOTOR_SPEED_READ, 10)
        speed = [(buf[i*2+1]<<8) | buf[i*2] for i in range(5)]
        return speed
    def get_fan_pi_following(self):
        return self.i2c.read(self.REG_FAN_PI_FOLLOWING_READ, 2)

    # 彩灯控制方法
    def set_led_color(self, led_id, r, g, b):
        cmd = [led_id, r, g, b]
        self.i2c.write(self.REG_LED_SPECIFIED, cmd)
    def set_all_led_color(self, r, g, b):
        cmd = [r, g, b]
        self.i2c.write(self.REG_LED_ALL, cmd)
    def set_led_mode(self, mode):
        self.i2c.write(self.REG_LED_MODE, mode)
    def get_led_color(self, led_id):
        self.i2c.write(self.REG_LED_SPECIFIED, led_id)
        return self.i2c.read(self.REG_LED_SPECIFIED_READ, 3)
    def get_all_led_color(self):
        return self.i2c.read(self.REG_LED_ALL_READ, 18)  # FNK0107 版本返回18字节
    def get_led_mode(self):
        return self.i2c.read(self.REG_LED_MODE_READ)

class Expansion:
    IIC_ADDRESS = 0x21
    REG_I2C_ADDRESS       = 0x00
    REG_I2C_ADDRESS_READ  = 0xf3
    REG_BRAND             = 0xfd
    REG_VERSION           = 0xfe
    REG_SAVE_FLASH        = 0xff

    def __init__(self, bus_number=1, address=IIC_ADDRESS):
        self.i2c_controller = I2CController(bus_number, address)
        self.case_controller = None
        self.board_type = None
        
        self._initialize_controller()
        self._map_controller_function()

    def get_board_type(self):
        return self.board_type

    def set_i2c_addr(self, addr):
        cmd = [0xaa, 0xbb, addr]
        self.i2c_controller.write(self.REG_I2C_ADDRESS, cmd)
        self.i2c_controller.address = addr
    def get_iic_addr(self):
        return self.i2c_controller.read(self.REG_I2C_ADDRESS_READ)
    def get_brand(self):
        brand_bytes = self.i2c_controller.read(self.REG_BRAND, 9)
        return ''.join(chr(b) for b in brand_bytes).rstrip('\x00')
    def get_version(self):
        version_bytes = self.i2c_controller.read(self.REG_VERSION, 14)
        return ''.join(chr(b) for b in version_bytes).rstrip('\x00')
    def set_save_flash(self, state):
        self.i2c_controller.write(self.REG_SAVE_FLASH, state)
    def end(self):
        self.i2c_controller.close()
    
    def _initialize_controller(self):
        if self.i2c_controller.check_device_exists():
            version = self.get_version()
            if version in ["20250317_V1.0", "20250724_V1.1"]:
                self.case_controller = FNK0100(self.i2c_controller)
                self.board_type = "FNK0100"
            elif version in ["20251015_V1.0", "20251125_V2.1"]:
                self.case_controller = FNK0107(self.i2c_controller)
                self.board_type = "FNK0107"
        else:
            self.board_type = "FNK0108"
    def _map_controller_function(self):
        self.get_temp = self.case_controller.get_temp
        self.set_power_on_check = self.case_controller.set_power_on_check

        self.set_led_color = self.case_controller.set_led_color
        self.set_all_led_color = self.case_controller.set_all_led_color
        self.set_led_mode = self.case_controller.set_led_mode

        self.get_led_color = self.case_controller.get_led_color
        self.get_all_led_color = self.case_controller.get_all_led_color
        self.get_led_mode = self.case_controller.get_led_mode

        self.set_fan_mode = self.case_controller.set_fan_mode
        self.set_fan_frequency = self.case_controller.set_fan_frequency
        self.set_fan_duty = self.case_controller.set_fan_duty
        self.set_fan_temp_mode_threshold = self.case_controller.set_fan_temp_mode_threshold

        self.get_fan_mode = self.case_controller.get_fan_mode
        self.get_fan_frequency = self.case_controller.get_fan_frequency
        self.get_fan_duty = self.case_controller.get_fan_duty
        self.get_fan_threshold = self.case_controller.get_fan_threshold

        if self.board_type == "FNK0100":  
            self.get_fan0_duty = self.case_controller.get_fan0_duty
            self.get_fan1_duty = self.case_controller.get_fan1_duty
        elif self.board_type == "FNK0107": 
            self.set_fan_power_switch = self.case_controller.set_fan_power_switch
            self.set_fan_temp_mode_speed = self.case_controller.set_fan_temp_mode_speed
            self.set_fan_pi_following = self.case_controller.set_fan_pi_following
            self.get_fan_power_switch    = self.case_controller.get_fan_power_switch
            self.get_fan_temp_mode_speed = self.case_controller.get_fan_temp_mode_speed
            self.get_fan_pi_following   = self.case_controller.get_fan_pi_following
            self.get_motor_speed        = self.case_controller.get_motor_speed
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()

    def reset_config(self):
        if self.board_type == "FNK0107":
            self.set_i2c_addr(self.IIC_ADDRESS)                             # set i2c address
            self.set_all_led_color(0, 0, 50)                                # set all led color: r,g,b. 0~255
            self.set_led_mode(4)                                            # led mode: 0: close, 1: RGB, 2: Following, 3: Breathing, 4: Rainbow
            self.case_controller.set_fan_mode(3)                            # fan mode: 0: close, 1: Manual Mode, 2: Auto Temp Mode, 3: PI PWM Following Mode
            self.case_controller.set_fan_frequency(50000)                   # Set fan frequency, 100-1000000
            self.case_controller.set_fan_duty(0, 0, 0)                      # Set the fan1 fan2 fan3 duty cycle, 0~255
            self.case_controller.set_fan_temp_mode_threshold(30, 50, 3)     # Set the temperature threshold, (low temperature, high temperature, schmitt value)
            self.case_controller.set_fan_temp_mode_speed(75, 125, 175)      # Set fan temperature mode speed, (low duty, mid duty, high duty), 0~255
            self.case_controller.set_fan_pi_following(0, 150)               # Set fan PI following map value, (min duty, max duty), 0~255
            self.case_controller.set_fan_power_switch(1)                    # Set fan power switch, 1: Enable, 0: Disable
            self.set_power_on_check(1)                                      # Set power-on check state, 1: Enable, 0: Disable
            self.set_save_flash(1)                                          # Save configuration to flash, 1: Enable, 0: Disable
            time.sleep(0.5)
        elif self.board_type == "FNK0100":
            self.set_i2c_addr(self.IIC_ADDRESS)
            self.set_all_led_color(0, 0, 50)                                # set all led color: r,g,b. 0~255
            self.set_led_mode(4)                                            # led mode: 0: close, 1: RGB, 2: Following, 3: Breathing, 4: Rainbow
            self.case_controller.set_fan_mode(2)                            # fan mode: 0: close, 1: Manual Mode, 2: Auto Mode
            self.case_controller.set_fan_duty(0, 0)                         # Set the fan 1 and fan 2 duty cycle, 0~255
            self.case_controller.set_fan_temp_mode_threshold(30, 45)        # Set the temperature threshold, (low temperature, high temperature)
            self.set_power_on_check(1)                                      # Set power-on check state, 1: Enable, 0: Disable
            self.set_save_flash(1)                                          # Save configuration to flash, 1: Enable, 0: Disable
            time.sleep(0.5)
    
if __name__ == '__main__':
    expansion_board = Expansion()
    expansion_board.reset_config()
    try:
        print(f"Detected board type: {expansion_board.board_type}")
        print(f"Detected version: {expansion_board.get_version()}")
        if expansion_board.board_type == "FNK0107":
            print("Configuring for FNK0107...")
            expansion_board.set_led_mode(3)  
            expansion_board.set_all_led_color(0, 50, 0)             # set all led color: r,g,b. 0~255
            expansion_board.set_fan_power_switch(1)
            expansion_board.set_fan_mode(1)                         # fan mode: 0: close, 1: Manual Mode, 2: Auto Temp Mode, 3: PI PWM Following Mode
            expansion_board.set_fan_frequency(50000)                # Set fan frequency, 100-1000000
            expansion_board.set_fan_duty(255, 255, 255)             # Set the fan1 fan2 fan3 duty cycle, 0~255
            expansion_board.set_fan_temp_mode_threshold(30, 50, 3)  # Set the temperature threshold, (low temperature, high temperature, schmitt)
            expansion_board.set_fan_temp_mode_speed(75, 125, 175)   # Set fan temperature mode speed, (low duty, mid duty, high duty), 0~255
            expansion_board.set_fan_pi_following(0, 255)            # Set fan PI following map value, (min duty, max duty), 0~255
        elif expansion_board.board_type == "FNK0100":
            print("Configuring for FNK0100...")
            expansion_board.set_led_mode(2)
            expansion_board.set_all_led_color(0, 0, 255)
            expansion_board.set_fan_mode(1)                         # fan mode: 0: close, 1: Manual Mode, 2: Auto Temp Mode        
            expansion_board.set_fan_frequency(50000)                # Set fan frequency, 100-1000000
            expansion_board.set_fan_duty(255, 255)                  # Set the fan1 fan2 duty cycle, 0~255
            expansion_board.set_fan_temp_mode_threshold(30, 45)     # Set the temperature threshold, (low temperature, high temperature)
        time.sleep(1)
        print("Configuration done!")

        count = 0
        while True:
            count += 1
            if count % 5 == 0:
                if expansion_board.board_type != "FNK0108":
                    print("Board Type:", expansion_board.board_type)
                    print("I2C Address: 0x{:02X}".format(expansion_board.get_iic_addr()))
                    print("All LED Color:", expansion_board.get_all_led_color())
                    print("LED Mode:", expansion_board.get_led_mode())
                    print("Fan Mode:", expansion_board.get_fan_mode())
                    print("Fan Frequency:", expansion_board.get_fan_frequency())
                    print("Temperature:", expansion_board.get_temp())
                    print("Brand:", expansion_board.get_brand())
                    print("Version:", expansion_board.get_version())
                    
                    if expansion_board.board_type == "FNK0107":
                        print("Fan Duty:", expansion_board.get_fan_duty())
                        print("Fan Threshold:", expansion_board.get_fan_threshold())
                        print("Fan Power Switch:", expansion_board.get_fan_power_switch())
                        print("Fan PI Following:", expansion_board.get_fan_pi_following())
                        print("Motor Speed:", expansion_board.get_motor_speed())
                    elif expansion_board.board_type == "FNK0100":
                        print("Fan0 Duty:", expansion_board.get_fan0_duty())
                        print("Fan1 Duty:", expansion_board.get_fan1_duty())
                        print("Fan Threshold:", expansion_board.get_fan_threshold())
                    
                    print("")
            time.sleep(0.3)

    except Exception as e:
        print("Exception:", e)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        if expansion_board.board_type == "FNK0107":
            expansion_board.set_led_mode(4)
            expansion_board.set_all_led_color(0, 0, 0)
            expansion_board.set_fan_mode(3)
            expansion_board.set_fan_duty(0, 0, 0)
        elif expansion_board.board_type == "FNK0100":
            expansion_board.set_led_mode(4)
            expansion_board.set_all_led_color(0, 0, 0)
            expansion_board.set_fan_mode(1)
            expansion_board.set_fan_frequency(50)
            expansion_board.set_fan_duty(0, 0)
        expansion_board.end()
