print("Debug: Starting...")

try:
    import tkinter as tk
    print("Debug: Tkinter imported OK")
    
    import sys
    import os
    print("Debug: sys, os imported OK")
    
    # Add src to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    print("Debug: Path added")
    
    # Try importing our modules
    from src.ui.app_settings import should_show_welcome
    print("Debug: app_settings imported OK")
    
    show_welcome = should_show_welcome()
    print(f"Debug: should_show_welcome = {show_welcome}")
    
    if show_welcome:
        print("Debug: Will show welcome screen")
        from src.ui.welcome_screen import show_welcome_screen
        print("Debug: welcome_screen imported OK")
    else:
        print("Debug: Will show main timer")
        
    print("Debug: All imports successful")
    
except Exception as e:
    print(f"Debug: Error occurred: {e}")
    import traceback
    traceback.print_exc()

print("Debug: Script completed")
