# app_ui_led.py
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton,QRadioButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class LedTab(QWidget):

    # Initialize LED control interface
    def __init__(self, width=700, height=400):
        """Initialize LED control interface"""
        super().__init__()
        # Control area
        self.led_mode_radio_buttons_names = ["Rainbow", "Breathing", "Follow", "Manual", "Custom", "Close"] # LED mode names
        self.title_label = None                     # Title label
        self.led_mode_radio_buttons = []            # Create radio button list
        self.led_lable_red_slider_label = None      # Red slider label
        self.led_lable_red_slider_value = None      # Red slider value label
        self.led_lable_green_slider_label = None    # Green slider label
        self.led_lable_green_slider_value = None    # Green slider value label
        self.led_lable_blue_slider_label = None     # Blue slider label
        self.led_lable_blue_slider_value = None     # Blue slider value label
        self.led_slider_red = None                  # Red slider
        self.led_slider_green = None                # Green slider
        self.led_slider_blue = None                 # Blue slider
        self.led_btn_save_config = None             # Save configuration button
        self.led_btn_default_config = None          # Restore default configuration button
        self.led_btn_edit_custom_code = None        # Edit custom code button
        self.led_btn_test_coustom_code = None       # Test custom code button
        # Variable area
        self.window_width = width               # Window width
        self.window_height = height             # Window height
        self.led_mode = 4                       # LED mode
        self.led_last_mode = 4                  # Last LED mode
        self.led_slider_red_value = 0           # Red slider value
        self.led_slider_green_value = 0         # Green slider value
        self.led_slider_blue_value = 0          # Blue slider value
        self.led_color_value = [0, 0, 0]        # LED color value
        self.led_process = None                 # Used to store running subprocess
        # Function area
        self.init_ui()                        # Initialize interface

        self.load_ui_events()
        self.set_led_mode(0)
        self.set_slider_control_state(False)


    # Initialize control interface
    def init_ui(self):
        """Initialize control interface"""
        # Set screen scaling factor
        self.scale_factor = 0.6
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setStyleSheet("background-color: #333333;")  # Set black background for monitoring tab
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))

        # Create two horizontal layouts, each containing 3 radio buttons for different LED mode options
        self.led_mode_hbox_layout1 = QHBoxLayout()  # First row radio button layout
        self.led_mode_hbox_layout2 = QHBoxLayout()  # Second row radio button layout
        # Create first row radio buttons (first 3)
        for i in range(3):
            radio_button = QRadioButton(self.led_mode_radio_buttons_names[i])
            radio_button.setStyleSheet("""
                QRadioButton {
                    background-color: #444444;
                    color: white;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 2px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            self.led_mode_radio_buttons.append(radio_button)
            self.led_mode_radio_buttons[i].setMinimumSize(50, 30)
            self.led_mode_hbox_layout1.addWidget(self.led_mode_radio_buttons[i])
        # Create second row radio buttons (last 3)
        for i in range(3, 6):
            radio_button = QRadioButton(self.led_mode_radio_buttons_names[i])
            radio_button.setStyleSheet("""
                QRadioButton {
                    background-color: #444444;
                    color: white;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 2px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            self.led_mode_radio_buttons.append(radio_button)
            self.led_mode_radio_buttons[i].setMinimumSize(50, 30)
            self.led_mode_hbox_layout2.addWidget(self.led_mode_radio_buttons[i])
        self.led_mode_hbox_layout1.setSpacing(10)          # Set control spacing
        self.led_mode_hbox_layout2.setSpacing(10)          # Set control spacing

        # Add title label
        self.title_label = QLabel("LED Color")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }
        """)
        self.title_label.setFixedHeight(40)
        # Create a horizontal layout
        self.title_layout = QHBoxLayout()
        self.title_layout.addWidget(self.title_label) # Add title label

        # Uniformly set style for all components
        self.slider_lable_style = """
            background-color: #444444;
            color: white;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 2px;
            font-size: 14px;
            font-weight: bold;
        """
        # Add label, slider, slider value display
        self.led_lable_red_slider_label = QLabel("Red:")
        self.led_lable_red_slider_label.setStyleSheet(self.slider_lable_style)
        self.led_lable_red_slider_label.setFixedWidth(65)
        self.led_slider_red = QSlider(Qt.Horizontal)
        self.led_slider_red.setStyleSheet("""
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
                background: red;      /* Handle color */
                width: 40px;          /* Handle width */
                height: 20px;         /* Handle height */
                margin-top: -8px;     /* Move handle up */
                margin-bottom: -8px;  /* Move handle down */
            }
        """)
        self.led_slider_red.setRange(0, 255)
        self.led_slider_red.setValue(0)
        self.led_lable_red_slider_value = QLabel("0")
        self.led_lable_red_slider_value.setStyleSheet(self.slider_lable_style)
        self.led_lable_red_slider_value.setFixedWidth(50)
        # Create a horizontal layout
        self.led_slider_red_layout = QHBoxLayout()
        self.led_slider_red_layout.addWidget(self.led_lable_red_slider_label, stretch=1)
        self.led_slider_red_layout.addWidget(self.led_slider_red, stretch=9)
        self.led_slider_red_layout.addWidget(self.led_lable_red_slider_value, stretch=1)
        self.led_slider_red_layout.setSpacing(10)
        
        # Add label, slider, slider value display
        self.led_lable_green_slider_label = QLabel("Green:")
        self.led_lable_green_slider_label.setStyleSheet(self.slider_lable_style)
        self.led_lable_green_slider_label.setFixedWidth(65)
        self.led_slider_green = QSlider(Qt.Horizontal)
        self.led_slider_green.setStyleSheet("""
            QSlider {
                border: 2px solid #444444;    /* Add external border */
                border-radius: 5px;           /* Border rounded corners */
                background-color: #333333;    /* Background color */
                padding: 2px;                /* Padding */
            }
            QSlider::groove:horizontal { 
                background: #555555;  /* Groove color */
                height: 20px;         /* Groove height */
                border-radius: 5px;   /* Groove rounded corners */
            }
            QSlider::handle:horizontal {
                background: green;    /* Handle color */
                width: 40px;          /* Handle width */
                height: 20px;         /* Handle height */
                margin-top: -8px;     /* Move handle up */
                margin-bottom: -8px;  /* Move handle down */
            }
        """)
        self.led_slider_green.setRange(0, 255)
        self.led_slider_green.setValue(0)
        self.led_lable_green_slider_value = QLabel("0")
        self.led_lable_green_slider_value.setStyleSheet(self.slider_lable_style)
        self.led_lable_green_slider_value.setFixedWidth(50)
        # Create a horizontal layout
        self.led_slider_green_layout = QHBoxLayout()
        self.led_slider_green_layout.addWidget(self.led_lable_green_slider_label, stretch=1)
        self.led_slider_green_layout.addWidget(self.led_slider_green, stretch=9)
        self.led_slider_green_layout.addWidget(self.led_lable_green_slider_value, stretch=1)
        self.led_slider_green_layout.setSpacing(10)
        
        # Add label, slider, slider value display
        self.led_lable_blue_slider_label = QLabel("Blue:")
        self.led_lable_blue_slider_label.setStyleSheet(self.slider_lable_style)
        self.led_lable_blue_slider_label.setFixedWidth(65)
        self.led_slider_blue = QSlider(Qt.Horizontal)
        self.led_slider_blue.setStyleSheet("""
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
                background: blue;    /* Handle color */
                width: 40px;          /* Handle width */
                height: 20px;         /* Handle height */
                margin-top: -8px;    /* Move handle up */
                margin-bottom: -8px; /* Move handle down */
            }
        """)
        self.led_slider_blue.setRange(0, 255)
        self.led_slider_blue.setValue(0)
        self.led_lable_blue_slider_value = QLabel("0")
        self.led_lable_blue_slider_value.setStyleSheet(self.slider_lable_style)
        self.led_lable_blue_slider_value.setFixedWidth(50)
        # Create a horizontal layout
        self.led_slider_blue_layout = QHBoxLayout()
        self.led_slider_blue_layout.addWidget(self.led_lable_blue_slider_label, stretch=1)
        self.led_slider_blue_layout.addWidget(self.led_slider_blue, stretch=9)
        self.led_slider_blue_layout.addWidget(self.led_lable_blue_slider_value, stretch=1)
        self.led_slider_blue_layout.setSpacing(10)

        # Create 4 buttons named: Save Config, Default Config, Create Task, Delete Task
        led_btn_style = """
            QPushButton {
                background-color: #444444;  /* Button background color */
                color: white;               /* Button text color */
                border: none;               /* No border */
                outline: none;              /* No outline */
                padding: 2px;               /* Button padding */
                border-radius: 5px;         /* Button rounded corners */
                font-size: 14px;            /* Font size */
                font-weight: bold;          /* Bold font */
            }
            QPushButton:hover {
                background-color: #555555;  /* Button background color when mouse hovers */
            }
            QPushButton:pressed {
                background-color: #666666;  /* Button background color when pressed */
            }
        """
        self.led_btn_default_config = QPushButton("Default")
        self.led_btn_default_config.setStyleSheet(led_btn_style)
        self.led_btn_save_config = QPushButton("Save")
        self.led_btn_save_config.setStyleSheet(led_btn_style)
        self.led_btn_edit_custom_code = QPushButton("Edit")
        self.led_btn_edit_custom_code.setStyleSheet(led_btn_style)
        self.led_btn_test_coustom_code = QPushButton("Test")
        self.led_btn_test_coustom_code.setStyleSheet(led_btn_style)

        self.btn_layout = QHBoxLayout() 
        self.btn_layout.addWidget(self.led_btn_default_config)
        self.btn_layout.addWidget(self.led_btn_save_config)
        self.btn_layout.addWidget(self.led_btn_edit_custom_code)
        self.btn_layout.addWidget(self.led_btn_test_coustom_code)
        
        # Set main layout
        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(10, 10, 10, 10)  # Set margins
        self.vbox_layout.setSpacing(10)  # Set control spacing
        self.vbox_layout.addLayout(self.led_mode_hbox_layout1)
        self.vbox_layout.addLayout(self.led_mode_hbox_layout2)
        self.vbox_layout.addLayout(self.title_layout)
        self.vbox_layout.addLayout(self.led_slider_red_layout)
        self.vbox_layout.addLayout(self.led_slider_green_layout)
        self.vbox_layout.addLayout(self.led_slider_blue_layout)
        self.vbox_layout.addLayout(self.btn_layout)

        # Set main window
        self.setLayout(self.vbox_layout)

    def load_ui_events(self):
        for i in range(len(self.led_mode_radio_buttons_names)):  
            self.led_mode_radio_buttons[i].clicked.connect(self.led_radio_clicked_event)

    def led_radio_clicked_event(self):
        """Handle LED radio button click event"""
        led_radio_mode = 0
        sender_button = self.sender()
        for i in range(len(self.led_mode_radio_buttons_names)):
            if sender_button.text() == self.led_mode_radio_buttons_names[i]:
                led_radio_mode = i
        if led_radio_mode in [0, 4, 5]: 
            self.set_slider_control_state(False)  
        else: 
            self.set_slider_control_state(True) 
        self.set_led_mode(led_radio_mode)


    # Recalculate control heights when window size changes
    def resizeEvent(self, event):
        """
        Recalculate control heights when window size changes
        """
        super().resizeEvent(event)

        # Recalculate led_ui_height
        self.led_ui_height = round((self.height() - 80) // 7)
        
        # Update maximum height of controls
        self.title_label.setMaximumHeight(self.led_ui_height)
        for i in range(len(self.led_mode_radio_buttons_names)):
            self.led_mode_radio_buttons[i].setMaximumHeight(self.led_ui_height)
        self.led_lable_red_slider_label.setMaximumHeight(self.led_ui_height)
        self.led_lable_green_slider_label.setMaximumHeight(self.led_ui_height)
        self.led_lable_blue_slider_label.setMaximumHeight(self.led_ui_height)
        self.led_lable_red_slider_value.setMaximumHeight(self.led_ui_height)
        self.led_lable_green_slider_value.setMaximumHeight(self.led_ui_height)
        self.led_lable_blue_slider_value.setMaximumHeight(self.led_ui_height)
        self.led_slider_red.setMaximumHeight(self.led_ui_height)
        self.led_slider_green.setMaximumHeight(self.led_ui_height)
        self.led_slider_blue.setMaximumHeight(self.led_ui_height)
        self.led_btn_save_config.setMaximumHeight(self.led_ui_height)
        self.led_btn_default_config.setMaximumHeight(self.led_ui_height)
        self.led_btn_edit_custom_code.setMaximumHeight(self.led_ui_height)
        self.led_btn_test_coustom_code.setMaximumHeight(self.led_ui_height)

    # Reset UI size
    def resetUiSize(self, width, height):
        self.window_width = width
        self.window_height = height
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))

    # Handle window close event
    def closeEvent(self, event):
        """Handle window close event"""
        event.accept()

    # Set LED mode
    def set_led_mode(self, mode):
        """Set LED mode"""
        for i in range(len(self.led_mode_radio_buttons_names)):
            if i == mode:
                self.led_mode_radio_buttons[i].setChecked(True)
                self.led_mode_radio_buttons[i].setEnabled(False)
            else:
                self.led_mode_radio_buttons[i].setChecked(False)
                self.led_mode_radio_buttons[i].setEnabled(True)
            if mode == 4:
                led_btn_style = """
                    QPushButton {
                        background-color: #444444;  /* Button background color */
                        color: white;               /* Button text color */
                        border: none;               /* No border */
                        outline: none;              /* No outline */
                        padding: 2px;               /* Button padding */
                        border-radius: 5px;         /* Button rounded corners */
                        font-size: 14px;            /* Font size */
                        font-weight: bold;          /* Bold font */
                    }
                    QPushButton:hover {
                        background-color: #555555;  /* Button background color when mouse hovers */
                    }
                    QPushButton:pressed {
                        background-color: #666666;  /* Button background color when pressed */
                    }
                """
                self.led_btn_edit_custom_code.setEnabled(True)
                self.led_btn_test_coustom_code.setEnabled(True)
                self.led_btn_edit_custom_code.setStyleSheet(led_btn_style)
                self.led_btn_test_coustom_code.setStyleSheet(led_btn_style)
            else:
                led_btn_style = """
                    QPushButton {
                        background-color: #444444;  /* Button background color */
                        color: #888888;             /* Button text color */
                        border: none;               /* No border */
                        outline: none;              /* No outline */
                        padding: 2px;               /* Button padding */
                        border-radius: 5px;         /* Button rounded corners */
                        font-size: 14px;            /* Font size */
                        font-weight: bold;          /* Bold font */
                    }
                    QPushButton:hover {
                        background-color: #444444;  /* Button background color when mouse hovers */
                    }
                    QPushButton:pressed {
                        background-color: #444444;  /* Button background color when pressed */
                    }
                """
                self.led_btn_edit_custom_code.setEnabled(False)
                self.led_btn_test_coustom_code.setEnabled(False)
                self.led_btn_edit_custom_code.setStyleSheet(led_btn_style)
                self.led_btn_test_coustom_code.setStyleSheet(led_btn_style)

    # Set slider color
    def set_slider_color(self, index, value):
        """Set slider color"""
        if index == 0:
            self.led_slider_red.setValue(value)
            self.led_lable_red_slider_value.setText(str(value))
        elif index == 1:
            self.led_slider_green.setValue(value)
            self.led_lable_green_slider_value.setText(str(value))
        elif index == 2:
            self.led_slider_blue.setValue(value)
            self.led_lable_blue_slider_value.setText(str(value))

    # Set title bar color
    def set_title_color(self, bg=(0, 0, 0), font=None):
        """Set title bar color"""
        # If font color is not specified, automatically select black or white based on background
        if font is None:
            # Calculate background brightness using standard brightness formula
            brightness = (bg[0] * 299 + bg[1] * 587 + bg[2] * 114) / 1000
            # If brightness is greater than 128, use black font; otherwise use white font
            font = (0, 0, 0) if brightness > 128 else (255, 255, 255)
        
        font_color = '#%02x%02x%02x' % (font[0], font[1], font[2])
        bg_color = '#%02x%02x%02x' % (bg[0], bg[1], bg[2])
        self.title_label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {font_color};
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }}
        """)

    # Set slider control state
    def set_slider_control_state(self, state):
        """Set slider control state"""
        if state:
            self.led_slider_red.setEnabled(True)
            self.led_slider_green.setEnabled(True)
            self.led_slider_blue.setEnabled(True)
            self.led_slider_red.setStyleSheet("""
                QSlider {
                    border: 2px solid #444444;    /* Add external border */
                    border-radius: 5px;           /* Border rounded corners */
                    background-color: #333333;    /* Background color */
                    padding: 2px;                /* Padding */
                }
                QSlider::groove:horizontal { 
                    background: #555555;  /* Groove color */
                    height: 20px;         /* Groove height */
                    border-radius: 5px;   /* Groove rounded corners */
                }
                QSlider::handle:horizontal {
                    background: #FF0000;  /* Handle color */
                    width: 40px;          /* Handle width */
                    height: 20px;         /* Handle height */
                    margin-top: -8px;     /* Move handle up */
                    margin-bottom: -8px;  /* Move handle down */
                }
            """)
            self.led_slider_green.setStyleSheet("""
                QSlider {
                    border: 2px solid #444444;    /* Add external border */
                    border-radius: 5px;           /* Border rounded corners */
                    background-color: #333333;    /* Background color */
                    padding: 2px;                /* Padding */
                }
                QSlider::groove:horizontal { 
                    background: #555555;  /* Groove color */
                    height: 20px;         /* Groove height */
                    border-radius: 5px;   /* Groove rounded corners */
                }
                QSlider::handle:horizontal {
                    background: #00FF00;  /* Handle color */
                    width: 40px;          /* Handle width */
                    height: 20px;         /* Handle height */
                    margin-top: -8px;     /* Move handle up */
                    margin-bottom: -8px;  /* Move handle down */
                }
            """)
            self.led_slider_blue.setStyleSheet("""
                QSlider {
                    border: 2px solid #444444;    /* Add external border */
                    border-radius: 5px;           /* Border rounded corners */
                    background-color: #333333;    /* Background color */
                    padding: 2px;                /* Padding */
                }
                QSlider::groove:horizontal { 
                    background: #555555;  /* Groove color */
                    height: 20px;         /* Groove height */
                    border-radius: 5px;   /* Groove rounded corners */
                }
                QSlider::handle:horizontal {
                    background: #0000FF;  /* Handle color */
                    width: 40px;          /* Handle width */
                    height: 20px;         /* Handle height */
                    margin-top: -8px;     /* Move handle up */
                    margin-bottom: -8px;  /* Move handle down */
                }
            """)
        else:
            self.led_slider_red.setEnabled(False)
            self.led_slider_green.setEnabled(False)
            self.led_slider_blue.setEnabled(False)
            self.led_slider_red.setStyleSheet("""
                QSlider {
                    border: 2px solid #444444;    /* Add external border */
                    border-radius: 5px;           /* Border rounded corners */
                    background-color: #333333;    /* Background color */
                    padding: 2px;                /* Padding */
                }
                QSlider::groove:horizontal { 
                    background: #555555;  /* Groove color */
                    height: 20px;         /* Groove height */
                    border-radius: 5px;   /* Groove rounded corners */
                }
                QSlider::handle:horizontal {
                    background: #880000;  /* Handle color */
                    width: 40px;          /* Handle width */
                    height: 20px;         /* Handle height */
                    margin-top: -8px;     /* Move handle up */
                    margin-bottom: -8px;  /* Move handle down */
                }
            """)
            self.led_slider_green.setStyleSheet("""
                QSlider {
                    border: 2px solid #444444;    /* Add external border */
                    border-radius: 5px;           /* Border rounded corners */
                    background-color: #333333;    /* Background color */
                    padding: 2px;                /* Padding */
                }
                QSlider::groove:horizontal { 
                    background: #555555;  /* Groove color */
                    height: 20px;         /* Groove height */
                    border-radius: 5px;   /* Groove rounded corners */
                }
                QSlider::handle:horizontal {
                    background: #008800;  /* Handle color */
                    width: 40px;          /* Handle width */
                    height: 20px;         /* Handle height */
                    margin-top: -8px;     /* Move handle up */
                    margin-bottom: -8px;  /* Move handle down */
                }
            """)
            self.led_slider_blue.setStyleSheet("""
                QSlider {
                    border: 2px solid #444444;    /* Add external border */
                    border-radius: 5px;           /* Border rounded corners */
                    background-color: #333333;    /* Background color */
                    padding: 2px;                /* Padding */
                }
                QSlider::groove:horizontal { 
                    background: #555555;  /* Groove color */
                    height: 20px;         /* Groove height */
                    border-radius: 5px;   /* Groove rounded corners */
                }
                QSlider::handle:horizontal {
                    background: #000088;  /* Handle color */
                    width: 40px;          /* Handle width */
                    height: 20px;         /* Handle height */
                    margin-top: -8px;     /* Move handle up */
                    margin-bottom: -8px;  /* Move handle down */
                }
            """)

    # Set slider value and title color
    def set_slider_slider_value(self, color):
        self.led_slider_red.setValue(color[0])
        self.led_slider_green.setValue(color[1])
        self.led_slider_blue.setValue(color[2])
        self.led_lable_red_slider_value.setText(str(color[0]))
        self.led_lable_green_slider_value.setText(str(color[1]))
        self.led_lable_blue_slider_value.setText(str(color[2]))
        self.set_title_color(color)

        
if __name__ == "__main__":
    from api_json import ConfigManager
    app = QApplication(sys.argv)
    app_ui_config = ConfigManager()
    screen_direction = app_ui_config.get_value('Monitor', 'screen_orientation')
    if screen_direction == 0:  
        window = LedTab(800, 420)
    elif screen_direction == 1: 
        window = LedTab(480, 740)
    window.show()
    sys.exit(app.exec_())