import os
from typing import List, Dict
from config.config_manager import ConfigManager
from utils.browser import BrowserManager
from social_media.instagram import Instagram
from social_media.facebook import Facebook
from social_media.threads import Threads
from social_media.tiktok import TikTok
from social_media.youtube import YouTube

class SocialMediaBot:
    """Bot principal para gestionar publicaciones en redes sociales"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.browser_manager = BrowserManager(
            headless=self.config_manager.config.browser_headless
        )
        self.platforms = {}
    
    def initialize_platforms(self):
        """Inicializa todas las plataformas configuradas"""
        platform_classes = {
            "instagram": Instagram,
            "facebook": Facebook,
            "threads": Threads,
            "tiktok": TikTok,
            "youtube": YouTube
        }
        
        for platform_name, platform_class in platform_classes.items():
            credentials = self.config_manager.get_credentials(platform_name)
            if credentials["username"] and credentials["password"]:
                self.platforms[platform_name] = platform_class(
                    self.browser_manager, credentials
                )
                print(f"✅ {platform_name.capitalize()} configurado")
            else:
                print(f"❌ {platform_name.capitalize()} no configurado")
    
    def update_credentials(self):
        """Permite actualizar credenciales desde la consola"""
        print("\n🔐 Actualizar Credenciales")
        print("1. Instagram")
        print("2. Facebook")
        print("3. Threads")
        print("4. TikTok")
        print("5. YouTube")
        print("6. Volver")
        
        choice = input("\nSelecciona una opción: ")
        
        platform_map = {
            "1": "instagram",
            "2": "facebook",
            "3": "threads",
            "4": "tiktok",
            "5": "youtube"
        }
        
        if choice in platform_map:
            platform = platform_map[choice]
            username = input(f"Usuario para {platform}: ")
            password = input(f"Contraseña para {platform}: ")
            
            self.config_manager.update_credentials(platform, username, password)
            print(f"✅ Credenciales de {platform} actualizadas")
        
        elif choice == "6":
            return
        else:
            print("❌ Opción inválida")
    
    def upload_to_all_platforms(self, video_path: str, description: str = ""):
        """Sube un reel a todas las plataformas configuradas"""
        if not os.path.exists(video_path):
            print(f"❌ El archivo {video_path} no existe")
            return
        
        print(f"\n🎬 Subiendo reel: {video_path}")
        
        for platform_name, platform in self.platforms.items():
            try:
                print(f"\n🔄 Subiendo a {platform_name.capitalize()}...")
                platform.upload_reel(video_path, description)
                print(f"✅ Subido exitosamente a {platform_name.capitalize()}")
            except Exception as e:
                print(f"❌ Error subiendo a {platform_name.capitalize()}: {str(e)}")
    
    def show_menu(self):
        """Muestra el menú principal"""
        while True:
            print("\n" + "="*50)
            print("🤖 BOT REDES SOCIALES - MeVoyADarUnLujoDiario")
            print("="*50)
            print("1. 📤 Subir Reel a todas las plataformas")
            print("2. ⚙️ Configurar credenciales")
            print("3. 📊 Ver plataformas configuradas")
            print("4. 🚪 Salir")
            
            choice = input("\nSelecciona una opción: ")
            
            if choice == "1":
                video_path = input("Ruta del video: ")
                description = input("Descripción (opcional): ")
                self.upload_to_all_platforms(video_path, description)
            
            elif choice == "2":
                self.update_credentials()
                # Re-inicializar plataformas con nuevas credenciales
                self.initialize_platforms()
            
            elif choice == "3":
                self.show_configured_platforms()
            
            elif choice == "4":
                print("👋 ¡Hasta luego!")
                self.browser_manager.close()
                break
            
            else:
                print("❌ Opción inválida")
    
    def show_configured_platforms(self):
        """Muestra las plataformas configuradas"""
        print("\n📊 Plataformas Configuradas:")
        for platform_name in self.platforms:
            print(f"✅ {platform_name.capitalize()}")
        
        # Mostrar no configuradas
        all_platforms = ["instagram", "facebook", "threads", "tiktok", "youtube"]
        configured = set(self.platforms.keys())
        not_configured = set(all_platforms) - configured
        
        for platform in not_configured:
            print(f"❌ {platform.capitalize()}")

def main():
    """Función principal"""
    try:
        bot = SocialMediaBot()
        bot.initialize_platforms()
        bot.show_menu()
    except KeyboardInterrupt:
        print("\n👋 Ejecución interrumpida por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()