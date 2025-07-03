.. _Communication_Protocols_and_Controls:

##############################################################################
Chapter 7 Communication Protocols and Controls
##############################################################################

7.1 OLED Control
******************************

Code
==============================

Below is the code for controlling OLED display.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :dedent:

Import the functional modules.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 1-6
    :dedent:

Create an OLDE class.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 8-8
    :dedent:

In the main function, instantiate an object by calling this class.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 136-139
    :dedent:

Step 1: Display texts on the OLED screen.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 140-145
    :dedent:

Step 2: Draw a point on it.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 147-151
    :dedent:

Step 3: Draw a line on the OLED display.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 153-158
    :dedent:

Step 4: Draw a rectangle on the OLED display. 

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 160-164
    :dedent:

Step 5: Draw an ellipse on the OLED display. 

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 166-170
    :dedent:

Step 6: Draw a circle on the OLED display.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 172-176
    :dedent:

Step 7: Draw an arc on the OLED display.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 178-183
    :dedent:

Step 8: Draw a polygon on the OLED display.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 185-190
    :dedent:

Step 9: Display images and GIF animations on the OLED Screen

If an exception occurs during program execution, print the error message. If a keyboard interrupt is detected, exit the running program.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 192-217
    :dedent:

Step 10: Clear the dislay.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 218-221
    :dedent:

Step 11: Turn OFF the OLDE display.

.. literalinclude:: ../../../freenove_Kit/Code/oled.py
    :language: python
    :linenos:
    :lines: 223-225
    :dedent:

Reference
----------------------------

.. py:function:: def __init__(self, bus_number=1, i2c_address=0x3C):

    Initialize the I2C interface and the OLED display.

    **Parameters**
    
    **bus_number:** I2C bus, default is I2C1
    
    **i2c_address:** I2C address, default is 0x3C.

.. py:function:: def clear(self):

    Clear all contents displayed on the screen.

.. py:function:: def show(self):

    Show contents on the OLED display.

.. py:function:: def close(self):

    Turn OFF the OLED display.

.. py:function:: def draw_point(self, xy, fill=None):

    Draw a point on the OLED screen.

    **Parameters**

    **xy:** Specifies the coordinates where the point should be drawn on the screen.

    **fill:** The fill color for the point.

.. py:function:: def draw_line(self, xy, fill=None):

    Draw a line on the OLED screen.

    **Parameters**

    **xy:** Specifies the coordinates where the line should be drawn on the screen.

    **fill:** The fill color for the line.

.. py:function:: def draw_rectangle(self, xy, outline=None, fill=None):

    Draw a rectangle on the OLED screen.

    **Parameters**

    **xy:** Specifies the coordinates where the rectangle should be drawn on the screen.

    **outline:** The color of the rectangle's border.

    **fill:** The color used to fill the inside of the rectangle.

.. py:function:: def draw_ellipse(self, xy, outline=None, fill=None):

    Draw an ellipse on the OLED screen.

    **Parameters**

    **xy:** Specifies the coordinates where the ellipse should be drawn on the screen.

    **outline:** The color of the ellipse 's border.

    **fill:** The color used to fill the inside of the ellipse.

.. py:function:: def draw_circle(self, xy, radius, outline=None, fill=None):

    Draw a circle on the OLED screen.

    **Parameters**

    **xy:** Specifies the coordinates where the circle should be drawn on the screen.

    **radius:** Radius of the circle.

    **outline:** The color of the circle 's border.

    **fill:** The color used to fill the inside of the circle.

7.2 GPIO Board Control
************************************

7.2.1 GPIO Board Registers
====================================

The GPIO Board is controlled via the I2C interface on the Raspberry Pi 5. Below are the register addresses for the GPIO Board:

.. table::
    :class: freenove-ow

    +----------+------------------------------------+----------+---------------------------+
    | Register |              Function              | Register |         KEY Value         |
    +==========+====================================+==========+===========================+
    | 0x00     | Set I2C Address                    | 0xF5     | Get all LED colors        |
    +----------+------------------------------------+----------+---------------------------+
    | 0x01     | Set specified LED color            | 0xF6     | Get LED mode              |
    +----------+------------------------------------+----------+---------------------------+
    | 0x02     | Set all LEDs' colors               | 0xF7     | Get fan mode              |
    +----------+------------------------------------+----------+---------------------------+
    | 0x03     | Set LED mode                       | 0xF8     | Get fan frequency         |
    +----------+------------------------------------+----------+---------------------------+
    | 0x04     | Set fan mode                       | 0xF9     | Get Fan0 duty cycle       |
    +----------+------------------------------------+----------+---------------------------+
    | 0x05     | Set fan frequency                  | 0xFA     | Get Fan1 duty cycle       |
    +----------+------------------------------------+----------+---------------------------+
    | 0x06     | Set fan duty cycle                 | 0xFB     | Get temperature threshold |
    +----------+------------------------------------+----------+---------------------------+
    | 0x07     | Set fan mode temperature threshold | 0xFC     | Get chassis temperature   |
    +----------+------------------------------------+----------+---------------------------+
    | 0x08     | Set power-on self-test feature     | 0xFD     | Get brand name            |
    +----------+------------------------------------+----------+---------------------------+
    | 0xF3     | Get I2C Address                    | 0xFE     | Get firmware version      |
    +----------+------------------------------------+----------+---------------------------+
    | 0xF4     | Get specified LED color            | 0xFF     | Save current data         |
    +----------+------------------------------------+----------+---------------------------+

We have flashed firmware onto the GPIO Board. The factory default I2C address of the GPIO Board is 0x21. Additionally, we have included some basic configurations within the firmware to control the LED lights and case fans. You can use the Raspberry Pi 5 to read from and write to the GPIO Board's registers in order to control the LED lights and fans.

LED lights
-----------------------------------

Regarding the LED lights, we have configured five modes:

0. Off Mode: In this mode, all LED lights are turned off.

1. Static Display Mode: The LED lights display a fixed color. You can set them to any desired color.

2. Follow Display Mode: The LED lights illuminate sequentially. You can set them to any desired color.

3. Breathing Mode: The brightness of the LED lights gradually increases and then decreases. You can set them to any desired color.

4. Rainbow Mode: The LED lights cycle through colors like a rainbow. The color cannot be customized in this mode.

Case Fans
-----------------------------------

Regarding the case fans, we have configured three modes:

0. **Off Mode:** In this mode, the fans remain inactive and do not start.

1. **Manual Mode:** You can manually set the fan speed by entering any duty cycle value between 0 and 255. This allows you to control the rotational speed of the fans precisely.

2. **Automatic Mode:** Upon reaching the minimum activation temperature, the fan will run at full speed, with the default activation temperature set to 30°C.

Cooling Down Behavior:

    -The fans cease operation entirely when the internal temperature falls below 27°C.

Default Temperature Thresholds: The default temperature monitoring range is set between 30°C and 45°C. If needed, you can adjust this range by modifying the appropriate register settings.

Other Functions
-----------------------------------

1.	Power-ON Check Function

To initiate the power-on check feature, change the value of register 0x07 to 1.

During power-up, the GPIO Board will be controlled to make the LED lights display in rainbow mode and start the case fans for 3 seconds.

2.	Saving Current Configurations

If you want to save the current configurations such as the LED light colors, running modes, case fan duty cycles, and their running modes, modify the value of register 0xFF to 1.

The saving process usually takes around 20 milliseconds. Make sure to wait for more than 20 milliseconds before sending new data; otherwise, the new data won't be saved.

Important Note: The saving operation is a one -time action.If you need to save a new set of configurations, you must modify the register value again.

7.2.2 Code
======================================

.. literalinclude:: ../../../freenove_Kit/Code/expansion.py
    :language: python
    :linenos:
    :dedent:

Import functional modules.

.. literalinclude:: ../../../freenove_Kit/Code/expansion.py
    :language: python
    :linenos:
    :lines: 2-3
    :dedent:

Create an Expansion class and define the I2C address and register address.

.. literalinclude:: ../../../freenove_Kit/Code/expansion.py
    :language: python
    :linenos:
    :lines: 5-29
    :dedent:

Instantiate an object by calling this class.

.. literalinclude:: ../../../freenove_Kit/Code/expansion.py
    :language: python
    :linenos:
    :lines: 163-164
    :dedent:

Set the color of all LED lights, set the case fans' duty cycle, set the LED light mode, set the fan mode.

.. literalinclude:: ../../../freenove_Kit/Code/expansion.py
    :language: python
    :linenos:
    :lines: 186-193
    :dedent:

Every 0.03 seconds, increment the duty cycle of the case fans by 1. Every 0.15 seconds, retrieve the following data: I2C address, colors of all LED lights, LED light mode, case fan mode, duty cycles of both case fans, temperature thresholds, temperature readings, developer information, and version number. Then, print out this information.

.. literalinclude:: ../../../freenove_Kit/Code/expansion.py
    :language: python
    :linenos:
    :lines: 194-209
    :dedent:

If an exception occurs during program execution, print the error value; if a keyboard input interruption is detected, exit the running program; finally, set the color of all LED lights to 0 and close the I2C communication.

.. literalinclude:: ../../../freenove_Kit/Code/expansion.py
    :language: python
    :linenos:
    :lines: 211-217
    :dedent:

Reference
---------------------------

.. py:function:: def __init__(self, bus_number=1, address=IIC_ADDRESS):	

    Initialize I2C interface and set the I2C address.

    **Parameters**

    **bus_number:**  I2C bus, default is I2C1

    **address:** I2C address

.. py:function:: def write(self, reg, values):	

    Write a value to the specified register.

    **Parameters**

    **reg:** the specified register

    **value:** the value to be sent

.. py:function:: def read(self, reg, length=1):	

    Retrieve a value from the specified register.

    **Parameters**

    **reg:** the specified register

    **length:** the length of the value to be retrieved

.. py:function:: def end(self):	

    Close the I2C communication.

.. py:function:: def set_i2c_addr(self, addr):	

    Set the I2C address.

    **Parameters**

    **addr:** The I2C address to be set, with a range of 0 - 255.

.. py:function:: def set_led_color(self, led_id, r, g, b):	

    Set the color of the specified LED light.

    **Parameters**

    **led_id:** number of the specified LED light, with a range of 0 - 3.

    **r:** The red component value for setting the color of all LED lights. The range is from 0 to 255.

    **g:** The green component value for setting the color of all LED lights. The range is from 0 to 255.

    **b:** The blue component value for setting the color of all LED lights. The range is from 0 to 255.

.. py:function:: def set_all_led_color(self, r, g, b):	

    Set the color of all LED lights.

    **Parameters**

    **r:** The red component value for setting the color of all LED lights. The range is from 0 to 255.

    **g:** The green component value for setting the color of all LED lights. The range is from 0 to 255.

    **b:** The blue component value for setting the color of all LED lights. The range is from 0 to 255.

.. py:function:: def set_led_mode(self, mode):	

    Set the mode of the LED lights.

    **Parameters**

    **mode:** The mode of the LED lights. The range of the parameter is from 0 to 4.

.. py:function:: def set_fan_mode(self, mode):	

    Set the mode of the case fans.

    **Parameters**

    **mode:** The mode of the case fans. The range of the parameter is from 0 to 2.

.. py:function:: def set_fan_frequency(self, freq):	

    Set the frequency of the case fans.

    **Parameters**

    **freq:** the frequency value of the case fan. The range of the parameter is from 46 to 1500000Hz.

.. py:function:: def set_fan_duty(self, duty0, duty1):	

    Set the duty cycle values of the case fans.

    **Parameters**

    **duty0:** the duty cycle value of case fan FAN0

    **duty1:** the duty cycle value of chassis fan FAN1

.. py:function:: def set_fan_threshold(self, low_threshold, high_threshold):	

    Set the temperature threshold range for the automatic mode of the case fans.

    **Parameters**

    **low_threshold:** the lower limit of the temperature threshold

    **high_threshold:** the upper limit of the temperature threshold

.. py:function:: def set_power_on_check(self, state):	

    Set the state of power-on check.

    **Parameters**

    **state:** The state of power-on check, with 0 as disabled and 1 as enabled.

.. py:function:: def set_save_flash(self, state):	

    Save the current configuration to flash.

    **Parameters**

    **state:** The state of configuration saving, with 0 meaning not saved, and 1 referring to saved.

.. py:function:: def get_iic_addr(self):	

    Get the I2C address.

.. py:function:: def get_led_color(self, led_id):	

    Get the color data of the specified colored light.

    **Parameters**

    **led_id:** The number of the specified LED light, with a range from 0 to 3.

.. py:function:: def get_all_led_color(self):	

    Get the color data of all LED lights.

.. py:function:: def get_led_mode(self):	

    Get the mode of the LED lights.

.. py:function:: def get_fan_mode(self):	

    Get the mode of the case fans.

.. py:function:: def get_fan_frequency(self):	

    Get the frequency value of the case fan.

.. py:function:: def get_fan0_duty(self):	

    Get the duty cycle value of case fan FAN0.

.. py:function:: def get_fan1_duty(self):	

    Get the duty cycle value of case fan FAN1.

.. py:function:: def get_fan_threshold(self):	

    Get the temperature threshold data of the case fans.

.. py:function:: def get_temp(self):	

    Get the internal temperature of the computer case.

.. py:function:: def get_brand(self):	

    Get the brand name.

.. py:function:: def get_version(self):	

    Get the current firmware version number.