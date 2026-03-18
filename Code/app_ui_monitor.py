# app_ui_monitor.py
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QApplication, QLabel
from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QBrush

class CircleProgressWidget(QWidget):
    """Circular progress bar control class implemented using PyQt"""
    def __init__(self, parent=None, size=100, position=(0, 0),
                 colors=('#4a90e2', '#000000'), progress_width=10):
        """
        Initialize circular progress bar control

        Args:
            parent: Parent container
            size: Control size (same width and height)
            position: Coordinates in parent container (x, y)
            colors: Ring color tuple (progress color, background color)
            progress_width: Ring thickness
        """
        super().__init__(parent)
        self.setFixedSize(size, size)  # Set fixed size
        self.move(position[0], position[1])  # Set position

        self.progress_color = QColor(colors[0])  # Progress color
        self.bg_color = QColor(colors[1])  # Background color
        self.progress_width = progress_width  # Ring thickness
        self.percentage = 0  # Current progress percentage
        self.label_text = ""  # Label text
        self.display_text = None  # Display text
        self.label_color = QColor('#FFFFFF')  # Label text color, default white
        self.display_text_color = QColor('#FFFFFF')  # Display text color, default white

    def paintEvent(self, event):
        """Paint event handler - responsible for drawing the appearance of the circular progress bar"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Enable antialiasing
        painter.setRenderHint(QPainter.TextAntialiasing)  # Text antialiasing

        # Calculate drawing area - add top margin to avoid occlusion
        margin = 8  # Add margin to avoid occlusion
        rect = QRectF(margin, margin,
                      self.width() - 2 * margin,
                      self.height() - 2 * margin)

        # Draw background ring
        pen = QPen(self.bg_color, self.progress_width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawEllipse(rect)

        # Draw progress arc
        if self.percentage > 0:
            pen.setColor(self.progress_color)
            painter.setPen(pen)
            span_angle = int(360 * 16 * self.percentage / 100)
            painter.drawArc(rect, 90 * 16, -span_angle)  # Draw from top

        # Draw center text (percentage)
        painter.setPen(self.display_text_color)  # Use settable text color
        font = QFont('Arial', max(8, int(self.height() * 0.12)))
        font.setBold(True)
        painter.setFont(font)

        if self.display_text is not None:
            text = self.display_text
        else:
            text = f"{self.percentage:.1f}%"  # Display percentage

        painter.drawText(rect, Qt.AlignCenter, text)

        # Draw label text (if exists) - below percentage
        if self.label_text:
            painter.setPen(self.label_color)  # Use settable label color
            font.setBold(False)
            font.setPointSize(max(6, int(self.height() * 0.08)))
            painter.setFont(font)

            # Calculate label position - below center text
            label_rect = QRectF(
                rect.x(),
                rect.y() + rect.height() * 0.5,  # Below center text
                rect.width(),
                rect.height() * 0.3
            )
            painter.drawText(label_rect, Qt.AlignCenter, self.label_text)

    def draw_progress(self, percentage, label="", display_text=None, label_color=QColor('#FFFFFF'),
                      display_text_color=QColor('#FFFFFF')):
        """
        Update progress bar display

        Args:
            percentage: Progress percentage (0-100)
            label: Label text
            display_text: Custom display text
            label_color: Label text color
            display_text_color: Display text color
        """
        self.percentage = max(0, min(100, percentage))  # Limit percentage between 0-100
        self.label_text = label
        self.display_text = display_text
        self.label_color = label_color
        self.display_text_color = display_text_color
        self.update()  # Trigger redraw

    def set_position(self, x, y):
        """Set control position"""
        self.move(x, y)


class MonitoringTab(QWidget):
    def __init__(self, width=700, height=400):
        super().__init__()
        # Control area
        self.progress_widgets = []
        # Variable area
        self.window_width = width     # Window width
        self.window_height = height   # Window height
        self.color_combinations = [
            ('#FF6B6B', '#FFD1D1'),  # Red
            ('#4ECDC4', '#D1F0EE'),  # Teal
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
            "RPi PWM",        # Raspberry Pi fan PWM
            "Case PWM1",     # Case PWM1
            "Case PWM2"      # Case PWM2
        ]

        # Function area
        self.init_ui()                # Initialize interface
        
    def init_ui(self):
        # Set screen scaling factor
        self.scale_factor = 0.6
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setStyleSheet("background-color: #333333;")  # Set black background for monitoring tab
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))
        
        self.grid_layout = QGridLayout() # Create grid layout
        # Determine grid arrangement based on aspect ratio
        if self.window_width >= self.window_height:
            self.rows = 2
            self.cols = 4
        else:
            self.rows = 4
            self.cols = 2
        # Calculate appropriate control size based on window dimensions
        self.widget_size = min(
            (self.window_width - 35) // self.cols,  # Consider left and right margins
            (self.window_height - 70) // self.rows # Consider top and bottom margins and other UI elements
        )
        # Ensure minimum size
        self.widget_size = max(70, self.widget_size)
        # Create 8 progress widgets with calculated size
        for i in range(8):
            row = i // self.cols
            col = i % self.cols
            progress_widget = CircleProgressWidget(
                size=self.widget_size,
                colors=(self.color_combinations[i][0], self.color_combinations[i][1]),
                progress_width=10
            )
            progress_widget.draw_progress(0, self.metric_labels[i])
            self.grid_layout.addWidget(progress_widget, row, col)
            self.progress_widgets.append(progress_widget)
        self.grid_layout.setColumnStretch(0, 1)      # Equal column widths
        self.grid_layout.setColumnStretch(1, 1)      # Equal column widths
        self.grid_layout.setRowStretch(0, 1)         # Equal row heights
        self.grid_layout.setRowStretch(1, 1)         # Equal row heights
        self.grid_layout.setContentsMargins(0, 0, 0, 5)

        self.vbox_layout = QVBoxLayout()             # Create vertical layout
        self.vbox_layout.addLayout(self.grid_layout) # Add grid layout to vertical layout
        self.setLayout(self.vbox_layout)             # Set vertical layout as window layout

    def closeEvent(self, event):
        """Handle window close event"""
        event.accept()

    def setCircleProgressValue(self, index, percentage, callword, display_value):
        self.progress_widgets[index].draw_progress(percentage, callword, display_value)

    def setCircleProgressColor(self, index, color_combinations=('#FF6B6B', '#444444')):
        self.progress_widgets[index].progress_color =  QColor(color_combinations[0])
        self.progress_widgets[index].bg_color = QColor(color_combinations[1])
        self.progress_widgets[index].update()

    def setDefaultCircleProgressColor(self):
        for i in range(len(self.color_combinations)):
            self.setCircleProgressColor(i, self.color_combinations[i])

    def resetUiSize(self, width, height):
        self.window_width = width
        self.window_height = height
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))

    def reloadUi(self):
        """Reload UI function"""
        # Update window dimensions
        self.window_width = self.width()
        self.window_height =  self.height()

        # Recalculate rows and columns
        if self.window_width >= self.window_height:
            self.rows = 2
            self.cols = 4
        else:
            self.rows = 4
            self.cols = 2
        
        # Recalculate control size
        self.widget_size = min(
            (self.window_width - 35) // self.cols,
            (self.window_height - 70) // self.rows
        )
        self.widget_size = max(70, self.widget_size)
        
        # Reset control size and position
        for i in range(8):
            row = i // self.cols
            col = i % self.cols
            self.progress_widgets[i].setFixedSize(self.widget_size, self.widget_size)
            self.grid_layout.addWidget(self.progress_widgets[i], row, col)

    def resizeEvent(self, event):
        """Handle window resize event"""
        super().resizeEvent(event)
        self.reloadUi()

    def keyPressEvent(self, event):
        """Handle keyboard key press events"""
        # Check if Ctrl+C is pressed
        if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            self.close()  # Trigger window close
        else:
            super().keyPressEvent(event)  # Call parent class keyboard event handler


# Program entry point
if __name__ == "__main__":
    import time
    from api_json import ConfigManager
    app = QApplication(sys.argv)
    app_ui_config = ConfigManager()
    screen_direction = app_ui_config.get_value('Monitor', 'screen_orientation')
    if screen_direction == 0:  
        window = MonitoringTab(800, 420)
    elif screen_direction == 1: 
        window = MonitoringTab(480, 740)
    window.show()

    window.setCircleProgressColor(0, ['#FF0000', '#444444'])
    window.setCircleProgressColor(1, ['#00FF00', '#444444'])
    window.setCircleProgressColor(2, ['#0000FF', '#444444'])
    window.setCircleProgressColor(3, ['#FFFF00', '#444444'])
    window.setCircleProgressColor(4, ['#FF00FF', '#444444'])
    window.setCircleProgressColor(5, ['#00FFFF', '#444444'])
    window.setCircleProgressColor(6, ['#FF6B6B', '#444444'])
    window.setCircleProgressColor(7, ['#6B6BFF', '#444444'])
    window.setCircleProgressValue(0, 12, "UI 1", "12%")
    window.setCircleProgressValue(1, 24, "UI 2", "24%")
    window.setCircleProgressValue(2, 36, "UI 3", "36%")
    window.setCircleProgressValue(3, 48, "UI 4", "48%")
    window.setCircleProgressValue(4, 60, "UI 5", "60%")
    window.setCircleProgressValue(5, 72, "UI 6", "72%")
    window.setCircleProgressValue(6, 84, "UI 7", "84%")
    window.setCircleProgressValue(7, 96, "UI 8", "96%")

    sys.exit(app.exec_())