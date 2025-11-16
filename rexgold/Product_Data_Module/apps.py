from django.apps import AppConfig
import os
import threading
class ProductDataModuleConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    name = 'Product_Data_Module'
    
    def ready(self):
        # فقط در پروسه اصلی (نه reloader)
        if os.environ.get('RUN_MAIN'):
            return

        # فقط اگر از celery نباشه
        if any(cmd in ' '.join(os.sys.argv) for cmd in ['celery', 'beat', 'worker']):
            return

        # فقط یک بار
        if not hasattr(ProductDataModuleConfig, '_listener_started'):
            from .price_listener import start_price_listener
            thread = threading.Thread(target=start_price_listener, daemon=True)
            thread.start()
            ProductDataModuleConfig._listener_started = True
            print("[Listener] Price listener started (once).")
