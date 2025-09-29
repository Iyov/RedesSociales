import os
from typing import Dict, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class SocialMediaConfig(BaseModel):
    """Configuración para credenciales de redes sociales"""
    
    # Instagram
    instagram_username: Optional[str] = Field(default=None)
    instagram_password: Optional[str] = Field(default=None)
    
    # Facebook
    facebook_username: Optional[str] = Field(default=None)
    facebook_password: Optional[str] = Field(default=None)
    
    # Threads
    threads_username: Optional[str] = Field(default=None)
    threads_password: Optional[str] = Field(default=None)
    
    # TikTok
    tiktok_username: Optional[str] = Field(default=None)
    tiktok_password: Optional[str] = Field(default=None)
    
    # YouTube
    youtube_username: Optional[str] = Field(default=None)
    youtube_password: Optional[str] = Field(default=None)
    
    # Configuración general
    browser_headless: bool = Field(default=False)
    duckduckgo_url: str = Field(default="https://duckduckgo.com")

class ConfigManager:
    """Gestor de configuración para el bot"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> SocialMediaConfig:
        """Carga la configuración desde variables de entorno"""
        return SocialMediaConfig(
            # Instagram
            instagram_username=os.getenv("INSTAGRAM_USERNAME"),
            instagram_password=os.getenv("INSTAGRAM_PASSWORD"),
            
            # Facebook
            facebook_username=os.getenv("FACEBOOK_USERNAME"),
            facebook_password=os.getenv("FACEBOOK_PASSWORD"),
            
            # Threads
            threads_username=os.getenv("THREADS_USERNAME"),
            threads_password=os.getenv("THREADS_PASSWORD"),
            
            # TikTok
            tiktok_username=os.getenv("TIKTOK_USERNAME"),
            tiktok_password=os.getenv("TIKTOK_PASSWORD"),
            
            # YouTube
            youtube_username=os.getenv("YOUTUBE_USERNAME"),
            youtube_password=os.getenv("YOUTUBE_PASSWORD"),
            
            # Configuración general
            browser_headless=os.getenv("BROWSER_HEADLESS", "False").lower() == "true",
            duckduckgo_url=os.getenv("DUCKDUCKGO_URL", "https://duckduckgo.com")
        )
    
    def get_credentials(self, platform: str) -> Dict[str, str]:
        """Obtiene credenciales para una plataforma específica"""
        platform = platform.lower()
        
        if platform == "instagram":
            return {
                "username": self.config.instagram_username,
                "password": self.config.instagram_password
            }
        elif platform == "facebook":
            return {
                "username": self.config.facebook_username,
                "password": self.config.facebook_password
            }
        elif platform == "threads":
            return {
                "username": self.config.threads_username,
                "password": self.config.threads_password
            }
        elif platform == "tiktok":
            return {
                "username": self.config.tiktok_username,
                "password": self.config.tiktok_password
            }
        elif platform == "youtube":
            return {
                "username": self.config.youtube_username,
                "password": self.config.youtube_password
            }
        else:
            raise ValueError(f"Plataforma no soportada: {platform}")
    
    def update_credentials(self, platform: str, username: str, password: str):
        """Actualiza credenciales para una plataforma"""
        platform = platform.lower()
        
        # Actualizar variables de entorno
        if platform == "instagram":
            os.environ["INSTAGRAM_USERNAME"] = username
            os.environ["INSTAGRAM_PASSWORD"] = password
        elif platform == "facebook":
            os.environ["FACEBOOK_USERNAME"] = username
            os.environ["FACEBOOK_PASSWORD"] = password
        elif platform == "threads":
            os.environ["THREADS_USERNAME"] = username
            os.environ["THREADS_PASSWORD"] = password
        elif platform == "tiktok":
            os.environ["TIKTOK_USERNAME"] = username
            os.environ["TIKTOK_PASSWORD"] = password
        elif platform == "youtube":
            os.environ["YOUTUBE_USERNAME"] = username
            os.environ["YOUTUBE_PASSWORD"] = password
        else:
            raise ValueError(f"Plataforma no soportada: {platform}")
        
        # Recargar configuración
        self.config = self._load_config()