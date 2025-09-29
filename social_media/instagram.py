import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import SocialMediaPlatform

class Instagram(SocialMediaPlatform):
    
    def get_profile_url(self) -> str:
        return "https://www.instagram.com/mevoyadarunlujodiario/"
    
    def login(self):
        """Inicia sesión en Instagram"""
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # Aceptar cookies si aparece
            cookie_button = self.browser_manager.find_element_safe(
                By.XPATH, "//button[contains(text(), 'Permitir')]"
            )
            if cookie_button:
                cookie_button.click()
                time.sleep(2)
            
            # Llenar credenciales
            username_input = self.browser_manager.wait_for_element(
                By.NAME, "username"
            )
            password_input = self.browser_manager.wait_for_element(
                By.NAME, "password"
            )
            
            username_input.clear()
            username_input.send_keys(self.credentials["username"])
            
            password_input.clear()
            password_input.send_keys(self.credentials["password"])
            
            # Click en login
            login_button = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//button[@type='submit']"
            )
            login_button.click()
            
            time.sleep(5)
            
            # Manejar "Guardar información de inicio de sesión"
            not_now_btn = self.browser_manager.find_element_safe(
                By.XPATH, "//button[contains(text(), 'Ahora no')]"
            )
            if not_now_btn:
                not_now_btn.click()
                time.sleep(2)
            
            # Manejar notificaciones
            not_now_notif = self.browser_manager.find_element_safe(
                By.XPATH, "//button[contains(text(), 'Ahora no')]"
            )
            if not_now_notif:
                not_now_notif.click()
            
            time.sleep(3)
            print("✅ Sesión iniciada en Instagram")
            
        except Exception as e:
            print(f"❌ Error en login de Instagram: {str(e)}")
            self.browser_manager.take_screenshot("instagram_login_error.png")
            raise
    
    def upload_reel(self, video_path: str, description: str = ""):
        """Sube un reel a Instagram"""
        try:
            self.ensure_logged_in()
            
            # Navegar a la página principal
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            # Click en el botón de crear (puede variar según la versión)
            create_button = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@role, 'button')]//span[text()='Crear']"
            )
            if not create_button:
                # Intentar con otro selector
                create_button = self.browser_manager.wait_for_element_clickable(
                    By.XPATH, "//div[@role='button']//span[text()='Crear']"
                )
            
            create_button.click()
            time.sleep(2)
            
            # Seleccionar subir desde dispositivo
            upload_option = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//button[contains(text(), 'Seleccionar') or contains(text(), 'Subir')]"
            )
            upload_option.click()
            time.sleep(2)
            
            # Buscar input file
            file_input = self.browser_manager.wait_for_element(
                By.XPATH, "//input[@type='file']"
            )
            
            # Subir video
            file_input.send_keys(video_path)
            time.sleep(5)  # Esperar a que procese el video
            
            # Siguiente paso
            next_button = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//button[contains(text(), 'Siguiente')]"
            )
            next_button.click()
            time.sleep(2)
            
            # Agregar descripción
            if description:
                caption_box = self.browser_manager.wait_for_element(
                    By.XPATH, "//textarea[@aria-label='Escribe un pie de foto.']"
                )
                caption_box.send_keys(description)
                time.sleep(2)
            
            # Seleccionar formato Reel
            reel_option = self.browser_manager.find_element_safe(
                By.XPATH, "//div[contains(text(), 'Reel')]"
            )
            if reel_option:
                reel_option.click()
                time.sleep(2)
            
            # Publicar
            share_button = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//button[contains(text(), 'Compartir')]"
            )
            share_button.click()
            
            time.sleep(10)  # Esperar a que complete la publicación
            print("✅ Reel publicado exitosamente en Instagram")
            
        except Exception as e:
            print(f"❌ Error subiendo reel a Instagram: {str(e)}")
            self.browser_manager.take_screenshot("instagram_upload_error.png")
            raise