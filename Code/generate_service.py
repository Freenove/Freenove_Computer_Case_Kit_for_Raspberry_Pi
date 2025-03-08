import os
import time
import sys
import shutil

DEBUG = False

def check_application_py(filenanme="application.py"):
    if not os.path.exists(filenanme):
        print("Error: {filenanme} does not exist in the current directory.")
        sys.exit(1)

def get_current_directory():
    if DEBUG:
        print("Getting current directory...")
    return os.getcwd()

def get_current_username_from_directory(directory):
    if DEBUG:
        print("Extracting username from directory path...")
    try:
        parts = directory.split('/')
        if len(parts) > 2 and parts[1] == 'home':
            return parts[2]
        else:
            print("Error: Unable to extract username from directory path.")
            sys.exit(1)
    except Exception as e:
        print(f"Error extracting username from directory path: {e}")
        sys.exit(1)

def create_my_app_running_service(directory, username):
    service_content = f"""[Unit]
Description=My Python Script Service

[Service]
ExecStart=/usr/bin/python3 {directory}/application.py
WorkingDirectory={directory}
StandardOutput=inherit
StandardError=inherit
Restart=always
User={username}

[Install]
WantedBy=multi-user.target
"""
    service_file_path = os.path.join('/etc/systemd/system/', 'my_app_running.service')
    if os.path.exists(service_file_path):
        os.remove(service_file_path)
        if DEBUG:
            print(f"Existing my_app_running.service file removed: {service_file_path}")
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)
    if DEBUG:
        print(f"my_app_running.service created at {service_file_path}")

def run_system_command(command):
    if DEBUG:
        print(f"Running command: {command}")
    try:
        result = os.system(command)
        if result != 0:
            print(f"Error executing command: {command}")
            sys.exit(1)
    except Exception as e:
        print(f"Error executing command: {command}")
        print(e)
        sys.exit(1)

def remove_pycache_folder(directory):
    pycache_path = os.path.join(directory, '__pycache__')
    if os.path.exists(pycache_path):
        try:
            shutil.rmtree(pycache_path)
            if DEBUG:
                print(f"__pycache__ folder removed: {pycache_path}")
        except Exception as e:
            print(f"Error removing __pycache__ folder: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # Step 1: Check if application.py exists
    check_application_py()

    # Step 2: Get current directory
    current_directory = get_current_directory()

    # Step 3: Get current username from directory
    current_username = get_current_username_from_directory(current_directory)

    print(f"Current Directory: {current_directory}")
    print(f"Current Username: {current_username}")

    # Step 4: Create my_app_running.service file
    create_my_app_running_service(current_directory, current_username)

    # Step 5: Run systemctl daemon-reload
    run_system_command("sudo systemctl daemon-reload")
    time.sleep(1)

    # Step 6: Enable my_app_running.service
    run_system_command("sudo systemctl enable my_app_running.service")
    time.sleep(1)

    '''
    # Disable my_app_running.service
    run_system_command("sudo systemctl disable my_app_running.service")
    time.sleep(1)

    # Stop my_app_running.service
    run_system_command("sudo systemctl stop my_app_running.service")
    time.sleep(1)
    '''

    # Step 7: Start my_app_running.service
    run_system_command("sudo systemctl start my_app_running.service")
    time.sleep(1)
    
    remove_pycache_folder(current_directory)


