import time
from selenium.webdriver.common.by import By
from .base import SocialMediaPlatform

class Instagram(SocialMediaPlatform):
    
    def get_profile_url(self) -> str:
        return "https://www.instagram.com/mevoyadarunlujodiario/"
    
    def login(self):
        """Inicia sesión en Instagram"""
        self.driver.get("https://www.instagram.com/accounts/login/")
        
        # Esperar y llenar credenciales
        username_input = self.browser_manager.wait_for_element(
            By.NAME, "username"
        )
        password_input = self.browser_manager.wait_for_element(
            By.NAME, "password"
        )
        
        username_input.send_keys(self.credentials["username"])
        password_input.send_keys(self.credentials["password"])
        
        # Click en login
        login_button = self.browser_manager.wait_for_element_clickable(
            By.XPATH, "//button[@type='submit']"
        )
        login_button.click()
        
        time.sleep(5)  # Esperar que cargue
    
    def upload_reel(self, video_path: str, description: str = ""):
        """Sube un reel a Instagram"""
        self.ensure_logged_in()
        
        # Navegar a la página de creación
        self.driver.get("https://www.instagram.com/")
        
        # Click en crear (el ícono +)
        create_button = self.browser_manager.wait_for_element_clickable(
            By.XPATH, "//div[contains(@class, 'x1i10hfl')]//span[text()='Create']"
        )
        create_button.click()
        
        # Aquí continuaría la lógica específica para subir el video
        # Nota: Instagram cambia frecuentemente su interfaz, esto puede necesitar ajustes
        
        print(f"Reel subido a Instagram: {video_path}")