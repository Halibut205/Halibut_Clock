import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from main import FliqloTimerApp
    app = FliqloTimerApp()
    print("✅ App created successfully")
    
    # Test 2 seconds
    app.root.after(2000, app.root.quit)
    app.run()
    print("✅ App test completed")
    
except Exception as e:
    print(f"❌ App error: {e}")
    import traceback
    traceback.print_exc()
