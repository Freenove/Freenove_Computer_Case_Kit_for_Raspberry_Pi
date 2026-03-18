# app_ui_fan.py
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QHBoxLayout, QSlider, QLabel, QPushButton, QRadioButton, QLineEdit
from PyQt5.QtCore import Qt

class FNK0107_FanTab(QWidget):
    def __init__(self, width=700, height=400):
        """Initialize the fan control interface"""
        super().__init__()
        
        # Control area
        self.fan_mode_radio_buttons_names = ["Follow Case", "Follow RPi", "Manual", "Custom", "Close"] # Fan mode names
        self.fan_mode_radio_buttons = []            # Create radio button list
        
        # Sub-interface controls
        self.fan_manual_widget = None                # Fan duty cycle sub-interface
        self.fan_case_follow_widget = None           # Temperature threshold sub-interface
        self.fan_pi_following_widget = None          # Pi PWM follow sub-interface
        
        # Manual control interface controls
        self.fan_manual_fan1_slider_label = None         # Fan 1 slider label
        self.fan_manual_fan1_slider_value = None         # Fan 1 slider value label
        self.fan_manual_fan2_slider_label = None         # Fan 2 slider label
        self.fan_manual_fan2_slider_value = None         # Fan 2 slider value label
        self.fan_manual_fan3_slider_label = None         # Fan 3 slider label
        self.fan_manual_fan3_slider_value = None         # Fan 3 slider value label
        self.fan_manual_slider_fan1 = None               # Fan 1 slider
        self.fan_manual_slider_fan2 = None               # Fan 2 slider
        self.fan_manual_slider_fan3 = None               # Fan 3 slider
        
        # Temperature threshold slider controls
        self.fan_case_low_temp_lable = None              # Low temperature threshold label
        self.fan_case_high_temp_lable = None             # High temperature threshold label
        self.fan_case_temp_schmitt_lable = None          # Schmitt threshold label
        self.fan_case_low_temp_input = None              # Low temperature threshold input box
        self.fan_case_high_temp_input = None             # High temperature threshold input box
        self.fan_case_temp_schmitt_input = None          # Schmitt threshold input box
        self.fan_case_low_temp_minus_btn = None          # Low temperature threshold minus button
        self.fan_case_low_temp_plus_btn = None           # Low temperature threshold plus button
        self.fan_case_high_temp_minus_btn = None         # High temperature threshold minus button
        self.fan_case_high_temp_plus_btn = None          # High temperature threshold plus button
        self.fan_case_temp_schmitt_minus_btn = None      # Schmitt threshold minus button
        self.fan_case_temp_schmitt_plus_btn = None       # Schmitt threshold plus button
        self.fan_case_low_speed_slider_label = None      # Low speed slider label
        self.fan_case_low_speed_slider_value = None      # Low speed slider value label
        self.fan_case_middle_speed_slider_label = None   # Middle speed slider label
        self.fan_case_middle_speed_slider_value = None   # Middle speed slider value label
        self.fan_case_high_speed_slider_label = None     # High speed slider label
        self.fan_case_high_speed_slider_value = None     # High speed slider value label
        self.fan_case_low_speed_slider = None            # Low speed slider
        self.fan_case_middle_speed_slider = None         # Middle speed slider
        self.fan_case_high_speed_slider = None           # High speed slider
        
        # Pi PWM follow slider controls
        self.fan_pi_pwm_min_lable = None                 # Pi PWM follow minimum value label
        self.fan_pi_pwm_max_lable = None                 # Pi PWM follow maximum value label
        self.fan_pi_pwm_min_slider = None                # Pi PWM follow minimum value slider
        self.fan_pi_pwm_max_slider = None                # Pi PWM follow maximum value slider
        self.fan_pi_pwm_min_value_lable = None           # Pi PWM follow minimum value display
        self.fan_pi_pwm_max_value_lable = None           # Pi PWM follow maximum value display
        
        # Button controls
        self.fan_btn_save_config = None                  # Save configuration button
        self.fan_btn_default_config = None               # Restore default configuration button
        self.fan_btn_edit_custom_code = None             # Edit custom code button
        self.fan_btn_test_coustom_code = None            # Test custom code button
        
        # Variable area
        self.window_width = width                      # Window width
        self.window_height = height                    # Window height
        self.fan_mode = 0                              # Fan mode
        self.fan_last_mode = 0                         # Last fan mode
        self.fan_manual_mode_duty = [0, 0, 0]          # Fan manual mode duty cycle values for 3 fan interfaces
        self.fan_temp_mode_threshold = [30, 50, 3]     # Fan temperature mode threshold parameters
        self.fan_temp_mode_duty = [75, 125, 175]       # Fan temperature mode duty cycle parameters
        self.fan_pi_follows_duty_map = [0, 255]        # Fan Raspberry Pi follow mode duty cycle mapping parameters
        self.fan_process = None                        # Used to store running subprocess
        
        # Function area
        self.init_ui()                        # Initialize interface
        self.load_ui_events()

    def init_ui(self):
        """Initialize control interface"""
        # Set screen scaling factor
        self.scale_factor = 0.6
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setStyleSheet("background-color: #333333;")  # Set black background for monitoring tab
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))


        self.create_radio_buttons()

        self.create_manual_widget()
        self.create_temp_threshold_widget()
        self.create_pi_following_widget()
        
        self.show_widget_by_mode(self.fan_mode)
        
        # Create slider display area layout
        self.slider_area_layout = QVBoxLayout()
        self.slider_area_layout.addWidget(self.fan_manual_widget)
        self.slider_area_layout.addWidget(self.fan_case_follow_widget)
        self.slider_area_layout.addWidget(self.fan_pi_following_widget)

        # Create buttons named: Save Config, Default Config, Edit, Test
        fan_btn_style = """
            QPushButton {
                background-color: #444444;  /* Button background color */
                color: white;               /* Button text color */
                border: none;               /* No border */
                outline: none;              /* No outline */
                padding: 2px;               /* Button padding */
                border-radius: 5px;         /* Button rounded corners */
                font-size: 14px;            /* Button font size */
                font-weight: bold;          /* Bold font */
            }
            QPushButton:hover {
                background-color: #555555;  /* Button background color when mouse hovers */
            }
            QPushButton:pressed {
                background-color: #666666;  /* Button background color when pressed */
            }
        """
        self.fan_btn_default_config = QPushButton("Default")
        self.fan_btn_default_config.setStyleSheet(fan_btn_style)
        self.fan_btn_save_config = QPushButton("Save")
        self.fan_btn_save_config.setStyleSheet(fan_btn_style)
        self.fan_btn_edit_custom_code = QPushButton("Edit")
        self.fan_btn_edit_custom_code.setStyleSheet(fan_btn_style)
        self.fan_btn_test_coustom_code = QPushButton("Test")
        self.fan_btn_test_coustom_code.setStyleSheet(fan_btn_style)

        self.btn_layout = QHBoxLayout() 
        self.btn_layout.addWidget(self.fan_btn_default_config)
        self.btn_layout.addWidget(self.fan_btn_save_config)
        self.btn_layout.addWidget(self.fan_btn_edit_custom_code)
        self.btn_layout.addWidget(self.fan_btn_test_coustom_code)
        
        # Set main layout
        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(10, 10, 10, 10)  # Set margins
        self.vbox_layout.setSpacing(10)  # Set control spacing
        self.vbox_layout.addLayout(self.fan_mode_hbox_layout_1)
        self.vbox_layout.addLayout(self.fan_mode_hbox_layout_2)
        self.vbox_layout.addLayout(self.slider_area_layout)
        self.vbox_layout.addLayout(self.btn_layout)
        self.vbox_layout.setStretch(0,1)
        self.vbox_layout.setStretch(1,1)
        self.vbox_layout.setStretch(2,8)
        self.vbox_layout.setStretch(3,1)

        # Set main window
        self.setLayout(self.vbox_layout)

    def load_ui_events(self):
        # Fan interface signals and slot functions
        for i in range(len(self.fan_mode_radio_buttons_names)):  
            self.fan_mode_radio_buttons[i].clicked.connect(self.fan_radio_clicked_event)

    def create_radio_buttons(self):
        # Create horizontal layout containing fan mode options
        self.fan_mode_hbox_layout_1 = QHBoxLayout()  # Fan mode radio button layout
        self.fan_mode_hbox_layout_2 = QHBoxLayout()  # Fan mode radio button layout
        radio_button_style = """
            QRadioButton {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
            }
        """
        for i in range(3):
            radio_button = QRadioButton(self.fan_mode_radio_buttons_names[i])
            radio_button.setStyleSheet(radio_button_style)
            self.fan_mode_radio_buttons.append(radio_button)
            self.fan_mode_radio_buttons[i].setMinimumSize(50, 30)
            self.fan_mode_hbox_layout_1.addWidget(self.fan_mode_radio_buttons[i])
        for i in range(3,5,1):
            radio_button = QRadioButton(self.fan_mode_radio_buttons_names[i])
            radio_button.setStyleSheet(radio_button_style)
            self.fan_mode_radio_buttons.append(radio_button)
            self.fan_mode_radio_buttons[i].setMinimumSize(50, 30)
            self.fan_mode_hbox_layout_2.addWidget(self.fan_mode_radio_buttons[i])
        self.fan_mode_hbox_layout_1.setSpacing(10)          # Set control spacing
        self.fan_mode_hbox_layout_2.setSpacing(10)
        self.fan_mode_hbox_layout_1.setStretch(0,1)
        self.fan_mode_hbox_layout_1.setStretch(1,1)
        self.fan_mode_hbox_layout_1.setStretch(2,1)
        self.fan_mode_hbox_layout_2.setStretch(0,1)
        self.fan_mode_hbox_layout_2.setStretch(1,1)

    def fan_radio_clicked_event(self):
        """Handle FAN mode switch event"""
        fan_radio_mode = 0
        sender_button = self.sender()
        for i in range(len(self.fan_mode_radio_buttons_names)):
            if sender_button.text() == self.fan_mode_radio_buttons_names[i]:
                fan_radio_mode = i
        self.set_fan_radio_mode(fan_radio_mode)

    def get_fan_manual_slider_style(self, color):
        """Get slider style based on color"""
        return f"""
            QSlider {{
                border: 2px solid #444444;    /* Add external border */
                border-radius: 5px;           /* Border rounded corners */
                background-color: #333333;    /* Background color */
                padding: 2px;                 /* Padding */
            }}
            QSlider::groove:horizontal {{ 
                background: #555555;  /* Groove color */
                height: 20px;         /* Groove height */
                border-radius: 5px;   /* Groove rounded corners */
            }}
            QSlider::handle:horizontal {{
                background: {color};  /* Handle color */
                width: 40px;          /* Handle width */
                height: 20px;         /* Handle height */
                margin-top: -8px;     /* Move handle up */
                margin-bottom: -8px;  /* Move handle down */
            }}
        """
    
    def create_manual_widget(self):
        """Create fan duty cycle sub-interface"""
        self.fan_manual_widget = QWidget()
        fan_duty_layout = QVBoxLayout()
        fan_duty_layout.setSpacing(10)
        self.slider_label_style = """
            background-color: #444444;
            color: white;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 2px;
            font-size: 14px;
            font-weight: bold;
        """
        
        # Add fan 1 label, slider, slider value display
        self.fan_manual_fan1_slider_label = QLabel("FAN 1&2:")
        self.fan_manual_fan1_slider_label.setStyleSheet(self.slider_label_style)
        self.fan_manual_fan1_slider_label.setFixedWidth(90)
        self.fan_manual_slider_fan1 = QSlider(Qt.Horizontal)
        self.fan_manual_slider_fan1.setStyleSheet(self.get_fan_manual_slider_style("#45B7D1"))
        self.fan_manual_slider_fan1.setRange(0, 255)
        self.fan_manual_slider_fan1.setValue(0)
        self.fan_manual_fan1_slider_value = QLabel("0")
        self.fan_manual_fan1_slider_value.setStyleSheet(self.slider_label_style)
        self.fan_manual_fan1_slider_value.setFixedWidth(60)
        # Create a horizontal layout
        self.fan_manual_slider_fan1_layout = QHBoxLayout()
        self.fan_manual_slider_fan1_layout.addWidget(self.fan_manual_fan1_slider_label, stretch=1)
        self.fan_manual_slider_fan1_layout.addWidget(self.fan_manual_slider_fan1, stretch=9)
        self.fan_manual_slider_fan1_layout.addWidget(self.fan_manual_fan1_slider_value, stretch=1)
        self.fan_manual_slider_fan1_layout.setSpacing(10)
        
        # Add fan 2 label, slider, slider value display
        self.fan_manual_fan2_slider_label = QLabel("FAN 3&4:")
        self.fan_manual_fan2_slider_label.setStyleSheet(self.slider_label_style)
        self.fan_manual_fan2_slider_label.setFixedWidth(90)
        self.fan_manual_slider_fan2 = QSlider(Qt.Horizontal)
        self.fan_manual_slider_fan2.setStyleSheet(self.get_fan_manual_slider_style("#03F8BB"))
        self.fan_manual_slider_fan2.setRange(0, 255)
        self.fan_manual_slider_fan2.setValue(0)
        self.fan_manual_fan2_slider_value = QLabel("0")
        self.fan_manual_fan2_slider_value.setStyleSheet(self.slider_label_style)
        self.fan_manual_fan2_slider_value.setFixedWidth(60)
        # Create a horizontal layout
        self.fan_manual_slider_fan2_layout = QHBoxLayout()
        self.fan_manual_slider_fan2_layout.addWidget(self.fan_manual_fan2_slider_label, stretch=1)
        self.fan_manual_slider_fan2_layout.addWidget(self.fan_manual_slider_fan2, stretch=9)
        self.fan_manual_slider_fan2_layout.addWidget(self.fan_manual_fan2_slider_value, stretch=1)
        self.fan_manual_slider_fan2_layout.setSpacing(10)
        
        # Add fan 3 label, slider, slider value display
        self.fan_manual_fan3_slider_label = QLabel("Fan 5:")
        self.fan_manual_fan3_slider_label.setStyleSheet(self.slider_label_style)
        self.fan_manual_fan3_slider_label.setFixedWidth(90)
        self.fan_manual_slider_fan3 = QSlider(Qt.Horizontal)
        self.fan_manual_slider_fan3.setStyleSheet(self.get_fan_manual_slider_style("#FFA500"))
        self.fan_manual_slider_fan3.setRange(0, 255)
        self.fan_manual_slider_fan3.setValue(0)
        self.fan_manual_fan3_slider_value = QLabel("0")
        self.fan_manual_fan3_slider_value.setStyleSheet(self.slider_label_style)
        self.fan_manual_fan3_slider_value.setFixedWidth(60)
        # Create a horizontal layout
        self.fan_manual_slider_fan3_layout = QHBoxLayout()
        self.fan_manual_slider_fan3_layout.addWidget(self.fan_manual_fan3_slider_label, stretch=1)
        self.fan_manual_slider_fan3_layout.addWidget(self.fan_manual_slider_fan3, stretch=9)
        self.fan_manual_slider_fan3_layout.addWidget(self.fan_manual_fan3_slider_value, stretch=1)
        self.fan_manual_slider_fan3_layout.setSpacing(10)
        
        fan_duty_layout.addLayout(self.fan_manual_slider_fan1_layout)
        fan_duty_layout.addLayout(self.fan_manual_slider_fan2_layout)
        fan_duty_layout.addLayout(self.fan_manual_slider_fan3_layout)
        self.fan_manual_widget.setLayout(fan_duty_layout)
        
    def create_temp_threshold_widget(self):
        """Create temperature threshold sub-interface"""
        self.fan_case_follow_widget = QWidget()
        
        # Uniformly set style for all components
        self.slider_label_style = """
            background-color: #444444;
            color: white;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 2px;
            font-size: 14px;
            font-weight: bold;
        """

        # Extract common styles for QPushButton and QLineEdit
        button_style = """
            QPushButton {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """
        
        line_edit_style = """
            QLineEdit {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
        """

        # Low temperature threshold label and input controls
        self.fan_case_low_temp_lable = QLabel("Low Temp")
        self.fan_case_low_temp_lable.setStyleSheet(self.slider_label_style)
        # High temperature threshold label and input controls
        self.fan_case_high_temp_lable = QLabel("High Temp")
        self.fan_case_high_temp_lable.setStyleSheet(self.slider_label_style)
        # Schmitt trigger label and input controls
        self.fan_case_temp_schmitt_lable = QLabel("Schmitt")
        self.fan_case_temp_schmitt_lable.setStyleSheet(self.slider_label_style)
        # Low temperature threshold text display box
        self.fan_case_low_temp_input = QLineEdit()
        self.fan_case_low_temp_input.setStyleSheet(line_edit_style)
        self.fan_case_low_temp_input.setText("30")
        self.fan_case_low_temp_input.setAlignment(Qt.AlignCenter)
        self.fan_case_low_temp_input.setEnabled(False)
        # Low temperature threshold minus button
        self.fan_case_low_temp_minus_btn = QPushButton("-")
        self.fan_case_low_temp_minus_btn.setStyleSheet(button_style)
        # Low temperature threshold plus button
        self.fan_case_low_temp_plus_btn = QPushButton("+")
        self.fan_case_low_temp_plus_btn.setStyleSheet(button_style)
        # High temperature threshold text display box
        self.fan_case_high_temp_input = QLineEdit()
        self.fan_case_high_temp_input.setStyleSheet(line_edit_style)
        self.fan_case_high_temp_input.setText("50")
        self.fan_case_high_temp_input.setAlignment(Qt.AlignCenter)
        self.fan_case_low_temp_input.setEnabled(False)
        # High temperature threshold minus button
        self.fan_case_high_temp_minus_btn = QPushButton("-")
        self.fan_case_high_temp_minus_btn.setStyleSheet(button_style)
        # High temperature threshold plus button
        self.fan_case_high_temp_plus_btn = QPushButton("+")
        self.fan_case_high_temp_plus_btn.setStyleSheet(button_style)
        # Schmitt trigger text display box
        self.fan_case_temp_schmitt_input = QLineEdit()
        self.fan_case_temp_schmitt_input.setStyleSheet(line_edit_style)
        self.fan_case_temp_schmitt_input.setText("3")
        self.fan_case_temp_schmitt_input.setAlignment(Qt.AlignCenter)
        self.fan_case_temp_schmitt_input.setEnabled(False)
        # Schmitt trigger minus button
        self.fan_case_temp_schmitt_minus_btn = QPushButton("-")
        self.fan_case_temp_schmitt_minus_btn.setStyleSheet(button_style)
        # Schmitt trigger plus button
        self.fan_case_temp_schmitt_plus_btn = QPushButton("+")
        self.fan_case_temp_schmitt_plus_btn.setStyleSheet(button_style)

        # Add controls to first row layout
        # First row: Low temperature threshold settings
        temp_settings_layout = QHBoxLayout()
        temp_settings_layout_1 = QHBoxLayout()
        temp_settings_layout_1.addWidget(self.fan_case_low_temp_minus_btn)
        temp_settings_layout_1.addWidget(self.fan_case_low_temp_input)
        temp_settings_layout_1.addWidget(self.fan_case_low_temp_plus_btn)
        temp_settings_layout_1.setStretch(0, 1)
        temp_settings_layout_1.setStretch(1, 1)
        temp_settings_layout_1.setStretch(2, 1)
        temp_settings_layout_1.setSpacing(5)
        
        temp_settings_layout_2 = QHBoxLayout()
        temp_settings_layout_2.addWidget(self.fan_case_high_temp_minus_btn)
        temp_settings_layout_2.addWidget(self.fan_case_high_temp_input)
        temp_settings_layout_2.addWidget(self.fan_case_high_temp_plus_btn)
        temp_settings_layout_2.setStretch(0, 1)
        temp_settings_layout_2.setStretch(1, 1)
        temp_settings_layout_2.setStretch(2, 1)
        temp_settings_layout_2.setSpacing(5)
        
        temp_settings_layout_3 = QHBoxLayout()
        temp_settings_layout_3.addWidget(self.fan_case_temp_schmitt_minus_btn)
        temp_settings_layout_3.addWidget(self.fan_case_temp_schmitt_input)
        temp_settings_layout_3.addWidget(self.fan_case_temp_schmitt_plus_btn)
        temp_settings_layout_3.setStretch(0, 1)
        temp_settings_layout_3.setStretch(1, 1)
        temp_settings_layout_3.setStretch(2, 1)
        temp_settings_layout_3.setSpacing(5)
        
        temp_settings_vbox_1 = QVBoxLayout()
        temp_settings_vbox_1.addWidget(self.fan_case_low_temp_lable)
        temp_settings_vbox_1.addLayout(temp_settings_layout_1)
        temp_settings_vbox_1.setStretch(0, 1)
        temp_settings_vbox_1.setStretch(1, 1)
        temp_settings_vbox_1.setSpacing(10)
        
        temp_settings_vbox_2 = QVBoxLayout()
        temp_settings_vbox_2.addWidget(self.fan_case_high_temp_lable)
        temp_settings_vbox_2.addLayout(temp_settings_layout_2)
        temp_settings_vbox_2.setStretch(0, 1)
        temp_settings_vbox_2.setStretch(1, 1)
        temp_settings_vbox_2.setSpacing(10)
        
        temp_settings_vbox_3 = QVBoxLayout()
        temp_settings_vbox_3.addWidget(self.fan_case_temp_schmitt_lable)
        temp_settings_vbox_3.addLayout(temp_settings_layout_3)
        temp_settings_vbox_3.setStretch(0, 1)
        temp_settings_vbox_3.setStretch(1, 1)
        temp_settings_vbox_3.setSpacing(10)
        
        temp_settings_layout.addLayout(temp_settings_vbox_1)
        temp_settings_layout.addLayout(temp_settings_vbox_2)
        temp_settings_layout.addLayout(temp_settings_vbox_3)
        temp_settings_layout.setSpacing(10)
        temp_settings_layout.setStretch(0, 1)
        temp_settings_layout.setStretch(1, 1)
        temp_settings_layout.setStretch(2, 1)
        
        # Second row: Low speed slider
        self.fan_case_low_speed_slider_label = QLabel("Low Speed:")
        self.fan_case_low_speed_slider_label.setStyleSheet(self.slider_label_style)
        self.fan_case_low_speed_slider_label.setFixedWidth(120)
        self.fan_case_low_speed_slider = QSlider(Qt.Horizontal)
        self.fan_case_low_speed_slider.setStyleSheet("""
            QSlider {
                border: 2px solid #444444;
                border-radius: 5px;
                background-color: #333333;
                padding: 2px;
            }
            QSlider::groove:horizontal { 
                background: #555555;
                height: 20px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #87CEEB;
                width: 40px;
                height: 20px;
                margin-top: -8px;
                margin-bottom: -8px;
            }
        """)
        self.fan_case_low_speed_slider.setRange(0, 100)
        self.fan_case_low_speed_slider.setValue(50)
        self.fan_case_low_speed_slider_value = QLabel("50")
        self.fan_case_low_speed_slider_value.setStyleSheet(self.slider_label_style)
        self.fan_case_low_speed_slider_value.setFixedWidth(60)
        
        low_speed_layout = QHBoxLayout()
        low_speed_layout.addWidget(self.fan_case_low_speed_slider_label)
        low_speed_layout.addWidget(self.fan_case_low_speed_slider)
        low_speed_layout.addWidget(self.fan_case_low_speed_slider_value)
        low_speed_layout.setSpacing(10)
        
        # Third row: Middle speed slider
        self.fan_case_middle_speed_slider_label = QLabel("Middle Speed:")
        self.fan_case_middle_speed_slider_label.setStyleSheet(self.slider_label_style)
        self.fan_case_middle_speed_slider_label.setFixedWidth(120)
        self.fan_case_middle_speed_slider = QSlider(Qt.Horizontal)
        self.fan_case_middle_speed_slider.setStyleSheet("""
            QSlider {
                border: 2px solid #444444;
                border-radius: 5px;
                background-color: #333333;
                padding: 2px;
            }
            QSlider::groove:horizontal { 
                background: #555555;
                height: 20px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #9370DB;
                width: 40px;
                height: 20px;
                margin-top: -8px;
                margin-bottom: -8px;
            }
        """)
        self.fan_case_middle_speed_slider.setRange(101, 150)
        self.fan_case_middle_speed_slider.setValue(125)
        self.fan_case_middle_speed_slider_value = QLabel("125")
        self.fan_case_middle_speed_slider_value.setStyleSheet(self.slider_label_style)
        self.fan_case_middle_speed_slider_value.setFixedWidth(60)
        
        middle_speed_layout = QHBoxLayout()
        middle_speed_layout.addWidget(self.fan_case_middle_speed_slider_label)
        middle_speed_layout.addWidget(self.fan_case_middle_speed_slider)
        middle_speed_layout.addWidget(self.fan_case_middle_speed_slider_value)
        middle_speed_layout.setSpacing(10)
        
        # Fourth row: High speed slider
        self.fan_case_high_speed_slider_label = QLabel("High Speed:")
        self.fan_case_high_speed_slider_label.setStyleSheet(self.slider_label_style)
        self.fan_case_high_speed_slider_label.setFixedWidth(120)
        self.fan_case_high_speed_slider = QSlider(Qt.Horizontal)
        self.fan_case_high_speed_slider.setStyleSheet("""
            QSlider {
                border: 2px solid #444444;
                border-radius: 5px;
                background-color: #333333;
                padding: 2px;
            }
            QSlider::groove:horizontal { 
                background: #555555;
                height: 20px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #FF6347;
                width: 40px;
                height: 20px;
                margin-top: -8px;
                margin-bottom: -8px;
            }
        """)
        self.fan_case_high_speed_slider.setRange(151, 255)
        self.fan_case_high_speed_slider.setValue(175)
        self.fan_case_high_speed_slider_value = QLabel("175")
        self.fan_case_high_speed_slider_value.setStyleSheet(self.slider_label_style)
        self.fan_case_high_speed_slider_value.setFixedWidth(60)
        
        high_speed_layout = QHBoxLayout()
        high_speed_layout.addWidget(self.fan_case_high_speed_slider_label)
        high_speed_layout.addWidget(self.fan_case_high_speed_slider)
        high_speed_layout.addWidget(self.fan_case_high_speed_slider_value)
        high_speed_layout.setSpacing(10)
        
        # Add all rows to main layout
        temp_threshold_layout = QVBoxLayout()
        temp_threshold_layout.setSpacing(10)
        temp_threshold_layout.addLayout(temp_settings_layout)
        temp_threshold_layout.addLayout(low_speed_layout)
        temp_threshold_layout.addLayout(middle_speed_layout)
        temp_threshold_layout.addLayout(high_speed_layout)
        temp_threshold_layout.setStretch(0, 1)
        temp_threshold_layout.setStretch(1, 1)
        temp_threshold_layout.setStretch(2, 1)
        temp_threshold_layout.setStretch(3, 1)

        self.fan_case_follow_widget.setLayout(temp_threshold_layout)
        
    def create_pi_following_widget(self):
        """Create Pi PWM follow sub-interface"""
        self.fan_pi_following_widget = QWidget()
        pi_following_layout = QVBoxLayout()
        pi_following_layout.setSpacing(10)
        
        # Add Pi PWM follow minimum value label, slider, value display
        self.fan_pi_pwm_min_lable = QLabel("Min Speed:")
        self.fan_pi_pwm_min_lable.setStyleSheet(self.slider_label_style)
        self.fan_pi_pwm_min_lable.setFixedWidth(90)
        self.fan_pi_pwm_min_slider = QSlider(Qt.Horizontal)
        self.fan_pi_pwm_min_slider.setStyleSheet("""
            QSlider {
                border: 2px solid #444444;    /* Add external border */
                border-radius: 5px;           /* Border rounded corners */
                background-color: #333333;    /* Background color */
                padding: 2px;                 /* Padding */
            }
            QSlider::groove:horizontal { 
                background: #555555;  /* Groove color */
                height: 20px;         /* Groove height */
                border-radius: 5px;   /* Groove rounded corners */
            }
            QSlider::handle:horizontal {
                background: #87CEEB;  /* Handle color */
                width: 40px;          /* Handle width */
                height: 20px;         /* Handle height */
                margin-top: -8px;    /* Move handle up */
                margin-bottom: -8px; /* Move handle down */
            }
        """)
        self.fan_pi_pwm_min_slider.setRange(0, 127)
        self.fan_pi_pwm_min_slider.setValue(0)
        self.fan_pi_pwm_min_value_lable = QLabel("0")
        self.fan_pi_pwm_min_value_lable.setStyleSheet(self.slider_label_style)
        self.fan_pi_pwm_min_value_lable.setFixedWidth(60)
        # Create a horizontal layout
        self.fan_pi_pwm_min_slider_layout = QHBoxLayout()
        self.fan_pi_pwm_min_slider_layout.addWidget(self.fan_pi_pwm_min_lable, stretch=1)
        self.fan_pi_pwm_min_slider_layout.addWidget(self.fan_pi_pwm_min_slider, stretch=9)
        self.fan_pi_pwm_min_slider_layout.addWidget(self.fan_pi_pwm_min_value_lable, stretch=1)
        self.fan_pi_pwm_min_slider_layout.setSpacing(10)

        # Add Pi PWM follow maximum value label, slider, value display
        self.fan_pi_pwm_max_lable = QLabel("Max Speed:")
        self.fan_pi_pwm_max_lable.setStyleSheet(self.slider_label_style)
        self.fan_pi_pwm_max_lable.setFixedWidth(90)
        self.fan_pi_pwm_max_slider = QSlider(Qt.Horizontal)
        self.fan_pi_pwm_max_slider.setStyleSheet("""
            QSlider {
                border: 2px solid #444444;    /* Add external border */
                border-radius: 5px;           /* Border rounded corners */
                background-color: #333333;    /* Background color */
                padding: 2px;                 /* Padding */
            }
            QSlider::groove:horizontal { 
                background: #555555;  /* Groove color */
                height: 20px;         /* Groove height */
                border-radius: 5px;   /* Groove rounded corners */
            }
            QSlider::handle:horizontal {
                background: #4169E1;  /* Handle color */
                width: 40px;          /* Handle width */
                height: 20px;         /* Handle height */
                margin-top: -8px;    /* Move handle up */
                margin-bottom: -8px; /* Move handle down */
            }
        """)
        self.fan_pi_pwm_max_slider.setRange(128, 255)
        self.fan_pi_pwm_max_slider.setValue(255)
        self.fan_pi_pwm_max_value_lable = QLabel("255")
        self.fan_pi_pwm_max_value_lable.setStyleSheet(self.slider_label_style)
        self.fan_pi_pwm_max_value_lable.setFixedWidth(60)
        # Create a horizontal layout
        self.fan_pi_pwm_max_slider_layout = QHBoxLayout()
        self.fan_pi_pwm_max_slider_layout.addWidget(self.fan_pi_pwm_max_lable, stretch=1)
        self.fan_pi_pwm_max_slider_layout.addWidget(self.fan_pi_pwm_max_slider, stretch=9)
        self.fan_pi_pwm_max_slider_layout.addWidget(self.fan_pi_pwm_max_value_lable, stretch=1)
        self.fan_pi_pwm_max_slider_layout.setSpacing(10)
        
        pi_following_layout.addLayout(self.fan_pi_pwm_min_slider_layout)
        pi_following_layout.addLayout(self.fan_pi_pwm_max_slider_layout)
        self.fan_pi_following_widget.setLayout(pi_following_layout)
        
    def resizeEvent(self, event):
        """Recalculate control heights when window size changes"""
        super().resizeEvent(event)
        self.fan_ui_height = round((self.height() - 50) // 7)

        for i in range(len(self.fan_mode_radio_buttons_names)):
            self.fan_mode_radio_buttons[i].setMaximumHeight(self.fan_ui_height)

        self.fan_btn_save_config.setMaximumHeight(self.fan_ui_height)
        self.fan_btn_default_config.setMaximumHeight(self.fan_ui_height)
        self.fan_btn_edit_custom_code.setMaximumHeight(self.fan_ui_height)
        self.fan_btn_test_coustom_code.setMaximumHeight(self.fan_ui_height)

        self.fan_manual_fan1_slider_label.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_fan2_slider_label.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_fan3_slider_label.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_fan1_slider_value.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_fan2_slider_value.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_fan3_slider_value.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_slider_fan1.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_slider_fan2.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_slider_fan3.setMaximumHeight(self.fan_ui_height)

        fan_case_follow_widget_height = round((self.fan_ui_height * 4 - 30) / 5)
        self.fan_case_low_temp_lable.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_high_temp_lable.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_temp_schmitt_lable.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_low_temp_minus_btn.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_low_temp_plus_btn.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_high_temp_minus_btn.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_high_temp_plus_btn.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_temp_schmitt_minus_btn.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_temp_schmitt_plus_btn.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_low_speed_slider_label.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_middle_speed_slider_label.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_high_speed_slider_label.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_low_speed_slider_value.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_middle_speed_slider_value.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_high_speed_slider_value.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_low_temp_input.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_high_temp_input.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_temp_schmitt_input.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_low_speed_slider.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_middle_speed_slider.setMaximumHeight(fan_case_follow_widget_height)
        self.fan_case_high_speed_slider.setMaximumHeight(fan_case_follow_widget_height)

        self.fan_pi_pwm_min_lable.setMaximumHeight(self.fan_ui_height)
        self.fan_pi_pwm_max_lable.setMaximumHeight(self.fan_ui_height)
        self.fan_pi_pwm_min_value_lable.setMaximumHeight(self.fan_ui_height)
        self.fan_pi_pwm_max_value_lable.setMaximumHeight(self.fan_ui_height)
        self.fan_pi_pwm_min_slider.setMaximumHeight(self.fan_ui_height)
        self.fan_pi_pwm_max_slider.setMaximumHeight(self.fan_ui_height)
        
    def resetUiSize(self, width, height):
        """Reset UI dimensions"""
        self.window_width = width
        self.window_height = height
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))
        
    def closeEvent(self, event):
        """Handle window close event"""
        event.accept()
    
    def show_widget_by_mode(self, mode):
        """Show corresponding sub-interface based on mode"""
        if mode == 0:  # 
            self.fan_manual_widget.setEnabled(False)
            self.fan_case_follow_widget.setEnabled(True)
            self.fan_pi_following_widget.setEnabled(False)
            self.fan_manual_widget.hide()
            self.fan_case_follow_widget.show()
            self.fan_pi_following_widget.hide()
        elif mode == 1:  
            self.fan_manual_widget.setEnabled(False)
            self.fan_case_follow_widget.setEnabled(False)
            self.fan_pi_following_widget.setEnabled(True)
            self.fan_manual_widget.hide()
            self.fan_case_follow_widget.hide()
            self.fan_pi_following_widget.show()
        elif mode == 2: 
            self.fan_manual_widget.setEnabled(True)
            self.fan_case_follow_widget.setEnabled(False)
            self.fan_pi_following_widget.setEnabled(False)
            self.fan_manual_widget.show()
            self.fan_case_follow_widget.hide()
            self.fan_pi_following_widget.hide()
        else:  
            self.fan_manual_widget.setEnabled(False)
            self.fan_case_follow_widget.setEnabled(False)
            self.fan_pi_following_widget.setEnabled(False)
    
    def set_fan_radio_mode(self, mode):
        """Set fan mode"""
        for i in range(len(self.fan_mode_radio_buttons_names)):
            if i == mode:
                self.fan_mode_radio_buttons[i].setChecked(True)
                self.fan_mode_radio_buttons[i].setEnabled(False)
            else:
                self.fan_mode_radio_buttons[i].setChecked(False)
                self.fan_mode_radio_buttons[i].setEnabled(True)
            if mode == 3:
                fan_btn_style = """
                    QPushButton {
                        background-color: #444444;  /* Button background color */
                        color: white;               /* Button text color */
                        border: none;               /* No border */
                        outline: none;              /* No outline */
                        padding: 2px;               /* Button padding */
                        border-radius: 5px;         /* Button rounded corners */
                        font-size: 14px;            /* Button font size */
                        font-weight: bold;          /* Bold font */
                    }
                    QPushButton:hover {
                        background-color: #555555;  /* Button background color when mouse hovers */
                    }
                    QPushButton:pressed {
                        background-color: #666666;  /* Button background color when pressed */
                    }
                """
                self.fan_btn_edit_custom_code.setEnabled(True)
                self.fan_btn_test_coustom_code.setEnabled(True)
                self.fan_btn_edit_custom_code.setStyleSheet(fan_btn_style)
                self.fan_btn_test_coustom_code.setStyleSheet(fan_btn_style)
            else:
                fan_btn_style = """
                    QPushButton {
                        background-color: #444444;  /* Button background color */
                        color: #888888;             /* Button text color */
                        border: none;               /* No border */
                        outline: none;              /* No outline */
                        padding: 2px;               /* Button padding */
                        border-radius: 5px;         /* Button rounded corners */
                        font-size: 14px;            /* Button font size */
                        font-weight: bold;          /* Bold font */
                    }
                    QPushButton:hover {
                        background-color: #444444;  /* Button background color when mouse hovers */
                    }
                    QPushButton:pressed {
                        background-color: #444444;  /* Button background color when pressed */
                    }
                """
                self.fan_btn_edit_custom_code.setEnabled(False)
                self.fan_btn_test_coustom_code.setEnabled(False)
                self.fan_btn_edit_custom_code.setStyleSheet(fan_btn_style)
                self.fan_btn_test_coustom_code.setStyleSheet(fan_btn_style)
        self.show_widget_by_mode(mode)

    def set_case_weight_temp(self, temp_threshold):
        """Set Case temperature thresholds"""
        self.fan_case_low_temp_input.setText(str(temp_threshold[0]))
        self.fan_case_high_temp_input.setText(str(temp_threshold[1]))
        self.fan_case_temp_schmitt_input.setText(str(temp_threshold[2]))
    
    def set_case_weight_slider_value(self, value):
        """Set Case temperature threshold slider values"""
        self.fan_case_low_speed_slider.setValue(value[0])
        self.fan_case_middle_speed_slider.setValue(value[1])
        self.fan_case_high_speed_slider.setValue(value[2])
        self.fan_case_low_speed_slider_value.setText(str(value[0]))
        self.fan_case_middle_speed_slider_value.setText(str(value[1]))
        self.fan_case_high_speed_slider_value.setText(str(value[2]))

    def set_pi_weight_slider_map(self, speed):
        """Set PWM mapping in PI mode"""
        self.fan_pi_pwm_min_slider.setValue(speed[0])
        self.fan_pi_pwm_max_slider.setValue(speed[1])
        self.fan_pi_pwm_min_value_lable.setText(str(speed[0]))
        self.fan_pi_pwm_max_value_lable.setText(str(speed[1]))
    
    def set_manual_weight_slider_value(self, speed):
        """Set PWM values in Manual mode"""
        self.fan_manual_slider_fan1.setValue(speed[0])
        self.fan_manual_slider_fan2.setValue(speed[1])
        self.fan_manual_slider_fan3.setValue(speed[2])
        self.fan_manual_fan1_slider_value.setText(str(speed[0]))
        self.fan_manual_fan2_slider_value.setText(str(speed[1]))
        self.fan_manual_fan3_slider_value.setText(str(speed[2]))

class FNK0100_FanTab(QWidget):
    def __init__(self, width=700, height=400):
        """Initialize the fan control interface"""
        super().__init__()
        
        # Control area
        self.fan_mode_radio_buttons_names = ["Follow Case", "Manual", "Custom", "Close"] # Fan mode names
        self.fan_mode_radio_buttons = []            # Create radio button list
        
        # Sub-interface controls
        self.fan_manual_widget = None                # Fan duty cycle sub-interface
        self.fan_case_follow_widget = None           # Temperature threshold sub-interface
        
        # Manual control interface controls
        self.fan_manual_fan1_slider_label = None         # Fan 1 slider label
        self.fan_manual_fan1_slider_value = None         # Fan 1 slider value label
        self.fan_manual_fan2_slider_label = None         # Fan 2 slider label
        self.fan_manual_fan2_slider_value = None         # Fan 2 slider value label
        self.fan_manual_slider_fan1 = None               # Fan 1 slider
        self.fan_manual_slider_fan2 = None               # Fan 2 slider
        
        # Temperature threshold slider controls
        self.fan_case_low_temp_lable = None              # Low temperature threshold label
        self.fan_case_low_temp_input = None              # Low temperature threshold input box
        self.fan_case_low_temp_minus_btn = None          # Low temperature threshold minus button
        self.fan_case_low_temp_plus_btn = None           # Low temperature threshold plus button

        self.fan_case_high_temp_lable = None             # High temperature threshold label
        self.fan_case_high_temp_input = None             # High temperature threshold input box
        self.fan_case_high_temp_minus_btn = None         # High temperature threshold minus button
        self.fan_case_high_temp_plus_btn = None          # High temperature threshold plus button

        # Button controls
        self.fan_btn_save_config = None                  # Save configuration button
        self.fan_btn_default_config = None               # Restore default configuration button
        self.fan_btn_edit_custom_code = None             # Edit custom code button
        self.fan_btn_test_coustom_code = None            # Test custom code button
        
        # Variable area
        self.window_width = width                      # Window width
        self.window_height = height                    # Window height
        self.fan_mode = 0                              # Fan mode
        self.fan_last_mode = 0                         # Last fan mode
        self.fan_manual_mode_duty = [0, 0, 0]          # Fan manual mode duty cycle values for 3 fan interfaces
        self.fan_temp_mode_threshold = [30, 50]        # Fan temperature mode threshold parameters
        
        # Function area
        self.init_ui()                        # Initialize interface
        self.load_ui_events()

    def get_fan_manual_slider_style(self, color):
        """Get slider style based on color"""
        return f"""
            QSlider {{
                border: 2px solid #444444;    /* Add external border */
                border-radius: 5px;           /* Border rounded corners */
                background-color: #333333;    /* Background color */
                padding: 2px;                 /* Padding */
            }}
            QSlider::groove:horizontal {{ 
                background: #555555;  /* Groove color */
                height: 20px;         /* Groove height */
                border-radius: 5px;   /* Groove rounded corners */
            }}
            QSlider::handle:horizontal {{
                background: {color};  /* Handle color */
                width: 40px;          /* Handle width */
                height: 20px;         /* Handle height */
                margin-top: -8px;     /* Move handle up */
                margin-bottom: -8px;  /* Move handle down */
            }}
        """
    
    def init_ui(self):
        """Initialize control interface"""
        # Set screen scaling factor
        self.scale_factor = 0.6
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setStyleSheet("background-color: #333333;")  # Set black background for monitoring tab
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))

        slider_label_style = """
            background-color: #444444;
            color: white;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 2px;
            font-size: 14px;
            font-weight: bold;
            text-align: center;
        """
        button_style = """
            QPushButton {
                background-color: #444444;  /* Button background color */
                color: white;               /* Button text color */
                border: none;               /* No border */
                outline: none;              /* No outline */
                padding: 2px;               /* Button padding */
                border-radius: 5px;         /* Button rounded corners */
                font-size: 14px;            /* Button font size */
                font-weight: bold;          /* Bold font */
            }
            QPushButton:hover {
                background-color: #555555;  /* Button background color when mouse hovers */
            }
            QPushButton:pressed {
                background-color: #666666;  /* Button background color when pressed */
            }
        """
        line_edit_style = """
            QLineEdit {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
        """
        radio_button_style = """
            QRadioButton {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
            }
        """

        # Create horizontal layout containing fan mode options
        fan_mode_hbox_layout_1 = QHBoxLayout()  # Fan mode radio button layout
        for i in range(2):
            radio_button = QRadioButton(self.fan_mode_radio_buttons_names[i])
            radio_button.setStyleSheet(radio_button_style)
            self.fan_mode_radio_buttons.append(radio_button)
            self.fan_mode_radio_buttons[i].setMinimumSize(50, 30)
            fan_mode_hbox_layout_1.addWidget(self.fan_mode_radio_buttons[i])
        fan_mode_hbox_layout_1.setSpacing(10)       
        fan_mode_hbox_layout_1.setStretch(0,1)
        fan_mode_hbox_layout_1.setStretch(1,1)

        fan_mode_hbox_layout_2 = QHBoxLayout()  # Fan mode radio button layout
        for i in range(2,4,1):
            radio_button = QRadioButton(self.fan_mode_radio_buttons_names[i])
            radio_button.setStyleSheet(radio_button_style)
            self.fan_mode_radio_buttons.append(radio_button)
            self.fan_mode_radio_buttons[i].setMinimumSize(50, 30)
            fan_mode_hbox_layout_2.addWidget(self.fan_mode_radio_buttons[i])
        fan_mode_hbox_layout_2.setSpacing(10)
        fan_mode_hbox_layout_2.setStretch(0,1)
        fan_mode_hbox_layout_2.setStretch(1,1)

        temp_settings_layout_1 = QHBoxLayout()
        self.fan_case_low_temp_input = QLineEdit()
        self.fan_case_low_temp_input.setStyleSheet(line_edit_style)
        self.fan_case_low_temp_input.setText("30")
        self.fan_case_low_temp_input.setAlignment(Qt.AlignCenter)
        self.fan_case_low_temp_input.setEnabled(False)
        self.fan_case_low_temp_minus_btn = QPushButton("-")
        self.fan_case_low_temp_minus_btn.setStyleSheet(button_style)
        self.fan_case_low_temp_plus_btn = QPushButton("+")
        self.fan_case_low_temp_plus_btn.setStyleSheet(button_style)
        temp_settings_layout_1.addWidget(self.fan_case_low_temp_minus_btn)
        temp_settings_layout_1.addWidget(self.fan_case_low_temp_input)
        temp_settings_layout_1.addWidget(self.fan_case_low_temp_plus_btn)
        temp_settings_layout_1.setStretch(0, 1)
        temp_settings_layout_1.setStretch(1, 1)
        temp_settings_layout_1.setStretch(2, 1)
        temp_settings_layout_1.setSpacing(5)
        
        temp_settings_vbox_1 = QVBoxLayout()
        self.fan_case_low_temp_lable = QLabel("Low Temp")
        self.fan_case_low_temp_lable.setStyleSheet(slider_label_style)
        temp_settings_vbox_1.addWidget(self.fan_case_low_temp_lable)
        temp_settings_vbox_1.addLayout(temp_settings_layout_1)
        temp_settings_vbox_1.setStretch(0, 1)
        temp_settings_vbox_1.setStretch(1, 1)
        temp_settings_vbox_1.setSpacing(10)
        
        temp_settings_layout_2 = QHBoxLayout()
        self.fan_case_high_temp_input = QLineEdit()
        self.fan_case_high_temp_input.setStyleSheet(line_edit_style)
        self.fan_case_high_temp_input.setText("50")
        self.fan_case_high_temp_input.setAlignment(Qt.AlignCenter)
        self.fan_case_high_temp_input.setEnabled(False)
        self.fan_case_high_temp_minus_btn = QPushButton("-")
        self.fan_case_high_temp_minus_btn.setStyleSheet(button_style)
        self.fan_case_high_temp_plus_btn = QPushButton("+")
        self.fan_case_high_temp_plus_btn.setStyleSheet(button_style)
        temp_settings_layout_2.addWidget(self.fan_case_high_temp_minus_btn)
        temp_settings_layout_2.addWidget(self.fan_case_high_temp_input)
        temp_settings_layout_2.addWidget(self.fan_case_high_temp_plus_btn)
        temp_settings_layout_2.setStretch(0, 1)
        temp_settings_layout_2.setStretch(1, 1)
        temp_settings_layout_2.setStretch(2, 1)
        temp_settings_layout_2.setSpacing(5)

        temp_settings_vbox_2 = QVBoxLayout()
        self.fan_case_high_temp_lable = QLabel("High Temp")
        self.fan_case_high_temp_lable.setStyleSheet(slider_label_style)
        temp_settings_vbox_2.addWidget(self.fan_case_high_temp_lable)
        temp_settings_vbox_2.addLayout(temp_settings_layout_2)
        temp_settings_vbox_2.setStretch(0, 1)
        temp_settings_vbox_2.setStretch(1, 1)
        temp_settings_vbox_2.setSpacing(10)

        temp_settings_layout = QHBoxLayout()
        temp_settings_layout.addLayout(temp_settings_vbox_1)
        temp_settings_layout.addLayout(temp_settings_vbox_2)
        temp_settings_layout.setSpacing(10)
        temp_settings_layout.setStretch(0, 1)
        temp_settings_layout.setStretch(1, 1)                      ###################################

        self.fan_manual_slider_fan1_layout = QHBoxLayout()
        self.fan_manual_fan1_slider_label = QLabel("FAN 1:")
        self.fan_manual_fan1_slider_label.setStyleSheet(slider_label_style)
        self.fan_manual_fan1_slider_label.setFixedWidth(90)
        self.fan_manual_slider_fan1 = QSlider(Qt.Horizontal)
        self.fan_manual_slider_fan1.setStyleSheet(self.get_fan_manual_slider_style("#1900FF"))
        self.fan_manual_slider_fan1.setRange(0, 255)
        self.fan_manual_slider_fan1.setValue(0)
        self.fan_manual_fan1_slider_value = QLabel("0")
        self.fan_manual_fan1_slider_value.setStyleSheet(slider_label_style)
        self.fan_manual_fan1_slider_value.setFixedWidth(60)
        self.fan_manual_slider_fan1_layout.addWidget(self.fan_manual_fan1_slider_label, stretch=1)
        self.fan_manual_slider_fan1_layout.addWidget(self.fan_manual_slider_fan1, stretch=9)
        self.fan_manual_slider_fan1_layout.addWidget(self.fan_manual_fan1_slider_value, stretch=1)
        self.fan_manual_slider_fan1_layout.setSpacing(10)
        
        self.fan_manual_slider_fan2_layout = QHBoxLayout()
        self.fan_manual_fan2_slider_label = QLabel("FAN 2:")
        self.fan_manual_fan2_slider_label.setStyleSheet(slider_label_style)
        self.fan_manual_fan2_slider_label.setFixedWidth(90)
        self.fan_manual_slider_fan2 = QSlider(Qt.Horizontal)
        self.fan_manual_slider_fan2.setStyleSheet(self.get_fan_manual_slider_style("#09FF00"))
        self.fan_manual_slider_fan2.setRange(0, 255)
        self.fan_manual_slider_fan2.setValue(0)
        self.fan_manual_fan2_slider_value = QLabel("0")
        self.fan_manual_fan2_slider_value.setStyleSheet(slider_label_style)
        self.fan_manual_fan2_slider_value.setFixedWidth(60)
        self.fan_manual_slider_fan2_layout.addWidget(self.fan_manual_fan2_slider_label, stretch=1)
        self.fan_manual_slider_fan2_layout.addWidget(self.fan_manual_slider_fan2, stretch=9)
        self.fan_manual_slider_fan2_layout.addWidget(self.fan_manual_fan2_slider_value, stretch=1)
        self.fan_manual_slider_fan2_layout.setSpacing(10)

        fan_duty_layout = QVBoxLayout()
        fan_duty_layout.addLayout(self.fan_manual_slider_fan1_layout)
        fan_duty_layout.addLayout(self.fan_manual_slider_fan2_layout)
        fan_duty_layout.setSpacing(10)                                         #################################
        fan_duty_layout.setStretch(0, 1)
        fan_duty_layout.setStretch(1, 1)

        # Create buttons named: Save Config, Default Config, Edit, Test

        self.fan_btn_default_config = QPushButton("Default")
        self.fan_btn_default_config.setStyleSheet(button_style)
        self.fan_btn_save_config = QPushButton("Save")
        self.fan_btn_save_config.setStyleSheet(button_style)
        self.fan_btn_edit_custom_code = QPushButton("Edit")
        self.fan_btn_edit_custom_code.setStyleSheet(button_style)
        self.fan_btn_test_coustom_code = QPushButton("Test")
        self.fan_btn_test_coustom_code.setStyleSheet(button_style)

        btn_layout = QHBoxLayout() 
        btn_layout.addWidget(self.fan_btn_default_config)
        btn_layout.addWidget(self.fan_btn_save_config)
        btn_layout.addWidget(self.fan_btn_edit_custom_code)
        btn_layout.addWidget(self.fan_btn_test_coustom_code)
        
        # Set main layout
        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(10, 10, 10, 10)  # Set margins
        self.vbox_layout.setSpacing(10)  # Set control spacing
        self.vbox_layout.addLayout(fan_mode_hbox_layout_1)
        self.vbox_layout.addLayout(fan_mode_hbox_layout_2)
        self.vbox_layout.addLayout(temp_settings_layout)
        self.vbox_layout.addLayout(fan_duty_layout)
        self.vbox_layout.addLayout(btn_layout)
        self.vbox_layout.setStretch(0,1)
        self.vbox_layout.setStretch(1,1)
        self.vbox_layout.setStretch(2,4)
        self.vbox_layout.setStretch(3,4)
        self.vbox_layout.setStretch(4,1)

        # Set main window
        self.setLayout(self.vbox_layout)

    def load_ui_events(self):
        # Fan interface signals and slot functions
        for i in range(len(self.fan_mode_radio_buttons_names)):  
            self.fan_mode_radio_buttons[i].clicked.connect(self.fan_radio_clicked_event)

    def fan_radio_clicked_event(self):
        """Handle FAN mode switch event"""
        fan_radio_mode = 0
        sender_button = self.sender()
        for i in range(len(self.fan_mode_radio_buttons_names)):
            if sender_button.text() == self.fan_mode_radio_buttons_names[i]:
                fan_radio_mode = i
        self.set_fan_radio_mode(fan_radio_mode)

    def resizeEvent(self, event):
        """Recalculate control heights when window size changes"""
        super().resizeEvent(event)
        self.fan_ui_height = round((self.height() - 80) // 7)
        for i in range(len(self.fan_mode_radio_buttons_names)):
            self.fan_mode_radio_buttons[i].setMaximumHeight(self.fan_ui_height)
        
        self.fan_btn_save_config.setMaximumHeight(self.fan_ui_height)
        self.fan_btn_default_config.setMaximumHeight(self.fan_ui_height)
        self.fan_btn_edit_custom_code.setMaximumHeight(self.fan_ui_height)
        self.fan_btn_test_coustom_code.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_fan1_slider_label.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_fan2_slider_label.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_fan1_slider_value.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_fan2_slider_value.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_slider_fan1.setMaximumHeight(self.fan_ui_height)
        self.fan_manual_slider_fan2.setMaximumHeight(self.fan_ui_height)
        self.fan_case_low_temp_lable.setMaximumHeight(self.fan_ui_height)
        self.fan_case_high_temp_lable.setMaximumHeight(self.fan_ui_height)
        self.fan_case_low_temp_minus_btn.setMaximumHeight(self.fan_ui_height)
        self.fan_case_low_temp_plus_btn.setMaximumHeight(self.fan_ui_height)
        self.fan_case_high_temp_minus_btn.setMaximumHeight(self.fan_ui_height)
        self.fan_case_high_temp_plus_btn.setMaximumHeight(self.fan_ui_height)
        self.fan_case_low_temp_input.setMaximumHeight(self.fan_ui_height)
        self.fan_case_high_temp_input.setMaximumHeight(self.fan_ui_height)
        
    def resetUiSize(self, width, height):
        """Reset UI dimensions"""
        self.window_width = width
        self.window_height = height
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))
        
    def closeEvent(self, event):
        """Handle window close event"""
        event.accept()
    
    def set_fan_radio_mode(self, mode):
        button_style = """
            QPushButton {
                background-color: #444444;  /* Button background color */
                color: white;               /* Button text color */
                border: none;               /* No border */
                outline: none;              /* No outline */
                padding: 2px;               /* Button padding */
                border-radius: 5px;         /* Button rounded corners */
                font-size: 14px;            /* Button font size */
                font-weight: bold;          /* Bold font */
            }
            QPushButton:hover {
                background-color: #555555;  /* Button background color when mouse hovers */
            }
            QPushButton:pressed {
                background-color: #666666;  /* Button background color when pressed */
            }
        """
        button_disable_style = """
            QPushButton {
                background-color: #444444;  /* Button background color */
                color: #888888;             /* Button text color */
                border: none;               /* No border */
                outline: none;              /* No outline */
                padding: 2px;               /* Button padding */
                border-radius: 5px;         /* Button rounded corners */
                font-size: 14px;            /* Button font size */
                font-weight: bold;          /* Bold font */
            }
            QPushButton:hover {
                background-color: #444444;  /* Button background color when mouse hovers */
            }
            QPushButton:pressed {
                background-color: #444444;  /* Button background color when pressed */
            }
        """
        line_style = """
            QLineEdit {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
        """
        line_disabled_style = """
            QLineEdit {
                background-color: #444444;
                color: #888888;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
                color: #888888;
            }
        """

        for i in range(len(self.fan_mode_radio_buttons_names)):
            if i == mode:
                self.fan_mode_radio_buttons[i].setChecked(True)
                self.fan_mode_radio_buttons[i].setEnabled(False)
            else:
                self.fan_mode_radio_buttons[i].setChecked(False)
                self.fan_mode_radio_buttons[i].setEnabled(True)
        if mode == 0:
            self.fan_case_low_temp_minus_btn.setEnabled(True)
            self.fan_case_low_temp_plus_btn.setEnabled(True)
            self.fan_case_high_temp_minus_btn.setEnabled(True)
            self.fan_case_high_temp_plus_btn.setEnabled(True)
            self.fan_case_low_temp_minus_btn.setStyleSheet(button_style)
            self.fan_case_low_temp_plus_btn.setStyleSheet(button_style)
            self.fan_case_high_temp_minus_btn.setStyleSheet(button_style)
            self.fan_case_high_temp_plus_btn.setStyleSheet(button_style)
            self.fan_case_low_temp_input.setStyleSheet(line_style)
            self.fan_manual_slider_fan1.setEnabled(False)
            self.fan_manual_slider_fan2.setEnabled(False)
            self.fan_manual_slider_fan1.setStyleSheet(self.get_fan_manual_slider_style("#A6B4A6"))
            self.fan_manual_slider_fan2.setStyleSheet(self.get_fan_manual_slider_style("#A6B4A6"))
            self.fan_btn_edit_custom_code.setEnabled(False)
            self.fan_btn_test_coustom_code.setEnabled(False)
            self.fan_btn_edit_custom_code.setStyleSheet(button_disable_style)
            self.fan_btn_test_coustom_code.setStyleSheet(button_disable_style)
        elif mode == 1:
            self.fan_case_low_temp_minus_btn.setEnabled(False)
            self.fan_case_low_temp_plus_btn.setEnabled(False)
            self.fan_case_high_temp_minus_btn.setEnabled(False)
            self.fan_case_high_temp_plus_btn.setEnabled(False)
            self.fan_case_low_temp_minus_btn.setStyleSheet(button_disable_style)
            self.fan_case_low_temp_plus_btn.setStyleSheet(button_disable_style)
            self.fan_case_high_temp_minus_btn.setStyleSheet(button_disable_style)
            self.fan_case_high_temp_plus_btn.setStyleSheet(button_disable_style)
            self.fan_manual_slider_fan1.setEnabled(True)
            self.fan_manual_slider_fan2.setEnabled(True)
            self.fan_manual_slider_fan1.setStyleSheet(self.get_fan_manual_slider_style("#1900FF"))
            self.fan_manual_slider_fan2.setStyleSheet(self.get_fan_manual_slider_style("#09FF00"))
            self.fan_btn_edit_custom_code.setEnabled(False)
            self.fan_btn_test_coustom_code.setEnabled(False)
            self.fan_btn_edit_custom_code.setStyleSheet(button_disable_style)
            self.fan_btn_test_coustom_code.setStyleSheet(button_disable_style)
        elif mode == 2:
            self.fan_case_low_temp_minus_btn.setEnabled(False)
            self.fan_case_low_temp_plus_btn.setEnabled(False)
            self.fan_case_high_temp_minus_btn.setEnabled(False)
            self.fan_case_high_temp_plus_btn.setEnabled(False)
            self.fan_case_low_temp_minus_btn.setStyleSheet(button_disable_style)
            self.fan_case_low_temp_plus_btn.setStyleSheet(button_disable_style)
            self.fan_case_high_temp_minus_btn.setStyleSheet(button_disable_style)
            self.fan_case_high_temp_plus_btn.setStyleSheet(button_disable_style)
            self.fan_manual_slider_fan1.setEnabled(False)
            self.fan_manual_slider_fan2.setEnabled(False)
            self.fan_manual_slider_fan1.setStyleSheet(self.get_fan_manual_slider_style("#A6B4A6"))
            self.fan_manual_slider_fan2.setStyleSheet(self.get_fan_manual_slider_style("#A6B4A6"))
            self.fan_btn_edit_custom_code.setEnabled(True)
            self.fan_btn_test_coustom_code.setEnabled(True)
            self.fan_btn_edit_custom_code.setStyleSheet(button_style)
            self.fan_btn_test_coustom_code.setStyleSheet(button_style)
        else:
            self.fan_case_low_temp_minus_btn.setEnabled(False)
            self.fan_case_low_temp_plus_btn.setEnabled(False)
            self.fan_case_high_temp_minus_btn.setEnabled(False)
            self.fan_case_high_temp_plus_btn.setEnabled(False)
            self.fan_case_low_temp_minus_btn.setStyleSheet(button_disable_style)
            self.fan_case_low_temp_plus_btn.setStyleSheet(button_disable_style)
            self.fan_case_high_temp_minus_btn.setStyleSheet(button_disable_style)
            self.fan_case_high_temp_plus_btn.setStyleSheet(button_disable_style)
            self.fan_manual_slider_fan1.setEnabled(False)
            self.fan_manual_slider_fan2.setEnabled(False)
            self.fan_manual_slider_fan1.setStyleSheet(self.get_fan_manual_slider_style("#A6B4A6"))
            self.fan_manual_slider_fan2.setStyleSheet(self.get_fan_manual_slider_style("#A6B4A6"))
            self.fan_btn_edit_custom_code.setEnabled(False)
            self.fan_btn_test_coustom_code.setEnabled(False)
            self.fan_btn_edit_custom_code.setStyleSheet(button_disable_style)
            self.fan_btn_test_coustom_code.setStyleSheet(button_disable_style)

    def set_case_weight_temp(self, temp_threshold):
        """Set Case temperature thresholds"""
        self.fan_case_low_temp_input.setText(str(temp_threshold[0]))
        self.fan_case_high_temp_input.setText(str(temp_threshold[1]))
    
    def set_manual_weight_slider_value(self, speed):
        """Set PWM values in Manual mode"""
        self.fan_manual_slider_fan1.setValue(speed[0])
        self.fan_manual_slider_fan2.setValue(speed[1])
        self.fan_manual_fan1_slider_value.setText(str(speed[0]))
        self.fan_manual_fan2_slider_value.setText(str(speed[1]))

    def set_case_weight_slider_value(self, value):
        pass
    
    def set_pi_weight_slider_map(self, speed):
        pass

if __name__ == "__main__":
    from api_json import ConfigManager
    app = QApplication(sys.argv)
    app_ui_config = ConfigManager()
    screen_direction = app_ui_config.get_value('Monitor', 'screen_orientation')

    if screen_direction == 0:  
        window = FNK0107_FanTab(800, 420) 
    elif screen_direction == 1: 
        window = FNK0107_FanTab(480, 740) 

    window.show()
    sys.exit(app.exec_())