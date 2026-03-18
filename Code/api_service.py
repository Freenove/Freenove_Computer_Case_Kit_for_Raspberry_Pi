import os
import time
import sys
import shutil

class ServiceGenerator:
    def __init__(self, filename="task_manager.py", service_name="my_app_running.service"):
        self.filename = filename
        self.service_name = service_name
        self.current_directory = None
        self.current_username = None
        self.get_current_directory()
        self.get_current_username_from_directory(self.current_directory)
        
    def check_target_py(self):
        """Check if target Python file exists"""
        if not os.path.exists(self.filename):
            print(f"Error: {self.filename} does not exist in the current directory.")
            sys.exit(1)
            
    def get_current_directory(self):
        """Get current directory path"""
        self.current_directory = os.getcwd()
        return self.current_directory
        
    def get_current_username_from_directory(self, directory):
        """Extract username from directory path"""
        try:
            parts = directory.split('/')
            if len(parts) > 2 and parts[1] == 'home':
                self.current_username = parts[2]
                return self.current_username
            else:
                print("Error: Unable to extract username from directory path.")
                sys.exit(1)
        except Exception as e:
            print(f"Error extracting username from directory path: {e}")
            sys.exit(1)
            
    def create_my_service(self):
        """Create systemd service file"""
        if not self.current_directory or not self.current_username:
            print("Error: Directory or username not set.")
            sys.exit(1)
            
        service_content = f"""[Unit]
Description=My Python Script Service

[Service]
ExecStart=/usr/bin/python3 {self.current_directory}/{self.filename}
WorkingDirectory={self.current_directory}
StandardOutput=inherit
StandardError=inherit
Restart=always
User={self.current_username}

[Install]
WantedBy=multi-user.target
"""
        service_file_path = os.path.join('/etc/systemd/system/', self.service_name)
        if os.path.exists(service_file_path):
            os.remove(service_file_path)
        with open(service_file_path, 'w') as service_file:
            service_file.write(service_content)
    
    def delete_my_service(self):
        """Delete systemd service file"""
        service_file_path = os.path.join('/etc/systemd/system/', self.service_name)
        if os.path.exists(service_file_path):
            os.remove(service_file_path)
        else:
            print(f"Error: {self.service_name} does not exist.")    

    def check_service_is_exist(self):
        """Check if service file exists"""
        service_file_path = os.path.join('/etc/systemd/system/', self.service_name)
        return os.path.exists(service_file_path)
    
    def run_system_command(self, command):
        """Execute system command"""
        try:
            result = os.system(command)
            if result != 0:
                print(f"Error executing command: {command}")
                sys.exit(1)
        except Exception as e:
            print(f"Error executing command: {command}")
            print(e)
            sys.exit(1)
            
    def remove_pycache_folder(self):
        """Remove __pycache__ folder"""
        pycache_path = os.path.join(self.current_directory, '__pycache__')
        if os.path.exists(pycache_path):
            try:
                shutil.rmtree(pycache_path)
            except Exception as e:
                print(f"Error removing __pycache__ folder: {e}")
                sys.exit(1)
              
    def create_service_on_rpi(self):
        """Run service on Raspberry Pi"""
        self.check_target_py()  
        self.create_my_service()    
        self.run_system_command("sudo systemctl daemon-reload")
        time.sleep(1)
        self.run_system_command(f"sudo systemctl enable {self.service_name}")
        self.remove_pycache_folder()
    
    def delete_service_on_rpi(self):
        """Delete service on Raspberry Pi"""
        self.run_system_command(f"sudo systemctl stop {self.service_name}")
        self.delete_my_service()
        self.run_system_command(f"sudo systemctl disable {self.service_name}")

    def run_service_on_rpi(self):
        """Run service on Raspberry Pi"""
        if self.check_service_is_exist():
            self.run_system_command(f"sudo systemctl start {self.service_name}")
        else:
            print(f"Error: {self.service_name} does not exist.")

    def stop_service_on_rpi(self):
        """Stop service on Raspberry Pi"""
        if self.check_service_is_exist():
            self.run_system_command(f"sudo systemctl stop {self.service_name}")
        else:
            print(f"Error: {self.service_name} does not exist.")

    def restart_service_on_rpi(self):
        """Restart service on Raspberry Pi"""
        if self.check_service_is_exist():
            self.run_system_command(f"sudo systemctl restart {self.service_name}")
        else:
            print(f"Error: {self.service_name} does not exist.")

    def generate_and_run_service(self):
        """Execute complete service generation and run process"""
        # Step 1: Check if target file exists
        self.check_target_py()
        
        # Step 2: Get current directory
        self.get_current_directory()
        
        # Step 3: Extract username from directory
        self.get_current_username_from_directory(self.current_directory)
        
        # Step 4: Create service file
        self.create_my_service()
        
        # Step 5: Run systemctl daemon-reload
        self.run_system_command("sudo systemctl daemon-reload")
        time.sleep(1)
        
        # Step 6: Enable service
        self.run_system_command(f"sudo systemctl enable {self.service_name}")
        time.sleep(1)
        
        # Step 7: Start service
        self.run_system_command(f"sudo systemctl start {self.service_name}")
        time.sleep(1)
        
        # Remove __pycache__ folder
        self.remove_pycache_folder()
        
        # Output shortcut command tips
        self.print_shortcut_commands()
        
    def print_shortcut_commands(self):
        """Print shortcut command tips"""
        print("*"*50)
        print("Here are some shortcut commands.")
        print("Create boot background task:          sudo systemctl enable my_app_running.service")
        print("Disable boot background task:         sudo systemctl disable my_app_running.service")
        print("Temporarily start background task:    sudo systemctl start my_app_running.service")
        print("Temporarily stop background task:     sudo systemctl stop my_app_running.service")
        print("Temporarily restart background task:  sudo systemctl restart my_app_running.service")
        print("*"*50)
        print("")

# Usage example
if __name__ == "__main__":
    generator = ServiceGenerator()
    generator.generate_and_run_service()