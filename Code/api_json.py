# api_json.py
import json
import os
import fcntl
from api_expansion import Expansion


class ConfigManager:
    def __init__(self, config_file='app_config.json'):
        """
        Initialize configuration manager
        
        Args:
            config_file (str): Configuration file path
        """
        self.expansion = Expansion()
        self.config_file = config_file
        self.config_data = {}
        self.load_config()

    def load_config(self):
        """
        Load configuration data from JSON file with file locking
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    try:
                        fcntl.flock(f.fileno(), fcntl.LOCK_SH)  
                        content = f.read().strip()
                        if content:  
                            self.config_data = json.loads(content)
                        else:  
                            print(f"Config file {self.config_file} is empty, creating default config")
                            self.create_config_file()
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN) 
            else:
                self.create_config_file()
        except json.JSONDecodeError as e:
            print(f"JSON decode error in {self.config_file}: {e}")
            print("Creating default configuration...")
            self.create_config_file()
        except Exception as e:
            print(f"Error loading configuration file: {e}")
            self.create_config_file()
            self.config_data = {}
    
    def save_config(self):
        try:
            directory = os.path.dirname(self.config_file)
            if directory:
                os.makedirs(directory, exist_ok=True)
                
            temp_file = self.config_file + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)  
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            os.rename(temp_file, self.config_file)
        except Exception as e:
            print(f"Error saving configuration file: {e}")
    
    def get_value(self, section, key):
        """
        Get configuration value
        
        Args:
            section (str): Configuration section name
            key (str): Configuration item name
            
        Returns:
            Configuration item value
        """
        return self.config_data.get(section, {}).get(key, None)
    
    def set_value(self, section, key, value):
        """
        Set configuration value
        
        Args:
            section (str): Configuration section name
            key (str): Configuration item name
            value: Value to set
        """
        if section not in self.config_data:
            self.config_data[section] = {}
        self.config_data[section][key] = value
    
    def get_section(self, section):
        """
        Get entire configuration section
        
        Args:
            section (str): Configuration section name
            
        Returns:
            dict: Configuration section data
        """
        self.load_config()
        return self.config_data.get(section, {})
    
    def set_section(self, section, data):
        """
        Set entire configuration section
        
        Args:
            section (str): Configuration section name
            data (dict): Data to set
        """
        self.config_data[section] = data
    
    def get_all_config(self):
        """
        Get all configuration data
        
        Returns:
            dict: All configuration data
        """
        return self.config_data
    
    def set_all_config(self, config_data):
        """
        Set all configuration data
        
        Args:
            config_data (dict): All configuration data
        """
        self.config_data = config_data
 
    def delete_config_file(self):
        """ Delete configuration file """
        try:
            os.remove(self.config_file)
        except Exception as e:
            print(f"Error deleting configuration file: {e}")

    def create_config_file(self):
        # Initialize default values
        led_mode_default = 0
        fan_mode_default = 0
        fan_temp_threshold_default = [30, 50, 3]
        fan_temp_speed_default = [75, 125, 175]
        fan_map_default = [0, 255]
        
        # Determine board type to handle differences between FNK0100 and FNK0107
        board_type = self.expansion.get_board_type()
        
        # Safely get configuration from expansion board based on board type
        try:
            led_mode = self.expansion.get_led_mode()
            # Map actual LED modes to UI-friendly values
            if led_mode == 4:  # Rainbow mode
                led_mode_default = 0
            elif led_mode == 3:  # Breathing mode
                led_mode_default = 1
            elif led_mode == 2:  # Following mode
                led_mode_default = 2
            elif led_mode == 1:  # RGB mode
                led_mode_default = 3
            elif led_mode == 0:  # Off
                led_mode_default = 5
            else:
                led_mode_default = 0  # Default to rainbow mode
                
            fan_mode = self.expansion.get_fan_mode()
            # Map actual fan modes to UI-friendly values based on board type
            if board_type == "FNK0107":
                # FNK0107 has 4 fan modes: 0-close, 1-Manual, 2-Auto Temp, 3-PI PWM Following
                if fan_mode == 3:  # PI PWM Following Mode
                    fan_mode_default = 1
                elif fan_mode == 2:  # Auto Temp Mode
                    fan_mode_default = 0
                elif fan_mode == 1:  # Manual Mode
                    fan_mode_default = 2
                elif fan_mode == 0:  # Off
                    fan_mode_default = 4
                else:
                    fan_mode_default = 0  # Default to Auto Temp Mode
            else:
                # FNK0100 has 3 fan modes: 0-close, 1-Manual, 2-Auto
                if fan_mode == 2:  # Auto Mode
                    fan_mode_default = 0
                elif fan_mode == 1:  # Manual Mode
                    fan_mode_default = 2
                elif fan_mode == 0:  # Off
                    fan_mode_default = 3
                else:
                    fan_mode_default = 0  # Default to Auto Mode
                    
            # Get current values from the expansion board based on board type
            if board_type == "FNK0107":
                # FNK0107-specific functions
                fan_temp_threshold_default = self.expansion.get_fan_threshold()  # Returns 3 values: [low, high, schmitt]
                fan_temp_speed_default = self.expansion.get_fan_temp_mode_speed()  # Returns 3 values: [low, mid, high]
                fan_map_default = self.expansion.get_fan_pi_following()  # Returns 2 values: [min, max]
            else:
                # FNK0100-specific functions
                fnk0100_threshold = self.expansion.get_fan_threshold()  # Returns 2 values: [low, high]
                # Convert to 3-element array by adding default schmitt trigger value
                fan_temp_threshold_default = [fnk0100_threshold[0], fnk0100_threshold[1], 3]
                # FNK0100 doesn't have temp mode speeds, so keep defaults
                # FNK0100 doesn't have PI following, so keep defaults
        
        except Exception as e:
            print(f"Error getting configuration from expansion board: {e}")
        
        try:
            if not os.path.exists(self.config_file):
                # Create basic configuration structure without optional fan features
                config = {
                    "Monitor": {
                        "screen_orientation": 0,
                        "follow_led_color": 0
                    },
                    "LED": {
                        "mode": led_mode_default,
                        "red_value": 0,
                        "green_value": 0,
                        "blue_value": 255,
                        "task_name": "task_led.py",
                        "is_run_on_startup": True
                    },
                    "Fan": {
                        "mode": fan_mode_default,
                        "task_name": "task_fan.py",
                        "is_run_on_startup": True
                    },
                    "OLED": {
                        "task_name": "task_oled.py",
                        "is_run_on_startup": True,
                        "screen1": {
                            "data_format": 0,
                            "time_format": 0,
                            "display_time": 3.0,
                            "is_run_on_oled": True
                        },
                        "screen2": {
                            "interchange": 0,
                            "display_time": 3.0,
                            "is_run_on_oled": True
                        },
                        "screen3": {
                            "interchange": 0,
                            "display_time": 3.0,
                            "cpu_temp_celsius_or_fahrenheit": False,
                            "case_temp_celsius_or_fahrenheit": False,
                            "is_run_on_oled": True
                        },
                        "screen4": {
                            "interchange": 0,
                            "display_time": 3.0,
                            "is_run_on_oled": True
                        }
                    },
                    "Service": {
                        "is_exist_on_rpi": False,
                        "is_run_on_startup": False
                    }
                }
                
                # Add fan configuration items based on board capabilities
                # Add basic fan duty cycle settings (common to both boards)
                config["Fan"]["mode1_fan_group1"] = 75
                config["Fan"]["mode1_fan_group2"] = 75
                
                # Add board-specific fan duty cycle settings
                if board_type == "FNK0107":
                    # Add third fan for FNK0107
                    config["Fan"]["mode1_fan_group3"] = 75
                
                # Add temperature threshold settings (number varies by board)
                config["Fan"]["mode2_low_temp_threshold"] = fan_temp_threshold_default[0]
                config["Fan"]["mode2_high_temp_threshold"] = fan_temp_threshold_default[1]
                
                # Add schmitt trigger setting only for FNK0107 (which returns 3 values from get_fan_threshold)
                if board_type == "FNK0107":
                    config["Fan"]["mode2_temp_schmitt"] = fan_temp_threshold_default[2]
                
                # Add temperature mode speeds only for FNK0107
                if board_type == "FNK0107":
                    config["Fan"]["mode2_low_speed"] = fan_temp_speed_default[0]
                    config["Fan"]["mode2_middle_speed"] = fan_temp_speed_default[1]
                    config["Fan"]["mode2_high_speed"] = fan_temp_speed_default[2]
                
                # Add PI following settings only for FNK0107
                if board_type == "FNK0107":
                    config["Fan"]["mode3_min_speed_mapping"] = fan_map_default[0]
                    config["Fan"]["mode3_max_speed_mapping"] = fan_map_default[1]
                
                self.config_data = config
                self.save_config()
            else:
                print(f"Configuration file already exists: {self.config_file}")
        except Exception as e:
            print(f"Error creating configuration file: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()


if __name__ == '__main__':
    # Create configuration manager instance (automatically loads configuration file)
    config_manager = ConfigManager('app_config.json')

    # Directly operate on all configuration data
    all_config = config_manager.get_all_config()
    print(f"All config: {all_config}")

    # Read configuration value
    led_mode = config_manager.get_value('LED', 'mode')
    print(f"LED Mode: {led_mode}")

    # Get entire configuration section
    fan_config = config_manager.get_section('Fan')
    print(f"FAN config: {fan_config}")

    # # Modify configuration value
    # config_manager.set_value('LED', 'mode', 1)
    # config_manager.set_value('LED', 'red_value', 255)

    # # Save modified configuration
    # config_manager.save_config()

    # # Get modified configuration data
    # updated_config = config_manager.get_all_config()
    # print(f"Updated config: {updated_config}")

    # # Modify configuration value
    # config_manager.set_value('LED', 'mode', 2)
    # config_manager.set_value('LED', 'red_value', 0)

    # # Save modified configuration
    # config_manager.save_config()