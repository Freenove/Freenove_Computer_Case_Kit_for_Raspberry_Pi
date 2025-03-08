from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import time
import os
import shutil

class OLED:
    def __init__(self, bus_number=1, i2c_address=0x3C):
        # Initialize I2C interface and OLED display
        self.bus_number = bus_number
        self.i2c_address = i2c_address
        self.serial = i2c(port=self.bus_number, address=self.i2c_address)
        self.device = ssd1306(self.serial)
        self.buffer = Image.new('1', (self.device.width, self.device.height))
        self.draw = ImageDraw.Draw(self.buffer)

        self.default_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" 
        self.default_font_size = 16
        self.font = ImageFont.load_default()

    def clear(self):
        # Clear the content in the buffer
        self.buffer = Image.new('1', (self.device.width, self.device.height))
        self.draw = ImageDraw.Draw(self.buffer)

    def show(self):
        # Display the content in the buffer on the OLED screen
        self.device.display(self.buffer)

    def close(self):
        # Close the I2C bus
        pass  # The luma.oled library does not require explicitly closing the I2C bus

    def draw_point(self, xy, fill=None):
        # Draw a point in the buffer
        self.draw.point(xy, fill=fill)

    def draw_line(self, xy, fill=None):
        # Draw a line in the buffer
        self.draw.line(xy, fill=fill)

    def draw_rectangle(self, xy, outline=None, fill=None):
        # Draw a rectangle in the buffer
        self.draw.rectangle(xy, outline=outline, fill=fill)

    def draw_ellipse(self, xy, outline=None, fill=None):
        # Draw an ellipse in the buffer
        self.draw.ellipse(xy, outline=outline, fill=fill)

    def draw_circle(self, xy, radius, outline=None, fill=None):
        # Draw a circle in the buffer
        self.draw.ellipse((xy[0] - radius, xy[1] - radius, xy[0] + radius, xy[1] + radius), outline=outline, fill=fill)

    def draw_arc(self, xy, start, end, fill=None, width=1):
        # Draw an arc in the buffer
        self.draw.arc(xy, start, end, fill=fill, width=width)

    def draw_polygon(self, xy, outline=None, fill=None):
        # Draw a polygon in the buffer
        self.draw.polygon(xy, outline=outline, fill=fill)

    def draw_text(self, text, position=(0, 0), font_size=None):
        # Display text in the buffer
        if font_size is None:
            font = self.font
        else:
            font = ImageFont.truetype(self.default_font_path, font_size)
        self.draw.text(position, text, font=font, fill="white")

    def draw_image(self, image_path, position=(0, 0), resize=None):
        # Display an image in the buffer
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
   
    def draw_gif(self, gif_path, position=(0, 0), resize=None):
        # Display a GIF animation
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
                target_height = height
                target_width = height * 2
                if width < target_width:
                    new_image = Image.new('L', (target_width, target_height), 0)
                    x_offset = (target_width - width) // 2
                    new_image.paste(frame, (x_offset, 0))
                else:
                    new_image = Image.new('L', (width, target_height), 0)
                    y_offset = (target_height - height) // 2
                    new_image.paste(frame, (0, y_offset))
                    target_width = width
                new_image = new_image.convert('1')
                if resize is not None:
                    new_image = new_image.resize(resize, Image.LANCZOS)
                else:   
                    new_image = new_image.resize((self.device.width, self.device.height), Image.LANCZOS)
                new_image = new_image.resize((self.device.width, self.device.height), Image.LANCZOS)
                frame_path = os.path.join(temp_folder, f"frame_{len(frames)}.png")
                new_image.save(frame_path)
                frames.append(frame_path)
            for frame_path, delay in zip(frames, frame_delays):
                self.draw_image(frame_path, position = position, resize = resize)
                self.show()
                if delay > 0.17:
                    time.sleep(delay - 0.17)
        except FileNotFoundError:
            print(f"Error: File not found - {gif_path}")
        except Exception as e:
            print(f"Error displaying GIF: {e}")
        finally:
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)

    def save_buffer_to_image(self, image_path="saved_image.png"):
        # Save the content in the buffer as an image file
        self.buffer.save(image_path) 


if __name__ == "__main__":
    print("Starting OLED display example...")

    oled = OLED()
    try:
        # Display text
        print("Step 1: Displaying text 'Hello, World!'")
        oled.draw_text("Hello, World!", position=(0, 0))
        oled.show()
        time.sleep(0.5)
        
        # Draw a point
        print("Step 2: Drawing point (64, 32)")
        oled.draw_point((64, 32), fill="white")
        oled.show()
        time.sleep(0.5)
        
        # Draw lines
        print("Step 3: Drawing line ((0, 0), (127, 63)), ((0, 63), (127, 0))")
        oled.draw_line(((0, 0), (127, 63)), fill="white")
        oled.draw_line(((0, 63), (127, 0)), fill="white")
        oled.show()
        time.sleep(0.5)
        
        # Draw a rectangle
        print("Step 4: Drawing rectangle ((44, 12), (84, 52))")
        oled.draw_rectangle(((44, 12), (84, 52)), outline="white", fill=None)
        oled.show()
        time.sleep(0.5)
        
        # Draw an ellipse
        print("Step 5: Drawing ellipse ((20, 20), (100, 60))")
        oled.draw_ellipse(((20, 20), (100, 60)), outline="white", fill=None)
        oled.show()
        time.sleep(0.5)
        
        # Draw a circle
        print("Step 6: Drawing circle (64, 32) with radius 20")
        oled.draw_circle((64, 32), 20, outline="white", fill=None)
        oled.show()
        time.sleep(0.5)

        # Draw an arc
        print("Step 7: Drawing arc ((10, 30), (110, 50)) from 0 to 180 degrees")
        oled.draw_arc(((10, 30), (110, 50)), 0, 180, fill="white", width=1)
        oled.draw_arc(((10, 30), (110, 50)), 180, 360, fill="white", width=1)
        oled.show()
        time.sleep(0.5)
        
        # Draw a polygon
        print("Step 8: Drawing polygon ((20, 20), (40, 40), (60, 20), (40, 0))")
        oled.draw_polygon(((20, 20), (40, 40), (60, 20), (40, 0)), outline="white", fill=None)

        oled.show()
        time.sleep(0.5)

        # Save the buffer content to an image file
        # Display an image
        print("Step 9: Displaying image './picture/1.bmp'")
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

        # Display a GIF animation
        oled.draw_gif("./picture/1.gif")
        time.sleep(0.5)

        # Save the buffer content to an image file
        #oled.save_buffer_to_image("1.bmp")
        #oled.save_buffer_to_image("1.png")
        #oled.save_buffer_to_image("1.jpg")
    except Exception as e:
        print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
    finally:
        # Clear the display
        print("Step 10: Clearing display")
        oled.clear()
        
        # Close the display
        print("Step 11: Closing OLED display")
        oled.close()