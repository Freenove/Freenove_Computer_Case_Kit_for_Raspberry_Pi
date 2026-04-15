# app_ui.py
import os
import sys
import time
import subprocess

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor

from app_ui_monitor import MonitoringTab               # Import monitoring interface
from app_ui_led import LedTab                          # Import LED interface
from app_ui_fan import FNK0100_FanTab,FNK0107_FanTab   # Import fan control interface
from app_ui_oled import OledTab                        # Import OLED interface
from app_ui_setting import SettingTab                  # Import settings interface

from api_json import ConfigManager                     # Import configuration management module
from api_expansion import Expansion                    # Import expansion module
from api_systemInfo import SystemInformation           # Import system information module
from api_service import ServiceGenerator               # Import background task generator module

class MainWindow(QMainWindow):
    def __init__(self, width=480, height=740):
        super().__init__()
        self.ui_factor = 1.0
        self.ui_main_width = width
        self.ui_main_height = height
        self.ui_fan_temp_mode_threshold_range = [[10, 40], [50, 80], [1, 5]]     # Fan temperature mode threshold range
        self.setWindowTitle("Freenove_Computer_Case_Kit_for_Raspberry_Pi")        # Set window title
        self.setGeometry(0, 0, self.ui_main_width, self.ui_main_height)          # Set window size
        self.setMinimumSize(round(self.ui_main_width*self.ui_factor), round(self.ui_main_height*self.ui_factor))  # Set minimum size
        self.is_convert_temp_to_fahrenheit = False                               # Set whether to convert temperature to Fahrenheit

        self.config_manager = ConfigManager()                        # Create configuration management object
        self.expansion = Expansion()                                 # Create expansion module object
        self.system_info = SystemInformation()                       # Create system information object
        self.service_generator = ServiceGenerator()                  # Create background task generator object

        self.screen_direction = 0                                    # Screen orientation
        self.ui_follow_led_color = 0                                 # Whether to follow LED color
        self.color_combinations = [
            ("#C53A3A", '#FFD1D1'),  # Red
            ('#4ECDC4', '#D1F0EE'),  # Blue-green
            ('#FFA500', '#FFE5B4'),  # Orange
            ('#4ECEB4', '#D1F2D1'),  # Green
            ('#EAEA77', '#FFFFF0'),  # Yellow
            ('#45B7D1', '#D1EBF0'),  # Blue
            ('#DDA0DD', '#F0E0F0'),  # Plum
            ('#F7DC6F', '#FBF5D9')   # Gold
        ]
        self.metric_labels = [
            "CPU Usage",     # CPU usage
            "RAM Usage",     # Memory usage
            "CPU Temp",      # Raspberry Pi temperature
            "Case Temp",     # Case temperature
            "Storage Usage", # Storage usage
            "RPi PWM",       # Raspberry Pi fan PWM
            "Case PWM1",     # Case PWM1
            "Case PWM2"      # Case PWM2
        ]

        self.monitoring_tab = None                                   # Create monitoring interface object
        self.led_tab = None                                          # Create LED interface object
        self.fan_tab = None                                          # Create fan control interface object
        self.setting_tab = None                                      # Create settings interface object

        self.monitor_update_data_timer = QTimer(self)                # Create monitor interface data update timer
        self.monitor_update_data_timer_is_running = True             # Whether timer is running
        self.monitor_update_color_timer = QTimer(self)               # Create monitor interface color update timer
        self.monitor_update_color_timer_is_running = False           # Whether timer is running

        self.led_mode = 0                                            # LED mode
        self.led_process = None                                      # LED process object
        self.led_slider_color = [0, 0, 0]                            # LED slider color values

        self.fan_mode = 0                                            # Fan mode
        self.fan_manual_mode_duty = [75, 75, 75]                     # Fan manual mode duty cycle values for 3 fan groups
        self.fan_temp_mode_threshold = [30, 50, 3]                   # Fan temperature mode threshold parameters
        self.fan_temp_mode_duty = [75, 125, 175]                     # Fan temperature mode duty cycle parameters
        self.fan_pi_follows_duty_map = [0, 255]                      # Fan follows Raspberry Pi mode duty cycle mapping parameters
        self.fan_process = None                                      # Used to store running subprocess

        self.oled_screen_interchange = [0, 0, 0, 0, 0]               # OLED screen interchange parameters
        self.oled_screen_display_time =  [3.0, 3.0, 3.0, 3.0]        # OLED screen display time
        self.oled_screen_is_run_on_oled  = [True, True, True, True]  # Whether to run on OLED
        self.oled_process = None                                     # OLED process object

        self.init_ui()                                               # Initialize UI
        self.load_ui_config()                                        # Load UI parameters
        self.load_ui_events()                                        # Set events
    def init_ui(self):
        # Set black background for main window
        self.setStyleSheet("""
            background-color: #000000;
            border: 1px solid #444444;
            outline: none;
        """)
        # Create tab widget
        self.tab_widget = QTabWidget()

        # Create monitor tab
        self.monitoring_tab = MonitoringTab(self.width(), self.height())
        self.monitoring_tab.setFocusPolicy(Qt.NoFocus)

        # Create led tab
        self.led_tab = LedTab(self.width(), self.height())
        self.led_tab.setFocusPolicy(Qt.NoFocus)

        # Create fan tab
        if self.expansion.get_board_type() == "FNK0100":
            self.fan_tab = FNK0100_FanTab(self.width(), self.height())
        elif self.expansion.get_board_type() == "FNK0107":
            self.fan_tab = FNK0107_FanTab(self.width(), self.height())
        self.fan_tab.setFocusPolicy(Qt.NoFocus)

        # Create Oled tab
        self.oled_tab = OledTab(self.width(), self.height())
        self.oled_tab.setFocusPolicy(Qt.NoFocus)

        # Create setting tab
        self.setting_tab = SettingTab(self.width(), self.height())
        self.setting_tab.setFocusPolicy(Qt.NoFocus)

        # Add tab to tab widget
        self.tab_widget.addTab(self.monitoring_tab, "Monitor")
        self.tab_widget.addTab(self.led_tab, "LED")
        self.tab_widget.addTab(self.fan_tab, "Fan")
        self.tab_widget.addTab(self.oled_tab, "OLED")
        self.tab_widget.addTab(self.setting_tab, "Settings")
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #333333;
                background-color: black;
            }
            QTabBar::tab {
                background-color: #444444;
                color: white;
                padding: 2px;
                border: 1px solid #333333;
                font-size: 16px;
                font-weight: bold;
                height: 50px;
                width: 80px;
            }
            QTabBar::tab:selected {
                background-color: #555555;
                color: white;
            }
        """)

        # Set central widget
        self.setCentralWidget(self.tab_widget)
    def load_ui_config(self):
        """Load configuration"""
        self.ui_follow_led_color = self.config_manager.get_value('Monitor', 'follow_led_color') or 0
        
        if self.is_convert_temp_to_fahrenheit == True:
            self.monitor_is_convert_cpu_temp_to_fahrenheit = True
            self.monitor_is_convert_case_temp_to_fahrenheit = True
        else:
            self.monitor_is_convert_cpu_temp_to_fahrenheit = False       # Whether to convert CPU temperature to Fahrenheit
            self.monitor_is_convert_case_temp_to_fahrenheit = False      # Whether to convert case temperature to Fahrenheit
        
        oled_screen_config = self.config_manager.get_value('OLED', 'screen3')
        oled_screen_config.update({
            'cpu_temp_celsius_or_fahrenheit': self.monitor_is_convert_cpu_temp_to_fahrenheit,
            'case_temp_celsius_or_fahrenheit': self.monitor_is_convert_case_temp_to_fahrenheit
        })
        self.config_manager.set_value('OLED', 'screen3', oled_screen_config)
        self.config_manager.save_config()

        self.led_mode = self.config_manager.get_value('LED', 'mode') or 0
        self.led_slider_color[0] = self.config_manager.get_value('LED', 'red_value') or 0
        self.led_slider_color[1] = self.config_manager.get_value('LED', 'green_value') or 0
        self.led_slider_color[2] = self.config_manager.get_value('LED', 'blue_value') or 255

        self.fan_mode = self.config_manager.get_value('Fan', 'mode') or 0
        self.fan_manual_mode_duty[0] = self.config_manager.get_value('Fan', 'mode1_fan_group1') or 75
        self.fan_manual_mode_duty[1] = self.config_manager.get_value('Fan', 'mode1_fan_group2') or 75
        self.fan_manual_mode_duty[2] = self.config_manager.get_value('Fan', 'mode1_fan_group3') or 75
        self.fan_temp_mode_threshold[0] = self.config_manager.get_value('Fan', 'mode2_low_temp_threshold') or 30
        self.fan_temp_mode_threshold[1] = self.config_manager.get_value('Fan', 'mode2_high_temp_threshold') or 50
        self.fan_temp_mode_threshold[2] = self.config_manager.get_value('Fan', 'mode2_temp_schmitt') or 3
        self.fan_temp_mode_duty[0] = self.config_manager.get_value('Fan', 'mode2_low_speed') or 75
        self.fan_temp_mode_duty[1] = self.config_manager.get_value('Fan', 'mode2_middle_speed') or 125
        self.fan_temp_mode_duty[2] = self.config_manager.get_value('Fan', 'mode2_high_speed') or 175
        self.fan_pi_follows_duty_map[0] = self.config_manager.get_value('Fan', 'mode3_min_speed_mapping') or 0
        self.fan_pi_follows_duty_map[1] = self.config_manager.get_value('Fan', 'mode3_max_speed_mapping') or 255

        self.oled_screen_interchange[0] = self.config_manager.get_value('OLED', 'screen1').get('data_format', 0)
        self.oled_screen_interchange[1] = self.config_manager.get_value('OLED', 'screen1').get('time_format', 0)
        self.oled_screen_interchange[2] = self.config_manager.get_value('OLED', 'screen2').get('interchange', 0)
        self.oled_screen_interchange[3] = self.config_manager.get_value('OLED', 'screen3').get('interchange', 0)
        self.oled_screen_interchange[4] = self.config_manager.get_value('OLED', 'screen4').get('interchange', 0)
        self.oled_screen_display_time[0] = self.config_manager.get_value('OLED', 'screen1').get('display_time', 3.0)
        self.oled_screen_display_time[1] = self.config_manager.get_value('OLED', 'screen2').get('display_time', 3.0)
        self.oled_screen_display_time[2] = self.config_manager.get_value('OLED', 'screen3').get('display_time', 3.0)
        self.oled_screen_display_time[3] = self.config_manager.get_value('OLED', 'screen4').get('display_time', 3.0)
        self.oled_screen_is_run_on_oled[0] = self.config_manager.get_value('OLED', 'screen1').get('is_run_on_oled', True)
        self.oled_screen_is_run_on_oled[1] = self.config_manager.get_value('OLED', 'screen2').get('is_run_on_oled', True)
        self.oled_screen_is_run_on_oled[2] = self.config_manager.get_value('OLED', 'screen3').get('is_run_on_oled', True)
        self.oled_screen_is_run_on_oled[3] = self.config_manager.get_value('OLED', 'screen4').get('is_run_on_oled', True)

        self.setting_led_task_is_running = self.config_manager.get_value('LED', 'is_run_on_startup') or False
        self.setting_fan_task_is_running = self.config_manager.get_value('Fan', 'is_run_on_startup') or False
        self.setting_oled_task_is_running = self.config_manager.get_value('OLED', 'is_run_on_startup') or False

        if self.service_generator.check_service_is_exist():
            self.setting_service_is_exist = True
            self.setting_service_is_running = True
        else:
            self.setting_service_is_exist = False
            self.setting_service_is_running = False
        self.config_manager.set_value('Service', 'is_exist_on_rpi', self.setting_service_is_exist)
        self.config_manager.set_value('Service', 'is_run_on_startup', self.setting_service_is_running)
        
        #self.showMaximized()
        self.screen_resolution = QApplication.desktop().screenGeometry()
        width = self.screen_resolution.width()
        height = self.screen_resolution.height()
        #self.showNormal()

        if width > height:
            self.screen_direction = 0
            self.ui_main_width = 800
            self.ui_main_height = 420
        else:
            self.screen_direction = 1
            self.ui_main_width = 480
            self.ui_main_height = 740
        self.config_manager.set_value('Monitor', 'screen_orientation', self.screen_direction)
        self.config_manager.save_config()

        # Load Monitor interface parameters
        self.setFixedSize(self.ui_main_width, self.ui_main_height)
        self.monitoring_tab.resetUiSize(self.width(), self.height())
        self.led_tab.resetUiSize(self.width(), self.height())
        self.fan_tab.resetUiSize(self.width(), self.height())
        self.oled_tab.resetUiSize(self.width(), self.height())
        self.setting_tab.resetUiSize(self.width(), self.height())
        if self.ui_follow_led_color == 1:
            self.update_monitor_colors_event()
            self.monitor_update_color_timer.start(1000)  # Start timer, update LED color every second
            self.monitor_update_color_timer_is_running = True
            self.setting_tab.btn_system_follow_color.setText("Default Color")
        else:
            self.monitoring_tab.setDefaultCircleProgressColor()
            self.monitor_update_color_timer.stop()
            self.monitor_update_color_timer_is_running = False
            self.setting_tab.btn_system_follow_color.setText("Follow LED")

        # Load LED interface parameters
        self.led_tab.set_led_mode(self.led_mode)                     # Configure radio buttons based on mode
        self.led_tab.set_slider_color(0, self.led_slider_color[0])   # Set slider value
        self.led_tab.set_slider_color(1, self.led_slider_color[1])   # Set slider value
        self.led_tab.set_slider_color(2, self.led_slider_color[2])   # Set slider value
        self.led_tab.set_title_color(self.led_slider_color)          # Set title color
        if self.led_mode in [0, 4, 5]:                               # If mode is 0, 4, 5, disable sliders
            self.led_tab.set_slider_control_state(False)  
        else:                                                        # If mode is 1, 2, 3, enable sliders
            self.led_tab.set_slider_control_state(True) 

        # Load fan interface parameters
        self.fan_tab.set_fan_radio_mode(self.fan_mode)
        self.fan_tab.set_case_weight_temp(self.fan_temp_mode_threshold)
        self.fan_tab.set_manual_weight_slider_value(self.fan_manual_mode_duty)
        
        # Load OLED interface parameters
        self.oled_tab.set_display_time_label(0, self.oled_screen_display_time[0])
        self.oled_tab.set_display_time_label(1, self.oled_screen_display_time[1])
        self.oled_tab.set_display_time_label(2, self.oled_screen_display_time[2])
        self.oled_tab.set_display_time_label(3, self.oled_screen_display_time[3])
        try:
            self.oled_tab.screen1_data_format_combo.setCurrentIndex(self.oled_screen_interchange[0])
            self.oled_tab.screen1_time_format_combo.setCurrentIndex(self.oled_screen_interchange[1])
            self.oled_tab.screen2_interchange_combo.setCurrentIndex(self.oled_screen_interchange[2])    
            self.oled_tab.screen3_interchange_combo.setCurrentIndex(self.oled_screen_interchange[3])
            self.oled_tab.screen4_interchange_combo.setCurrentIndex(self.oled_screen_interchange[4])
            self.oled_tab.screen1_checkbox.setChecked(self.oled_screen_is_run_on_oled[0])
            self.oled_tab.screen2_checkbox.setChecked(self.oled_screen_is_run_on_oled[1])
            self.oled_tab.screen3_checkbox.setChecked(self.oled_screen_is_run_on_oled[2])
            self.oled_tab.screen4_checkbox.setChecked(self.oled_screen_is_run_on_oled[3])
        except:
            pass

        # Load settings interface parameters
        self.setting_tab.btn_led_switch.setChecked(self.setting_led_task_is_running)
        self.setting_tab.btn_fan_switch.setChecked(self.setting_fan_task_is_running)
        self.setting_tab.btn_oled_switch.setChecked(self.setting_oled_task_is_running)
        self.setting_tab.set_system_settings_button_state(self.setting_service_is_exist)
        self.setting_tab.set_custom_task_led_button_state(self.setting_service_is_exist, self.setting_led_task_is_running)
        self.setting_tab.set_custom_task_fan_button_state(self.setting_service_is_exist, self.setting_fan_task_is_running)
        self.setting_tab.set_custom_task_oled_button_state(self.setting_service_is_exist, self.setting_oled_task_is_running)
        self.setting_tab.set_run_and_stop_button_state(self.setting_service_is_exist, self.setting_service_is_running)

        # When starting the software, regardless of the mode, start the LED, fan, and OLED
        if self.setting_service_is_exist is False or self.setting_service_is_running is False:
            self.send_led_mode_to_expansion(self.led_mode)
            self.send_fan_mode_to_expansion(self.fan_mode)
            self.set_oled_process(True)
        else:
            if self.setting_led_task_is_running is False:
                self.send_led_mode_to_expansion(self.led_mode)
            if self.setting_fan_task_is_running is False:
                self.send_fan_mode_to_expansion(self.fan_mode)
            if self.setting_oled_task_is_running is False:
                self.set_oled_process(True)
            if self.setting_service_is_exist is True and self.setting_service_is_running is True:
                self.service_generator.restart_service_on_rpi()
    def load_ui_events(self):
        """Handle events"""
        # Monitor interface signals and slot functions
        self.monitor_update_data_timer.timeout.connect(self.update_monitor_data_event)          # Connect to slot function
        self.monitor_update_data_timer.start(1000)                                              # Start timer, update data every second
        self.monitor_update_color_timer.timeout.connect(self.update_monitor_colors_event)       # Connect to slot function

        # LED interface signals and slot functions
        for i in range(len(self.led_tab.led_mode_radio_buttons_names)):  
            self.led_tab.led_mode_radio_buttons[i].clicked.connect(self.led_radio_clicked_event)
        self.led_tab.led_slider_red.valueChanged.connect(self.led_slider_value_change_event)   
        self.led_tab.led_slider_green.valueChanged.connect(self.led_slider_value_change_event)  
        self.led_tab.led_slider_blue.valueChanged.connect(self.led_slider_value_change_event)
        self.led_tab.led_slider_red.sliderReleased.connect(self.led_slider_release_event)
        self.led_tab.led_slider_green.sliderReleased.connect(self.led_slider_release_event)
        self.led_tab.led_slider_blue.sliderReleased.connect(self.led_slider_release_event)
        self.led_tab.led_btn_default_config.clicked.connect(self.led_default_config_event)
        self.led_tab.led_btn_save_config.clicked.connect(self.led_save_config_event)
        self.led_tab.led_btn_edit_custom_code.clicked.connect(self.led_edit_custom_code_event)
        self.led_tab.led_btn_test_coustom_code.clicked.connect(self.led_test_custom_code_event)
        
        # Fan interface signals and slot functions
        for i in range(len(self.fan_tab.fan_mode_radio_buttons_names)):  
            self.fan_tab.fan_mode_radio_buttons[i].clicked.connect(self.fan_radio_clicked_event)
        self.fan_tab.fan_case_low_temp_minus_btn.clicked.connect(self.fan_case_weight_low_temp_minus_btn_event)
        self.fan_tab.fan_case_low_temp_plus_btn.clicked.connect(self.fan_case_weight_low_temp_plus_btn_event)
        self.fan_tab.fan_case_high_temp_minus_btn.clicked.connect(self.fan_case_weight_high_temp_minus_btn_event)
        self.fan_tab.fan_case_high_temp_plus_btn.clicked.connect(self.fan_case_weight_high_temp_plus_btn_event)
        self.fan_tab.fan_manual_slider_fan1.valueChanged.connect(self.fan_manual_slider_fan1_value_change_event)
        self.fan_tab.fan_manual_slider_fan2.valueChanged.connect(self.fan_manual_slider_fan2_value_change_event)
        self.fan_tab.fan_manual_slider_fan1.sliderReleased.connect(self.fan_manual_slider_release_event)
        self.fan_tab.fan_manual_slider_fan2.sliderReleased.connect(self.fan_manual_slider_release_event)
        self.fan_tab.fan_btn_default_config.clicked.connect(self.fan_default_config_event)
        self.fan_tab.fan_btn_save_config.clicked.connect(self.fan_save_config_event)
        self.fan_tab.fan_btn_edit_custom_code.clicked.connect(self.fan_edit_custom_code_event)
        self.fan_tab.fan_btn_test_coustom_code.clicked.connect(self.fan_test_custom_code_event)

        if self.expansion.get_board_type() == 'FNK0107':
            self.fan_tab.fan_case_temp_schmitt_minus_btn.clicked.connect(self.fan_case_weight_schmitt_minus_event)
            self.fan_tab.fan_case_temp_schmitt_plus_btn.clicked.connect(self.fan_case_weight_schmitt_plus_event)
            self.fan_tab.fan_case_low_speed_slider.valueChanged.connect(self.fan_case_low_slider_value_change_event)
            self.fan_tab.fan_case_middle_speed_slider.valueChanged.connect(self.fan_case_middle_slider_value_change_event)
            self.fan_tab.fan_case_high_speed_slider.valueChanged.connect(self.fan_case_high_slider_value_change_event)
            self.fan_tab.fan_case_low_speed_slider.sliderReleased.connect(self.fan_case_slider_release_event)
            self.fan_tab.fan_case_middle_speed_slider.sliderReleased.connect(self.fan_case_slider_release_event)
            self.fan_tab.fan_case_high_speed_slider.sliderReleased.connect(self.fan_case_slider_release_event)
            self.fan_tab.fan_pi_pwm_min_slider.valueChanged.connect(self.fan_pi_follow_min_slider_value_change_event)
            self.fan_tab.fan_pi_pwm_max_slider.valueChanged.connect(self.fan_pi_follow_max_slider_value_change_event)
            self.fan_tab.fan_pi_pwm_min_slider.sliderReleased.connect(self.fan_pi_follow_slider_release_event)
            self.fan_tab.fan_pi_pwm_max_slider.sliderReleased.connect(self.fan_pi_follow_slider_release_event)
            self.fan_tab.fan_manual_slider_fan3.valueChanged.connect(self.fan_manual_slider_fan3_value_change_event)
            self.fan_tab.fan_manual_slider_fan3.sliderReleased.connect(self.fan_manual_slider_release_event)

        # OLED interface signals and slot functions
        self.oled_tab.screen1_checkbox.clicked.connect(self.oled_screen1_checkbox_event)
        self.oled_tab.screen2_checkbox.clicked.connect(self.oled_screen2_checkbox_event)
        self.oled_tab.screen3_checkbox.clicked.connect(self.oled_screen3_checkbox_event)
        self.oled_tab.screen4_checkbox.clicked.connect(self.oled_screen4_checkbox_event)
        self.oled_tab.screen1_data_format_combo.currentIndexChanged.connect(self.oled_screen1_data_format_combo_event)
        self.oled_tab.screen1_time_format_combo.currentIndexChanged.connect(self.oled_screen1_time_format_combo_event)
        self.oled_tab.screen2_interchange_combo.currentIndexChanged.connect(self.oled_screen2_interchange_combo_event)
        self.oled_tab.screen3_interchange_combo.currentIndexChanged.connect(self.oled_screen3_interchange_combo_event)
        self.oled_tab.screen4_interchange_combo.currentIndexChanged.connect(self.oled_screen4_interchange_combo_event)
        self.oled_tab.screen_display_time_minus_btn.clicked.connect(self.oled_screen_display_time_minus_btn_event)
        self.oled_tab.screen_display_time_plus_btn.clicked.connect(self.oled_screen_display_time_plus_btn_event)

        # Settings interface signals and slot functions
        self.setting_tab.btn_led_edit.clicked.connect(self.led_edit_custom_code_event)
        self.setting_tab.btn_fan_edit.clicked.connect(self.fan_edit_custom_code_event)
        self.setting_tab.btn_oled_edit.clicked.connect(self.oled_edit_custom_code_event)
        self.setting_tab.btn_led_test.clicked.connect(self.setting_led_test_button_event)
        self.setting_tab.btn_fan_test.clicked.connect(self.setting_fan_test_button_event)
        self.setting_tab.btn_oled_test.clicked.connect(self.setting_oled_test_button_event)

        self.setting_tab.btn_system_rotate.clicked.connect(self.setting_rotate_window_event)          
        self.setting_tab.btn_system_follow_color.clicked.connect(self.setting_follow_led_color_event)  

        self.setting_tab.btn_create_task.clicked.connect(self.setting_stop_process)
        self.setting_tab.btn_create_task.clicked.connect(self.setting_create_task_event)
        self.setting_tab.btn_delete_task.clicked.connect(self.setting_delete_task_event)
        self.setting_tab.btn_run_task.clicked.connect(self.setting_run_task_event)
        self.setting_tab.btn_stop_task.clicked.connect(self.setting_stop_task_event)

        self.setting_tab.btn_led_switch.clicked.connect(self.setting_led_switch_event)
        self.setting_tab.btn_fan_switch.clicked.connect(self.setting_fan_switch_event)
        self.setting_tab.btn_oled_switch.clicked.connect(self.setting_oled_switch_event)

        # Main interface screen navigation function
        self.tab_widget.currentChanged.connect(self.tab_changed_event)

    # UI display related signals and slot functions
    def celsius_to_fahrenheit(self, celsius):
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9/5) + 32
    def update_monitor_data_event(self):
        """Periodically update monitor interface display data"""
        try:
            # Get system information
            rpi_temp = self.system_info.get_raspberry_pi_cpu_temperature()  # Raspberry Pi CPU temperature
            case_temp = self.expansion.get_temp()                           # Case temperature
            cpu_usage = self.system_info.get_raspberry_pi_cpu_usage()       # CPU usage
            memory_info = self.system_info.get_raspberry_pi_memory_usage()  # Memory usage information
            ram_usage = memory_info[0] if isinstance(memory_info, list) else memory_info
            disk_info = self.system_info.get_raspberry_pi_disk_usage()      # Disk usage information
            disk_usage = disk_info[0] if isinstance(disk_info, list) else disk_info
            rpi_fan_pwm = self.system_info.get_raspberry_pi_fan_duty()      # Raspberry Pi fan PWM
            case_fan_pwm = self.expansion.get_fan_duty()[:2]                # Case fan PWM values
            
            rpi_temp_fahrenheit = self.celsius_to_fahrenheit(rpi_temp)      # Convert Raspberry Pi temperature to Fahrenheit
            case_temp_fahrenheit = self.celsius_to_fahrenheit(case_temp)    # Convert case temperature to Fahrenheit

            # Update progress controls
            # CPU usage
            self.monitoring_tab.setCircleProgressValue(0, cpu_usage, self.metric_labels[0], f"{cpu_usage:.1f}%")
            
            # Memory usage
            self.monitoring_tab.setCircleProgressValue(1, ram_usage, self.metric_labels[1], f"{ram_usage:.1f}%")

            # Raspberry Pi temperature 
            if self.monitor_is_convert_cpu_temp_to_fahrenheit == False:
                self.monitoring_tab.setCircleProgressValue(2, min(100, rpi_temp/80*100), self.metric_labels[2], f"{rpi_temp:.1f}°C")
            else:
                self.monitoring_tab.setCircleProgressValue(2, min(100, rpi_temp/80*100), self.metric_labels[2], f"{rpi_temp_fahrenheit:.1f}°F")
            
            # Case temperature (using Raspberry Pi temperature as placeholder, can be replaced with actual sensor data)
            if self.monitor_is_convert_case_temp_to_fahrenheit == False:
                self.monitoring_tab.setCircleProgressValue(3, min(100, case_temp/80*100), self.metric_labels[3], f"{case_temp:.1f}°C")
            else:
                self.monitoring_tab.setCircleProgressValue(3, min(100, case_temp/80*100), self.metric_labels[3], f"{case_temp_fahrenheit:.1f}°F")
            
            # Storage usage
            self.monitoring_tab.setCircleProgressValue(4, disk_usage, self.metric_labels[4], f"{disk_usage:.1f}%")
            
            # Raspberry Pi fan PWM (0-255 range)
            rpi_fan_percent = (rpi_fan_pwm / 255) * 100 if rpi_fan_pwm >= 0 else 0
            self.monitoring_tab.setCircleProgressValue(5, rpi_fan_percent, self.metric_labels[5], f"{rpi_fan_percent:.1f}%")
            
            # Case fan PWM values
            if case_fan_pwm and len(case_fan_pwm) >= 2:
                # Fan 1
                fan1_percent = (case_fan_pwm[0] / 255) * 100 if case_fan_pwm[0] >= 0 else 0
                self.monitoring_tab.setCircleProgressValue(6, fan1_percent, self.metric_labels[6], f"{fan1_percent:.1f}%")
                
                # Fan 2
                fan2_percent = (case_fan_pwm[1] / 255) * 100 if case_fan_pwm[1] >= 0 else 0
                self.monitoring_tab.setCircleProgressValue(7, fan2_percent, self.metric_labels[7], f"{fan2_percent:.1f}%")
            else:
                # If unable to get fan data, display default values
                self.monitoring_tab.setCircleProgressValue(6, 0, self.metric_labels[6], "N/A")
                self.monitoring_tab.setCircleProgressValue(7, 0, self.metric_labels[7], "N/A")
                
        except Exception as e:
            print(f"Error updating data: {e}")
    def update_monitor_colors_event(self):
        """Periodically update LED colors to circular progress bars"""
        try:
            # Get LED tab color values
            if hasattr(self.led_tab, 'led_color_value'): # Check if attribute exists
                r, g, b = self.led_slider_color
                hex_color = f"#{r:02X}{g:02X}{b:02X}"
                if hasattr(self.monitoring_tab, 'setCircleProgressColor'):
                    for i in range(8):
                        self.monitoring_tab.setCircleProgressColor(i, [hex_color, '#444444'])
        except Exception as e:
            print(f"Error updating LED colors: {e}")
    
    # LED interface signals and slot functions
    def set_led_process(self, enable = True):
        """Handle LED process"""
        if enable:
            if self.led_process is not None and self.led_process.poll() is None:
                return
            else:
                try:
                    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_led.py")
                    if os.path.exists(script_path):
                        self.led_process = subprocess.Popen([sys.executable, script_path])
                    else:
                        print(f"Error: task_led.py not found at {script_path}")
                except Exception as e:
                    print(f"Error starting task_led.py: {e}")
        else:
            if self.led_process is not None and self.led_process.poll() is None:
                # If process is running, terminate it
                self.led_process.terminate()
                try:
                    self.led_process.wait(timeout=0.1)  # Wait up to 0.1 seconds
                except subprocess.TimeoutExpired:
                    self.led_process.kill()  # Force kill process
                self.led_process = None
            elif self.led_process is not None and self.led_process.poll() is not None:
                self.led_process = None
    def send_led_mode_to_expansion(self, led_mode):
        """Send LED mode to expansion board"""
        if led_mode == 0:
            self.expansion.set_led_mode(4)                 
        elif led_mode == 1:
            self.expansion.set_led_mode(3)
            self.expansion.set_all_led_color(self.led_slider_color[0],self.led_slider_color[1],self.led_slider_color[2])  
        elif led_mode == 2:
            self.expansion.set_led_mode(2)
            self.expansion.set_all_led_color(self.led_slider_color[0],self.led_slider_color[1],self.led_slider_color[2])    
        elif led_mode == 3:
            self.expansion.set_led_mode(1)
            self.expansion.set_all_led_color(self.led_slider_color[0],self.led_slider_color[1],self.led_slider_color[2])  
        elif led_mode == 5:
            self.expansion.set_led_mode(0)
    def led_radio_clicked_event(self):
        """Handle LED radio button click event"""
        sender_button = self.sender()
        for i in range(len(self.led_tab.led_mode_radio_buttons_names)):
            if sender_button.text() == self.led_tab.led_mode_radio_buttons_names[i]:
                self.led_mode = i
        if self.led_mode == 4: 
            self.set_led_process(True)
            self.led_tab.led_btn_test_coustom_code.setText("Stop")
        else:
            self.set_led_process(False)
            self.led_tab.led_btn_test_coustom_code.setText("Test")
        self.send_led_mode_to_expansion(self.led_mode)
    def led_slider_value_change_event(self):
        """Handle LED slider value change event"""
        self.led_slider_color[0] = self.led_tab.led_slider_red.value()
        self.led_slider_color[1] = self.led_tab.led_slider_green.value()
        self.led_slider_color[2] = self.led_tab.led_slider_blue.value()
        self.led_tab.set_slider_slider_value(self.led_slider_color)
    def led_slider_release_event(self):
        """Handle LED slider release event"""
        self.led_slider_color[0] = self.led_tab.led_slider_red.value()
        self.led_slider_color[1] = self.led_tab.led_slider_green.value()
        self.led_slider_color[2] = self.led_tab.led_slider_blue.value()
        self.expansion.set_all_led_color(self.led_slider_color[0],self.led_slider_color[1],self.led_slider_color[2])
    def led_default_config_event(self):
        """Handle LED default configuration button click event"""
        self.led_mode = 0
        self.led_slider_color = [0, 0, 255]
        self.set_led_process(False)
        self.led_tab.led_btn_test_coustom_code.setText("Test")
        self.led_tab.set_led_mode(self.led_mode)
        self.led_tab.set_slider_slider_value(self.led_slider_color)
        self.led_tab.set_slider_control_state(False) 
        self.send_led_mode_to_expansion(self.led_mode)
        self.led_save_config_event()
    def led_save_config_event(self):
        """Handle LED save configuration button click event"""
        self.config_manager.set_value('LED', 'mode', self.led_mode)
        self.config_manager.set_value('LED', 'red_value', self.led_slider_color[0])
        self.config_manager.set_value('LED', 'green_value', self.led_slider_color[1])
        self.config_manager.set_value('LED', 'blue_value', self.led_slider_color[2])
        self.config_manager.set_value('LED', 'is_run_on_startup', self.setting_led_task_is_running)
        self.config_manager.save_config()
        self.send_led_mode_to_expansion(self.led_mode)
        self.expansion.set_save_flash(True)
    def led_edit_custom_code_event(self):
        """Handle edit custom code button event"""
        # Try different editors in order of priority
        editors = [
            ("xdg-open", "gui"),     # System default editor
            ("nano", "terminal"),    # Nano editor
            ("vim", "terminal")      # Vim editor
        ]
        
        # Try to use editors in order of priority
        for editor, editor_type in editors:
            if os.system(f"which {editor} > /dev/null 2>&1") == 0:
                try:
                    if editor_type == "terminal":
                        # Terminal editors need blocking calls
                        os.system(f"sudo {editor} task_led.py")
                    else:
                        # GUI editors run in background
                        os.system(f"{editor} task_led.py &")
                    return
                except Exception as e:
                    print(f"Error opening file with {editor}: {e}")
                    continue
        
        print("No suitable text editor found. Please install a text editor.")
    def led_test_custom_code_event(self):
        """Handle LED test custom code button click event"""
        if self.led_process is not None:
            self.set_led_process(False)
            self.led_tab.led_btn_test_coustom_code.setText("Test")
        else:
            self.set_led_process(True)
            self.led_tab.led_btn_test_coustom_code.setText("Stop")
    
    # FAN interface signals and slot functions
    def set_fan_process(self, enable = True):
        """Handle FAN process"""
        if enable:
            if self.fan_process is not None and self.fan_process.poll() is None:
                return
            else:
                try:
                    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_fan.py")
                    if os.path.exists(script_path):
                        self.fan_process = subprocess.Popen([sys.executable, script_path])
                    else:
                        print(f"Error: task_fan.py not found at {script_path}")
                except Exception as e:
                    print(f"Error starting task_fan.py: {e}")
        else:
            if self.fan_process is not None and self.fan_process.poll() is None:
                # If process is running, terminate it
                self.fan_process.terminate()
                try:
                    self.fan_process.wait(timeout=0.1)  # Wait up to 0.1 seconds
                except subprocess.TimeoutExpired:
                    self.fan_process.kill()  # Force kill process
                self.fan_process = None
            elif self.fan_process is not None and self.fan_process.poll() is not None:
                self.fan_process = None
    def send_fan_mode_to_expansion(self, mode):
        """Send fan mode to expansion board"""
        if self.expansion.get_board_type() == "FNK0100":
            if mode == 0:
                self.expansion.set_fan_mode(2)  
                self.expansion.set_fan_temp_mode_threshold(
                    self.fan_temp_mode_threshold[0],
                    self.fan_temp_mode_threshold[1]
                )
            elif mode == 1:
                self.expansion.set_fan_mode(1)
                self.expansion.set_fan_duty(
                    self.fan_manual_mode_duty[0],
                    self.fan_manual_mode_duty[1]
                )
            elif mode == 3:
                self.expansion.set_fan_mode(0)
                self.expansion.set_fan_duty(0, 0)
        elif self.expansion.get_board_type() == "FNK0107":
            if mode == 0:
                self.expansion.set_fan_mode(2)  
                self.expansion.set_fan_temp_mode_threshold(
                    self.fan_temp_mode_threshold[0],
                    self.fan_temp_mode_threshold[1],
                    self.fan_temp_mode_threshold[2]
                )
                self.expansion.set_fan_temp_mode_speed(
                    self.fan_temp_mode_duty[0],
                    self.fan_temp_mode_duty[1],
                    self.fan_temp_mode_duty[2]
                )
            elif mode == 1:
                self.expansion.set_fan_mode(3)
                self.expansion.set_fan_pi_following(
                    self.fan_pi_follows_duty_map[0],
                    self.fan_pi_follows_duty_map[1]
                )
            elif mode == 2:
                self.expansion.set_fan_mode(1)
                self.expansion.set_fan_duty(
                    self.fan_manual_mode_duty[0],
                    self.fan_manual_mode_duty[1],
                    self.fan_manual_mode_duty[2]
                )
            elif mode == 4:
                self.expansion.set_fan_mode(0)
                self.expansion.set_fan_duty(0, 0, 0)
    def fan_radio_clicked_event(self):
        """Handle FAN mode switch event"""
        sender_button = self.sender()
        for i in range(len(self.fan_tab.fan_mode_radio_buttons_names)):
            if sender_button.text() == self.fan_tab.fan_mode_radio_buttons_names[i]:
                self.fan_mode = i
        self.send_fan_mode_to_expansion(self.fan_mode)
        if self.expansion.get_board_type() == 'FNK0107':
            if self.fan_mode == 3: 
                self.set_fan_process(True)
                self.fan_tab.fan_btn_test_coustom_code.setText("Stop")
            else:
                self.set_fan_process(False)
                self.fan_tab.fan_btn_test_coustom_code.setText("Test")
        elif self.expansion.get_board_type() == 'FNK0100':
            if self.fan_mode == 2: 
                self.set_fan_process(True)
                self.fan_tab.fan_btn_test_coustom_code.setText("Stop")
            else:
                self.set_fan_process(False)
                self.fan_tab.fan_btn_test_coustom_code.setText("Test")
        
    def fan_case_weight_low_temp_minus_btn_event(self):
        current_value = int(self.fan_tab.fan_case_low_temp_input.text())
        self.fan_temp_mode_threshold[0] = max(self.ui_fan_temp_mode_threshold_range[0][0], current_value - 1) # Minimum value is 10
        self.fan_tab.fan_case_low_temp_input.setText(str(self.fan_temp_mode_threshold[0]))
        low_temp, high_temp, schmitt = self.fan_temp_mode_threshold
        if self.expansion.get_board_type() == "FNK0100":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp)
        elif self.expansion.get_board_type() == "FNK0107":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp, schmitt)
    def fan_case_weight_low_temp_plus_btn_event(self):
        current_value = int(self.fan_tab.fan_case_low_temp_input.text())
        self.fan_temp_mode_threshold[0] = min(self.ui_fan_temp_mode_threshold_range[0][1], current_value + 1)  # Maximum value is 40
        self.fan_tab.fan_case_low_temp_input.setText(str(self.fan_temp_mode_threshold[0]))
        low_temp, high_temp, schmitt = self.fan_temp_mode_threshold
        if self.expansion.get_board_type() == "FNK0100":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp)
        elif self.expansion.get_board_type() == "FNK0107":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp, schmitt)
    def fan_case_weight_high_temp_minus_btn_event(self):
        current_value = int(self.fan_tab.fan_case_high_temp_input.text())
        self.fan_temp_mode_threshold[1] = max(self.ui_fan_temp_mode_threshold_range[1][0], current_value - 1)  # Minimum value is 50
        self.fan_tab.fan_case_high_temp_input.setText(str(self.fan_temp_mode_threshold[1]))
        low_temp, high_temp, schmitt = self.fan_temp_mode_threshold
        if self.expansion.get_board_type() == "FNK0100":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp)
        elif self.expansion.get_board_type() == "FNK0107":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp, schmitt)
    def fan_case_weight_high_temp_plus_btn_event(self):
        current_value = int(self.fan_tab.fan_case_high_temp_input.text())
        self.fan_temp_mode_threshold[1] = min(self.ui_fan_temp_mode_threshold_range[1][1], current_value + 1)  # Maximum value is 80
        self.fan_tab.fan_case_high_temp_input.setText(str(self.fan_temp_mode_threshold[1]))
        low_temp, high_temp, schmitt = self.fan_temp_mode_threshold
        if self.expansion.get_board_type() == "FNK0100":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp)
        elif self.expansion.get_board_type() == "FNK0107":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp, schmitt)
    def fan_case_weight_schmitt_minus_event(self):
        current_value = int(self.fan_tab.fan_case_temp_schmitt_input.text())
        self.fan_temp_mode_threshold[2] = max(self.ui_fan_temp_mode_threshold_range[2][0], current_value - 1)  # Minimum value is 1
        self.fan_tab.fan_case_temp_schmitt_input.setText(str(self.fan_temp_mode_threshold[2]))
        low_temp, high_temp, schmitt = self.fan_temp_mode_threshold
        if self.expansion.get_board_type() == "FNK0100":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp)
        elif self.expansion.get_board_type() == "FNK0107":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp, schmitt)
    def fan_case_weight_schmitt_plus_event(self):
        current_value = int(self.fan_tab.fan_case_temp_schmitt_input.text())
        self.fan_temp_mode_threshold[2] = min(self.ui_fan_temp_mode_threshold_range[2][1], current_value + 1)  # Maximum value is 5
        self.fan_tab.fan_case_temp_schmitt_input.setText(str(self.fan_temp_mode_threshold[2]))
        low_temp, high_temp, schmitt = self.fan_temp_mode_threshold
        if self.expansion.get_board_type() == "FNK0100":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp)
        elif self.expansion.get_board_type() == "FNK0107":
            self.expansion.set_fan_temp_mode_threshold(low_temp, high_temp, schmitt)
    def fan_case_low_slider_value_change_event(self):
        self.fan_temp_mode_duty[0] = self.fan_tab.fan_case_low_speed_slider.value()
        self.fan_tab.set_case_weight_slider_value(self.fan_temp_mode_duty)
    def fan_case_middle_slider_value_change_event(self):
        self.fan_temp_mode_duty[1] = self.fan_tab.fan_case_middle_speed_slider.value()
        self.fan_tab.set_case_weight_slider_value(self.fan_temp_mode_duty)
    def fan_case_high_slider_value_change_event(self):
        self.fan_temp_mode_duty[2] = self.fan_tab.fan_case_high_speed_slider.value()
        self.fan_tab.set_case_weight_slider_value(self.fan_temp_mode_duty)
    def fan_case_slider_release_event(self):
        self.expansion.set_fan_temp_mode_speed(
            self.fan_temp_mode_duty[0],
            self.fan_temp_mode_duty[1],
            self.fan_temp_mode_duty[2]
        )
    def fan_pi_follow_min_slider_value_change_event(self):
        self.fan_pi_follows_duty_map[0] = self.fan_tab.fan_pi_pwm_min_slider.value()
        self.fan_tab.set_pi_weight_slider_map(self.fan_pi_follows_duty_map)
    def fan_pi_follow_max_slider_value_change_event(self):
        self.fan_pi_follows_duty_map[1] = self.fan_tab.fan_pi_pwm_max_slider.value()
        self.fan_tab.set_pi_weight_slider_map(self.fan_pi_follows_duty_map)
    def fan_pi_follow_slider_release_event(self):
        min_duty, max_duty = self.fan_pi_follows_duty_map
        self.expansion.set_fan_pi_following(min_duty, max_duty)
    def fan_manual_slider_fan1_value_change_event(self):
        self.fan_manual_mode_duty[0] = self.fan_tab.fan_manual_slider_fan1.value()
        self.fan_tab.set_manual_weight_slider_value(self.fan_manual_mode_duty)
    def fan_manual_slider_fan2_value_change_event(self):
        self.fan_manual_mode_duty[1] = self.fan_tab.fan_manual_slider_fan2.value()
        self.fan_tab.set_manual_weight_slider_value(self.fan_manual_mode_duty)
    def fan_manual_slider_fan3_value_change_event(self):
        self.fan_manual_mode_duty[2] = self.fan_tab.fan_manual_slider_fan3.value()
        self.fan_tab.set_manual_weight_slider_value(self.fan_manual_mode_duty)
    def fan_manual_slider_release_event(self):
        d1, d2, d3 = self.fan_manual_mode_duty
        if self.expansion.get_board_type() == "FNK0100":
            self.expansion.set_fan_duty(d1, d2)
        elif self.expansion.get_board_type() == "FNK0107":
            self.expansion.set_fan_duty(d1, d2, d3)
    def fan_default_config_event(self):
        """Handle FAN default configuration button click event"""
        self.fan_mode = 0                                            # Fan mode
        self.fan_manual_mode_duty = [75, 75, 75]                     # Fan manual mode duty cycle values for 3 fan groups
        self.fan_temp_mode_threshold = [30, 50, 3]                   # Fan temperature mode threshold parameters
        self.fan_temp_mode_duty = [75, 125, 175]                     # Fan temperature mode duty cycle parameters
        self.fan_pi_follows_duty_map = [0, 255]                      # Fan follows Raspberry Pi mode duty cycle mapping parameters
        self.set_fan_process(False)
        self.fan_tab.fan_btn_test_coustom_code.setText("Test")
        self.fan_tab.set_fan_radio_mode(self.fan_mode)
        self.fan_tab.set_manual_weight_slider_value(self.fan_manual_mode_duty)
        self.fan_tab.set_case_weight_temp(self.fan_temp_mode_threshold)
        self.fan_tab.set_case_weight_slider_value(self.fan_temp_mode_duty)
        self.fan_tab.set_pi_weight_slider_map(self.fan_pi_follows_duty_map)
        self.send_fan_mode_to_expansion(self.fan_mode)
        self.fan_save_config_event()
    def fan_save_config_event(self):
        """Handle FAN save configuration button click event"""
        self.config_manager.set_value('Fan', 'mode', self.fan_mode)
        self.config_manager.set_value('Fan', 'mode1_fan_group1', self.fan_manual_mode_duty[0])
        self.config_manager.set_value('Fan', 'mode1_fan_group2', self.fan_manual_mode_duty[1])
        self.config_manager.set_value('Fan', 'mode1_fan_group3', self.fan_manual_mode_duty[2])
        self.config_manager.set_value('Fan', 'mode2_low_temp_threshold', self.fan_temp_mode_threshold[0])
        self.config_manager.set_value('Fan', 'mode2_high_temp_threshold', self.fan_temp_mode_threshold[1])
        self.config_manager.set_value('Fan', 'mode2_temp_schmitt', self.fan_temp_mode_threshold[2])
        self.config_manager.set_value('Fan', 'mode2_low_speed', self.fan_temp_mode_duty[0])
        self.config_manager.set_value('Fan', 'mode2_middle_speed', self.fan_temp_mode_duty[1])
        self.config_manager.set_value('Fan', 'mode2_high_speed', self.fan_temp_mode_duty[2])
        self.config_manager.set_value('Fan', 'mode3_min_speed_mapping', self.fan_pi_follows_duty_map[0])
        self.config_manager.set_value('Fan', 'mode3_max_speed_mapping', self.fan_pi_follows_duty_map[1])
        self.config_manager.set_value('Fan', 'is_run_on_startup', self.setting_fan_task_is_running)
        self.config_manager.save_config()
        self.send_fan_mode_to_expansion(self.fan_mode)
        self.expansion.set_save_flash(True)
    def fan_edit_custom_code_event(self):
        """Handle edit custom code button event"""
        # Try different editors in order of priority
        editors = [
            ("xdg-open", "gui"),     # System default editor
            ("nano", "terminal"),    # Nano editor
            ("vim", "terminal")      # Vim editor
        ]
        
        # Try to use editors in order of priority
        for editor, editor_type in editors:
            if os.system(f"which {editor} > /dev/null 2>&1") == 0:
                try:
                    if editor_type == "terminal":
                        # Terminal editors need blocking calls
                        os.system(f"sudo {editor} task_fan.py")
                    else:
                        # GUI editors run in background
                        os.system(f"{editor} task_fan.py &")
                    return
                except Exception as e:
                    print(f"Error opening file with {editor}: {e}")
                    continue
        
        print("No suitable text editor found. Please install a text editor.")
    def fan_test_custom_code_event(self):
        """Handle FAN test custom code button click event"""
        if self.fan_process is not None:
            self.set_fan_process(False)
            self.fan_tab.fan_btn_test_coustom_code.setText("Test")
        else:
            self.set_fan_process(True)
            self.fan_tab.fan_btn_test_coustom_code.setText("Stop")
    
    # OLED interface signals and slot functions
    def oled_process_reboot(self):
        """Handle OLED process reboot"""
        if self.oled_process is not None and self.oled_process.poll() is None:
            self.set_oled_process(False)
            time.sleep(0.03)
            self.set_oled_process(True)
        if self.setting_service_is_exist and self.setting_service_is_running and self.setting_oled_task_is_running:
            self.service_generator.stop_service_on_rpi()
            self.set_oled_process(True)
    def oled_screen1_checkbox_event(self):
        """Handle OLED screen1 checkbox event"""
        is_checked = self.oled_tab.screen1_checkbox.isChecked()
        self.oled_tab.set_display_time_is_enabled(0, is_checked)
        screen1_config = self.config_manager.get_value('OLED', 'screen1') or {}
        screen1_config['is_run_on_oled'] = is_checked
        self.config_manager.set_value('OLED', 'screen1', screen1_config)
        self.config_manager.save_config()
        self.oled_screen_is_run_on_oled[0] = is_checked
        self.oled_process_reboot()
    def oled_screen2_checkbox_event(self):
        """Handle OLED screen2 checkbox event"""
        is_checked = self.oled_tab.screen2_checkbox.isChecked()
        self.oled_tab.set_display_time_is_enabled(1, is_checked)
        screen2_config = self.config_manager.get_value('OLED', 'screen2') or {}
        screen2_config['is_run_on_oled'] = is_checked
        self.config_manager.set_value('OLED', 'screen2', screen2_config)
        self.config_manager.save_config()
        self.oled_screen_is_run_on_oled[1] = is_checked
        self.oled_process_reboot()
    def oled_screen3_checkbox_event(self):
        """Handle OLED screen3 checkbox event"""
        is_checked = self.oled_tab.screen3_checkbox.isChecked()
        self.oled_tab.set_display_time_is_enabled(2, is_checked)
        screen3_config = self.config_manager.get_value('OLED', 'screen3') or {}
        screen3_config['is_run_on_oled'] = is_checked
        self.config_manager.set_value('OLED', 'screen3', screen3_config)
        self.config_manager.save_config()
        self.oled_screen_is_run_on_oled[2] = is_checked
        self.oled_process_reboot()
    def oled_screen4_checkbox_event(self):
        """Handle OLED screen4 checkbox event"""
        is_checked = self.oled_tab.screen4_checkbox.isChecked()
        self.oled_tab.set_display_time_is_enabled(3, is_checked)
        screen4_config = self.config_manager.get_value('OLED', 'screen4') or {}
        screen4_config['is_run_on_oled'] = is_checked
        self.config_manager.set_value('OLED', 'screen4', screen4_config)
        self.config_manager.save_config()
        self.oled_screen_is_run_on_oled[3] = is_checked
        self.oled_process_reboot()
    def oled_screen1_data_format_combo_event(self, index):
        """Handle OLED screen1 data format combo box event"""
        screen1_config = self.config_manager.get_value('OLED', 'screen1') or {}
        screen1_config['data_format'] = index
        self.config_manager.set_value('OLED', 'screen1', screen1_config)
        self.config_manager.save_config()
        self.oled_screen_interchange[0] = index
        self.oled_process_reboot()
    def oled_screen1_time_format_combo_event(self, index):
        """Handle OLED screen1 time format combo box event"""
        screen1_config = self.config_manager.get_value('OLED', 'screen1') or {}
        screen1_config['time_format'] = index
        self.config_manager.set_value('OLED', 'screen1', screen1_config)
        self.config_manager.save_config()
        self.oled_screen_interchange[1] = index
        self.oled_process_reboot()
    def oled_screen2_interchange_combo_event(self, index):
        """Handle OLED screen2 interchange combo box event"""
        screen2_config = self.config_manager.get_value('OLED', 'screen2') or {}
        screen2_config['interchange'] = index
        self.config_manager.set_value('OLED', 'screen2', screen2_config)
        self.config_manager.save_config()
        self.oled_screen_interchange[2] = index
        self.oled_process_reboot()
    def oled_screen3_interchange_combo_event(self, index):
        """Handle OLED screen3 interchange combo box event"""
        screen3_config = self.config_manager.get_value('OLED', 'screen3') or {}
        screen3_config['interchange'] = index
        self.config_manager.set_value('OLED', 'screen3', screen3_config)
        self.config_manager.save_config()
        self.oled_screen_interchange[3] = index
        self.oled_process_reboot()
    def oled_screen4_interchange_combo_event(self, index):
        """Handle OLED screen4 interchange combo box event"""
        screen4_config = self.config_manager.get_value('OLED', 'screen4') or {}
        screen4_config['interchange'] = index
        self.config_manager.set_value('OLED', 'screen4', screen4_config)
        self.config_manager.save_config()
        self.oled_screen_interchange[4] = index
        self.oled_process_reboot()
    def oled_screen_display_time_minus_btn_event(self):
        """Handle OLED screen display time minus button event"""
        checkboxes = [
            self.oled_tab.screen1_checkbox,
            self.oled_tab.screen2_checkbox,
            self.oled_tab.screen3_checkbox,
            self.oled_tab.screen4_checkbox
        ]
        for i, checkbox in enumerate(checkboxes):
            if checkbox.isChecked(): 
                screen_num = i + 1
                screen_key = f'screen{screen_num}'
                screen_config = self.config_manager.get_value('OLED', screen_key) or {}
                current_time = screen_config.get('display_time', 3.0)
                new_time = current_time - 0.5
                if new_time <= 0:
                    new_time = 0.5
                screen_config['display_time'] = round(new_time, 1)
                self.config_manager.set_value('OLED', screen_key, screen_config)
                self.oled_screen_display_time[i] = new_time
                self.oled_tab.set_display_time_label(i, new_time)
        self.config_manager.save_config()
        self.oled_process_reboot()
    def oled_screen_display_time_plus_btn_event(self):
        """Handle OLED screen display time plus button event"""
        checkboxes = [
            self.oled_tab.screen1_checkbox,
            self.oled_tab.screen2_checkbox,
            self.oled_tab.screen3_checkbox,
            self.oled_tab.screen4_checkbox
        ]
        for i, checkbox in enumerate(checkboxes):
            if checkbox.isChecked(): 
                screen_num = i + 1
                screen_key = f'screen{screen_num}'
                screen_config = self.config_manager.get_value('OLED', screen_key) or {}
                current_time = screen_config.get('display_time', 3.0)
                new_time =  current_time + 0.5
                screen_config['display_time'] = round(new_time, 1)
                self.config_manager.set_value('OLED', screen_key, screen_config)
                self.oled_screen_display_time[i] = new_time
                self.oled_tab.set_display_time_label(i, new_time)
        self.config_manager.save_config()
        self.oled_process_reboot()
    
    # Setting interface signals and slot functions
    def set_oled_process(self, enable = True):
        """Handle OLED process"""
        if enable:
            if self.oled_process is not None and self.oled_process.poll() is None:
                return
            else:
                try:
                    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_oled.py")
                    if os.path.exists(script_path):
                        self.oled_process = subprocess.Popen([sys.executable, script_path])
                    else:
                        print(f"Error: task_oled.py not found at {script_path}")
                except Exception as e:
                    print(f"Error starting task_oled.py: {e}")
        else:
            if self.oled_process is not None and self.oled_process.poll() is None:
                # If process is running, terminate it
                self.oled_process.terminate()
                try:
                    self.oled_process.wait(timeout=0.1)  # Wait up to 0.1 seconds
                except subprocess.TimeoutExpired:
                    self.oled_process.kill()  # Force kill process
                self.oled_process = None
    def oled_edit_custom_code_event(self):
        """Handle edit custom code button event"""
        # Try different editors in order of priority
        editors = [
            ("xdg-open", "gui"),     # System default editor
            ("nano", "terminal"),    # Nano editor
            ("vim", "terminal")      # Vim editor
        ]
        
        # Try to use editors in order of priority
        for editor, editor_type in editors:
            if os.system(f"which {editor} > /dev/null 2>&1") == 0:
                try:
                    if editor_type == "terminal":
                        # Terminal editors need blocking calls
                        os.system(f"sudo {editor} task_oled.py")
                    else:
                        # GUI editors run in background
                        os.system(f"{editor} task_oled.py &")
                    return
                except Exception as e:
                    print(f"Error opening file with {editor}: {e}")
                    continue
        
        print("No suitable text editor found. Please install a text editor.")
    def setting_led_test_button_event(self):
        """Handle LED test custom code button click event"""
        if self.led_process is not None:
            self.set_led_process(False)
            self.setting_tab.btn_led_test.setText("Test")
        else:
            self.set_led_process(True)
            self.setting_tab.btn_led_test.setText("Stop")
    def setting_fan_test_button_event(self):
        """Handle FAN test custom code button click event"""
        if self.fan_process is not None:
            self.set_fan_process(False)
            self.setting_tab.btn_fan_test.setText("Test")
        else:
            self.set_fan_process(True)
            self.setting_tab.btn_fan_test.setText("Stop")
    def setting_oled_test_button_event(self):
        """Handle OLED test custom code button click event"""
        if self.oled_process is not None:
            self.set_oled_process(False)
            self.setting_tab.btn_oled_test.setText("Test")
        else:
            self.set_oled_process(True)
            self.setting_tab.btn_oled_test.setText("Stop")
    def setting_rotate_window_event(self):
        """Handle window rotation"""
        if self.config_manager.get_value('Monitor', 'screen_orientation') == 0:  
            self.config_manager.set_value('Monitor', 'screen_orientation', 1) 
            self.ui_main_width = 480
            self.ui_main_height = 740
        else: 
            self.config_manager.set_value('Monitor', 'screen_orientation', 0)
            self.ui_main_width = 800
            self.ui_main_height = 420
        self.config_manager.save_config()
        self.setFixedSize(self.ui_main_width, self.ui_main_height)
        self.monitoring_tab.resetUiSize(self.width(), self.height())
        self.led_tab.resetUiSize(self.width(), self.height())
        self.fan_tab.resetUiSize(self.width(), self.height())
        self.setting_tab.resetUiSize(self.width(), self.height())
    def setting_follow_led_color_event(self):
        """Handle window follow LED color"""
        if self.monitor_update_color_timer_is_running:
            self.monitoring_tab.setDefaultCircleProgressColor()
            self.monitor_update_color_timer.stop()
            self.monitor_update_color_timer_is_running = False
            self.setting_tab.btn_system_follow_color.setText("Follow LED")
            self.config_manager.set_value('Monitor', 'follow_led_color', 0)
            self.config_manager.save_config()
        else:
            self.update_monitor_colors_event()
            self.monitor_update_color_timer.start(1000)  # Start timer, update LED color every second
            self.monitor_update_color_timer_is_running = True
            self.setting_tab.btn_system_follow_color.setText("Default Color")
            self.config_manager.set_value('Monitor', 'follow_led_color', 1)
            self.config_manager.save_config()
    def setting_create_task_event(self):
        """Handle create task button click event"""
        self.setting_service_is_exist = True
        self.setting_tab.set_system_settings_button_state(self.setting_service_is_exist)              
        self.setting_tab.set_custom_task_led_button_state(self.setting_service_is_exist, self.setting_led_task_is_running)
        self.setting_tab.set_custom_task_fan_button_state(self.setting_service_is_exist, self.setting_fan_task_is_running)
        self.setting_tab.set_custom_task_oled_button_state(self.setting_service_is_exist, self.setting_oled_task_is_running)
        self.config_manager.set_value('Service', 'is_exist_on_rpi', self.setting_service_is_exist)
        self.config_manager.save_config()
        self.service_generator.create_service_on_rpi()               
    def setting_delete_task_event(self):
        """Handle delete task button click event"""
        self.setting_service_is_exist = False
        self.setting_tab.set_system_settings_button_state(self.setting_service_is_exist)
        self.config_manager.set_value('Service', 'is_exist_on_rpi', self.setting_service_is_exist)
        self.config_manager.save_config()
        self.service_generator.delete_service_on_rpi()
    def setting_run_task_event(self):
        """Handle run task button click event"""
        self.setting_service_is_running = True
        self.config_manager.set_value('Service', 'is_run_on_startup', self.setting_service_is_running)
        self.config_manager.save_config()
        self.setting_tab.set_run_and_stop_button_state(self.setting_service_is_exist, self.setting_service_is_running)
        self.service_generator.run_service_on_rpi()
    def setting_stop_task_event(self):
        """Handle stop task button click event"""
        self.setting_service_is_running = False
        self.config_manager.set_value('Service', 'is_run_on_startup', self.setting_service_is_running)
        self.config_manager.save_config()
        self.setting_tab.set_run_and_stop_button_state(self.setting_service_is_exist, self.setting_service_is_running)
        self.service_generator.stop_service_on_rpi()
    def setting_stop_process(self):
        """Handle stop process"""
        if self.led_process is not None:
            self.set_led_process(False)
            self.setting_tab.btn_led_test.setText("Test")
        if self.fan_process is not None:
            self.set_fan_process(False)
            self.setting_tab.btn_fan_test.setText("Test")
        if self.oled_process is not None:
            self.set_oled_process(False)
            self.setting_tab.btn_oled_test.setText("Test")
    def setting_led_switch_event(self):
        """Handle LED switch button click event"""
        self.setting_led_task_is_running = self.setting_tab.btn_led_switch.isChecked()
        self.config_manager.set_value('LED', 'is_run_on_startup', self.setting_led_task_is_running)
        self.config_manager.save_config()
        self.setting_tab.set_custom_task_led_button_state(self.setting_service_is_exist, self.setting_led_task_is_running)
        if self.setting_led_task_is_running:
            self.set_led_process(False)
            self.setting_tab.btn_led_test.setText("Test")
    def setting_fan_switch_event(self):
        """Handle FAN switch button click event"""
        self.setting_fan_task_is_running = self.setting_tab.btn_fan_switch.isChecked()
        self.config_manager.set_value('Fan', 'is_run_on_startup', self.setting_fan_task_is_running)
        self.config_manager.save_config()
        self.setting_tab.set_custom_task_fan_button_state(self.setting_service_is_exist, self.setting_fan_task_is_running)
        if self.setting_fan_task_is_running:
            self.set_fan_process(False)
            self.setting_tab.btn_fan_test.setText("Test")
    def setting_oled_switch_event(self):
        """Handle OLED switch button click event"""
        self.setting_oled_task_is_running = self.setting_tab.btn_oled_switch.isChecked()
        self.config_manager.set_value('OLED', 'is_run_on_startup', self.setting_oled_task_is_running)
        self.config_manager.save_config()
        self.setting_tab.set_custom_task_oled_button_state(self.setting_service_is_exist, self.setting_oled_task_is_running)
        if self.setting_oled_task_is_running:
            self.set_oled_process(False)
            self.setting_tab.btn_oled_test.setText("Test")
    
    def tab_changed_event(self):
        """Handle Tab switch event"""
        # Get current Tab index
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index == 1:
            if self.setting_service_is_exist and self.setting_led_task_is_running: 
                self.setting_led_task_is_running = False 
                self.config_manager.set_value('LED', 'is_run_on_startup', self.setting_led_task_is_running)           
                self.config_manager.save_config()
                self.setting_tab.btn_led_switch.setChecked(self.setting_led_task_is_running)                           
                self.setting_tab.set_custom_task_led_button_state(self.setting_service_is_exist, self.setting_led_task_is_running)
                self.led_tab.set_led_mode(self.led_mode)
                self.led_tab.led_btn_test_coustom_code.setText("Test")
                time.sleep(0.5)
                self.send_led_mode_to_expansion(self.led_mode)
                if self.led_mode == 4:
                    self.set_led_process(True)
                    self.led_tab.led_btn_test_coustom_code.setText("Stop")
                else:
                    self.set_led_process(False)
                    self.led_tab.led_btn_test_coustom_code.setText("Test")
            else:
                if self.led_process is not None:
                    self.led_mode = 4
                    self.led_tab.set_led_mode(self.led_mode)
                    self.led_tab.led_btn_test_coustom_code.setText("Stop")
                else:
                    self.led_tab.set_led_mode(self.led_mode)
                    self.send_led_mode_to_expansion(self.led_mode)
                    self.led_tab.led_btn_test_coustom_code.setText("Test")

        elif current_tab_index == 2:
            if self.setting_service_is_exist and self.setting_fan_task_is_running: # If background service is running fan task
                self.setting_fan_task_is_running = False 
                self.config_manager.set_value('Fan', 'is_run_on_startup', self.setting_fan_task_is_running)            # Stop fan task by modifying config file
                self.config_manager.save_config()
                self.setting_tab.btn_fan_switch.setChecked(self.setting_fan_task_is_running)
                self.setting_tab.set_custom_task_fan_button_state(self.setting_service_is_exist, self.setting_fan_task_is_running)
                self.fan_tab.set_fan_radio_mode(self.fan_mode)
                time.sleep(1)
                self.send_fan_mode_to_expansion(self.fan_mode)
                if self.expansion.get_board_type() == "FNK0107":
                    if self.fan_mode == 3:
                        self.set_fan_process(True)
                        self.fan_tab.fan_btn_test_coustom_code.setText("Stop")
                    else:
                        self.set_fan_process(False)
                        self.fan_tab.fan_btn_test_coustom_code.setText("Test")
                elif self.expansion.get_board_type() == "FNK0100":
                    if self.fan_mode == 2:
                        self.set_fan_process(True)
                        self.fan_tab.fan_btn_test_coustom_code.setText("Stop")
                    else:
                        self.set_fan_process(False)
                        self.fan_tab.fan_btn_test_coustom_code.setText("Test")
            else:
                if self.expansion.get_board_type() == "FNK0107":
                    if self.fan_process is not None:
                        self.fan_mode = 3
                        self.fan_tab.set_fan_radio_mode(self.fan_mode)
                        self.fan_tab.fan_btn_test_coustom_code.setText("Stop")
                    else:
                        self.fan_tab.set_fan_radio_mode(self.fan_mode)
                        self.send_fan_mode_to_expansion(self.fan_mode)
                        self.fan_tab.fan_btn_test_coustom_code.setText("Test")
                elif self.expansion.get_board_type() == "FNK0100":
                    if self.fan_process is not None:
                        self.fan_mode = 2
                        self.fan_tab.set_fan_radio_mode(self.fan_mode)
                        self.fan_tab.fan_btn_test_coustom_code.setText("Stop")
                    else:
                        self.fan_tab.set_fan_radio_mode(self.fan_mode)
                        self.send_fan_mode_to_expansion(self.fan_mode)
                        self.fan_tab.fan_btn_test_coustom_code.setText("Test")
        
        elif current_tab_index == 3:
            if self.setting_service_is_exist and self.setting_oled_task_is_running: # If background service is running oled task
                self.setting_oled_task_is_running = False 
                self.config_manager.set_value('OLED', 'is_run_on_startup', self.setting_oled_task_is_running)            # Stop oled task by modifying config file
                self.config_manager.save_config()
                self.setting_tab.btn_oled_switch.setChecked(self.setting_oled_task_is_running)
                self.setting_tab.set_custom_task_oled_button_state(self.setting_service_is_exist, self.setting_oled_task_is_running)
                time.sleep(1)
                self.set_oled_process(True)
            else:
                if  self.oled_process is not None:
                    self.set_oled_process(True)
                    self.setting_tab.btn_oled_test.setText("Stop")
                else:
                    self.set_oled_process(False)
                    self.setting_tab.btn_oled_test.setText("Test")

        elif current_tab_index == 4:
            if self.led_process is not None:
                self.setting_tab.btn_led_test.setText("Stop")
            else:
                self.setting_tab.btn_led_test.setText("Test")
            if self.fan_process is not None:
                self.setting_tab.btn_fan_test.setText("Stop")
            else:
                self.setting_tab.btn_fan_test.setText("Test")
            if self.oled_process is not None:
                self.setting_tab.btn_oled_test.setText("Stop")
            else:
                self.setting_tab.btn_oled_test.setText("Test")
    def closeEvent(self, event):
        """Handle window close event"""
        if self.monitor_update_data_timer_is_running:  # If timer is running, stop timer and save config
            self.monitor_update_data_timer.stop()
            self.monitor_update_data_timer_is_running = False
        if self.monitor_update_color_timer_is_running:  # If timer is running, stop timer and save config
            self.monitor_update_color_timer.stop()
            self.monitor_update_color_timer_is_running = False
        self.set_led_process(False)
        self.set_fan_process(False)
        if self.setting_service_is_exist and self.oled_process is not None:
            self.set_oled_process(False)
            self.setting_oled_task_is_running = True
            self.config_manager.set_value('OLED', 'is_run_on_startup', self.setting_oled_task_is_running)
            self.config_manager.save_config()
        os.system('sudo rm __pycache__ -rf')
        event.accept()
    def keyPressEvent(self, event):
        """Handle keyboard key press events"""
        # Check if Ctrl+C is pressed
        if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            self.close()  # Trigger window close
        else:
            super().keyPressEvent(event)  # Call parent class keyboard event handler


if __name__ == "__main__":
    os.system('sudo chmod 700 /run/user/1000')
    app = QApplication(sys.argv)
    screens = app.screens()
    dsi_screen = None
    for screen in screens:
        if "DSI" in screen.name().upper():
            dsi_screen = screen
            break
    window = MainWindow()
    window.show()
    if dsi_screen:
        window.move(dsi_screen.geometry().topLeft()) 
    sys.exit(app.exec_())
