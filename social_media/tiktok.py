import time
from selenium.webdriver.common.by import By
from .base import SocialMediaPlatform

class TikTok(SocialMediaPlatform):
    
    def get_profile_url(self) -> str:
        return "https://www.tiktok.com/@mevoyadarunlujodiario"
    
    def login(self):
        """Inicia sesión en TikTok"""
        try:
            self.driver.get("https://www.tiktok.com/login/")
            time.sleep(3)
            
            # TikTok tiene múltiples métodos de login, usaremos email/usuario
            login_with_email = self.browser_manager.find_element_safe(
                By.XPATH, "//a[contains(text(), 'Use phone') or contains(text(), 'Email')]"
            )
            if login_with_email:
                login_with_email.click()
                time.sleep(2)
            
            # Intentar con usuario/email
            username_input = self.browser_manager.wait_for_element(
                By.XPATH, "//input[@type='text']"
            )
            password_input = self.browser_manager.wait_for_element(
                By.XPATH, "//input[@type='password']"
            )
            
            username_input.send_keys(self.credentials["username"])
            password_input.send_keys(self.credentials["password"])
            
            login_button = self.browser_manager.wait_for_element_clickable(
                By.XPATH, "//button[contains(text(), 'Log in') or contains(text(), 'Iniciar')]"
            )
            login_button.click()
            
            time.sleep(5)
            
            # Manejar verificación si aparece
            print("✅ Sesión iniciada en TikTok (puede requerir verificación manual)")
            
        except Exception as e:
            print(f"❌ Error en login de TikTok: {str(e)}")
            print("💡 TikTok puede requerir verificación manual o captcha")
            self.browser_manager.take_screenshot("tiktok_login_error.png")
    
    def upload_reel(self, video_path: str, description: str = ""):
        """Sube un video a TikTok"""
        try:
            self.ensure_logged_in()
            
            # TikTok web no permite subida directa, redirigir a studio
            self.driver.get("https://www.tiktok.com/upload?lang=en")
            time.sleep(5)
            
            print("⚠️ TikTok Web requiere subida manual desde el estudio")
            print("💡 Alternativa: Usar la aplicación móvil para subidas automáticas")
            print(f"📁 Video listo: {video_path}")
            print("📝 Descripción: " + description)
            
            # Intentar subida si encuentra el input
            file_input = self.browser_manager.find_element_safe(
                By.XPATH, "//input[@type='file']"
            )
            
            if file_input:
                file_input.send_keys(video_path)
                time.sleep(8)
                
                # Agregar descripción
                if description:
                    caption_box = self.browser_manager.find_element_safe(
                        By.XPATH, "//div[@contenteditable='true']"
                    )
                    if caption_box:
                        caption_box.send_keys(description)
                        time.sleep(2)
                
                # Publicar
                post_button = self.browser_manager.find_element_safe(
                    By.XPATH, "//button[contains(text(), 'Publicar')]"
                )
                if post_button:
                    post_button.click()
                    time.sleep(10)
                    print("✅ Video publicado en TikTok")
                else:
                    print("⚠️ TikTok requiere interacción manual para publicar")
            else:
                print("ℹ️ Para TikTok automatizado, considera usar su API oficial")
                
        except Exception as e:
            print(f"❌ Error subiendo a TikTok: {str(e)}")
            self.browser_manager.take_screenshot("tiktok_upload_error.png")