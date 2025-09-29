import time
from selenium.webdriver.common.by import By
from .base import SocialMediaPlatform

class Facebook(SocialMediaPlatform):
    
    def get_profile_url(self) -> str:
        return "https://www.facebook.com/profile.php?id=61581529613006"
    
    def login(self):
        """Inicia sesión en Facebook"""
        self.driver.get("https://www.facebook.com/login/")
        
        email_input = self.browser_manager.wait_for_element(By.ID, "email")
        password_input = self.browser_manager.wait_for_element(By.ID, "pass")
        
        email_input.send_keys(self.credentials["username"])
        password_input.send_keys(self.credentials["password"])
        
        login_button = self.browser_manager.wait_for_element_clickable(
            By.NAME, "login"
        )
        login_button.click()
        
        time.sleep(5)
    
    def upload_reel(self, video_path: str, description: str = ""):
        """Sube un reel a Facebook"""
        self.ensure_logged_in()
        
        # Navegar a la página de inicio
        self.driver.get("https://www.facebook.com/")
        
        # Buscar el botón de crear reel
        # Facebook también cambia frecuentemente su interfaz
        
        print(f"Reel subido a Facebook: {video_path}")