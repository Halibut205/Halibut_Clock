import sys
try:
    import pygame
    print("✅ pygame imported successfully!")
    print(f"Version: {pygame.version.ver}")
    
    # Test pygame mixer
    pygame.mixer.init()
    print("✅ pygame mixer initialized!")
    
except ImportError as e:
    print(f"❌ pygame import error: {e}")
except Exception as e:
    print(f"❌ pygame error: {e}")
