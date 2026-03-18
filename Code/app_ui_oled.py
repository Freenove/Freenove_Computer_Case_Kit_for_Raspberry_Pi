# app_ui_oled.py
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QComboBox, QGroupBox, QFrame, QPushButton
from PyQt5.QtCore import Qt

class PressableButton(QPushButton):
    """A custom push button class with a pressed state."""
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
                font-size: 14px;
                margin: 0px;
                outline: none; /* Remove focus outline */
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        self.is_pressed = False
        self.original_style = self.styleSheet()

    def mousePressEvent(self, event):
        """Mouse press event handler"""
        self.is_pressed = True
        pressed_style = """
            QPushButton {
                background-color: #333333;
                color: #cccccc;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
                font-size: 14px;
                margin: 0px;
                border-style: inset;
                outline: none; /* Remove focus outline */
            }
        """
        self.setStyleSheet(pressed_style)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Mouse release event handler"""
        self.is_pressed = False
        self.setStyleSheet(self.original_style)
        super().mouseReleaseEvent(event)

class OledTab(QWidget):
    def __init__(self, width=700, height=400):
        """Initialize OLED control interface"""
        super().__init__()
        
        # Control area
        self.screen1_checkbox = None      # Screen 1 display checkbox
        self.screen2_checkbox = None      # Screen 2 display checkbox
        self.screen3_checkbox = None      # Screen 3 display checkbox
        self.screen4_checkbox = None      # Screen 4 display checkbox
        
        # Screen 1 controls
        self.screen1_data_format_combo = None    # Screen 1 data format combo box
        self.screen1_time_format_combo = None    # Screen 1 time format combo box
        self.screen1_display_time_label = None      # Screen 1 display time label
        
        # Screen 2 controls
        self.screen2_interchange_combo = None    # Screen 2 interchange combo box
        self.screen2_display_time_label = None      # Screen 2 display time label
        
        # Screen 3 controls
        self.screen3_interchange_combo = None    # Screen 3 interchange combo box
        self.screen3_display_time_label = None      # Screen 3 display time label
        
        # Screen 4 controls
        self.screen4_interchange_combo = None    # Screen 4 interchange combo box
        self.screen4_display_time_label = None      # Screen 4 display time label

        self.screen_display_time_minus_btn = None  # Screen 4 display time minus button
        self.screen_display_time_plus_btn = None   # Screen 4 display time plus button
        
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
        self.setStyleSheet("background-color: #333333;")  # Set dark background
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))

        # Define common styles
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
                font-size: 14px;
                text-align: left; /* Changed from center to left */
            }
        """

        self.combo_style = """
            QComboBox {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px 20px 5px 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(./arrow-down.png);
            }
            QComboBox QAbstractItemView {
                text-align: center;
                background-color: #444444;
                color: white;
                selection-background-color: #555555;
            }
        """

        self.checkbox_style = """
            QCheckBox {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
                font-size: 14px;
                outline: none; /* Remove focus outline */
            }
            QCheckBox:hover {
                background-color: #555555;
            }
            QCheckBox:focus { /* Remove focus indicator */
                outline: none;
            }
        """

        # Create main group box
        self.main_groupbox = QGroupBox("OLED Settings")
        self.main_groupbox.setStyleSheet(self.groupbox_style)
        
        # Create main layout - vertical layout for 5 containers
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)  # Set margins
        self.main_layout.setSpacing(10)  # Set control spacing

        # Container 1 - Checkboxes for all screens (now left-aligned)
        self.container1 = QFrame()
        self.container1.setStyleSheet("background-color: #333333; border: 1px solid #555555; border-radius: 5px;")
        self.container1_layout = QHBoxLayout()
        self.container1_layout.setContentsMargins(5, 5, 5, 5)
        self.container1_layout.setSpacing(5)
        # Remove center alignment to make it left-aligned by default

        # Checkboxes for all screens
        self.screen1_checkbox = QCheckBox("Time")
        self.screen1_checkbox.setStyleSheet(self.checkbox_style)
        self.screen1_checkbox.setChecked(True)
        self.screen1_checkbox.setFocusPolicy(Qt.NoFocus)  # Disable focus for checkbox
        self.container1_layout.addWidget(self.screen1_checkbox)
        
        self.screen2_checkbox = QCheckBox("Usage")
        self.screen2_checkbox.setStyleSheet(self.checkbox_style)
        self.screen2_checkbox.setChecked(True)
        self.screen2_checkbox.setFocusPolicy(Qt.NoFocus)  # Disable focus for checkbox
        self.container1_layout.addWidget(self.screen2_checkbox)
        
        self.screen3_checkbox = QCheckBox("Temp")
        self.screen3_checkbox.setStyleSheet(self.checkbox_style)
        self.screen3_checkbox.setChecked(True)
        self.screen3_checkbox.setFocusPolicy(Qt.NoFocus)  # Disable focus for checkbox
        self.container1_layout.addWidget(self.screen3_checkbox)
        
        self.screen4_checkbox = QCheckBox("Fan")
        self.screen4_checkbox.setStyleSheet(self.checkbox_style)
        self.screen4_checkbox.setChecked(True)
        self.screen4_checkbox.setFocusPolicy(Qt.NoFocus)  # Disable focus for checkbox
        self.container1_layout.addWidget(self.screen4_checkbox)
        
        self.container1.setLayout(self.container1_layout)
        self.main_layout.addWidget(self.container1)

        # Container 2 - All display time labels (combining previous row 2 and 3) - left aligned
        self.container2 = QFrame()
        self.container2.setStyleSheet("background-color: #333333; border: 1px solid #555555; border-radius: 5px;")
        self.container2_layout = QHBoxLayout()
        self.container2_layout.setContentsMargins(5, 5, 5, 5)
        self.container2_layout.setSpacing(5)
        self.container2_layout.setAlignment(Qt.AlignLeft)  # Left align the labels

        self.screen1_display_time_label = QLabel("3.0s")
        self.screen1_display_time_label.setStyleSheet(self.label_style)
        self.screen1_display_time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Changed alignment to left and vertically centered
        self.container2_layout.addWidget(self.screen1_display_time_label)

        self.screen2_display_time_label = QLabel("3.0s")
        self.screen2_display_time_label.setStyleSheet(self.label_style)
        self.screen2_display_time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Changed alignment to left and vertically centered
        self.container2_layout.addWidget(self.screen2_display_time_label)

        self.screen3_display_time_label = QLabel("3.0s")
        self.screen3_display_time_label.setStyleSheet(self.label_style)
        self.screen3_display_time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Changed alignment to left and vertically centered
        self.container2_layout.addWidget(self.screen3_display_time_label)

        self.screen4_display_time_label = QLabel("3.0s")
        self.screen4_display_time_label.setStyleSheet(self.label_style)
        self.screen4_display_time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Changed alignment to left and vertically centered
        self.container2_layout.addWidget(self.screen4_display_time_label)

        self.container2.setLayout(self.container2_layout)
        self.main_layout.addWidget(self.container2)

        # Container 3 - Screen 1 combo boxes (date and time format)
        self.container3 = QFrame()
        self.container3.setStyleSheet("background-color: #333333; border: 1px solid #555555; border-radius: 5px;")
        self.container3_layout = QHBoxLayout()
        self.container3_layout.setContentsMargins(5, 5, 5, 5)
        self.container3_layout.setSpacing(5)

        self.screen1_data_format_combo = QComboBox()
        self.screen1_data_format_combo.addItems(["Year-Month-Day", "Month-Day-Year", "Day-Month-Year"])
        self.screen1_data_format_combo.setStyleSheet(self.combo_style)
        self.container3_layout.addWidget(self.screen1_data_format_combo)

        self.screen1_time_format_combo = QComboBox()
        self.screen1_time_format_combo.addItems(["24-hour Format", "12-hour Format"])
        self.screen1_time_format_combo.setStyleSheet(self.combo_style)
        self.container3_layout.addWidget(self.screen1_time_format_combo)

        self.container3.setLayout(self.container3_layout)
        self.main_layout.addWidget(self.container3)

        # Container 4 - Screen 2 and Screen 3 combo boxes
        self.container4 = QFrame()
        self.container4.setStyleSheet("background-color: #333333; border: 1px solid #555555; border-radius: 5px;")
        self.container4_layout = QHBoxLayout()
        self.container4_layout.setContentsMargins(5, 5, 5, 5)
        self.container4_layout.setSpacing(5)

        # Screen 2 combo box
        self.screen2_interchange_combo = QComboBox()
        self.screen2_interchange_combo.addItems([
            "CPU, MEM, DISK", 
            "CPU, DISK, MEM", 
            "MEM, CPU, DISK", 
            "DISK, CPU, MEM", 
            "MEM, DISK, CPU", 
            "DISK, MEM, CPU"
        ])
        self.screen2_interchange_combo.setStyleSheet(self.combo_style)
        self.container4_layout.addWidget(self.screen2_interchange_combo)

        # Screen 3 combo box
        self.screen3_interchange_combo = QComboBox()
        self.screen3_interchange_combo.addItems([
            "Pi, Case", 
            "Case, Pi"
        ])
        self.screen3_interchange_combo.setStyleSheet(self.combo_style)
        self.container4_layout.addWidget(self.screen3_interchange_combo)

        self.container4.setLayout(self.container4_layout)
        self.main_layout.addWidget(self.container4)

        # Container 5 - Screen 4 combo box and control buttons
        self.container5 = QFrame()
        self.container5.setStyleSheet("background-color: #333333; border: 1px solid #555555; border-radius: 5px;")
        self.container5_layout = QHBoxLayout()
        self.container5_layout.setContentsMargins(5, 5, 5, 5)
        self.container5_layout.setSpacing(5)

        # Screen 4 combo box (takes half the space)
        self.screen4_interchange_combo = QComboBox()
        self.screen4_interchange_combo.addItems([
            "Pi, C1, C2", 
            "Pi, C2, C1", 
            "C1, Pi, C2", 
            "C2, Pi, C1", 
            "C1, C2, Pi", 
            "C2, C1, Pi"
        ])
        self.screen4_interchange_combo.setStyleSheet(self.combo_style)
        self.container5_layout.addWidget(self.screen4_interchange_combo)

        # Control container (Sub and Add buttons) takes the other half
        self.control_container1 = QFrame()
        self.control_layout1 = QHBoxLayout()
        self.control_layout1.setSpacing(5)  # Add spacing between elements
        self.control_layout1.setContentsMargins(0, 0, 0, 0)

        self.screen_display_time_minus_btn = PressableButton("Sub")
        self.screen_display_time_minus_btn.setFocusPolicy(Qt.NoFocus)  # Disable focus for button
        self.control_layout1.addWidget(self.screen_display_time_minus_btn)

        self.screen_display_time_plus_btn = PressableButton("Add")
        self.screen_display_time_plus_btn.setFocusPolicy(Qt.NoFocus)  # Disable focus for button
        self.control_layout1.addWidget(self.screen_display_time_plus_btn)

        self.control_container1.setLayout(self.control_layout1)
        self.container5_layout.addWidget(self.control_container1)

        self.container5.setLayout(self.container5_layout)
        self.main_layout.addWidget(self.container5)

        # Set main layout to group box
        self.main_groupbox.setLayout(self.main_layout)
        
        # Set main window layout
        self.window_layout = QVBoxLayout()
        self.window_layout.addWidget(self.main_groupbox)
        self.setLayout(self.window_layout)

    def set_display_time_label(self, index, value):
        """
        Set the display time label for a specific screen
        """
        value = round(value, 1)
        if index == 0:
            self.screen1_display_time_label.setText(f"{value}s")
        elif index == 1:
            self.screen2_display_time_label.setText(f"{value}s")
        elif index == 2:
            self.screen3_display_time_label.setText(f"{value}s")
        elif index == 3:
            self.screen4_display_time_label.setText(f"{value}s")
        else:
            pass

    def set_display_time_is_enabled(self, index, state):
        """
        Enable or disable the display time label for a specific screen
        """
        if state:
            btn_style = """
                QLabel {
                    background-color: #444444;
                    color: white;              
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 5px;
                    font-weight: bold;
                    font-size: 14px;
                    text-align: left;
                }
            """
            if index == 0:
                self.screen1_display_time_label.setStyleSheet(btn_style)
            elif index == 1:
                self.screen2_display_time_label.setStyleSheet(btn_style)
            elif index == 2:
                self.screen3_display_time_label.setStyleSheet(btn_style)
            elif index == 3:
                self.screen4_display_time_label.setStyleSheet(btn_style)
            else:
                pass
        else:
            btn_style = """
                QLabel {
                    background-color: #444444;
                    color: #888888;             
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 5px;
                    font-weight: bold;
                    font-size: 14px;
                    text-align: left;
                }
            """
            if index == 0:
                self.screen1_display_time_label.setStyleSheet(btn_style)
            elif index == 1:
                self.screen2_display_time_label.setStyleSheet(btn_style)
            elif index == 2:
                self.screen3_display_time_label.setStyleSheet(btn_style)
            elif index == 3:
                self.screen4_display_time_label.setStyleSheet(btn_style)
            else:
                pass

    def resizeEvent(self, event):
        """
        Recalculate control dimensions when window size changes
        """
        super().resizeEvent(event)
        # Recalculate the dimensions for each widget
        self.adjust_size_dimensions()

    def adjust_size_dimensions(self):
        """Calculate and set the size of each control according to window size"""
        # First adjust the main group box to fit the window
        main_width = self.width() - 40  # Consider window margins
        main_height = self.height() - 40  # Consider window margins
        self.main_groupbox.setGeometry(10, 10, main_width, main_height) # Set the size of the main group box

        # Calculate available size for the group box content area (subtract group box margins)
        content_width = main_width - 20  # 10px left margin + 10px right margin
        content_height = main_height - 20  # 10px top margin + 10px bottom margin + title height

        # Calculate container size - dynamically adjust based on window height
        container_height = (content_height - 30) // 5  # 30px for spacing between containers, 5 containers (10px spacing * 4)
        container_width = content_width  # Full width for each container

        # Set minimum height for proper display
        min_container_height = 50
        container_height = max(container_height, min_container_height)

        # Set the size of each container
        self.container1.setFixedHeight(container_height)
        self.container2.setFixedHeight(container_height)
        self.container3.setFixedHeight(container_height)
        self.container4.setFixedHeight(container_height)
        self.container5.setFixedHeight(container_height)

        # Calculate internal container dimensions (subtract container margins, 5px each side)
        inner_width = container_width - 10  # 5px left margin + 5px right margin
        inner_height = container_height - 10  # 5px top margin + 5px bottom margin

        # Row 1 - All checkboxes
        self.container1.setFixedWidth(container_width)
        self.container1.setFixedHeight(container_height)
        # Distribute space evenly among the 4 checkboxes
        checkbox_width = (inner_width - 15) // 4  # Subtract spacing between checkboxes
        self.screen1_checkbox.setFixedWidth(checkbox_width)
        self.screen1_checkbox.setFixedHeight(inner_height)
        self.screen2_checkbox.setFixedWidth(checkbox_width)
        self.screen2_checkbox.setFixedHeight(inner_height)
        self.screen3_checkbox.setFixedWidth(checkbox_width)
        self.screen3_checkbox.setFixedHeight(inner_height)
        self.screen4_checkbox.setFixedWidth(checkbox_width)
        self.screen4_checkbox.setFixedHeight(inner_height)

        # Row 2 - All display time labels
        self.container2.setFixedWidth(container_width)
        self.container2.setFixedHeight(container_height)
        # Distribute space evenly among the 4 labels
        label_width = (inner_width - 15) // 4  # Subtract spacing between labels
        self.screen1_display_time_label.setFixedWidth(label_width)
        self.screen1_display_time_label.setFixedHeight(inner_height)
        self.screen2_display_time_label.setFixedWidth(label_width)
        self.screen2_display_time_label.setFixedHeight(inner_height)
        self.screen3_display_time_label.setFixedWidth(label_width)
        self.screen3_display_time_label.setFixedHeight(inner_height)
        self.screen4_display_time_label.setFixedWidth(label_width)
        self.screen4_display_time_label.setFixedHeight(inner_height)

        # Row 3 - Screen 1 combo boxes (date and time format)
        self.container3.setFixedWidth(container_width)
        self.container3.setFixedHeight(container_height)
        # Split width between the two combo boxes
        combo_spacing = 5  # 5px spacing between combo boxes
        available_combo_width = inner_width - combo_spacing  # Subtract spacing between combo boxes
        combo1_width = available_combo_width // 2
        combo2_width = available_combo_width - combo1_width
        self.screen1_data_format_combo.setFixedWidth(combo1_width)
        self.screen1_data_format_combo.setFixedHeight(inner_height)
        self.screen1_time_format_combo.setFixedWidth(combo2_width)
        self.screen1_time_format_combo.setFixedHeight(inner_height)

        # Row 4 - Screen 2 and Screen 3 combo boxes
        self.container4.setFixedWidth(container_width)
        self.container4.setFixedHeight(container_height)
        # Split width between the two combo boxes
        combo4_spacing = 5  # 5px spacing between combo boxes
        available_combo4_width = inner_width - combo4_spacing  # Subtract spacing between combo boxes
        combo4_1_width = available_combo4_width // 2
        combo4_2_width = available_combo4_width - combo4_1_width
        self.screen2_interchange_combo.setFixedWidth(combo4_1_width)
        self.screen2_interchange_combo.setFixedHeight(inner_height)
        self.screen3_interchange_combo.setFixedWidth(combo4_2_width)
        self.screen3_interchange_combo.setFixedHeight(inner_height)

        # Row 5 - Screen 4 combo box and control buttons
        self.container5.setFixedWidth(container_width)
        self.container5.setFixedHeight(container_height)
        # Divide space: combo box takes half, controls take half
        combo5_width = inner_width // 2 - 5  # Half width minus spacing
        controls_width = inner_width - combo5_width - 5  # Remaining width for controls
        self.screen4_interchange_combo.setFixedWidth(combo5_width)
        self.screen4_interchange_combo.setFixedHeight(inner_height)
        self.control_container1.setFixedWidth(controls_width)
        self.control_container1.setFixedHeight(inner_height)
        # Control buttons - split the controls area evenly
        minus_btn_width = controls_width // 2
        plus_btn_width = controls_width - minus_btn_width
        self.screen_display_time_minus_btn.setFixedWidth(minus_btn_width)
        self.screen_display_time_minus_btn.setFixedHeight(inner_height)
        self.screen_display_time_plus_btn.setFixedWidth(plus_btn_width)
        self.screen_display_time_plus_btn.setFixedHeight(inner_height)
        
    def resetUiSize(self, width, height):
        """Reset UI size"""
        self.window_width = width
        self.window_height = height
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))
        # Update the dimensions after resetting UI size
        self.adjust_size_dimensions()

    # Handle window close event
    def closeEvent(self, event):
        """Handle window close event"""
        event.accept()


if __name__ == "__main__":
    from api_json import ConfigManager
    app = QApplication(sys.argv)
    app_ui_config = ConfigManager()
    screen_direction = app_ui_config.get_value('Monitor', 'screen_orientation')
    if screen_direction == 0:  
        window = OledTab(800, 420)
    elif screen_direction == 1: 
        window = OledTab(480, 740)
    
    window.show()
    sys.exit(app.exec_())