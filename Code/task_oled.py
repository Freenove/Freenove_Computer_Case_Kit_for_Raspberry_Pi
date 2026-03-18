from api_oled import OLED
from api_expansion import Expansion
from api_systemInfo import SystemInformation
from api_json import ConfigManager
import atexit
import signal
import time
import sys

class OLED_TASK:

    def __init__(self):
        # Initialize OLED and Expansion objects
        self.convert_to_fahrenheit = False   # Whether to convert to Fahrenheit

        self.oled = None
        self.expansion = None
        self.board_type = None
        self.is_convert_cpu_temp_to_fahrenheit = False
        self.is_convert_case_temp_to_fahrenheit = False
        self.font_size = 12
        self.running = True  # Add flag to control main loop
        
        # Initialize config manager
        self.config_manager = ConfigManager()
        self.screen1_data_format = self.config_manager.get_value('OLED', 'screen1').get('data_format', 0)
        self.screen1_time_format = self.config_manager.get_value('OLED', 'screen1').get('time_format', 0)
        self.screen2_interchange = self.config_manager.get_value('OLED', 'screen2').get('interchange', 0)
        self.screen3_interchange = self.config_manager.get_value('OLED', 'screen3').get('interchange', 0)
        self.screen4_interchange = self.config_manager.get_value('OLED', 'screen4').get('interchange', 0)

        # Cache hwmon path lookup for performance
        self._fan_pwm_path = None

        try:
            self.expansion = Expansion()                            # Initialize Expansion object
            self.board_type = self.expansion.get_board_type()
        except Exception as e:
            sys.exit(1)

        try:
            if self.board_type == "FNK0100":
                self.oled = OLED(rotate_angle=0)
            elif self.board_type == "FNK0107":
                self.oled = OLED(rotate_angle=180)
        except Exception as e:
            sys.exit(1)

        try:
            self.system_information = SystemInformation()
        except Exception as e:
            sys.exit(1)

        atexit.register(self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)

    def celsius_to_fahrenheit(self, celsius):
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9/5) + 32
    
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
            return self.expansion.get_fan_duty()
        except Exception as e:
            return 0

    def get_computer_led_mode(self):
        # Get the computer LED mode using Expansion object
        try:
            return self.expansion.get_led_mode()
        except Exception as e:
            return 0

    def handle_signal(self, signum=None, frame=None):
        try:
            if self.oled:
                self.oled.close()
        except Exception as e:
            print(e)
        
        # Set running flag to False to exit main loop
        self.running = False

    def format_date(self, date_str):
        """Format date based on data_format configuration"""
        # Split the date string (assuming it's in Year-Month-Day format)
        year, month, day = date_str.split('-')
        if self.screen1_data_format == 0:  # Year-Month-Day
            return f"{year}-{month}-{day}"
        elif self.screen1_data_format == 1:  # Month-Day-Year
            return f"{month}-{day}-{year}"
        elif self.screen1_data_format == 2:  # Day-Month-Year
            return f"{day}-{month}-{year}"
        else:  # Default to Year-Month-Day
            return f"{year}-{month}-{day}"

    def format_time(self, time_str):
        """Format time based on time_format configuration"""
        # For simplicity, assume time_str is in HH:MM:SS format
        if self.screen1_time_format == 0:  # HH:MM:SS
            return time_str  # Return full time
        elif self.screen1_time_format == 1:  # 12-hour format
            # Convert 24-hour to 12-hour format
            hour, minute, second = time_str.split(':')
            hour = int(hour)
            am_pm = "AM" if hour < 12 else "PM"
            if hour == 0:
                hour = 12
            elif hour > 12:
                hour -= 12
            return f"{am_pm} {hour}:{minute}:{second}"
        else:  # Default to # HH:MM:SS
            return time_str

    def oled_ui_1_show(self, date, weekday, time):
        self.oled.clear()

        # Draw a large box, same size as screen, no fill, then draw 2 horizontal lines, dividing into 3 rows
        self.oled.draw_rectangle((0, 0, self.oled.width-1, self.oled.height-1), outline="white")
        self.oled.draw_line(((0, 16), (self.oled.width-1, 16)), fill="white")
        self.oled.draw_line(((0, 48), (self.oled.width-1, 48)), fill="white")
        
        # Update configuration
        self.screen1_data_format = self.config_manager.get_value('OLED', 'screen1').get('data_format', 0)
        self.screen1_time_format = self.config_manager.get_value('OLED', 'screen1').get('time_format', 0)

        # Format date and time according to configuration
        formatted_date = self.format_date(date)
        formatted_time = self.format_time(time)

        # First row writes date, second row writes time, third row writes weekday
        self.oled.draw_text(formatted_date, position=((0,0),(128,16)), directory="center", offset=(0, 1), font_size=self.font_size)
        if self.screen1_time_format == 1:
            self.oled.draw_text(formatted_time, position=((0,16),(128,48)), directory="center", offset=(0, 5), font_size=18)
        else:
            self.oled.draw_text(formatted_time, position=((0,16),(128,48)), directory="center", offset=(0, 2), font_size=24)
        self.oled.draw_text(weekday, position=((0,48),(128,64)), directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.show()

    def oled_ui_2_show(self, ip_address, cpu_usage, memory_usage, disk_usage):
        self.oled.clear()

        # Draw basic interface outline
        self.oled.draw_rectangle((0, 0, self.oled.width-1, self.oled.height-1), outline="white")
        self.oled.draw_line(((0, 16), (self.oled.width-1, 16)), fill="white")
        self.oled.draw_line(((43,16),(43, self.oled.height-1)), fill="white")
        self.oled.draw_line(((86,16),(86, self.oled.height-1)), fill="white")

        # Write Raspberry Pi IP address in first row
        self.oled.draw_text("IP:"+ip_address, position=((0,0),(128,16)),  directory="center", offset=(0, 0), font_size=self.font_size)

        # Get screen2 interchange setting
        self.screen2_interchange = self.config_manager.get_value('OLED', 'screen2').get('interchange', 0)

        # Define positions based on interchange setting
        if self.screen2_interchange == 1:
            # Order: CPU, DISK, MEM
            cpu_pos = ((0,16),(42,32))
            mem_pos = ((87,16),(128,32))
            disk_pos = ((43,16),(86,32))
            cpu_circle_pos = (21,46)
            mem_circle_pos = (107,46)
            disk_circle_pos = (64,46)
        elif self.screen2_interchange == 2:
            # Order: MEM, CPU, DISK
            cpu_pos = ((43,16),(86,32))
            mem_pos = ((0,16),(42,32))
            disk_pos = ((87,16),(128,32))
            cpu_circle_pos = (64,46)
            mem_circle_pos = (21,46)
            disk_circle_pos = (107,46)
        elif self.screen2_interchange == 3:
            # Order: DISK, CPU, MEM
            cpu_pos = ((43,16),(86,32))
            mem_pos = ((87,16),(128,32))
            disk_pos = ((0,16),(42,32))
            cpu_circle_pos = (64,46)
            mem_circle_pos = (107,46)
            disk_circle_pos = (21,46)
        elif self.screen2_interchange == 4:
            # Order: MEM, DISK, CPU
            cpu_pos = ((87,16),(128,32))
            mem_pos = ((0,16),(42,32))
            disk_pos = ((43,16),(86,32))
            cpu_circle_pos = (107,46)
            mem_circle_pos = (21,46)
            disk_circle_pos = (64,46)
        elif self.screen2_interchange == 5:
            # Order: DISK, MEM, CPU
            cpu_pos = ((87,16),(128,32))
            mem_pos = ((43,16),(86,32))
            disk_pos = ((0,16),(42,32))
            cpu_circle_pos = (107,46)
            mem_circle_pos = (64,46)
            disk_circle_pos = (21,46)
        else:
            # Default: CPU, MEM, DISK
            cpu_pos = ((0,16),(42,32))
            mem_pos = ((43,16),(86,32))
            disk_pos = ((87,16),(128,32))
            cpu_circle_pos = (21,46)
            mem_circle_pos = (64,46)
            disk_circle_pos = (107,46)
        
        # Draw text labels in specified positions
        self.oled.draw_text("CPU",  position=cpu_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.draw_text("MEM",  position=mem_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.draw_text("DISK", position=disk_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        
        # Draw percentage circles in corresponding positions
        self.oled.draw_circle_with_percentage(cpu_circle_pos, 16, cpu_usage, outline="white", fill="white")
        self.oled.draw_circle_with_percentage(mem_circle_pos, 16, memory_usage, outline="white", fill="white")
        self.oled.draw_circle_with_percentage(disk_circle_pos, 16, disk_usage, outline="white", fill="white")
        self.oled.show()
    
    def oled_ui_3_show(self, pi_temperature, cpu_temperature):
        self.oled.clear()

        # Convert temperature to Fahrenheit
        cpu_fahrenheit = round(cpu_temperature * 1.8 + 32)
        pi_fahrenheit = round(pi_temperature * 1.8 + 32)

        # Draw basic interface outline
        self.oled.draw_rectangle((0, 0, self.oled.width-1, self.oled.height-1), outline="white")
        self.oled.draw_line(((64, 0), (64, self.oled.height-1)), fill="white")

        # Get screen3 interchange setting
        self.screen3_interchange = self.config_manager.get_value('OLED', 'screen3').get('interchange', 0)
        self.is_convert_cpu_temp_to_fahrenheit = self.config_manager.get_value('OLED', 'screen3').get('cpu_temp_celsius_or_fahrenheit', False)
        self.is_convert_case_temp_to_fahrenheit = self.config_manager.get_value('OLED', 'screen3').get('case_temp_celsius_or_fahrenheit', False)

        if self.screen3_interchange == 1:
            # First row first column shows Pi temperature, first row second column shows PC temperature
            self.oled.draw_text("Case", position=((0,0),(64,16)), directory="center", offset=(0, 0), font_size=self.font_size)
            self.oled.draw_text("Pi", position=((65,0),(128,16)), directory="center", offset=(0, 0), font_size=self.font_size)
            # Draw a dial in the center of each column of the second row
            self.oled.draw_dial(center_xy=(32,34), radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=cpu_temperature, start_value=0, end_value=100)
            self.oled.draw_dial(center_xy=(96,34), radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=pi_temperature, start_value=0, end_value=100)
            # First row first column shows Pi temperature, first row second column shows CPU temperature
            if self.is_convert_cpu_temp_to_fahrenheit:
                self.oled.draw_text("{}℉".format(cpu_fahrenheit), position=((0,48),(64,64)), directory="center", offset=(0, 0), font_size=self.font_size)
            else:
                self.oled.draw_text("{}℃".format(cpu_temperature), position=((0,48),(64,64)), directory="center", offset=(0, 0), font_size=self.font_size)
            if self.is_convert_case_temp_to_fahrenheit:
                self.oled.draw_text("{}℉".format(pi_fahrenheit), position=((65,48),(128,64)), directory="center", offset=(0, 0), font_size=self.font_size)
            else:
                self.oled.draw_text("{}℃".format(round(pi_temperature)), position=((65,48),(128,64)), directory="center", offset=(0, 0), font_size=self.font_size)
        else:
            # First row first column shows Pi temperature, first row second column shows PC temperature
            self.oled.draw_text("Pi", position=((0,0),(64,16)), directory="center", offset=(0, 0), font_size=self.font_size)
            self.oled.draw_text("Case", position=((65,0),(128,16)), directory="center", offset=(0, 0), font_size=self.font_size)
            # Draw a dial in the center of each column of the second row
            self.oled.draw_dial(center_xy=(32,34), radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=pi_temperature, start_value=0, end_value=100)
            self.oled.draw_dial(center_xy=(96,34), radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=cpu_temperature, start_value=0, end_value=100)
            # First row first column shows Pi temperature, first row second column shows CPU temperature
            if self.is_convert_cpu_temp_to_fahrenheit:
                self.oled.draw_text("{}℉".format(cpu_fahrenheit), position=((65,48),(128,64)), directory="center", offset=(0, 0), font_size=self.font_size)
            else:
                self.oled.draw_text("{}℃".format(round(pi_temperature)), position=((0,48),(64,64)), directory="center", offset=(0, 0), font_size=self.font_size)
            if self.is_convert_case_temp_to_fahrenheit:
                self.oled.draw_text("{}℉".format(pi_fahrenheit), position=((0,48),(64,64)), directory="center", offset=(0, 0), font_size=self.font_size)
            else:
                self.oled.draw_text("{}℃".format(cpu_temperature), position=((65,48),(128,64)), directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.show()

    def oled_ui_4_show(self, duty):
        self.oled.clear()
        # Draw basic interface outline
        self.oled.draw_rectangle((0, 0, self.oled.width-1, self.oled.height-1), outline="white")
        self.oled.draw_line(((43, 0), (43, self.oled.height-1)), fill="white")
        self.oled.draw_line(((86, 0), (86, self.oled.height-1)), fill="white")
        
        # Get screen4 interchange setting
        self.screen4_interchange = self.config_manager.get_value('OLED', 'screen4').get('interchange', 0)
        
        # Define positions based on interchange setting
        if self.screen4_interchange == 1:
            # Order: Pi, C2, C1
            pi_pos = ((0,0),(42,16))
            c1_pos = ((87,0),(128,16))
            c2_pos = ((43,0),(86,16))
            pi_dial_pos = (21,34)
            c1_dial_pos = (105,34)
            c2_dial_pos = (63,34)
            pi_percent_pos = ((0,48),(42,64))
            c1_percent_pos = ((86,48),(128,64))
            c2_percent_pos = ((43,48),(85,64))
        elif self.screen4_interchange == 2:
            # Order: C1, Pi, C2
            pi_pos = ((43,0),(86,16))
            c1_pos = ((0,0),(42,16))
            c2_pos = ((87,0),(128,16))
            pi_dial_pos = (63,34)
            c1_dial_pos = (21,34)
            c2_dial_pos = (105,34)
            pi_percent_pos = ((43,48),(85,64))
            c1_percent_pos = ((0,48),(42,64))
            c2_percent_pos = ((86,48),(128,64))
        elif self.screen4_interchange == 3:
            # Order: C2, Pi, C1
            pi_pos = ((43,0),(86,16))
            c1_pos = ((87,0),(128,16))
            c2_pos = ((0,0),(42,16))
            pi_dial_pos = (63,34)
            c1_dial_pos = (105,34)
            c2_dial_pos = (21,34)
            pi_percent_pos = ((43,48),(85,64))
            c1_percent_pos = ((86,48),(128,64))
            c2_percent_pos = ((0,48),(42,64))
        elif self.screen4_interchange == 4:
            # Order: C1, C2, Pi
            pi_pos = ((87,0),(128,16))
            c1_pos = ((0,0),(42,16))
            c2_pos = ((43,0),(86,16))
            pi_dial_pos = (105,34)
            c1_dial_pos = (21,34)
            c2_dial_pos = (63,34)
            pi_percent_pos = ((86,48),(128,64))
            c1_percent_pos = ((0,48),(42,64))
            c2_percent_pos = ((43,48),(85,64))
        elif self.screen4_interchange == 5:
            # Order: C2, C1, Pi
            pi_pos = ((87,0),(128,16))
            c1_pos = ((43,0),(86,16))
            c2_pos = ((0,0),(42,16))
            pi_dial_pos = (105,34)
            c1_dial_pos = (63,34)
            c2_dial_pos = (21,34)
            pi_percent_pos = ((86,48),(128,64))
            c1_percent_pos = ((43,48),(85,64))
            c2_percent_pos = ((0,48),(42,64))
        else:
            # Default: Pi, C1, C2
            pi_pos = ((0,0),(42,16))
            c1_pos = ((43,0),(86,16))
            c2_pos = ((87,0),(128,16))
            pi_dial_pos = (21,34)
            c1_dial_pos = (63,34)
            c2_dial_pos = (105,34)
            pi_percent_pos = ((0,48),(42,64))
            c1_percent_pos = ((43,48),(85,64))
            c2_percent_pos = ((86,48),(128,64))
        
        # Write titles in first row
        self.oled.draw_text("Pi",  position=pi_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.draw_text("C1",  position=c1_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.draw_text("C2",  position=c2_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        
        # Draw dials in second row
        percentage_value = [round(duty[i]/255*100) for i in range(3)]
        self.oled.draw_dial(center_xy=pi_dial_pos, radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=percentage_value[0], start_value=0, end_value=100)
        self.oled.draw_dial(center_xy=c1_dial_pos, radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=percentage_value[1], start_value=0, end_value=100)
        self.oled.draw_dial(center_xy=c2_dial_pos, radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=percentage_value[2], start_value=0, end_value=100)
        
        # Print duty cycle percentage values in third row
        self.oled.draw_text("{}%".format(percentage_value[0]), position=pi_percent_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.draw_text("{}%".format(percentage_value[1]), position=c1_percent_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.draw_text("{}%".format(percentage_value[2]), position=c2_percent_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        
        self.oled.show()

    def run_oled_loop(self):
        """Main monitoring loop - single-threaded infinite loop for both OLED display and fan control"""
        oled_counter = 0  # Counter to control OLED update frequency
        screen_start_time = time.time()  # Record the start time of current screen
        current_screen = 0  # Current screen index
        
        while self.running:
            # Update data every 0.3 seconds
            current_date = self.system_information.get_raspberry_pi_date()
            current_weekday = self.system_information.get_raspberry_pi_weekday()
            current_time = self.system_information.get_raspberry_pi_time()

            ip_address = self.system_information.get_raspberry_pi_ip_address()
            cpu_usage = self.system_information.get_raspberry_pi_cpu_usage()
            memory_usage = self.system_information.get_raspberry_pi_memory_usage()
            disk_usage = self.system_information.get_raspberry_pi_disk_usage()

            cpu_temperature = self.system_information.get_raspberry_pi_cpu_temperature()
            computer_temperature = self.get_computer_temperature()

            current_pi_duty = self.system_information.get_raspberry_pi_fan_duty()
            computer_fan_duty = self.get_computer_fan_duty()
            
            # Get display time configuration for each screen
            screen1_duration = self.config_manager.get_value('OLED', 'screen1').get('display_time', 3.0)
            screen2_duration = self.config_manager.get_value('OLED', 'screen2').get('display_time', 3.0)
            screen3_duration = self.config_manager.get_value('OLED', 'screen3').get('display_time', 3.0)
            screen4_duration = self.config_manager.get_value('OLED', 'screen4').get('display_time', 3.0)

            screen1_is_run_on_oled = self.config_manager.get_value('OLED', 'screen1').get('is_run_on_oled', True)
            screen2_is_run_on_oled = self.config_manager.get_value('OLED', 'screen2').get('is_run_on_oled', True)
            screen3_is_run_on_oled = self.config_manager.get_value('OLED', 'screen3').get('is_run_on_oled', True)
            screen4_is_run_on_oled = self.config_manager.get_value('OLED', 'screen4').get('is_run_on_oled', True)

            # Determine which screens need to be displayed according to configuration
            active_screens = []
            screen_durations = []
            screen_functions = []
            
            if screen1_is_run_on_oled:
                active_screens.append(0)
                screen_durations.append(screen1_duration)
                screen_functions.append(lambda: self.oled_ui_1_show(current_date, current_weekday, current_time))
            
            if screen2_is_run_on_oled:
                active_screens.append(1)
                screen_durations.append(screen2_duration)
                screen_functions.append(lambda: self.oled_ui_2_show(ip_address, cpu_usage, memory_usage[0], disk_usage[0]))
            
            if screen3_is_run_on_oled:
                active_screens.append(2)
                screen_durations.append(screen3_duration)
                screen_functions.append(lambda: self.oled_ui_3_show(cpu_temperature, computer_temperature))
            
            if screen4_is_run_on_oled:
                active_screens.append(3)
                screen_durations.append(screen4_duration)
                screen_functions.append(lambda: self.oled_ui_4_show([current_pi_duty, computer_fan_duty[0], computer_fan_duty[1]]))
            
            # Skip if no active screens
            if not active_screens:
                time.sleep(0.3)
                continue
            
            # Get the current active screen index
            current_active_index = current_screen % len(active_screens)
            current_screen_index = active_screens[current_active_index]
            
            # Check if screen needs to be switched (based on time instead of counter)
            elapsed_time = time.time() - screen_start_time
            if elapsed_time >= screen_durations[current_active_index]:
                current_screen = (current_screen + 1) % len(active_screens)
                current_active_index = current_screen % len(active_screens)
                screen_start_time = time.time()
            
            # Update OLED every 0.3 seconds
            try:
                # Use the function of current active screen
                screen_functions[current_active_index]()
            except Exception as e:
                print(e)
            time.sleep(0.3)  # Base interval of 0.3 second


if __name__ == "__main__":
    oled_task= None
    try:
        oled_task = OLED_TASK()

        # Use simple infinite loop instead of threading
        oled_task.run_oled_loop()

    except KeyboardInterrupt:
        print("\nShutdown requested by user (Ctrl+C)")
    except Exception as e:
        print(f"Unexpected error: {e}")