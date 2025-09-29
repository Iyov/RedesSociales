import time
from selenium.webdriver.common.by import By
from .base import SocialMediaPlatform

class Facebook(SocialMediaPlatform):
    
    def get_profile_url(self) -> str:
        return "https://www.facebook.com/profile.php?id=61581529613006"
    
    def login(self):
        """Inicia sesión en Facebook"""
        try:
            self.driver.get("https://www.facebook.com/login/")
            time.sleep(3)
            
            email_input = self.browser_manager.wait_for_element(By.ID, "email")
            password_input = self.browser_manager.wait_for_element(By.ID, "pass")
            
            email_input.clear()
            email_input.send_keys(self.credentials["username"])
            
            password_input.clear()
            password_input.send_keys(self.credentials["password"])
            
            login_button = self.browser_manager.wait_for_element_clickable(
                By.NAME, "login"
            )
            login_button.click()
            
            time.sleep(5)
            
            # Verificar login exitoso
            if "login" not in self.driver.current_url.lower():
                print("✅ Sesión iniciada en Facebook")
            else:
                raise Exception("Error en el login de Facebook")
                
        except Exception as e:
            print(f"❌ Error en login de Facebook: {str(e)}")
            self.browser_manager.take_screenshot("facebook_login_error.png")
            raise
    
    def upload_reel(self, video_path: str, description: str = ""):
        """Sube un reel a Facebook"""
        try:
            self.ensure_logged_in()
            
            # Navegar a la página de creación de reels
            self.driver.get("https://www.facebook.com/reels/create")
            time.sleep(5)
            
            # Subir video
            file_input = self.browser_manager.wait_for_element(
                By.XPATH, "//input[@type='file']"
            )
            file_input.send_keys(video_path)
            time.sleep(8)  # Esperar a que procese el video
            
            # Agregar descripción
            if description:
                caption_box = self.browser_manager.find_element_safe(
                    By.XPATH, "//div[@aria-label='Escribe un pie de foto.']"
                )
                if caption_box:
                    caption_box.send_keys(description)
                    time.sleep(2)
            
            # Publicar
            share_button = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//div[@aria-label='Compartir reel']"
            )
            share_button.click()
            
            time.sleep(10)
            print("✅ Reel publicado exitosamente en Facebook")
            
        except Exception as e:
            print(f"❌ Error subiendo reel a Facebook: {str(e)}")
            self.browser_manager.take_screenshot("facebook_upload_error.png")
            raise