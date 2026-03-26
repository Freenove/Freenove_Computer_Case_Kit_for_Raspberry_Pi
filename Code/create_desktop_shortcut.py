import os
import sys

class DesktopShortcutCreator:
    def __init__(self, name="FNK0100", comment="Freenove Computer Case Kit for Raspberry Pi"):
        self.name = name
        self.comment = comment
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
    def set_name(self, name):
        """Set desktop shortcut name"""
        self.name = name
        return self
        
    def set_comment(self, comment):
        """Set desktop shortcut comment"""
        self.comment = comment
        return self
        
    def _get_original_user_home(self):
        """Get the original user's home directory when running with sudo"""
        # Check if running with sudo
        sudo_user = os.environ.get('SUDO_USER')
        
        if sudo_user:
            # Running with sudo, get the original user's home
            import pwd
            try:
                user_info = pwd.getpwnam(sudo_user)
                return user_info.pw_dir
            except KeyError:
                # Fallback if we can't find the user info
                print(f"Warning: Could not get home directory for user {sudo_user}, using /home/pi as fallback")
                return "/home/pi"
        else:
            # Not running with sudo, use current user's home
            return os.path.expanduser("~")
    
    def _get_desktop_path(self):
        """Get desktop path"""
        try:
            # Try to get the original user's home directory
            home_dir = self._get_original_user_home()
        except Exception:
            # If getting username fails, use default pi user
            home_dir = "/home/pi"
            print("Warning: Unable to get current username, using default path /home/pi")
        
        return os.path.join(home_dir, "Desktop")
    
    def _ensure_desktop_directory(self, desktop_dir):
        """Ensure desktop directory exists and is writable"""
        # Ensure desktop directory exists
        if not os.path.exists(desktop_dir):
            try:
                os.makedirs(desktop_dir, mode=0o755, exist_ok=True)
                print(f"Created desktop directory: {desktop_dir}")
            except Exception as e:
                raise Exception(f"Failed to create desktop directory: {e}")
        
        # Check if desktop directory is valid and writable
        if not os.path.isdir(desktop_dir):
            raise Exception(f"Desktop directory {desktop_dir} is not a valid directory")
        
        if not os.access(desktop_dir, os.W_OK):
            raise Exception(f"Desktop directory {desktop_dir} does not have write permission")
    
    def _validate_files(self):
        """Validate required files exist"""
        run_script_path = os.path.join(self.current_dir, "run_app.sh")
        if not os.path.exists(run_script_path):
            raise FileNotFoundError(f"Script file {run_script_path} does not exist")

        icon_path = os.path.join(self.current_dir, "Freenove_Logo.xpm")
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"Icon file {icon_path} does not exist")
        
        return run_script_path, icon_path
    
    def _create_application_content(self, run_script_path, icon_path):
        """Create Application-type desktop file content"""
        return f"""[Desktop Entry]
Version=1.0
Type=Application
Name={self.name}
Comment={self.comment}
Exec=bash {run_script_path}
Icon={icon_path}
Terminal=false
Categories=Application;Development;
"""
    
    def _make_executable(self, file_path, run_script_path=None):
        """Make file executable, optionally also make the run script executable"""
        try:
            os.chmod(file_path, 0o755)
            if run_script_path:
                # Also make the run_app.sh script executable
                os.chmod(run_script_path, 0o755)
        except Exception as e:
            raise Exception(f"Error setting file permissions: {e}")
    
    def _clean_pycache(self):
        """Clean __pycache__ folder"""
        pycache_path = os.path.join(self.current_dir, "__pycache__")
        if os.path.exists(pycache_path) and os.path.isdir(pycache_path):
            try:
                # Recursively remove __pycache__ directory and its contents using os module
                for root, dirs, files in os.walk(pycache_path, topdown=False):
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        os.rmdir(dir_path)
                os.rmdir(pycache_path)
            except Exception as e:
                print(f"Warning: Failed to remove __pycache__ folder: {e}")
    
    def create_shortcut_to_desktop(self, target_filename=None):
        """Create a desktop link shortcut (Type=Link) directly on the desktop"""
        try:
            # Get desktop path
            desktop_dir = self._get_desktop_path()

            # Ensure desktop directory exists and is writable
            self._ensure_desktop_directory(desktop_dir)

            # Use provided target filename or default to current name
            if target_filename:
                target_name = target_filename.replace(' ', '_')
            else:
                target_name = self.name.replace(' ', '_')

            # Validate required files
            run_script_path, icon_path = self._validate_files()

            # Get original user's home directory for the URL
            original_user_home = self._get_original_user_home()
            apps_dir = os.path.join(original_user_home, ".local/share/applications")
            url_path = os.path.join(apps_dir, f"{target_name}.desktop")

            # Create desktop file content with Type=Link
            application_content = f"""[Desktop Entry]
Version=1.0
Type=Link
Name={self.name}
Comment={self.comment}
Icon={icon_path}
URL={url_path}
"""

            # Destination path on desktop
            destination_path = os.path.join(desktop_dir, f"{target_name}.desktop")

            # Write desktop file directly to desktop
            try:
                with open(destination_path, 'w', encoding='utf-8') as f:
                    f.write(application_content)
                print(f"Created desktop link file directly on desktop: {destination_path}")
            except Exception as e:
                raise Exception(f"Error creating desktop file: {e}")

            # Make the file executable
            self._make_executable(destination_path)

            return True

        except FileNotFoundError as e:
            print(f"File not found error: {e}")
            return False
        except PermissionError as e:
            print(f"Permission error: {e}")
            return False
        except Exception as e:
            print(f"Operation failed: {e}")
            return False
    
    def remove_shortcut_from_desktop(self, target_filename=None):
        """Remove desktop link shortcut from desktop"""
        try:
            # Get desktop path
            desktop_dir = self._get_desktop_path()
            
            # Use provided target filename or default to current name
            if target_filename:
                target_name = target_filename.replace(' ', '_')
            else:
                target_name = self.name.replace(' ', '_')
            
            # Path to the file on desktop
            desktop_path = os.path.join(desktop_dir, f"{target_name}.desktop")
            
            # Check if file exists before attempting to remove
            if os.path.exists(desktop_path):
                # Remove file using os.remove
                os.remove(desktop_path)
                print(f"Successfully removed desktop file from desktop: {desktop_path}")
                return True
            else:
                print(f"Desktop file does not exist on desktop: {desktop_path}")
                return False
                
        except Exception as e:
            print(f"Error removing desktop file from desktop: {e}")
            return False

    def create_application_to_programming(self, target_filename=None):
        """Create application desktop file directly in applications folder"""
        try:
            # Use provided target filename or default to current name
            if target_filename:
                target_name = target_filename.replace(' ', '_')
            else:
                target_name = self.name.replace(' ', '_')
            
            # Validate required files
            run_script_path, icon_path = self._validate_files()
            
            # Create desktop file content
            application_content = self._create_application_content(run_script_path, icon_path)
            
            # Get original user's home directory instead of current user when using sudo
            original_user_home = self._get_original_user_home()
            dest_dir = os.path.join(original_user_home, ".local/share/applications/")
            dest_path = os.path.join(dest_dir, f"{target_name}.desktop")
            
            # Ensure destination directory exists
            os.makedirs(dest_dir, exist_ok=True)
            
            # Write desktop file directly to applications folder
            try:
                with open(dest_path, 'w', encoding='utf-8') as f:
                    f.write(application_content)
                print(f"Created desktop file directly in applications folder: {dest_path}")
            except Exception as e:
                raise Exception(f"Error creating desktop file: {e}")
            
            # Make the file executable
            self._make_executable(dest_path, run_script_path)
                
            return True
            
        except FileNotFoundError as e:
            print(f"File not found error: {e}")
            return False
        except PermissionError as e:
            print(f"Permission error: {e}")
            return False
        except Exception as e:
            print(f"Operation failed: {e}")
            return False
    
    def remove_application_from_programming(self, target_filename=None):
        """Remove application desktop file from applications folder"""
        try:
            # Use provided target filename or default to current name
            if target_filename:
                target_name = target_filename.replace(' ', '_')
            else:
                target_name = self.name.replace(' ', '_')
            
            # Get original user's home directory
            original_user_home = self._get_original_user_home()
            dest_dir = os.path.join(original_user_home, ".local/share/applications/")
            dest_path = os.path.join(dest_dir, f"{target_name}.desktop")
            
            # Check if file exists before attempting to remove
            if os.path.exists(dest_path):
                # Remove file using os.remove
                os.remove(dest_path)
                print(f"Successfully removed desktop file from applications folder: {dest_path}")
                return True
            else:
                print(f"Desktop file does not exist in applications folder: {dest_path}")
                return False
                
        except Exception as e:
            print(f"Error removing desktop file from applications folder: {e}")
            return False


if __name__ == "__main__":
    creator = DesktopShortcutCreator("FNK0100", "Freenove Computer Case Kit for Raspberry Pi")
    #creator.remove_application_from_programming()
    creator.create_application_to_programming()
    #creator.remove_shortcut_from_desktop()
    creator.create_shortcut_to_desktop()
    sys.exit(0)