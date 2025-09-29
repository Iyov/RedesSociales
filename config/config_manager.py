import os
from typing import Dict, Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

class SocialMediaConfig(BaseSettings):
    """Configuración para credenciales de redes sociales"""
    
    # Instagram
    instagram_username: Optional[str] = Field(None, env="INSTAGRAM_USERNAME")
    instagram_password: Optional[str] = Field(None, env="INSTAGRAM_PASSWORD")
    
    # Facebook
    facebook_username: Optional[str] = Field(None, env="FACEBOOK_USERNAME")
    facebook_password: Optional[str] = Field(None, env="FACEBOOK_PASSWORD")
    
    # Threads
    threads_username: Optional[str] = Field(None, env="THREADS_USERNAME")
    threads_password: Optional[str] = Field(None, env="THREADS_PASSWORD")
    
    # TikTok
    tiktok_username: Optional[str] = Field(None, env="TIKTOK_USERNAME")
    tiktok_password: Optional[str] = Field(None, env="TIKTOK_PASSWORD")
    
    # YouTube
    youtube_username: Optional[str] = Field(None, env="YOUTUBE_USERNAME")
    youtube_password: Optional[str] = Field(None, env="YOUTUBE_PASSWORD")
    
    # Configuración general
    browser_headless: bool = Field(False, env="BROWSER_HEADLESS")
    duckduckgo_url: str = Field("https://duckduckgo.com", env="DUCKDUCKGO_URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class ConfigManager:
    """Gestor de configuración para el bot"""
    
    def __init__(self):
        self.config = SocialMediaConfig()
    
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
        
        if platform == "instagram":
            self.config.instagram_username = username
            self.config.instagram_password = password
        elif platform == "facebook":
            self.config.facebook_username = username
            self.config.facebook_password = password
        elif platform == "threads":
            self.config.threads_username = username
            self.config.threads_password = password
        elif platform == "tiktok":
            self.config.tiktok_username = username
            self.config.tiktok_password = password
        elif platform == "youtube":
            self.config.youtube_username = username
            self.config.youtube_password = password
        else:
            raise ValueError(f"Plataforma no soportada: {platform}")