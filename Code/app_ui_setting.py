# app_ui_setting.py
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QCheckBox
from PyQt5.QtCore import Qt

class SettingTab(QWidget):
    def __init__(self, width=700, height=400):
        """Initialize setting interface"""
        super().__init__()
        
        # Control area
        self.case_groupbox = None    # Settings group box
        self.system_groupbox = None  # System settings group box
        
        # Button controls
        self.btn_system_rotate = None         # System rotation button
        self.btn_system_follow_color = None   # System color follow button

        self.btn_led_edit = None              # LED edit button
        self.btn_led_test = None              # LED test button
        self.btn_led_switch = None            # LED task switch button
        self.btn_fan_edit = None              # Fan edit button
        self.btn_fan_test = None              # Fan test button
        self.btn_fan_switch = None            # Fan task switch button
        self.btn_oled_edit = None             # OLED edit button
        self.btn_oled_test = None             # OLED test button
        self.btn_oled_switch = None           # OLED task switch button

        self.btn_create_task = None           # Create power on/off task button
        self.btn_delete_task = None           # Delete power on/off task button
        self.btn_run_task = None              # Run power on/off task button
        self.btn_stop_task = None             # Stop power on/off task button
        
        # Variable area
        self.window_width = width
        self.window_height = height
        
        # Function area
        self.init_ui()

    def init_ui(self):
        """Initialize control interface"""
        # Set screen scaling factor
        self.scale_factor = 0.6
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setStyleSheet("background-color: black;")  # Set background color
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))

        # Create main layout
        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(10, 10, 10, 10)  # Set margins
        self.vbox_layout.setSpacing(10)  # Set control spacing

        # Define stylesheet variables
        self.groupbox_style = """
            QGroupBox {
                border: 1px solid #555555;
                background-color: #222222;
                border-radius: 5px;
                padding: 10px;
                margin-top: 1ex;  
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 0 3px; 
            }
        """
        
        self.label_style = """
            QLabel {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
                font-size: 16px;
                text-align: center;
            }
        """

        self.button_style = """
            QPushButton {
                background-color: #444444;
                color: white;
                border: none;
                outline: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px; 
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """

        self.checkbox_style = """
            QCheckBox {
                background-color: #444444;
                color: white;
                border: none;
                outline: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px; 
            }
            QCheckBox:hover {
                background-color: #555555;
            }
            QCheckBox:pressed {
                background-color: #666666;
            }
        """

        self.button_disable_style = """
            QPushButton {
                background-color: #444444;
                color: #888888;
                border: none;
                outline: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px; 
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """

        self.checkbox_disable_style = """
            QCheckBox {
                background-color: #444444;
                color: #888888;
                border: none;
                outline: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px; 
            }
            QCheckBox:hover {
                background-color: #555555;
            }
            QCheckBox:pressed {
                background-color: #666666;
            }
        """

        # First part: Case settings
        self.case_groupbox = QGroupBox("Custom Tasks")
        self.case_groupbox.setStyleSheet(self.groupbox_style)

        # Create Case settings layout
        case_layout = QVBoxLayout()       # Create vertical layout
        case_layout.setSpacing(10)        # Set control spacing

        # First row: LED settings
        led_row_layout = QHBoxLayout()    # Create horizontal layout
        led_row_layout.setSpacing(10)     # Set control spacing
        self.btn_led_switch = QCheckBox("LED Task")
        self.btn_led_switch.setStyleSheet(self.checkbox_style)
        self.btn_led_switch.setChecked(True)
        self.btn_led_edit = QPushButton("Edit")
        self.btn_led_edit.setStyleSheet(self.button_style)
        self.btn_led_test = QPushButton("Test")
        self.btn_led_test.setStyleSheet(self.button_style)
        led_row_layout.addWidget(self.btn_led_switch)
        led_row_layout.addWidget(self.btn_led_edit)
        led_row_layout.addWidget(self.btn_led_test)
        case_layout.addLayout(led_row_layout)
        
        # Second row: Fan settings
        fan_row_layout = QHBoxLayout()
        fan_row_layout.setSpacing(10)
        self.btn_fan_switch = QCheckBox("Fan Task")
        self.btn_fan_switch.setStyleSheet(self.checkbox_style)
        self.btn_fan_switch.setChecked(True)
        self.btn_fan_edit = QPushButton("Edit")
        self.btn_fan_edit.setStyleSheet(self.button_style)
        self.btn_fan_test = QPushButton("Test")
        self.btn_fan_test.setStyleSheet(self.button_style)
        fan_row_layout.addWidget(self.btn_fan_switch)
        fan_row_layout.addWidget(self.btn_fan_edit)
        fan_row_layout.addWidget(self.btn_fan_test)
        case_layout.addLayout(fan_row_layout)
        
        # Third row: OLED settings
        oled_row_layout = QHBoxLayout()
        oled_row_layout.setSpacing(10)
        self.btn_oled_switch = QCheckBox("OLED Task")
        self.btn_oled_switch.setStyleSheet(self.checkbox_style)
        self.btn_oled_switch.setChecked(True)
        self.btn_oled_edit = QPushButton("Edit")
        self.btn_oled_edit.setStyleSheet(self.button_style)
        self.btn_oled_test = QPushButton("Test")
        self.btn_oled_test.setStyleSheet(self.button_style)
        oled_row_layout.addWidget(self.btn_oled_switch)
        oled_row_layout.addWidget(self.btn_oled_edit)
        oled_row_layout.addWidget(self.btn_oled_test)
        case_layout.addLayout(oled_row_layout)
        
        # Set Case layout to self.case_groupbox
        self.case_groupbox.setLayout(case_layout)
        
        # Second part: System settings
        self.system_groupbox = QGroupBox("System Setting")
        self.system_groupbox.setStyleSheet(self.groupbox_style)
        
        # Create system settings layout
        system_layout = QHBoxLayout()
        system_layout.setSpacing(10)
        
        # Interface rotation button
        self.btn_system_rotate = QPushButton("Rotate UI")
        self.btn_system_rotate.setStyleSheet(self.button_style)
        
        # Color follow button
        self.btn_system_follow_color = QPushButton("Follow LED")
        self.btn_system_follow_color.setStyleSheet(self.button_style)
        
        # Add to layout
        system_layout.addWidget(self.btn_system_rotate)
        system_layout.addWidget(self.btn_system_follow_color)

        # Create background task buttons
        self.btn_create_task = QPushButton("Create Service")
        self.btn_create_task.setStyleSheet(self.button_style)
        
        # Delete background task button
        self.btn_delete_task = QPushButton("Delete Service")
        self.btn_delete_task.setStyleSheet(self.button_style)
        
        # Run background task button
        self.btn_run_task = QPushButton("Run Tasks")
        self.btn_run_task.setStyleSheet(self.button_style)
        
        # Stop background task button
        self.btn_stop_task = QPushButton("Stop Tasks")
        self.btn_stop_task.setStyleSheet(self.button_style)
        
        # Add to layout
        task_layout_1 = QHBoxLayout()
        task_layout_1.setSpacing(10)
        task_layout_2 = QHBoxLayout()
        task_layout_2.setSpacing(10)
        task_layout_1.addWidget(self.btn_create_task)
        task_layout_1.addWidget(self.btn_delete_task)
        task_layout_2.addWidget(self.btn_run_task)
        task_layout_2.addWidget(self.btn_stop_task)
        
        task_vbox_layout = QVBoxLayout() 
        task_vbox_layout.addLayout(system_layout)
        task_vbox_layout.addLayout(task_layout_1)
        task_vbox_layout.addLayout(task_layout_2)
        task_vbox_layout.setStretch(0, 1)
        task_vbox_layout.setStretch(1, 1)
        task_vbox_layout.setStretch(2, 1)

        # Set system settings layout
        self.system_groupbox.setLayout(task_vbox_layout)
        
        # Add all group boxes to main layout
        self.vbox_layout.addWidget(self.case_groupbox)
        self.vbox_layout.addWidget(self.system_groupbox)
        
        # Set main window
        self.setLayout(self.vbox_layout)

    def set_system_settings_button_state(self, state):
        if state is False:
            self.btn_create_task.setEnabled(True)
            self.btn_create_task.setStyleSheet(self.button_style)
            self.btn_delete_task.setEnabled(False)
            self.btn_delete_task.setStyleSheet(self.button_disable_style)
            self.btn_run_task.setEnabled(False)
            self.btn_run_task.setStyleSheet(self.button_disable_style)
            self.btn_stop_task.setEnabled(False)
            self.btn_stop_task.setStyleSheet(self.button_disable_style)
            self.btn_led_switch.setEnabled(False)
            self.btn_led_switch.setStyleSheet(self.checkbox_disable_style)
            self.btn_fan_switch.setEnabled(False)
            self.btn_fan_switch.setStyleSheet(self.checkbox_disable_style)
            self.btn_oled_switch.setEnabled(False)
            self.btn_oled_switch.setStyleSheet(self.checkbox_disable_style)
            self.btn_led_edit.setEnabled(True)
            self.btn_led_edit.setStyleSheet(self.button_style)
            self.btn_fan_edit.setEnabled(True)
            self.btn_fan_edit.setStyleSheet(self.button_style)
            self.btn_oled_edit.setEnabled(True)
            self.btn_oled_edit.setStyleSheet(self.button_style)
            self.btn_led_test.setEnabled(True)
            self.btn_led_test.setStyleSheet(self.button_style)
            self.btn_fan_test.setEnabled(True)
            self.btn_fan_test.setStyleSheet(self.button_style)
            self.btn_oled_test.setEnabled(True)
            self.btn_oled_test.setStyleSheet(self.button_style)
        else:
            self.btn_create_task.setEnabled(False)
            self.btn_create_task.setStyleSheet(self.button_disable_style)
            self.btn_delete_task.setEnabled(True)
            self.btn_delete_task.setStyleSheet(self.button_style)
            self.btn_run_task.setEnabled(True)
            self.btn_run_task.setStyleSheet(self.button_style)
            self.btn_stop_task.setEnabled(False)
            self.btn_stop_task.setStyleSheet(self.button_disable_style)
            self.btn_led_switch.setEnabled(True)
            self.btn_led_switch.setStyleSheet(self.checkbox_style)
            self.btn_fan_switch.setEnabled(True)
            self.btn_fan_switch.setStyleSheet(self.checkbox_style)
            self.btn_oled_switch.setEnabled(True)
            self.btn_oled_switch.setStyleSheet(self.checkbox_style)
            self.btn_led_edit.setEnabled(False)
            self.btn_led_edit.setStyleSheet(self.button_disable_style)
            self.btn_fan_edit.setEnabled(False)
            self.btn_fan_edit.setStyleSheet(self.button_disable_style)
            self.btn_oled_edit.setEnabled(False)
            self.btn_oled_edit.setStyleSheet(self.button_disable_style)
            self.btn_led_test.setEnabled(False)
            self.btn_led_test.setStyleSheet(self.button_disable_style)
            self.btn_fan_test.setEnabled(False)
            self.btn_fan_test.setStyleSheet(self.button_disable_style)
            self.btn_oled_test.setEnabled(False)
            self.btn_oled_test.setStyleSheet(self.button_disable_style)
            
    def set_custom_task_led_button_state(self, is_exist_on_rpi, state):
        """Set custom task LED button state"""
        if is_exist_on_rpi:
            if state:
                self.btn_led_edit.setEnabled(False)
                self.btn_led_edit.setStyleSheet(self.button_disable_style)
                self.btn_led_test.setEnabled(False)
                self.btn_led_test.setStyleSheet(self.button_disable_style)
            else:
                self.btn_led_edit.setEnabled(True)
                self.btn_led_edit.setStyleSheet(self.button_style)
                self.btn_led_test.setEnabled(True)
                self.btn_led_test.setStyleSheet(self.button_style)
                
    def set_custom_task_fan_button_state(self, is_exist_on_rpi, state):
        """Set custom task fan button state"""
        if is_exist_on_rpi:
            if state:
                self.btn_fan_edit.setEnabled(False)
                self.btn_fan_edit.setStyleSheet(self.button_disable_style)
                self.btn_fan_test.setEnabled(False)
                self.btn_fan_test.setStyleSheet(self.button_disable_style)
            else:
                self.btn_fan_edit.setEnabled(True)
                self.btn_fan_edit.setStyleSheet(self.button_style)
                self.btn_fan_test.setEnabled(True)
                self.btn_fan_test.setStyleSheet(self.button_style)
                
    def set_custom_task_oled_button_state(self, is_exist_on_rpi, state):
        """Set custom task OLED button state"""
        if is_exist_on_rpi:
            if state:
                self.btn_oled_edit.setEnabled(False)
                self.btn_oled_edit.setStyleSheet(self.button_disable_style)
                self.btn_oled_test.setEnabled(False)
                self.btn_oled_test.setStyleSheet(self.button_disable_style)
            else:
                self.btn_oled_edit.setEnabled(True)
                self.btn_oled_edit.setStyleSheet(self.button_style)
                self.btn_oled_test.setEnabled(True)
                self.btn_oled_test.setStyleSheet(self.button_style) 

    def set_run_and_stop_button_state(self, is_exist_on_rpi, state):
        """Set run and stop button state"""
        if is_exist_on_rpi:
            if state is False:
                self.btn_run_task.setEnabled(True)
                self.btn_run_task.setStyleSheet(self.button_style)
                self.btn_stop_task.setEnabled(False)
                self.btn_stop_task.setStyleSheet(self.button_disable_style)
            else:
                self.btn_run_task.setEnabled(False)
                self.btn_run_task.setStyleSheet(self.button_disable_style)
                self.btn_stop_task.setEnabled(True)
                self.btn_stop_task.setStyleSheet(self.button_style)

    def resizeEvent(self, event):
        """
        Recalculate control heights when window size changes
        """
        super().resizeEvent(event)
        # Recalculate ui_height
        groupbox_height = round((self.height() - 30) // 2)
        self.case_groupbox.setMaximumHeight(groupbox_height)
        self.system_groupbox.setMaximumHeight(groupbox_height)

        self.ui_groupbox_case_height = round((groupbox_height-40)//3)

        self.btn_led_edit.setMaximumHeight(self.ui_groupbox_case_height)
        self.btn_led_test.setMaximumHeight(self.ui_groupbox_case_height)
        self.btn_led_switch.setMaximumHeight(self.ui_groupbox_case_height)
        self.btn_fan_edit.setMaximumHeight(self.ui_groupbox_case_height)
        self.btn_fan_test.setMaximumHeight(self.ui_groupbox_case_height)
        self.btn_fan_switch.setMaximumHeight(self.ui_groupbox_case_height)
        self.btn_oled_edit.setMaximumHeight(self.ui_groupbox_case_height)
        self.btn_oled_test.setMaximumHeight(self.ui_groupbox_case_height)
        self.btn_oled_switch.setMaximumHeight(self.ui_groupbox_case_height)

        self.ui_groupbox_system_height = round((groupbox_height-40)//3)
        self.btn_system_rotate.setMaximumHeight(self.ui_groupbox_system_height)
        self.btn_system_follow_color.setMaximumHeight(self.ui_groupbox_system_height)
        self.btn_create_task.setMaximumHeight(self.ui_groupbox_system_height)
        self.btn_delete_task.setMaximumHeight(self.ui_groupbox_system_height)
        self.btn_run_task.setMaximumHeight(self.ui_groupbox_system_height)
        self.btn_stop_task.setMaximumHeight(self.ui_groupbox_system_height)

    def resetUiSize(self, width, height):
        """Reset UI size"""
        self.window_width = width
        self.window_height = height
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))


if __name__ == "__main__":
    from api_json import ConfigManager
    app = QApplication(sys.argv)
    app_ui_config = ConfigManager()
    screen_direction = app_ui_config.get_value('Monitor', 'screen_orientation')
    if screen_direction == 0:  
        window = SettingTab(800, 420)
    elif screen_direction == 1: 
        window = SettingTab(480, 740)
    
    window.show()
    sys.exit(app.exec_())