##############################################################################
Installing Raspberry Pi OS
##############################################################################

After the assembly is complete, we will start installing the system for the Raspberry Pi. Regardless of whether you want to install the system on the NVMe SSD or not, you need to install the system on an SD card or USB flash drive first.

**Analysis**

1. First of all, make sure you can enter the Raspberry Pi OS via SD card or U drive.

2. After booting the Raspberry Pi, you can use it to flash the OS image directly onto the NVMe SSD. Alternatively, you can purchase an NVMe SSD to USB adapter and flash the image using USB on Windows or macOS, much like you would for an SD card or USB drive.

3. With this analysis in mind, we can systematically carry out the necessary steps.

Raspberry Pi models manufactured at different times might not boot up in the same way as described, but that's okay; just follow our guide to proceed.

There are various ways to burn the Raspberry Pi OS to SSD, each requiring different hardware tools.

.. table::
    :class: zebra
    :align: center
    
    +------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+
    | Ways | Ways of burning                                                                                                                                                        | Requirements                                                |
    +======+========================================================================================================================================================================+=============================================================+
    | 1    | Use Raspberry Pi to burn the OS. This requires that you can successfully boot up the Raspberry Pi via SD card or U disk. (**Recommended, described in this tutorial**) | An SD card or a U disk that can access the Raspberry Pi OS. |
    +------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+
    | 2    | Purchase an NVMe SSD to USB adapter and flash the image just like you would with an SD card or USB drive.                                                              | NVME SSD to USB adapter (need to be bought separately)      |
    +------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+
    | 3    | If there are spare M.2 NVME interface on the motherboard of your PC, you can insert the SSD to it to flash the OS.                                                     | PC with M.2 NVME interface                                  |
    +------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+

.. _Incompatible_SSDs:

**Caution: Incompatible SSDs**

The recognition and read/write operations of the NVMe SSD are handled by the drivers of the Raspberry Pi 5. If you find that your SSD cannot be recognized by Pi 5 or is not readable/writable, please try to find a driver suitable for your SSD and install it on the Raspberry Pi, or replace the SSD, or purchase the adapter kit that comes with the SSD.

1 Flashing OS to SD Card or USB Drive
************************************************

Based on the analysis above, our first step should be to install the Raspberry Pi operating system onto an SD card or USB drive, with a capacity of at least 16GB. If you are already able to boot the Raspberry Pi using an SD card or USB drive, you can :ref:`skip this section and move on to the next section <fnk0100/codes/install/installing_raspberry_pi_os:2 flashing os to nvme ssd>`.

1.1 Component List
===============================

Required Components
--------------------------------

.. table::
    :class: table-line
    :align: center
    
    +----------------------+---------------------------------------------------------------------------------------------------------------------------------------+
    | Raspberry Pi 5 x 1   | One 27W power adapter (:combo:`red font-bolder:or a power adapter compatible with Raspberry Pi official one that can output 5.1V/5A`) |
    |                      |                                                                                                                                       |
    | |Install04|          | |Install05|                                                                                                                           |
    +----------------------+---------------------------------------------------------------------------------------------------------------------------------------+
    | Micro SD Card(TF Card)x1, Card Reader x1                                                                                                                     |
    |                                                                                                                                                              |
    | |Install06|                                                                                                                                                  |
    +----------------------+---------------------------------------------------------------------------------------------------------------------------------------+

.. |Install04| image:: ../_static/imgs/Install/Install04.png
.. |Install05| image:: ../_static/imgs/Install/Install05.png
.. |Install06| image:: ../_static/imgs/Install/Install06.png

1.2 Raspberry Pi OS
===============================

**Without Screen - Use Raspberry Pi - under Windows PC:**

.. raw:: html

   <iframe style="display: block; margin: 0 auto;" height="421.875" width="750" src="https://www.youtube.com/embed/XpiT_ezb_7c" frameborder="0" allowfullscreen></iframe>

**With Screen - Use Raspberry Pi - under Windows PC:**

.. raw:: html

   <iframe style="display: block; margin: 0 auto;" height="421.875" width="750" src="https://www.youtube.com/embed/HEywFsFrj3I" frameborder="0" allowfullscreen></iframe>

Automatically Method (Recommended)
------------------------------------------

You can follow the official method to install the system for raspberry pi via visiting link below:

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2

In this way, the system will be downloaded automatically via the application. 

Manually Methed
------------------------------------------

After installing the Imager Tool in the **link above**. You can **also** download the system **manually** first. (:combo:`red font-bolder:Note: Unless necessary, it is not recommended to manually download the offline installation package.`)

Visit https://www.raspberrypi.com/software/operating-systems/  

.. image:: ../_static/imgs/Install/Install07.png
    :align: center

Choose Raspberry Pi Device
------------------------------------------

First, put your Micro **SD card** into card reader and connect it to USB port of PC. 

.. image:: ../_static/imgs/Install/Install08.png
    :align: center

Open Raspberry Pi Imager. 

Select **Raspberry Pi 5** under Device, and then click NEXT.

.. image:: ../_static/imgs/Install/Install09.png
    :align: center

Choose Operating System
------------------------------------------

Click OS, scroll down to **locate and click Raspberry Pi OS (other)**, and then select **Raspberry Pi OS Full(64-bit)**. Click NEXT.

.. image:: ../_static/imgs/Install/Install10.png
    :align: center

Choose Storage Devide
------------------------------------------

Choose the SD card and click on Next. 

.. image:: ../_static/imgs/Install/Install11.png
    :align: center

Customisation
------------------------------------------

Step 1: Input the hostname, which is **"raspberrypi"** by default. Then click NEXT.

.. image:: ../_static/imgs/Install/Install12.png
    :align: center

Step 2: Select your location, timezone and keyboard layout. Then click NEXT.

.. image:: ../_static/imgs/Install/Install13.png
    :align: center

Step 3: Configure your username and passowrd. The password needs to re-enter to confirm. The default username is pi and the default password is raspberry. Then click NEXT.

.. image:: ../_static/imgs/Install/Install14.png
    :align: center

Step 4: Input the SSID and password of your wireless network. The passwords needs to re-enter to confirm. Then click NEXT.

.. image:: ../_static/imgs/Install/Install15.png
    :align: center

Step 5: Enable SSH for ssh remote and click NEXT.

.. image:: ../_static/imgs/Install/Install16.png
    :align: center

Step 6: Click NEXT.

.. image:: ../_static/imgs/Install/Install17.png
    :align: center

Writing System to Micro SD Card
------------------------------------------

After finishing customisation configuration, the interface will show all the configuration you have made. Click WRITE to write the OS to your SD card after confirming everything is correct.

.. image:: ../_static/imgs/Install/Install18.png
    :align: center

:red:`Warning: Before starting the write process, ensure you have backed up all data on the storage device. This operation will permanently erase all data on the device. If you have completed the backup, click` :combo:`red font-bolder:I UNDERSTAND, ERASE AND WRITE` :red:`to continue.`

.. image:: ../_static/imgs/Install/Install19.png
    :align: center

Wait for it to finish writing and verifying.

.. image:: ../_static/imgs/Install/Install20.png
    :align: center

Done
--------

Congratulations! The Raspberry Pi OS has been successfully written to the SD card. All your custom configurations have taken effect. Click FINISH to complete the process.

.. image:: ../_static/imgs/Install/Install21.png
    :align: center

1.3 HDMI Monitor desktop
===================================

If you do not have a spare monitor, please skip to next section :ref:`Remote desktop & VNC <fnk0100/codes/install/important_information:about freenove>`. If you have a spare monitor, please follow the steps in this section. 

Connect the Raspberry Pi 5 to your display via the HDMI interface, attach your mouse and keyboard through the USB ports, and finally, connect your power supply (making sure that it meets the specifications required by your RPi Module Version. Your RPi should start (power up). Later, after setup, you will need to enter your user name and password to login. The default user name: pi; password: raspberry. After login, you should see the following screen.

.. image:: ../_static/imgs/Install/Install22.png
    :align: center

Congratulations! You have successfully installed the RASPBERRY PI OS on your RPi.

Raspberry Pi 5 integrates a Wi-Fi adaptor. You can use it to connect to your Wi-Fi. Then you can use the wireless remote desktop to control your RPi. This will be helpful for the following work. 

.. image:: ../_static/imgs/Install/Install23.png
    :align: center

1.4 Remote desktop & VNC
===================================

If you don't have a spare display, mouse and keyboard for your RPi, you can use a remote desktop to share a display, keyboard, and mouse with your PC. Below is how to use: 

:ref:`MAC OS remote desktop <fnk0100/codes/install/installing_raspberry_pi_os:mac os remote desktop>` and :ref:`Windows OS remote desktop <fnk0100/codes/install/installing_raspberry_pi_os:windows os remote desktop>`.

Mac OS Remote desktop
-------------------------------

Open the terminal and type following command.

If you have set your own hostname during writing the OS, please modify it accordingly.

:combo:`red font-bolder:If this command doesn't work, please move to next page.`

.. code-block:: console
    
    ssh pi@raspberrypi.local

The password is :blue:`raspberry` by default, case sensitive.

.. image:: ../_static/imgs/Install/Install24.png
    :align: center

You may need to type **yes** during the process.

.. image:: ../_static/imgs/Install/Install25.png
    :align: center

You can also use the IP address to log in Pi. 

Enter **router** client to **inquiry IP address** named "raspberry pi". For example, I have inquired to **my RPi IP address, and it is "192.168.1.131".**

Open the terminal and type following command.

.. code-block:: console
    
    ssh pi@192.168.1.131

When you see :green:`pi@raspberrypi`::blue:`~ $`, you have logged in Pi successfully. Then you can skip to next section.

.. image:: ../_static/imgs/Install/Install26.png
    :align: center

Then you can skip to :ref:`VNC Viewer <fnk0100/codes/install/installing_raspberry_pi_os:1.5 vnc viewer & vnc>`.

Windows OS remote desktop
-------------------------------

**If you are using win10, you can use follow way to login Raspberry Pi without desktop.**

Press Win+R. Enter cmd. Then use this command to check IP:

.. code-block:: console
    
    ping -4 raspberrypi.local

.. image:: ../_static/imgs/Install/Install27.png
    :align: center

Then 192.168.1.147 is my Raspberry Pi IP.

Or enter **router** client to **inquiry IP address** named **"raspberrypi"**. For example, I have inquired to **my RPi IP address, and it is "192.168.1.147".**

.. code-block:: console
    
    ssh pi@xxxxxxxxxxx(IP address)

Enter the following command：

.. code-block:: console
    
    ssh pi@192.168.1.147

.. image:: ../_static/imgs/Install/Install28.png
    :align: center

1.5 VNC Viewer & VNC
===================================

Enable VNC
-----------------------

Enter the following commands: select Interface Options -> I3 VNC -> Enter -> Yes -> OK. You may need to restart the Raspberry Pi 5 here, select OK, and then open the VNC interface.

.. code-block:: console
    
    sudo raspi-config

.. image:: ../_static/imgs/Install/Install29.png
    :align: center

Set Resolution
-----------------------

You can also set other resolutions. If you don't know what to set, you can set it as 800x600 first.

.. image:: ../_static/imgs/Install/Install30.png
    :align: center

.. image:: ../_static/imgs/Install/Install31.png
    :align: center

Then download and install VNC Viewer according to your computer system by click following link:

https://www.realvnc.com/en/connect/download/viewer/

After installation is completed, open VNC Viewer. And click File -> New Connection. Then the interface is shown below.

.. image:: ../_static/imgs/Install/Install32.png
    :align: center

Enter ip address of your Raspberry Pi and fill in a name. Then click OK.

Then on the VNC Viewer panel, double-click new connection you just created, 

.. image:: ../_static/imgs/Install/Install33.png
    :align: center

Then the following dialog box pops up.

Enter username: **pi** and Password: **raspberry**. 

If you have set your own username and password, please input them accordingly. Then click OK.

.. image:: ../_static/imgs/Install/Install34.png
    :align: center

Here, you have logged in to Raspberry Pi successfully by using VNC Viewer.

.. image:: ../_static/imgs/Install/Install35.png
    :align: center

If there is black window, please :ref:`set another resolution <fnk0100/codes/install/installing_raspberry_pi_os:set resolution>`.

.. image:: ../_static/imgs/Install/Install36.png
    :align: center

In addition, your VNC Viewer window may zoom your Raspberry Pi desktop. You can change it. On your VNC View control panel, click right key. And select Properties->Options label->Scaling. Then set proper scaling. 

.. image:: ../_static/imgs/Install/Install37.png
    :align: center

Here, you have logged in to Raspberry Pi successfully by using VNC Viewer and operated proper setting.

Raspberry Pi 5 integrates a Wi-Fi adaptor.If you did not connect Pi to WiFi. You can connect it to wirelessly control the robot.

.. image:: ../_static/imgs/Install/Install38.png
    :align: center

2 Flashing OS to NVMe SSD
*************************************

This step is to install the Raspberry Pi OS into the NVME SSD.

2.1 SSD Detection
==============================

:ref:`(Note: Not all SSDs are supported by Pi5.) <Incompatible_SSDs>`

**Booting the Rpi 5 from SD card**, and run the following command in the Terminal to check whether SSD is detected.

**Note that the information varies among SSDs.**

.. code-block:: console
    
    lspci

.. image:: ../_static/imgs/Install/Install39.png
    :align: center

.. code-block:: console
    
    lsblk

.. image:: ../_static/imgs/Install/Install40.png
    :align: center

As shown in the figure above, the device 'nvme0n1' with a capacity of 476.9GBytes shows up, indicating that the SSD has been correctly recognized. The detected capacity will depend on the size of your SSD. If your drive has been previously partitioned, you may also see some partition information displayed.

**Please note: Installing the system will format the SSD, erasing all data. If necessary, please back up any data on your SSD before proceeding.**

2.2 Enable PCIe 3.0(on OS written into SD Card)
=====================================================

If your SSD with Phison controller, you may need to enable PCIE 3.0. (This step is strongly recommended; without this step, the later process may fail.) 

If it is not with Phison controller, you do not need to enable PCIE 3.0. :ref:`You may skip this section <fnk0100/codes/install/installing_raspberry_pi_os:2.3 ssd partitioning and formatting>`.

Run the command ``lspci`` to check the controller.

.. image:: ../_static/imgs/Install/Install41.png
    :align: center

(The above screenshot is the result of a 128GB SSD with Phison as main controller.)

Enable PCIe Gen 3.0
--------------------------

Add the line ``dtparam=pciex1_gen=3`` to /boot/firmware/config.txt to enable PCIe Gen3.0.

As shown below, enter the command to open the file.

.. code-block:: console
    
    sudo nano /boot/firmware/config.txt

Add the line ``dtparam=pciex1_gen=3`` to the end of the file, as shown below:

.. image:: ../_static/imgs/Install/Install42.png
    :align: center

Press Ctrl-O to save the file, Enter to confirm, and Ctrl-X to exit.

Reboot your Raspberry Pi.

.. code-block:: console
    
    sudo reboot

2.3 SSD Partitioning and Formatting
===============================================

**This step is not a must-do, but it can further test whether the SSD perform normally on Raspberry Pi** to ensure smooth performance in later steps.

At this point, the hard drive cannot be seen in the file manager as the disk has not been partitioned yet.

.. image:: ../_static/imgs/Install/Install43.png
    :align: center

Install a disk management tool with the following command:

.. code-block:: console
    
    sudo apt-get install gparted

.. image:: ../_static/imgs/Install/Install44.png
    :align: center

Open gparted with the command:

.. code-block:: console
    
    sudo gparted

.. image:: ../_static/imgs/Install/Install45.png
    :align: center

Click on the dropdown menu in the upper right corner and switch to NVME SSD.

.. image:: ../_static/imgs/Install/Install46.png
    :align: center

Click Device on the menu bar and select Create Partition Table.

.. image:: ../_static/imgs/Install/Install47.png
    :align: center

You will see the prompt that data will be erased. It is recommended to select gpt for partition table type. Click Apply.

.. image:: ../_static/imgs/Install/Install48.png
    :align: center

Click Partition on the menu bar, choose New.

.. image:: ../_static/imgs/Install/Install49.png
    :align: center

As shown in the figure below, the size of partition can be adjusted by dragging the mouse left and right, or by entering the size directly. The other options can be left as default setting. Here, we allocate all the capacity to a single partition. Click on Add.

.. image:: ../_static/imgs/Install/Install50.png
    :align: center

Click the check icon ✔ to save the partition just built, as illustrated below.

.. image:: ../_static/imgs/Install/Install51.png
    :align: center

Click on Apply.

.. image:: ../_static/imgs/Install/Install52.png
    :align: center

Wait for it to complete and click on Close.

.. image:: ../_static/imgs/Install/Install53.png
    :align: center

At this point, you can mount the disk using the mount command and then access the disk space through the file manager. Use the following command to mount the SSD:

.. code-block:: console
    
    mkdir pi
    sudo mount /dev/nvme0n1p1 /media/pi

.. image:: ../_static/imgs/Install/Install54.png
    :align: center

Open the file manager, as shown below.

.. image:: ../_static/imgs/Install/Install55.png
    :align: center

If you plan to use the SSD as a standard storage device, you can conclude the process here. However, if you want to further proceed with installing an operating system on the SSD, please read on.

2.4 Flashing the OS
=============================

Install the OS to SSD with the method similar to that in the previous section on installing a system onto an SD card. This time, operate on the Raspberry Pi.

Install rpi-imager with the following command:

.. code-block:: console
    
    sudo apt install rpi-imager

.. image:: ../_static/imgs/Install/Install56.png
    :align: center

Open rpi-imager:

.. code-block:: console
    
    sudo rpi-imager

.. image:: ../_static/imgs/Install/Install57.png
    :align: center

By this point, you should be quite familiar with the process.

Select the Raspberry Pi 5 as your device and choose the online download for the operating system. (It is recommended to use a 64-bit Raspberry Pi system with recommended software). Choose your NVME SSD as the storage device. Click NEXT.

.. image:: ../_static/imgs/Install/Install58.png
    :align: center

Enter the hostname.

.. image:: ../_static/imgs/Install/Install59.png
    :align: center

Select your location, timezone and keyboard layout. Then click NEXT.

.. image:: ../_static/imgs/Install/Install60.png
    :align: center

Configure your username and passowrd. The password needs to re-enter to confirm. 

.. image:: ../_static/imgs/Install/Install61.png
    :align: center

Step 4: Input the SSID and password of your wireless network. The passwords needs to re-enter to confirm. Then click NEXT.

.. image:: ../_static/imgs/Install/Install62.png
    :align: center

Enable SSH for ssh remote and click NEXT.

.. image:: ../_static/imgs/Install/Install63.png
    :align: center

After finishing customisation configuration, the interface will show all the configuration you have made. Click **WRITE** to write the OS to your SD card after confirming everything is correct.

.. image:: ../_static/imgs/Install/Install64.png
    :align: center

:red:`Warning: Before starting the write process, ensure you have backed up all data on the storage device. This operation will permanently erase all data on the device. If you have completed the backup, click` :combo:`red font-bolder:I UNDERSTAND, ERASE AND WRITE` :red:`to continue.`

.. image:: ../_static/imgs/Install/Install65.png
    :align: center

Wait for it to finish writing and verifying.

.. image:: ../_static/imgs/Install/Install66.png
    :align: center

Congratulations! You have done the trickiest and the time-consuming part. Now that you have successfully installed the operating system onto the NVMe SSD, you are very close to achieving a triumph. 

.. image:: ../_static/imgs/Install/Install67.png
    :align: center

Next, boot into the system from SSD.

2.5 Enable PCIe 3.0 (on system written into SSD)
=======================================================

:red:`Note: This section does not apply to the Dual-NVMe Adapter Board or the Quad-NVMe Adapter Board, as they do not support the PCIe 3.0 protocol. If enabled, it may fail to boot from SSD.`

If you have confirmed that SSD is with Phison controller in :ref:`step 2 <fnk0100/codes/install/installing_raspberry_pi_os:2.2 enable pcie 3.0(on os written into sd card)>`, then you also need to enable PCIE3.0 on the system written into SSD.

If the controller of your SSD is not from Phison, :ref:`you can skip this section <fnk0100/codes/install/installing_raspberry_pi_os:2.6 booting from ssd>`.

The operation is as below:

Run the command ``lsblk`` to check the partitions of the SSD with Raspberry Pi OS written, as shown below:

.. image:: ../_static/imgs/Install/Install68.png
    :align: center

(The above screenshot is the result of a 128GB SSD with Phison as main controller.)

Run the following commands one by one to mount partition 1 of the SSD to the directory of /media/pi.

.. code-block:: console
    
    sudo mkdir /media/pi
    sudo mount /dev/nvme0n1p1 /media/pi

.. image:: ../_static/imgs/Install/Install69.png
    :align: center

If it mounts successfully, you'll see the following disk icon on the desktop.

.. image:: ../_static/imgs/Install/Install70.png
    :align: center

Open and modify the config.txt file with the following command.

.. code-block:: console
    
    sudo nano /media/pi/config.txt

.. image:: ../_static/imgs/Install/Install71.png
    :align: center

Add the line ``dtparam=pciex1_gen=3`` to the end of the file, as shown below:

.. image:: ../_static/imgs/Install/Install72.png
    :align: center

Press Ctrl-O to save the file, Enter to confirm, and Ctrl-X to exit.

2.6 Booting from SSD
=============================

After finishing flashing the OS to SSD, shutdown Raspberry Pi, **remove the power supply, and remove the SD card. Then connect the power, the Raspberry Pi will boot from SSD.**

The default boot order of Raspberry Pi is SD card -> SSD -> USB, Therefore, when the SD card is removed, the Raspberry Pi cannot detect the SD card, it will boot from SSD. By far, the Raspberry Pi can boot successfully from NVME SSD.

.. image:: ../_static/imgs/Install/Install73.png
    :align: center

If you want the Raspberry Pi to boot from the SSD first, please continue with the following steps to modify the boot order. The boot order is saved in the Pi’s EEPROM, so it does not matter whether you modify the boot order on SD card system or SSD system.

If you do not want to change the boot order, please skip this chapter.

Configuring the Boot Order
------------------------------------

Type the following command in the Terminal.

.. code-block:: console
    
    sudo raspi-config

.. image:: ../_static/imgs/Install/Install74.png
    :align: center

Using the keyboard's arrow keys and the Enter key, select the options in sequence.

"6 Advanced Options" -> "A4 Boot Order" -> "B2 NVME/USB Boot ..."

.. image:: ../_static/imgs/Install/Install75.png
    :align: center

Select "OK" -> "Finish" -> "Yes", and reboot your Raspberry Pi.

.. image:: ../_static/imgs/Install/Install76.png
    :align: center

At this point, upon restarting, the Raspberry Pi will boot from the NVME SSD first. If you are using an external monitor, you will see that the Raspberry Pi has booted up correctly. If your SD card is still inserted, you will also see an icon on the desktop as shown below. 

With this, the process of booting the Raspberry Pi from the NVME SSD has been fully completed.

.. image:: ../_static/imgs/Install/Install77.png
    :align: center

If you use VNC viewer, you will need to repeat the previous steps to activate the VNC service as it is not yet enabled in the new system on the SSD. Here, we take Windows as an example.

Run the following command:

.. code-block:: console
    
    ssh pi@raspberrypi.local

.. image:: ../_static/imgs/Install/Install78.png
    :align: center

Once successfully ssh into Raspberry Pi, run the following command to open the configuration and enable VNC.

.. code-block:: console
    
    sudo raspi-config

Select "3 Interface Options" -> "I2 VNC" -> "Yes" -> "Finish".

.. image:: ../_static/imgs/Install/Install79.png
    :align: center

Now you should be able to access Raspberry Pi via VNC.