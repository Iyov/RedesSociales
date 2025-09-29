import time
from selenium.webdriver.common.by import By
from .base import SocialMediaPlatform

class YouTube(SocialMediaPlatform):
    
    def get_profile_url(self) -> str:
        return "https://www.youtube.com/@MeVoyADarUnLujoDiario"
    
    def login(self):
        """Inicia sesión en YouTube"""
        try:
            self.driver.get("https://accounts.google.com/ServiceLogin?service=youtube")
            time.sleep(3)
            
            # Llenar email
            email_input = self.browser_manager.wait_for_element(By.ID, "identifierId")
            email_input.send_keys(self.credentials["username"])
            
            next_button = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//span[contains(text(), 'Siguiente')]"
            )
            next_button.click()
            
            time.sleep(3)
            
            # Llenar contraseña
            password_input = self.browser_manager.wait_for_element(
                By.NAME, "Passwd"
            )
            password_input.send_keys(self.credentials["password"])
            
            next_button = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//span[contains(text(), 'Siguiente')]"
            )
            next_button.click()
            
            time.sleep(5)
            print("✅ Sesión iniciada en YouTube")
            
        except Exception as e:
            print(f"❌ Error en login de YouTube: {str(e)}")
            self.browser_manager.take_screenshot("youtube_login_error.png")
            raise
    
    def upload_reel(self, video_path: str, description: str = ""):
        """Sube un Short a YouTube"""
        try:
            self.ensure_logged_in()
            
            # Navegar a YouTube Studio
            self.driver.get("https://studio.youtube.com/")
            time.sleep(5)
            
            # Click en crear
            create_button = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//ytcp-button[@id='create-icon']"
            )
            create_button.click()
            time.sleep(2)
            
            # Seleccionar subir video
            upload_option = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//tp-yt-paper-item[@test-id='upload-menuitem']"
            )
            upload_option.click()
            time.sleep(3)
            
            # Subir archivo
            file_input = self.browser_manager.wait_for_element(
                By.XPATH, "//input[@type='file']"
            )
            file_input.send_keys(video_path)
            time.sleep(10)  # Esperar a que procese el video
            
            # Marcar como Short
            shorts_checkbox = self.browser_manager.find_element_safe(
                By.XPATH, "//ytcp-video-metadata-shorts-toggle//tp-yt-paper-checkbox"
            )
            if shorts_checkbox and not shorts_checkbox.get_attribute("checked"):
                shorts_checkbox.click()
                time.sleep(2)
            
            # Siguiente paso
            next_buttons = self.browser_manager.driver.find_elements(
                By.XPATH, "//ytcp-button[@id='next-button']"
            )
            for button in next_buttons:
                if button.is_displayed():
                    button.click()
                    time.sleep(3)
            
            # Agregar descripción
            if description:
                description_box = self.browser_manager.find_element_safe(
                    By.XPATH, "//div[@id='textbox']"
                )
                if description_box:
                    description_box.clear()
                    description_box.send_keys(description)
                    time.sleep(2)
            
            # Publicar
            public_button = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//ytcp-button[@id='done-button']"
            )
            public_button.click()
            
            time.sleep(10)
            print("✅ Short publicado exitosamente en YouTube")
            
        except Exception as e:
            print(f"❌ Error subiendo short a YouTube: {str(e)}")
            self.browser_manager.take_screenshot("youtube_upload_error.png")
            raise