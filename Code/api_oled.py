from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import time
import os
import shutil
import math

class OLED:
    def __init__(self, bus_number=1, i2c_address=0x3C, rotate_angle=0):
        """
        Initialize OLED display
        Args:
            bus_number: I2C bus number, default is 1
            i2c_address: I2C device address, default is 0x3C
            rotate_angle: Rotation angle, optional 0, 90, 180, 270, default is 0
        """
        # Initialize I2C interface and OLED display
        self.bus_number = bus_number
        self.i2c_address = i2c_address
        self.rotate_angle = self._angle_to_rotate_param(rotate_angle)
        self.serial = i2c(port=self.bus_number, address=self.i2c_address)
        # Use ssd1306 constructor's rotate parameter
        self.device = ssd1306(self.serial, rotate=self.rotate_angle)
        self.width = 128
        self.height = 64
        
        # Create initial buffer (now matching device dimensions)
        self._create_buffer()
        self.default_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" 
        self.default_font_size = 16
        self.font = ImageFont.load_default()

    def _angle_to_rotate_param(self, angle):
        """
        Convert angle to rotation parameter required by luma.oled library
        Args:
            angle: Angle value, must be one of 0, 90, 180, 270
        Returns:
            Corresponding rotation parameter (0, 1, 2, 3)
        """
        angle_map = {0: 0, 90: 1, 180: 2, 270: 3}
        if angle not in angle_map:
            raise ValueError("Angle must be 0, 90, 180, or 270")
        return angle_map[angle]

    def _create_buffer(self):
        """
        Create buffer matching device dimensions
        """
        # Create buffer matching actual device dimensions
        self.buffer = Image.new('1', (self.device.width, self.device.height))
        self.draw = ImageDraw.Draw(self.buffer)

    def set_rotation(self, angle):
        """
        Set rotation by recreating device
        Args:
            angle: Rotation angle, must be one of 0, 90, 180, 270
        """
        # Convert angle to format required by luma.oled
        rotate_param = self._angle_to_rotate_param(angle)
        self.rotate_angle = angle  # Save original angle value
        # Recreate device with new rotation parameter
        self.device = ssd1306(self.serial, rotate=rotate_param)
        # Recreate buffer to match new dimensions
        self._create_buffer()

    def show(self):
        """
        Display buffer content on OLED screen
        """
        self.device.display(self.buffer)

    def clear(self):
        """
        Clear buffer content
        """
        self._create_buffer()

    def close(self):
        """
        Close I2C bus
        """
        pass  # luma.oled library doesn't require explicit I2C bus closing

    def draw_point(self, xy, fill=None):
        """
        Draw a point in buffer
        Args:
            xy: Point coordinates (x, y)
            fill: Fill color
        """
        self.draw.point(xy, fill=fill)

    def draw_line(self, xy, fill=None):
        """
        Draw a line in buffer
        Args:
            xy: Line start and end coordinates ((x1, y1), (x2, y2))
            fill: Fill color
        """
        self.draw.line(xy, fill=fill)

    def draw_rectangle(self, xy, outline=None, fill=None):
        """
        Draw a rectangle in buffer
        Args:
            xy: Rectangle diagonal coordinates ((x1, y1), (x2, y2))
            outline: Border color
            fill: Fill color
        """
        self.draw.rectangle(xy, outline=outline, fill=fill)

    def draw_ellipse(self, xy, outline=None, fill=None):
        """
        Draw an ellipse in buffer
        Args:
            xy: Ellipse bounding rectangle diagonal coordinates ((x1, y1), (x2, y2))
            outline: Border color
            fill: Fill color
        """
        self.draw.ellipse(xy, outline=outline, fill=fill)

    def draw_circle(self, xy, radius, outline=None, fill=None):
        """
        Draw a circle in buffer
        Args:
            xy: Circle center coordinates (x, y)
            radius: Circle radius
            outline: Border color
            fill: Fill color
        """
        self.draw.ellipse((xy[0] - radius, xy[1] - radius, xy[0] + radius, xy[1] + radius), outline=outline, fill=fill)

    def draw_arc(self, xy, start, end, fill=None, width=1):
        """
        Draw an arc in buffer
        Args:
            xy: Arc ellipse bounding rectangle diagonal coordinates ((x1, y1), (x2, y2))
            start: Start angle
            end: End angle
            fill: Fill color
            width: Line width
        """
        self.draw.arc(xy, start, end, fill=fill, width=width)

    def draw_polygon(self, xy, outline=None, fill=None):
        """
        Draw a polygon in buffer
        Args:
            xy: Polygon vertex coordinates list
            outline: Border color
            fill: Fill color
        """
        self.draw.polygon(xy, outline=outline, fill=fill)

    def draw_text(self, text, position=((0, 0), (128, 64)), directory="center", offset=(0,0), font_size=None):
        """
        Display text in buffer
        Args:
            text: Text to display
            position: Text display area ((x1, y1), (x2, y2)), top-left and bottom-right coordinates
            directory: Text alignment ("center", "left", "right")
            offset: Text offset (x, y)
            font_size: Font size
        """
        if font_size is None:
            font = self.font
        else:
            font = ImageFont.truetype(self.default_font_path, font_size)
        
        # Parse position parameters
        start_xy, end_xy = position
        x1, y1 = start_xy
        x2, y2 = end_xy
        
        # Get text dimensions
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate text drawing position
        if directory == "center":
            # Center alignment
            text_x = x1 + (x2 - x1 - text_width) // 2 + offset[0]
            text_y = y1 + offset[1]
        elif directory == "left":
            # Left alignment
            text_x = x1 + offset[0]
            text_y = y1 + offset[1]
        elif directory == "right":
            # Right alignment
            text_x = x2 - text_width + offset[0]
            text_y = y1 + offset[1]
        else:
            # Default center
            text_x = x1 + (x2 - x1 - text_width) // 2 + offset[0]
            text_y = y1 + offset[1]
        
        # Draw text
        self.draw.text((text_x, text_y), text, font=font, fill="white")

    def draw_image(self, image_path, position=(0, 0), resize=None):
        """
        Display image in buffer
        Args:
            image_path: Image file path
            position: Image display position (x, y)
            resize: Resize image (width, height)
        """
        try:
            image = Image.open(image_path).convert('1')
            if resize is not None:
                image = image.resize(resize, Image.LANCZOS)
            else:
                image = image.resize((self.device.width, self.device.height), Image.LANCZOS)
            self.buffer.paste(image, position)
        except FileNotFoundError:
            print(f"Error: File not found - {image_path}")
        except Exception as e:
            print(f"Error displaying image: {e}")
   
    def draw_gif(self, gif_path, position=(0, 0), resize=None, center=True):
        """
        Display GIF animation
        Args:
            gif_path: GIF file path
            position: GIF display position (x, y)
            resize: Resize GIF (width, height)
            center: Whether to center display
        """
        temp_folder = "temp"
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        try:
            gif = Image.open(gif_path)
            frames = []
            frame_delays = []
            for frame in ImageSequence.Iterator(gif):
                delay = frame.info.get('duration', 100) / 1000.0
                frame_delays.append(delay)
                width, height = frame.size
                
                # Convert frame to monochrome image
                frame = frame.convert('L').convert('1')
                
                # Process image dimensions - scale proportionally
                if resize is not None:
                    # Scale image proportionally
                    target_width, target_height = resize
                    frame_ratio = width / height
                    target_ratio = target_width / target_height
                    
                    if frame_ratio > target_ratio:
                        # Scale by width
                        new_width = target_width
                        new_height = int(target_width / frame_ratio)
                    else:
                        # Scale by height
                        new_height = target_height
                        new_width = int(target_height * frame_ratio)
                    
                    frame = frame.resize((new_width, new_height), Image.LANCZOS)
                elif not center:
                    # Only scale to screen size when not centering and no resize specified
                    screen_width, screen_height = self.device.width, self.device.height
                    frame_ratio = width / height
                    screen_ratio = screen_width / screen_height
                    
                    if frame_ratio > screen_ratio:
                        # Scale by width
                        new_width = screen_width
                        new_height = int(screen_width / frame_ratio)
                    else:
                        # Scale by height
                        new_height = screen_height
                        new_width = int(screen_height * frame_ratio)
                    
                    frame = frame.resize((new_width, new_height), Image.LANCZOS)
                
                frame_path = os.path.join(temp_folder, f"frame_{len(frames)}.png")
                frame.save(frame_path)
                frames.append(frame_path)
                
            # Display each frame
            for frame_path, delay in zip(frames, frame_delays):
                # Clear buffer
                self.clear()
                
                # Load frame image
                frame_image = Image.open(frame_path).convert('1')
                frame_width, frame_height = frame_image.size
                
                # Calculate display position
                if center:
                    # Center display
                    x = (self.device.width - frame_width) // 2
                    y = (self.device.height - frame_height) // 2
                    display_position = (x, y)
                else:
                    # Use specified position
                    display_position = position
                    
                # Paste image to buffer
                self.buffer.paste(frame_image, display_position)
                
                # Display
                self.show()
                
                # Delay
                if delay > 0.02:  # Minimum delay 0.02 seconds
                    time.sleep(delay)
                else:
                    time.sleep(0.1)
                    
        except FileNotFoundError:
            print(f"Error: File not found - {gif_path}")
        except Exception as e:
            print(f"Error displaying GIF: {e}")
        finally:
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)

    def save_buffer_to_image(self, image_path="saved_image.png"):
        """
        Save buffer content to image file
        Args:
            image_path: Save image file path
        """
        self.buffer.save(image_path) 

    # Progress bar with percentage
    def draw_progress_bar(self, start_xy, end_xy, percentage, outline=None, fill=None):
        """
        Draw a progress bar in buffer
        Args:
            start_xy: Progress bar start position (x, y)
            end_xy: Progress bar end position (x, y)
            percentage: Progress percentage (0.0 to 100.0)
            outline: Progress bar border color
            fill: Progress bar fill color
        """
        # Ensure percentage is within valid range
        percentage = max(0, min(100, percentage))
        
        # Calculate progress bar width and height
        bar_width = end_xy[0] - start_xy[0]
        bar_height = end_xy[1] - start_xy[1]
        
        # Draw progress bar background box
        self.draw.rectangle((start_xy[0], start_xy[1], end_xy[0], end_xy[1]), outline=outline or "white")
        
        # Calculate filled portion width
        fill_width = int(bar_width * percentage / 100.0)
        
        # Draw filled portion
        if fill_width > 0:
            self.draw.rectangle(
                (start_xy[0], start_xy[1], start_xy[0] + fill_width, end_xy[1]), 
                fill=fill or "white"
            )

    # Circle with percentage
    def draw_circle_with_percentage(self, position, radius, percentage, outline=None, fill=None):
        """
        Draw a circle with percentage sector fill
        Args:
            position: Circle center coordinates (x, y)
            radius: Circle radius
            percentage: Fill percentage (0.0 to 100.0)
            outline: Circle border color
            fill: Sector fill color
        """
        # Ensure percentage is numeric type
        percentage = float(percentage)
        
        # Ensure percentage is within valid range
        percentage = max(0.5, min(100.0, percentage))
        
        # Calculate percentage corresponding angle (0 to 360 degrees)
        angle = (percentage / 100.0) * 360.0
        
        # Draw complete circle border
        if outline is not None or (outline is None and fill is None):
            self.draw_circle(position, radius, outline=outline or "white", fill=None)
        
        # If percentage > 0 and fill color specified, draw sector
        if percentage > 0 and fill is not None:
            # Calculate circle bounding box
            bbox = (position[0] - radius, position[1] - radius, 
                    position[0] + radius, position[1] + radius)
            
            # Draw sector (pie slice)
            self.draw.pieslice(bbox, start=0, end=angle, fill=fill)
            
            # If percentage < 100, redraw circle border to cover possible artifacts
            if percentage < 100.0 and (outline is not None or fill is not None):
                self.draw_circle(position, radius, outline=outline or "white", fill=None)
        elif percentage > 0.0 and fill is None:
            # If only percentage specified but no fill color, use default fill
            bbox = (position[0] - radius, position[1] - radius, 
                    position[0] + radius, position[1] + radius)
            self.draw.pieslice(bbox, start=0, end=angle, fill="white")

    # Semicircle with percentage
    def draw_semicircle_with_percentage(self, position, radius, percentage, orientation="top", outline=None, fill=None):
        """
        Draw a semicircle with percentage sector fill
        Args:
            position: Circle center coordinates (x, y)
            radius: Circle radius
            percentage: Fill percentage (0.0 to 100.0)
            orientation: Semicircle direction, optional "top"(upper semicircle), "bottom"(lower semicircle), "left"(left semicircle), "right"(right semicircle)
            outline: Semicircle border color
            fill: Sector fill color
        """
        # Determine start and end angles
        if orientation == "top":
            start_angle = 180
            end_angle = 360
        elif orientation == "bottom":
            start_angle = 0
            end_angle = 180
        elif orientation == "left":
            start_angle = 90
            end_angle = 270
        elif orientation == "right":
            start_angle = 270
            end_angle = 450  # Or -90 to 90
        else:
            raise ValueError("Direction must be 'top', 'bottom', 'left', or 'right'")
        
        # Draw semicircle border
        if outline is not None or (outline is None and fill is None):
            # Calculate semicircle bounding box
            bbox = (position[0] - radius, position[1] - radius, 
                    position[0] + radius, position[1] + radius)
            # Draw semicircle arc
            self.draw.arc(bbox, start=start_angle, end=end_angle, fill=outline or "white", width=1)
            
            # Draw diameter line according to direction
            if orientation == "top" or orientation == "bottom":
                self.draw.line([(position[0] - radius, position[1]), 
                            (position[0] + radius, position[1])], 
                            fill=outline or "white")
            else:  # left or right
                self.draw.line([(position[0], position[1] - radius), 
                            (position[0], position[1] + radius)], 
                            fill=outline or "white")
        
        # Calculate fill angle
        fill_angle_range = end_angle - start_angle
        fill_end_angle = start_angle + (percentage / 100.0) * fill_angle_range
        
        # If percentage > 0 and fill color specified, draw sector
        if percentage > 0 and fill is not None:
            # Calculate semicircle bounding box
            bbox = (position[0] - radius, position[1] - radius, 
                    position[0] + radius, position[1] + radius)
            
            # Draw sector (pie slice)
            self.draw.pieslice(bbox, start=start_angle, end=fill_end_angle, fill=fill)
            
            # If percentage < 100, redraw semicircle border to cover possible artifacts
            if percentage < 100 and (outline is not None or fill is not None):
                # Draw semicircle arc
                self.draw.arc(bbox, start=start_angle, end=end_angle, fill=outline or "white", width=1)
                
                # Draw diameter line according to direction
                if orientation == "top" or orientation == "bottom":
                    self.draw.line([(position[0] - radius, position[1]), 
                                (position[0] + radius, position[1])], 
                                fill=outline or "white")
                else:  # left or right
                    self.draw.line([(position[0], position[1] - radius), 
                                (position[0], position[1] + radius)], 
                                fill=outline or "white")
        elif percentage > 0 and fill is None:
            # If only percentage specified but no fill color, use default fill
            bbox = (position[0] - radius, position[1] - radius, 
                    position[0] + radius, position[1] + radius)
            self.draw.pieslice(bbox, start=start_angle, end=fill_end_angle, fill="white")

    # Text display with inverse color effect
    def draw_text_with_inverse_color(self, text, position=((0, 0), (128, 64)), directory="center", offset=(0,0), font_size=None):
        """
        Display text in buffer with inverse color display
        Args:
            text: Text to display
            position: Text display area ((x1, y1), (x2, y2)), top-left and bottom-right coordinates
            directory: Text alignment ("center", "left", "right")
            offset: Text offset (x, y)
            font_size: Font size
        """
        # Use specified font size or default font
        if font_size is None:
            font = self.font
        else:
            font = ImageFont.truetype(self.default_font_path, font_size)
        # Parse position parameters
        start_xy, end_xy = position
        x1, y1 = start_xy
        x2, y2 = end_xy
        # Get text dimensions
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        # First draw inverse color background for entire area
        self.draw.rectangle((x1, y1, x2, y2), fill="white")
        # Calculate text drawing position
        if directory == "center":
            # Center alignment
            text_x = x1 + (x2 - x1 - text_width) // 2 + offset[0]
            text_y = y1 + offset[1]
        elif directory == "left":
            # Left alignment
            text_x = x1 + offset[0]
            text_y = y1 + offset[1]
        elif directory == "right":
            # Right alignment
            text_x = x2 - text_width  + offset[0]
            text_y = y1 + offset[1]
        else:
            # Default center
            text_x = x1 + (x2 - x1 - text_width) // 2 + offset[0]
            text_y = y1 + offset[1]
        # Draw black text on inverse color background
        self.draw.text((text_x, text_y), text, font=font, fill="black")

    # Draw dial
    def draw_dial(self, center_xy=(64,32), radius=20, angle=(225, 315), directory="CW", tick_count=10, percentage=0, start_value=0, end_value=100):
        """
        Draw a dial with scales
        Args:
            center_xy: Circle center coordinates (x, y)
            radius: Circle radius
            angle: Angle tuple (start angle, end angle) - 0 degrees is right, counterclockwise increases
            directory: Direction "CW"(clockwise) or "CCW"(counterclockwise)
            tick_count: Scale count
            percentage: Current value percentage (0.0 to 100.0)
            start_value: Start value
            end_value: End value
        """
        # Parse parameters
        cx, cy = center_xy
        start_angle, end_angle = angle
        
        # Ensure angles are within correct range
        start_angle = start_angle % 360
        end_angle = end_angle % 360
        
        # Calculate main arc bounding box
        bbox = (
            (cx - radius, cy - radius),
            (cx + radius, cy + radius)
        )
        
        # Draw main arc (need to adjust angles to adapt to screen coordinate system)
        # Screen coordinate system Y-axis increases downward, need to mirror angles
        screen_start_angle = (360 - start_angle) % 360
        screen_end_angle = (360 - end_angle) % 360
        
        # Correctly draw main arc
        if directory == "CW":
            # Clockwise direction in mathematical coordinate system is from start_angle to end_angle
            # But in screen coordinate system need to go from screen_end_angle to screen_start_angle
            self.draw_arc(bbox, screen_start_angle, screen_end_angle, fill="white", width=1)
        else:
            # Counterclockwise direction in mathematical coordinate system is from start_angle to end_angle
            # In screen coordinate system similarly from screen_start_angle to screen_end_angle
            self.draw_arc(bbox, screen_end_angle, screen_start_angle, fill="white", width=1)
        
        # Calculate scales and pointer
        if directory == "CW":
            # Clockwise direction
            # Calculate angle range in mathematical coordinate system
            if start_angle > end_angle:
                arc_range = start_angle - end_angle
            else:
                arc_range = (360 - end_angle) + start_angle
                
            # Draw scale lines
            for i in range(tick_count + 1):
                tick_percent = i / tick_count
                # Angle in mathematical coordinate system (clockwise)
                math_angle = (start_angle - tick_percent * arc_range) % 360
                # Convert to screen coordinate system angle
                angle_pos = (360 - math_angle) % 360
                
                # Scale line inner and outer endpoints
                inner_radius = radius - 3
                outer_radius = radius
                
                x1 = cx + inner_radius * math.cos(math.radians(angle_pos))
                y1 = cy + inner_radius * math.sin(math.radians(angle_pos))
                x2 = cx + outer_radius * math.cos(math.radians(angle_pos))
                y2 = cy + outer_radius * math.sin(math.radians(angle_pos))
                
                self.draw_line(((x1, y1), (x2, y2)), fill="white")
            
            # Calculate pointer angle corresponding to current value
            math_pointer_angle = (start_angle - (percentage / 100.0) * arc_range) % 360
            pointer_angle = (360 - math_pointer_angle) % 360
        else:  # CCW (counterclockwise)
            # Calculate angle range in mathematical coordinate system
            if end_angle > start_angle:
                arc_range = end_angle - start_angle
            else:
                arc_range = (360 - start_angle) + end_angle
                
            # Draw scale lines
            for i in range(tick_count + 1):
                tick_percent = i / tick_count
                # Angle in mathematical coordinate system (counterclockwise)
                math_angle = (start_angle + tick_percent * arc_range) % 360
                # Convert to screen coordinate system angle
                angle_pos = (360 - math_angle) % 360
                
                # Scale line inner and outer endpoints
                inner_radius = radius - 3
                outer_radius = radius
                
                x1 = cx + inner_radius * math.cos(math.radians(angle_pos))
                y1 = cy + inner_radius * math.sin(math.radians(angle_pos))
                x2 = cx + outer_radius * math.cos(math.radians(angle_pos))
                y2 = cy + outer_radius * math.sin(math.radians(angle_pos))
                
                self.draw_line(((x1, y1), (x2, y2)), fill="white")
            
            # Calculate pointer angle corresponding to current value
            math_pointer_angle = (start_angle + (percentage / 100.0) * arc_range) % 360
            pointer_angle = (360 - math_pointer_angle) % 360
        
        self.draw_circle(center_xy, radius - 4, fill="black")
        # Draw pointer
        pointer_length = radius - 5
        pointer_x = cx + pointer_length * math.cos(math.radians(pointer_angle))
        pointer_y = cy + pointer_length * math.sin(math.radians(pointer_angle))
        
        # Draw pointer line
        self.draw_line(((cx, cy), (pointer_x, pointer_y)), fill="white")
        
        # Draw a small dot at center
        self.draw_circle((cx, cy), 1, fill="white")

if __name__ == "__main__":
    print("Starting OLED display example...")

    oled = OLED()
    oled.set_rotation(180)
    
    try:
        oled.clear()
        print("Display text 'Hello, World!'")
        oled.draw_text("Hello, World!", position=((0, 0), (128, 20)), directory="center")
        oled.draw_text("Hello, World!", position=((0, 20), (128, 40)), directory="left")
        oled.draw_text("Hello, World!", position=((0, 40), (128, 60)), directory="right")
        oled.show()
        time.sleep(0.5)

        oled.clear()
        print("Inverse color text 'Hello, World!'")
        oled.draw_text_with_inverse_color("Hello, World!", position=((0, 0), (128, 20)), directory="center")
        oled.draw_text_with_inverse_color("Hello, World!", position=((0, 20), (128, 40)), directory="left")
        oled.draw_text_with_inverse_color("Hello, World!", position=((0, 40), (128, 60)), directory="right")
        oled.show()
        time.sleep(0.5)

        oled.clear()
        print("Draw point (64, 32)")
        oled.draw_point((64, 32), fill="white")
        oled.show()
        time.sleep(0.5)
        
        print("Draw lines ((0, 0), (127, 63)), ((0, 63), (127, 0))")
        oled.draw_line(((0, 0), (127, 63)), fill="white")
        oled.draw_line(((0, 63), (127, 0)), fill="white")
        oled.show()
        time.sleep(0.5)
        
        print("Draw rectangle ((44, 12), (84, 52))")
        oled.draw_rectangle(((44, 12), (84, 52)), outline="white", fill=None)
        oled.show()
        time.sleep(0.5)
        
        print("Draw ellipse ((24, 12), (104, 52))")
        oled.draw_ellipse(((24, 12), (104, 52)), outline="white", fill=None)
        oled.show()
        time.sleep(0.5)
        
        print("Draw circle (64, 32) radius 20")
        oled.draw_circle((64, 32), 20, outline="white", fill=None)
        oled.show()
        time.sleep(0.5)

        print("Draw arc ((14, 12), (114, 52)) from 0 to 180 degrees")
        oled.draw_arc(((14, 12), (114, 52)), 0, 180, fill="white", width=1)
        oled.draw_arc(((14, 12), (114, 52)), 180, 360, fill="white", width=1)
        oled.show()
        time.sleep(0.5)
        
        print("Draw polygon ((44, 32), (64, 52), (84, 32), (64, 12))")
        oled.draw_polygon(((44, 32), (64, 52), (84, 32), (64, 12)), outline="white", fill=None)
        oled.show()
        time.sleep(0.5)

        oled.clear()
        print("Draw circle with percentage")
        for i in range(0, 101):
            oled.draw_circle_with_percentage((64, 32), 32, i, outline="white", fill="white")
            oled.show()
            time.sleep(0.005)
        time.sleep(0.5)

        oled.clear()
        print("Draw semicircle with percentage")
        for i in range(0, 101):
            oled.draw_semicircle_with_percentage((64, 22), 20, i, orientation="top", outline="white", fill="white")
            oled.draw_semicircle_with_percentage((64, 42), 20, i, orientation="bottom", outline="white", fill="white")
            oled.draw_semicircle_with_percentage((32, 32), 20, i, orientation="left", outline="white", fill="white")
            oled.draw_semicircle_with_percentage((96, 32), 20, i, orientation="right", outline="white", fill="white")
            oled.show()
            time.sleep(0.005)

        oled.clear()
        print("Draw progress bar")
        for i in range(0, 101):
            oled.draw_progress_bar((10, 22), (118, 42), i, outline="white", fill="white")
            oled.show()
            time.sleep(0.005)
        time.sleep(0.5)

        # Create a thermometer dial
        oled.clear()
        print("Create a thermometer dial")
        for i in range(0, 101):
            oled.draw_dial(
                center_xy=(64, 32),
                radius=25,
                angle=(225, 315),  
                directory="CW",
                tick_count=10,
                percentage=i,
                start_value=0,
                end_value=100
            )
            oled.show()
            time.sleep(0.005)
        time.sleep(0.5)

        oled.clear()  
        # Save buffer content to image file
        # Display image
        print("Display image './picture/1.bmp'")
        oled.draw_image("./picture/1.bmp")
        oled.show()
        time.sleep(0.5)
        oled.draw_image("./picture/2.png")
        oled.show()
        time.sleep(0.5)
        oled.draw_image("./picture/3.jpg")
        oled.show()
        time.sleep(0.5)
        oled.clear()

        # # Display GIF animation
        # print("Display GIF animation './picture/1.gif'")
        # oled.draw_gif("./picture/1.gif", (0, 0), (128, 64), center=True)
        # time.sleep(0.5)

        # Save buffer content to image file
        #oled.save_buffer_to_image("1.bmp")
        #oled.save_buffer_to_image("1.png")
        #oled.save_buffer_to_image("1.jpg")
    except Exception as e:
        print(f"Error occurred: {e}")
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
    finally:
      # Clear display
        print("Clear display")
        oled.clear()
    

    # Close display
    print("Close OLED display")
    oled.close()