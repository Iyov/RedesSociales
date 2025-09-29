from abc import ABC, abstractmethod
from typing import Optional
from selenium.webdriver.chrome.webdriver import WebDriver
from utils.browser import BrowserManager
import time
import os

class SocialMediaPlatform(ABC):
    """Clase base abstracta para todas las plataformas de redes sociales"""
    
    def __init__(self, browser_manager: BrowserManager, credentials: dict):
        self.browser_manager = browser_manager
        self.credentials = credentials
        self.driver: Optional[WebDriver] = None
        self.is_logged_in = False
    
    @abstractmethod
    def login(self):
        """Método abstracto para iniciar sesión"""
        pass
    
    @abstractmethod
    def upload_reel(self, video_path: str, description: str = ""):
        """Método abstracto para subir un reel"""
        pass
    
    @abstractmethod
    def get_profile_url(self) -> str:
        """Método abstracto para obtener la URL del perfil"""
        pass
    
    def ensure_logged_in(self):
        """Verifica si está logueado y si no, inicia sesión"""
        if not self.driver:
            self.driver = self.browser_manager.navigate_to_duckduckgo()
        
        if not self.is_logged_in:
            print(f"🔐 Iniciando sesión en {self.__class__.__name__}...")
            self.login()
            self.is_logged_in = True
    
    def upload_file(self, file_input_selector: str, video_path: str):
        """Sube un archivo a un input file"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"El archivo {video_path} no existe")
        
        file_input = self.browser_manager.wait_for_element_clickable(
            self.browser_manager.driver.find_element_by_css_selector, file_input_selector
        )
        
        # Usar JavaScript para establecer el valor del file input
        self.browser_manager.driver.execute_script(
            f"arguments[0].value = '{os.path.abspath(video_path)}';", 
            file_input
        )
        
        # Disparar evento change
        self.browser_manager.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));", 
            file_input
        )
        
        time.sleep(3)  # Esperar a que procese el archivo