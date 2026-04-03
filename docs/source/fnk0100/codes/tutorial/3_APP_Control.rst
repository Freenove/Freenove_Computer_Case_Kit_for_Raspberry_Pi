##############################################################################
Chapter 3 APP Control
##############################################################################

Before powering on the Freenove Computer Case Kit for Raspberry Pi, please make sure that all cable connections are correct.

:red:`Due to its multiple functions, this case requires an adequate power supply. We highly recommend using the official Raspberry Pi 5.1V / 5A power adapter (https://www.raspberrypi.com/products/27w-power-supply ).`

:red:`Failure to do so may result in the Freenove Computer Case Kit for Raspberry Pi being unusable or causing damage to components.`

**Installing Raspberry Pi OS**

If you have not yet installed the Raspberry Pi OS, please refer to the documentation ":ref:`Installing Raspberry Pi OS <fnk0100/codes/install/installing_raspberry_pi_os:installing raspberry pi os>`" under the directory Freenove Computer Case Kit for Raspberry Pi to install the OS to your SD card or SSD.

If you have a display ready, please continue reading the tutorial below.

3.1 Boot Behavior & Environment Settings
**************************************************

3.1.1 What to Expect on First Startup
=============================================

When you first power on the assembled chassis, the Raspberry Pi does not talk to the GPIO adapter board. This causes the board to operate on its own in a default mode, and you will observe the following.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_00.png
    :align: center

1. The case RGB lights will operate in rainbow mode.

2. During initial startup, the fan will run at maximum speed for 3 seconds. After this period, the system switches to temperature-controlled mode, where fan speed is regulated by the thermal sensor on the GPIO adapter board

3.	The screen will remain off during this phase - this is normal and expected.

**Troubleshooting Guide:**

If the RGB lights fail to illuminate, or if the fan doesn't perform the 3-second full-speed initialization, please:

Immediately power off the system

* Verify proper alignment and connection between the GPIO adapter board and Raspberry Pi

* Check all relevant power and data connections

If you have any questions of the above, please contact us at support@freenove.com

4. RPi 5 Status LED: The green STAT LED will remain steadily illuminated. If this LED is not lit or displays any pattern other than a steady green light, it indicates that the Raspberry Pi operating system has not booted successfully. In this case, please check your Raspberry Pi hardware and OS installation separately.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_01.png
    :align: center

5. The case adapter board's onboard PWR LEDs remain solid, while the STA LED flashes in sync with SSD activity.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_02.png
    :align: center

**Troubleshooting Guide:**

If any indicator shows abnormal behavior, immediately power off the system.

* If the PWR LED is off: Check the USB port and power cable connections.

* If the ON LED is off: Verify the FPC cable connection.

* If the STA LED remains solid (with the SSD connected): Inspect all SSD-related connections.

If you have any questions of the above, please contact us at support@freenove.com

If all components behaves as expected, then your computer case is correctly assembled and functioning well.

In this case, you can connect a screen to your Raspberry Pi or access it via VNC viewer.

Speaker Test
--------------------------

Before playing music, please check whether the speak switch is ON.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_03.png
    :align: center

Open the data folder under the Freenove_Computer_Case_Kit_for_Raspberry_Pi/Code/data directory, and click the mp3 file to display.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_04.png
    :align: center

If you have enabled Advanced Options -> A7 Wayland -> W1 X11 in **raspi-config** and experience abnormal audio output, please re-enable HDMI to restore normal audio function.

Right-click in any blank area upon the desktop and choose "**Desktop Preferences...**".

.. image:: ../_static/imgs/3_APP_Control/Chapter03_05.png
    :align: center

In the pop-up Control Centre window, select "Screens" from the left pane. Select Screens  HDMI-A-1  Active to reactivate HDMI。

.. image:: ../_static/imgs/3_APP_Control/Chapter03_06.png
    :align: center

3.1.2 Switching Taskbar Display
============================================

If your kit is a non-display verion (Model numbers: FNK0100A/B), you can skip this section by clicking here.

For versions equipped with a 4.3-inch IPS screen (Model numbers: FNK0100H/K), after booting the RPi 5, the system will create two independent display areas: DSI-1 and HDMI-A-1. When connecting via VNC, you are viewing a mirrored display of HDMI-A-1. Since the system status bar is prioritized for display on the DSI screen, it is not included by default in the VNC interface. Please follow the instructions below to display the status bar in the HDMI-A-1 area.

Right-click in any blank area upon the desktop and choose "Desktop Preferences...".

.. image:: ../_static/imgs/3_APP_Control/Chapter03_07.png
    :align: center

In the pop-up Control Centre window, select "**Taskbar**" from the left pane. Find the "**Location**" setting and change it from :red:`DSI-1 to HDMI-A-1.`

.. image:: ../_static/imgs/3_APP_Control/Chapter03_08.png
    :align: center

3.1.3 Software Setup
===============================

Software Packages Update
============================================

Run the following command on the terminal to update your Raspberry Pi's package list to the latest version.

.. code-block:: console
    
    sudo apt update

.. image:: ../_static/imgs/3_APP_Control/Chapter03_09.png
    :align: center

Code downloading
------------------------------

Open the Raspberry Pi Terminal, type the following two commands one by one to download the code for the case.

.. code-block:: console
    
    cd
    git clone https://github.com/Freenove/Freenove_Computer_Case_Kit_for_Raspberry_Pi.git

.. image:: ../_static/imgs/3_APP_Control/Chapter03_10.png
    :align: center

OLED Library Installation (Important)
============================================

Run the following command to install the OLED library. Fail to do so will result in software malfunction.

.. code-block:: console
    
    sudo apt install python3-luma.oled

.. image:: ../_static/imgs/3_APP_Control/Chapter03_11.png
    :align: center

Enable I2C (Important)
-------------------------------

The I2C function must be enabled, as it is required for communication between the Raspberry Pi, the OLED display, and the GPIO adapter board. Without it, the chassis software will fail to operate.

Run the following command to open the Raspberry Pi configuration interface.

.. code-block:: console
    
    sudo raspi-config

Navigate to Interface Options and press Enter.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_12.png
    :align: center

Select I2C and press Enter to enable it.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_13.png
    :align: center

Select Yes, and press Enter.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_14.png
    :align: center

Select Finish to save the change and exit the configuration inferface.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_15.png
    :align: center

Creating Desktop Shortcut
-------------------------------

Run the following two commands one by one in the Raspberry Pi terminal to create a desktop shortcut for the case control software.

.. code-block:: console
    
    cd Freenove_Computer_Case_Kit_for_Raspberry_Pi/Code/
    sudo python create_desktop_shortcut.py

.. image:: ../_static/imgs/3_APP_Control/Chapter03_16.png
    :align: center

:combo:`red font-bolder:If you are interested in the code implementation, you can explore the files in the Freenove_Computer_Case_Kit_for_Raspberry_Pi/Code directory.`

:combo:`red font-bolder:Should you wish to modify the code, please ensure you back it up first to avoid potential software malfunctions caused by unintended changes.`

3.2 About the Case Control Software
********************************************

With the environment configured from the previous chapter, the accompanying host software can now be used to manage case functions including ARGB lighting, the OLED display, and fan control.

This chapter provides a detailed guide on the software's usage. For insight into the interface design, the app_ui.py file is available in the Freenove_Computer_Case_Kit_for_Raspberry_Pi/Code directory.

Double click the software with Freenove logo on RPi's desktop, and a window will pop up. Click “Execute” to run the program.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_17.png
    :align: center

The software interface is as shown below.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_18.png
    :align: center

3.2.1 Dashboard Monitoring
====================================

The dashboard provides live monitoring of key RPi 5 and case component stats, giving you an at-a-glance view of the system status.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_19.png
    :align: center

Below is a detailed explanation of the parameters displayed on the monitoring interface:

* CPU Usage: Current processor utilization percentage of the Raspberry Pi 5

* RAM Usage: Current system memory utilization percentage of the Raspberry Pi 5

* CPU TEMP: The internal temperature of the Raspberry Pi 5's SoC (System on Chip)

* Case Temp: The temperature inside the chassis, provided by the temperature sensor on the GPIO Board

* Storage Usage: The total storage space utilization. This value reflects the usage of the SD card if one is used. If single or multiple SSDs are installed, it calculates the aggregate usage across all drives.

* RPi PWM: PWM duty cycle for the Raspberry Pi's active cooler fan.

* Case PWM1: PWM duty cycle for case fan 1.

* Case PWM2: PWM duty cycle for case fan 2.

**Data Source & Troubleshooting:**

**CPU Usage, RAM Usage, CPU Temp, Storage Usage, and RPi PWM** are retrieved directly from the Raspberry Pi. If any of these values are missing, check the Raspberry Pi for faults.

**Case Temp, Case PWM1, and Case PWM2** are read from the GPIO Board via I2C communication with Raspberry Pi 5.

If these data cannot be obtained consistently, please contact us by email: support@freenove.com

:combo:`red font-bolder:For those interested in the interface implementation, please refer to the files api_systemInfo.py and api_expansion.py in the Freenove_Computer_Case_Kit_for_Raspberry_Pi/Code directory.`

3.2.2 LED Control Interface
====================================

This is the control interface for the case ARGB lights. You can select different modes to display various lighting effects.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_20.png
    :align: center

It is set to rainbow mode by default, as shown below. 

.. image:: ../_static/imgs/3_APP_Control/Chapter03_21.png
    :align: center

There are four preset lighting modes available: **Rainbow**、 **Breathing**、 **Follow**、 **Manual**. You can select the corresponding option to switch among the modes.

Note: Only in **Breathing**, **Follow**, and **Manual** modes can the color of the RGB lights be controlled using the slider below. In other modes, the color of the RGB lights cannot be adjusted. 

.. image:: ../_static/imgs/3_APP_Control/Chapter03_22.png
    :align: center
 
If you do not turn ON the RGB lights, you can select the Close mode to turn off them.

Please note: Any lighting mode you select is temporary. The case will revert to its default mode after a shutdown and restart.

To set a new default mode, select your desired mode and click the "**Save**" button.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_23.png
    :align: center

To restore the RGB lights and sliders to their default settings, click the ”Default” button once.

If the four preset lighting modes do not meet your needs, you can use the ”Custom” mode for personalized settings.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_24.png
    :align: center

Click "**Edit**" will open the "task_led.py" file. You can modify the code in the editor.

Click "**Test**" will create a temporary thread and run task_led.py, allowing you to quickly debug and observe the LED light effects.

You can also view the source code directly:

Freenove_Computer_Case_Kit_for_Raspberry_Pi/Code/task_led.py

For more about LED control interface, you can refer to the source file:

Freenove_Computer_Case_Kit_for_Raspberry_Pi/Code/api_expansion.py

**Important Notes:**

1. Back up the source code before making any modifications.

2. Custom mode is an advanced feature. Modifying the code in task_led.py requires a basic understanding of Python programming. If you are not familiar with programming, we do not recommend editing this file.

3. The “Test” button only runs the code in the current state. The code will not automatically run after rebooting the Raspberry Pi.

4. If the LED lights show no response after you modify the code and click “Test,” it indicates an error in your code preventing it from running properly. Please review your code.

5. If you want the Custom mode code to execute automatically on every startup, please refer to the instructions in the ":ref:`3.2.5 Settings Interface <fnk0100/codes/tutorial/3_app_control:3.2.5 settings interface>`" Section.

3.2.3 Fan Control Interface
=====================================

This is the case fan control interface for convenient fan management. The interface will change when you select different modes: Follow Case or Manual mode.

.. table::
    :class: table-line
    :align: center
    
    +------------------+
    | Follow Case Mode |
    |                  |
    | |Chapter03_25|   |
    +------------------+
    | Manual Mode      |
    |                  |
    | |Chapter03_26|   |
    +------------------+

.. |Chapter03_25| image:: ../_static/imgs/3_APP_Control/Chapter03_25.png
.. |Chapter03_26| image:: ../_static/imgs/3_APP_Control/Chapter03_26.png

Follow Case
----------------------------

In Follow Case mode, the GPIO Adapter board samples the temperature sensor at regular intervals and regulates the fan PWM signal based on the readings.

The specific control logic governing this process is depicted in the following figure.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_27.png
    :align: center

* Heating Phase:

  - When temperature ≥ **Low Temp** (default: 30°C), fan PWM set value: 100.

  - When temperature ≥ **High Temp** (default: 50°C), fan PWM set value: 175.

* Cooling Phase:

  - When temperature < **High Temp** (default: 50°C), fan PWM set value: 100.

  - **Low Temp - Schmitt** (default: 30 - 3 = 27°C) ≤ When temperature < **Low Temp** (default: 30°C), fan PWM set value: 75.

  - When temperature < **Low Temp- Schmitt** (default: 30 - 3 = 27°C), the fan stops.

You can configure the following parameters via the software. 

.. image:: ../_static/imgs/3_APP_Control/Chapter03_28.png
    :align: center

Manual
----------------

In Manual mode, you can adjust FAN1 and FAN2 PWM values via the respective sliders in manual mode.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_29.png
    :align: center

Custom
------------------

If the predefined modes do not meet your needs, you can select the **Custom** mode for advanced configuration.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_30.png
    :align: center

Click "**Edit**" will open the “task_fan.py” file. You can modify the code in the editor.

Click "**Test**" will create a temporary thread and run task_fan.py, allowing you to quickly debug and observe the fan effects.

You can also view the source code directly:

Freenove_Computer_Case_Kit_for_Raspberry_Pi/Code/task_fan.py

**Important Notes:**

1. Back up the source code before making any modifications.

2. Custom mode is an advanced feature. Modifying the code in task_fan.py requires a basic understanding of Python programming. If you are not familiar with programming, we do not recommend editing this file.

3. The “Test” button only runs the code in the current state. The code will not automatically run after rebooting the Raspberry Pi.

4. If the fans do no response after you modify the code and click “Test,” it indicates an error in your code preventing it from running properly. Please review your code.

5. If you want the Custom mode code to execute automatically on every startup, please refer to the instructions in the ":ref:`3.2.5 Settings Interface <fnk0100/codes/tutorial/3_app_control:3.2.5 settings interface>`" Section.

3.2.4 OLED Control Interface
==================================

This is the interface for controlling the OLED display content. You can choose from different display layouts according to your preference.

By default, the OLED cycles through four screens: Time, Usage, Temp, and Fan. If you uncheck any of these, that screen will be skipped during the cycle.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_31.png
    :align: center

Below are six customizable options. Click the drop-down lists to select different time formats, data display orders, display durations, and more.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_32.png
    :align: center

Adjusting Display Durations
-----------------------------------

The duration for each display screen can be adjusted by clicking the "**Sub**" button to decrease by 0.5s or the "**Add**" button to increase by 0.5s.

To adjust the display time for a single interface, simply uncheck the other screens so that only the desired one remains active.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_33.png
    :align: center

Modifying Date Format
---------------------------------

.. table::
    :class: table-line
    :align: center
    
    +----------------+----------------+
    | Options        | OLED Display   |
    +================+================+
    | |Chapter03_34| | |Chapter03_35| |
    +----------------+----------------+
    | |Chapter03_36| | |Chapter03_37| |
    +----------------+----------------+
    | |Chapter03_38| | |Chapter03_39| |
    +----------------+----------------+

.. |Chapter03_34| image:: ../_static/imgs/3_APP_Control/Chapter03_34.png
.. |Chapter03_35| image:: ../_static/imgs/3_APP_Control/Chapter03_35.png
.. |Chapter03_36| image:: ../_static/imgs/3_APP_Control/Chapter03_36.png
.. |Chapter03_37| image:: ../_static/imgs/3_APP_Control/Chapter03_37.png
.. |Chapter03_38| image:: ../_static/imgs/3_APP_Control/Chapter03_38.png
.. |Chapter03_39| image:: ../_static/imgs/3_APP_Control/Chapter03_39.png

Changing Time Format
---------------------------------

.. table::
    :class: table-line
    :align: center
    
    +----------------+----------------+
    | Options        | OLED Display   |
    +================+================+
    | |Chapter03_40| | |Chapter03_41| |
    +----------------+----------------+
    | |Chapter03_42| | |Chapter03_43| |
    +----------------+----------------+

.. |Chapter03_40| image:: ../_static/imgs/3_APP_Control/Chapter03_40.png
.. |Chapter03_41| image:: ../_static/imgs/3_APP_Control/Chapter03_41.png
.. |Chapter03_42| image:: ../_static/imgs/3_APP_Control/Chapter03_42.png
.. |Chapter03_43| image:: ../_static/imgs/3_APP_Control/Chapter03_43.png

Modifying the Display Order of CPU, MEM, and DISK Usage
------------------------------------------------------------------

.. table::
    :class: table-line
    :align: center
    
    +----------------+----------------+
    | Options        | OLED Display   |
    +----------------+----------------+
    | |Chapter03_44| | |Chapter03_45| |
    +----------------+----------------+
    | |Chapter03_46| | |Chapter03_47| |
    +----------------+----------------+
    | |Chapter03_48| | |Chapter03_49| |
    +----------------+----------------+
    | |Chapter03_50| | |Chapter03_51| |
    +----------------+----------------+
    | |Chapter03_52| | |Chapter03_53| |
    +----------------+----------------+
    | |Chapter03_54| | |Chapter03_55| |
    +----------------+----------------+

.. |Chapter03_44| image:: ../_static/imgs/3_APP_Control/Chapter03_44.png
.. |Chapter03_45| image:: ../_static/imgs/3_APP_Control/Chapter03_45.png
.. |Chapter03_46| image:: ../_static/imgs/3_APP_Control/Chapter03_46.png
.. |Chapter03_47| image:: ../_static/imgs/3_APP_Control/Chapter03_47.png
.. |Chapter03_48| image:: ../_static/imgs/3_APP_Control/Chapter03_48.png
.. |Chapter03_49| image:: ../_static/imgs/3_APP_Control/Chapter03_49.png
.. |Chapter03_50| image:: ../_static/imgs/3_APP_Control/Chapter03_50.png
.. |Chapter03_51| image:: ../_static/imgs/3_APP_Control/Chapter03_51.png
.. |Chapter03_52| image:: ../_static/imgs/3_APP_Control/Chapter03_52.png
.. |Chapter03_53| image:: ../_static/imgs/3_APP_Control/Chapter03_53.png
.. |Chapter03_54| image:: ../_static/imgs/3_APP_Control/Chapter03_54.png
.. |Chapter03_55| image:: ../_static/imgs/3_APP_Control/Chapter03_55.png

Changing the Display Order of Pi and Case Temperature
------------------------------------------------------------

.. table::
    :class: table-line
    :align: center
    
    +----------------+----------------+
    | Options        | OLED Display   |
    +----------------+----------------+
    | |Chapter03_56| | |Chapter03_57| |
    +----------------+----------------+
    | |Chapter03_58| | |Chapter03_59| |
    +----------------+----------------+

.. |Chapter03_56| image:: ../_static/imgs/3_APP_Control/Chapter03_56.png
.. |Chapter03_57| image:: ../_static/imgs/3_APP_Control/Chapter03_57.png
.. |Chapter03_58| image:: ../_static/imgs/3_APP_Control/Chapter03_58.png
.. |Chapter03_59| image:: ../_static/imgs/3_APP_Control/Chapter03_59.png

Adjusting the Display Order of Pi, C1, and C2 Fans PWM
------------------------------------------------------------

.. table::
    :class: table-line
    :align: center
    
    +----------------+----------------+
    | Options        | OLED Display   |
    +----------------+----------------+
    | |Chapter03_60| | |Chapter03_61| |
    +----------------+----------------+
    | |Chapter03_62| | |Chapter03_63| |
    +----------------+----------------+
    | |Chapter03_64| | |Chapter03_65| |
    +----------------+----------------+
    | |Chapter03_66| | |Chapter03_67| |
    +----------------+----------------+
    | |Chapter03_68| | |Chapter03_69| |
    +----------------+----------------+
    | |Chapter03_70| | |Chapter03_71| |
    +----------------+----------------+

.. |Chapter03_60| image:: ../_static/imgs/3_APP_Control/Chapter03_60.png
.. |Chapter03_61| image:: ../_static/imgs/3_APP_Control/Chapter03_61.png
.. |Chapter03_62| image:: ../_static/imgs/3_APP_Control/Chapter03_62.png
.. |Chapter03_63| image:: ../_static/imgs/3_APP_Control/Chapter03_63.png
.. |Chapter03_64| image:: ../_static/imgs/3_APP_Control/Chapter03_64.png
.. |Chapter03_65| image:: ../_static/imgs/3_APP_Control/Chapter03_65.png
.. |Chapter03_66| image:: ../_static/imgs/3_APP_Control/Chapter03_66.png
.. |Chapter03_67| image:: ../_static/imgs/3_APP_Control/Chapter03_67.png
.. |Chapter03_68| image:: ../_static/imgs/3_APP_Control/Chapter03_68.png
.. |Chapter03_69| image:: ../_static/imgs/3_APP_Control/Chapter03_69.png
.. |Chapter03_70| image:: ../_static/imgs/3_APP_Control/Chapter03_70.png
.. |Chapter03_71| image:: ../_static/imgs/3_APP_Control/Chapter03_71.png

3.2.5 Settings Interface
==================================

This interface integrates advanced customization features, allowing you to edit code, debug, and create startup tasks for the case LED lights, fans, and OLED display.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_72.png
    :align: center

Enable Terminal Display (For Debugging)
-----------------------------------------------

Before getting started, we can configure a desktop shortcut to run the software with a visible terminal window. This will allow you to view debug messages and other code output.

Steps:

Open the terminal on your Raspberry Pi.

Run the following command to set the correct permissions for the Freenove desktop software:

.. code-block:: console
    
    ls -al ~/Desktop/Freenove.desktop
    sudo chmod 777 ~/Desktop/Freenove.desktop

.. image:: ../_static/imgs/3_APP_Control/Chapter03_73.png
    :align: center

To revert to the default permissions, run the following command:

.. code-block:: console
    
    ls -al ~/Desktop/Freenove.desktop
    sudo chmod 755 ~/Desktop/Freenove.desktop

.. image:: ../_static/imgs/3_APP_Control/Chapter03_74.png
    :align: center

After modifying the permissions for Freenove.desktop, please follow these steps:

1. Close the current upper-computer software completely.

2. Double-click the Freenove software on the desktop to restart the application.

3. In the pop-up window, click Open to launch the software.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_75.png
    :align: center

Change the parameter of **Terminal** from false to **ture**, save and clost the file.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_76.png
    :align: center

Double click Freenove software on the desktop, click "**Execute**" upon the pop-up window to launch it

.. image:: ../_static/imgs/3_APP_Control/Chapter03_77.png
    :align: center

When you open the Freenove software control interface, a command terminal will automatically launch alongside it. All debug information and program logs will be displayed in this terminal window.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_78.png
    :align: center

Interface Configuration
----------------------------------

The "**Rotate UI**" button toggles the software interface instantly between landscape and portrait display modes.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_79.png
    :align: center

Clicking the "**Follow LED**" button activates synchronization between the LED effects and the Monitor interface. Once enabled, the color of the circular progress bar will mirror any real-time changes you make to the LED colors.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_80.png
    :align: center

The "**Default Color**" button reverts the circular progress bar (on the Monitor interface) to its default color.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_81.png
    :align: center

Code Editing and Testing
-----------------------------------------------

The Edit and Test buttons on the Settings interface allows for quick editing and testing of your code.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_82.png
    :align: center

You can open and edit the task_led.py, task_fan.py, task_oled.py files by click the corresponding Edit button.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_83.png
    :align: center

Similarly, you can click Test to quickly verify if the edited code performs as expected. Debug information will typically be printed in the terminal window.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_84.png
    :align: center

Background Task Management
-----------------------------------------------

This section is for comprehensive configuration. Here you can set up the software's interface features and configure background tasks for automatic operation of LEDs, fans, and the OLED display.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_85.png
    :align: center

Click the "**Create Service**" button creates a background system service on your Raspberry Pi. This service will automatically run every time the case boots up, ensuring that your customized task_led.py, task_fan.py, and task_oled.py scripts are executed after startup.

This service is activated with every boot of the Raspberry Pi 5.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_86.png
    :align: center

To prevent the background service from running on startup, click the Delete Service button to remove it.

**Delete Service:** Click to permanently remove the service. This prevents it from running automatically upon case startup.

**Run Tasks:** Click to temporarily start the service for immediate testing.

**Stop Tasks:** Click to temporarily halt the currently running service. 

.. image:: ../_static/imgs/3_APP_Control/Chapter03_87.png
    :align: center

You can enable the execution of one or more custom tasks by checking their corresponding boxes

Please Note:

When switching from the Settings interface to the LED or Fan control interface, the corresponding **LED Task** or **Fan Task** will be automatically unchecked, pausing their background operation. You can re-enable them by checking the boxes again.

To stop the custom LED task and use a built-in mode instead, simply switch from the Settings interface to the LED interface and select one of the preset modes (Rainbow, Breathing, Follow, or Manual). This action will automatically uncheck the **LED Task**.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_88.png
    :align: center

To stop the custom Fan Task and use a preset mode instead, simply switch from the Settings interface to the Fan interface and select one of the standard modes (Follow Case or Manual). This action will automatically uncheck the Fan Task.

.. image:: ../_static/imgs/3_APP_Control/Chapter03_89.png
    :align: center