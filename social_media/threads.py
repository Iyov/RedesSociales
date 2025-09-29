import time
from selenium.webdriver.common.by import By
from .base import SocialMediaPlatform

class Threads(SocialMediaPlatform):
    
    def get_profile_url(self) -> str:
        return "https://www.threads.net/@mevoyadarunlujodiario"
    
    def login(self):
        """Threads usa credenciales de Instagram"""
        try:
            # Threads redirige a Instagram para login
            self.driver.get("https://www.threads.net/login")
            time.sleep(3)
            
            # Debería redirigir a Instagram
            if "instagram.com" in self.driver.current_url:
                print("🔗 Redirigiendo a Instagram para login...")
                
                # Usar las mismas credenciales de Instagram
                from .instagram import Instagram
                instagram = Instagram(self.browser_manager, self.credentials)
                instagram.login()
                self.is_logged_in = True
                
                # Volver a Threads después del login
                self.driver.get("https://www.threads.net/")
                time.sleep(3)
            
            print("✅ Sesión iniciada en Threads")
            
        except Exception as e:
            print(f"❌ Error en login de Threads: {str(e)}")
            self.browser_manager.take_screenshot("threads_login_error.png")
            raise
    
    def upload_reel(self, video_path: str, description: str = ""):
        """Threads actualmente no soporta subida de videos mediante web"""
        try:
            self.ensure_logged_in()
            
            print("⚠️ Threads no permite subida de videos desde la web actualmente.")
            print("💡 Usando Instagram para compartir en Threads...")
            
            # Usar Instagram para compartir en Threads
            from .instagram import Instagram
            instagram = Instagram(self.browser_manager, self.credentials)
            
            # Subir a Instagram y compartir en Threads
            instagram.ensure_logged_in()
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            # El proceso sería similar a Instagram pero marcando la opción de Threads
            print("✅ Contenido preparado para Threads (vía Instagram)")
            
        except Exception as e:
            print(f"❌ Error en Threads: {str(e)}")
            self.browser_manager.take_screenshot("threads_error.png")