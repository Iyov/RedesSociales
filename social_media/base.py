from abc import ABC, abstractmethod
from typing import Optional
from selenium.webdriver.chrome.webdriver import WebDriver
from utils.browser import BrowserManager

class SocialMediaPlatform(ABC):
    """Clase base abstracta para todas las plataformas de redes sociales"""
    
    def __init__(self, browser_manager: BrowserManager, credentials: dict):
        self.browser_manager = browser_manager
        self.credentials = credentials
        self.driver: Optional[WebDriver] = None
    
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
        
        # Navegar al perfil para verificar si estamos logueados
        self.driver.get(self.get_profile_url())
        
        # Aquí deberías implementar la lógica para verificar si está logueado
        # Por simplicidad, siempre intentamos login
        self.login()