import os
import sys
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
                print(f"❌ {platform_name.capitalize()} - Credenciales faltantes")
    
    def update_credentials(self):
        """Permite actualizar credenciales desde la consola"""
        print("\n🔐 Actualizar Credenciales")
        print("1. Instagram")
        print("2. Facebook") 
        print("3. Threads")
        print("4. TikTok")
        print("5. YouTube")
        print("6. Volver")
        
        choice = input("\nSelecciona una opción: ").strip()
        
        platform_map = {
            "1": "instagram",
            "2": "facebook",
            "3": "threads", 
            "4": "tiktok",
            "5": "youtube"
        }
        
        if choice in platform_map:
            platform = platform_map[choice]
            username = input(f"Usuario/Email para {platform}: ").strip()
            password = input(f"Contraseña para {platform}: ").strip()
            
            if username and password:
                self.config_manager.update_credentials(platform, username, password)
                print(f"✅ Credenciales de {platform} actualizadas")
                
                # Re-inicializar plataformas
                self.initialize_platforms()
            else:
                print("❌ Usuario y contraseña no pueden estar vacíos")
        
        elif choice == "6":
            return
        else:
            print("❌ Opción inválida")
    
    def upload_to_platforms(self, video_path: str, description: str = "", platforms: list = None):
        """Sube un reel a las plataformas especificadas"""
        if not os.path.exists(video_path):
            print(f"❌ El archivo {video_path} no existe")
            return False
        
        if platforms is None:
            platforms = list(self.platforms.keys())
        
        print(f"\n🎬 Subiendo reel: {video_path}")
        print(f"📝 Descripción: {description}")
        
        success_count = 0
        for platform_name in platforms:
            if platform_name in self.platforms:
                try:
                    print(f"\n🔄 Subiendo a {platform_name.capitalize()}...")
                    self.platforms[platform_name].upload_reel(video_path, description)
                    print(f"✅ Subido exitosamente a {platform_name.capitalize()}")
                    success_count += 1
                except Exception as e:
                    print(f"❌ Error subiendo a {platform_name.capitalize()}: {str(e)}")
            else:
                print(f"❌ {platform_name.capitalize()} no está configurado")
        
        print(f"\n📊 Resultado: {success_count}/{len(platforms)} plataformas exitosas")
        return success_count > 0
    
    def show_menu(self):
        """Muestra el menú principal"""
        while True:
            print("\n" + "="*50)
            print("🤖 BOT REDES SOCIALES - MeVoyADarUnLujoDiario")
            print("="*50)
            print("1. 📤 Subir Reel a TODAS las plataformas")
            print("2. 🎯 Subir Reel a plataformas específicas") 
            print("3. ⚙️ Configurar credenciales")
            print("4. 📊 Ver plataformas configuradas")
            print("5. 🚪 Salir")
            
            choice = input("\nSelecciona una opción: ").strip()
            
            if choice == "1":
                video_path = input("Ruta completa del video: ").strip()
                description = input("Descripción (opcional): ").strip()
                self.upload_to_platforms(video_path, description)
            
            elif choice == "2":
                self.upload_to_specific_platforms()
            
            elif choice == "3":
                self.update_credentials()
            
            elif choice == "4":
                self.show_configured_platforms()
            
            elif choice == "5":
                print("👋 ¡Hasta luego!")
                self.browser_manager.close()
                break
            
            else:
                print("❌ Opción inválida")
    
    def upload_to_specific_platforms(self):
        """Sube a plataformas específicas seleccionadas por el usuario"""
        available_platforms = list(self.platforms.keys())
        
        if not available_platforms:
            print("❌ No hay plataformas configuradas")
            return
        
        print("\n🎯 Selecciona plataformas (ej: 1,3,5):")
        for i, platform in enumerate(available_platforms, 1):
            print(f"{i}. {platform.capitalize()}")
        
        try:
            selections = input("\nPlataformas: ").strip()
            selected_indices = [int(x.strip()) - 1 for x in selections.split(",")]
            selected_platforms = [available_platforms[i] for i in selected_indices 
                                if 0 <= i < len(available_platforms)]
            
            if selected_platforms:
                video_path = input("Ruta completa del video: ").strip()
                description = input("Descripción (opcional): ").strip()
                self.upload_to_platforms(video_path, description, selected_platforms)
            else:
                print("❌ No se seleccionaron plataformas válidas")
                
        except ValueError:
            print("❌ Formato inválido. Usa números separados por comas.")
    
    def show_configured_platforms(self):
        """Muestra las plataformas configuradas"""
        print("\n📊 Plataformas Configuradas:")
        for platform_name, platform in self.platforms.items():
            print(f"✅ {platform_name.capitalize()}")
        
        # Mostrar no configuradas
        all_platforms = ["instagram", "facebook", "threads", "tiktok", "youtube"]
        configured = set(self.platforms.keys())
        not_configured = set(all_platforms) - configured
        
        for platform in not_configured:
            print(f"❌ {platform.capitalize()}")

def main():
    """Función principal"""
    # Verificar Python version
    if sys.version_info < (3, 7):
        print("❌ Se requiere Python 3.7 o superior")
        return
    
    print("🐍 Python version:", sys.version)
    
    try:
        bot = SocialMediaBot()
        bot.initialize_platforms()
        bot.show_menu()
    except KeyboardInterrupt:
        print("\n👋 Ejecución interrumpida por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()