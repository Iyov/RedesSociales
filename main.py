import os
import time
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

class SocialMediaBot:
    def __init__(self):
        self.config_file = "social_media_config.json"
        self.load_config()
        
    def load_config(self):
        """Cargar configuración desde archivo JSON"""
        default_config = {
            "instagram": {
                "username": "",
                "password": "",
                "profile_url": "https://www.instagram.com/tu_usuario/"
            },
            "youtube": {
                "email": "",
                "password": "",
                "channel_url": "https://www.youtube.com/@tu_usuario"
            },
            "chrome_path": "",
            "video_path": "",
            "headless": False
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            self.config = default_config

    def save_config(self):
        """Guardar configuración en archivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")

    def setup_driver(self):
        """Configurar el driver de Selenium en modo incógnito"""
        try:
            chrome_options = Options()
            
            # Modo incógnito
            chrome_options.add_argument("--incognito")
            
            if self.config.get("headless", False):
                chrome_options.add_argument("--headless")
            
            # Configuraciones adicionales para mayor estabilidad
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User agent realista
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Ruta personalizada de Chrome si se especifica
            chrome_path = self.config.get("chrome_path", "")
            if chrome_path and os.path.exists(chrome_path):
                chrome_options.binary_location = chrome_path
            
            driver = webdriver.Chrome(options=chrome_options)
            
            # Eliminar la propiedad webdriver para evitar detección
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
        except Exception as e:
            raise Exception(f"Error configurando el driver de Chrome: {e}")

    def post_to_instagram(self, video_path, description=""):
        """Publicar reel en Instagram"""
        driver = None
        try:
            driver = self.setup_driver()
            wait = WebDriverWait(driver, 20)
            
            self.log("🚀 Iniciando publicación en Instagram...")
            self.log("🌐 Navegando a Instagram...")
            
            # Navegar a Instagram
            driver.get("https://www.instagram.com/accounts/login/")
            
            # Login
            self.log("🔐 Realizando login...")
            username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_input = driver.find_element(By.NAME, "password")
            
            username_input.send_keys(self.config["instagram"]["username"])
            password_input.send_keys(self.config["instagram"]["password"])
            
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Esperar a que cargue la página principal
            self.log("⏳ Esperando carga de la página...")
            time.sleep(8)
            
            # Manejar ventanas emergentes de notificaciones
            try:
                not_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ahora no')]")))
                not_now_button.click()
                self.log("📱 Ventana de notificaciones cerrada")
                time.sleep(2)
            except:
                pass
            
            # Navegar a la página de crear publicación
            self.log("📸 Accediendo a crear publicación...")
            driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            # Click en crear publicación (botón +)
            try:
                create_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@style, 'media')]")))
                create_button.click()
            except:
                # Alternativa si no encuentra el botón por clase
                create_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Crear')]")))
                create_button.click()
            
            self.log("🎥 Subiendo video...")
            # Seleccionar archivo de video
            file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(os.path.abspath(video_path))
            
            # Esperar a que se procese el video
            self.log("⏳ Procesando video...")
            time.sleep(10)
            
            # Click en siguiente
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Siguiente')]")))
            next_button.click()
            time.sleep(2)
            
            # Click en siguiente otra vez (pantalla de filtros)
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Siguiente')]")))
            next_button.click()
            time.sleep(2)
            
            # Escribir descripción
            if description:
                self.log("📝 Añadiendo descripción...")
                caption_area = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Escribe un pie de foto.']")))
                caption_area.clear()
                caption_area.send_keys(description)
            
            # Publicar
            self.log("✅ Publicando reel...")
            share_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Compartir')]")))
            share_button.click()
            
            # Esperar a que se complete la publicación
            self.log("⏳ Esperando confirmación...")
            time.sleep(15)
            
            return True, "✅ Reel publicado exitosamente en Instagram"
            
        except Exception as e:
            return False, f"❌ Error publicando en Instagram: {str(e)}"
        finally:
            if driver:
                driver.quit()
                self.log("🔒 Navegador cerrado")

    def post_to_youtube(self, video_path, title="", description="", tags=""):
        """Publicar Short en YouTube"""
        driver = None
        try:
            driver = self.setup_driver()
            wait = WebDriverWait(driver, 25)
            
            self.log("🚀 Iniciando publicación en YouTube...")
            self.log("🌐 Navegando a YouTube Studio...")
            
            # Navegar a YouTube Studio
            driver.get("https://studio.youtube.com/")
            
            # Login si es necesario
            if "accounts.google.com" in driver.current_url:
                self.log("🔐 Realizando login en Google...")
                email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
                email_input.send_keys(self.config["youtube"]["email"])
                
                next_button = driver.find_element(By.ID, "identifierNext")
                next_button.click()
                time.sleep(3)
                
                password_input = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
                password_input.send_keys(self.config["youtube"]["password"])
                
                password_next = driver.find_element(By.ID, "passwordNext")
                password_next.click()
                
                time.sleep(8)
            
            # Click en crear botón
            self.log("📹 Accediendo a crear contenido...")
            create_button = wait.until(EC.element_to_be_clickable((By.ID, "create-icon")))
            create_button.click()
            
            # Seleccionar subir video
            upload_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//ytcp-menu-service-item[@id='text-item-0']")))
            upload_item.click()
            
            self.log("🎥 Subiendo video...")
            # Seleccionar archivo
            file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(os.path.abspath(video_path))
            
            # Esperar a que se procese el video
            self.log("⏳ Procesando video...")
            time.sleep(15)
            
            # Rellenar título
            if title:
                self.log("📝 Añadiendo título...")
                title_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='textbox']")))
                title_input.clear()
                title_input.send_keys(title)
            else:
                # Usar descripción como título si no hay título específico
                title_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='textbox']")))
                title_input.clear()
                title_input.send_keys(description if description else "Short Video")
            
            # Rellenar descripción
            if description:
                self.log("📝 Añadiendo descripción...")
                description_input = driver.find_element(By.XPATH, "//textarea[@id='description-textarea']")
                description_input.send_keys(description)
            
            # Click en siguiente varias veces
            self.log("↪️ Avanzando pasos...")
            for i in range(3):
                next_button = wait.until(EC.element_to_be_clickable((By.ID, "next-button")))
                next_button.click()
                time.sleep(3)
                self.log(f"✅ Paso {i+1}/3 completado")
            
            # Publicar
            self.log("✅ Publicando Short...")
            publicar_button = wait.until(EC.element_to_be_clickable((By.ID, "done-button")))
            publicar_button.click()
            
            # Esperar confirmación
            self.log("⏳ Esperando confirmación...")
            time.sleep(10)
            
            return True, "✅ Short publicado exitosamente en YouTube"
            
        except Exception as e:
            return False, f"❌ Error publicando en YouTube: {str(e)}"
        finally:
            if driver:
                driver.quit()
                self.log("🔒 Navegador cerrado")
    
    def log(self, message):
        """Método para logging (será sobreescrito por la GUI)"""
        print(message)

class BotGUI:
    def __init__(self):
        self.bot = SocialMediaBot()
        # Sobrescribir el método log del bot
        self.bot.log = self.log
        self.root = tk.Tk()
        self.setup_gui()
        
    def setup_gui(self):
        """Configurar la interfaz gráfica"""
        self.root.title("Bot para Publicar Reels - MeVoyADarUnLujoDiario")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Bot para Publicar Reels", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Configuración de Instagram
        insta_frame = ttk.LabelFrame(main_frame, text="Configuración Instagram", padding="10")
        insta_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        insta_frame.columnconfigure(1, weight=1)
        
        ttk.Label(insta_frame, text="Usuario:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.insta_user = tk.StringVar(value=self.bot.config["instagram"]["username"])
        ttk.Entry(insta_frame, textvariable=self.insta_user).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(insta_frame, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.insta_pass = tk.StringVar(value=self.bot.config["instagram"]["password"])
        ttk.Entry(insta_frame, textvariable=self.insta_pass, show="*").grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Configuración de YouTube
        yt_frame = ttk.LabelFrame(main_frame, text="Configuración YouTube", padding="10")
        yt_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        yt_frame.columnconfigure(1, weight=1)
        
        ttk.Label(yt_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.yt_email = tk.StringVar(value=self.bot.config["youtube"]["email"])
        ttk.Entry(yt_frame, textvariable=self.yt_email).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(yt_frame, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.yt_pass = tk.StringVar(value=self.bot.config["youtube"]["password"])
        ttk.Entry(yt_frame, textvariable=self.yt_pass, show="*").grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Configuración del navegador
        browser_frame = ttk.LabelFrame(main_frame, text="Configuración de Chrome", padding="10")
        browser_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        browser_frame.columnconfigure(1, weight=1)
        
        ttk.Label(browser_frame, text="Ruta de Chrome (opcional):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.chrome_path = tk.StringVar(value=self.bot.config["chrome_path"])
        ttk.Entry(browser_frame, textvariable=self.chrome_path).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(browser_frame, text="Buscar", command=self.browse_chrome).grid(row=0, column=2, padx=(5, 0))
        
        ttk.Label(browser_frame, text="Modo de navegación:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(browser_frame, text="✅ Chrome en modo incógnito", foreground="green").grid(row=1, column=1, sticky=tk.W, pady=5)
        
        self.headless_var = tk.BooleanVar(value=self.bot.config.get("headless", False))
        ttk.Checkbutton(browser_frame, text="Modo headless (sin interfaz gráfica)", variable=self.headless_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Configuración de video por defecto
        video_config_frame = ttk.LabelFrame(main_frame, text="Configuración de Video por Defecto", padding="10")
        video_config_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        video_config_frame.columnconfigure(1, weight=1)
        
        ttk.Label(video_config_frame, text="Ruta de video por defecto:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.default_video_path = tk.StringVar(value=self.bot.config.get("video_path", ""))
        ttk.Entry(video_config_frame, textvariable=self.default_video_path).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(video_config_frame, text="Buscar", command=self.browse_default_video).grid(row=0, column=2, padx=(5, 0))
        
        # Selección de video actual
        video_frame = ttk.LabelFrame(main_frame, text="Video a Publicar", padding="10")
        video_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        video_frame.columnconfigure(1, weight=1)
        
        ttk.Label(video_frame, text="Ruta del video:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.video_path = tk.StringVar(value=self.bot.config.get("video_path", ""))
        ttk.Entry(video_frame, textvariable=self.video_path).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(video_frame, text="Seleccionar", command=self.browse_video).grid(row=0, column=2, padx=(5, 0))
        
        ttk.Button(video_frame, text="Usar video por defecto", 
                  command=self.use_default_video).grid(row=1, column=0, columnspan=3, pady=5)
        
        # Descripción
        ttk.Label(video_frame, text="Descripción:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.description = tk.StringVar()
        ttk.Entry(video_frame, textvariable=self.description).grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Guardar Configuración", 
                  command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Publicar en Instagram", 
                  command=lambda: self.start_posting("instagram")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Publicar en YouTube", 
                  command=lambda: self.start_posting("youtube")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Publicar en Ambos", 
                  command=lambda: self.start_posting("both")).pack(side=tk.LEFT, padx=5)
        
        # Área de logs
        log_frame = ttk.LabelFrame(main_frame, text="Logs", padding="10")
        log_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, width=60)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def browse_chrome(self):
        """Buscar ejecutable de Chrome"""
        path = filedialog.askopenfilename(
            title="Seleccionar Chrome",
            filetypes=[("Ejecutables", "*.exe"), ("Todos los archivos", "*.*")]
        )
        if path:
            self.chrome_path.set(path)
            
    def browse_default_video(self):
        """Buscar archivo de video por defecto"""
        path = filedialog.askopenfilename(
            title="Seleccionar video por defecto",
            filetypes=[("Videos", "*.mp4 *.mov *.avi *.mkv"), ("Todos los archivos", "*.*")]
        )
        if path:
            self.default_video_path.set(path)
            
    def browse_video(self):
        """Buscar archivo de video"""
        path = filedialog.askopenfilename(
            title="Seleccionar video",
            filetypes=[("Videos", "*.mp4 *.mov *.avi *.mkv"), ("Todos los archivos", "*.*")]
        )
        if path:
            self.video_path.set(path)
            
    def use_default_video(self):
        """Usar el video por defecto configurado"""
        if self.default_video_path.get() and os.path.exists(self.default_video_path.get()):
            self.video_path.set(self.default_video_path.get())
            self.log("✅ Video por defecto cargado correctamente")
        else:
            messagebox.showerror("Error", "No hay un video por defecto configurado o la ruta no existe")
            
    def save_config(self):
        """Guardar configuración"""
        try:
            self.bot.config["instagram"]["username"] = self.insta_user.get()
            self.bot.config["instagram"]["password"] = self.insta_pass.get()
            self.bot.config["youtube"]["email"] = self.yt_email.get()
            self.bot.config["youtube"]["password"] = self.yt_pass.get()
            self.bot.config["chrome_path"] = self.chrome_path.get()
            self.bot.config["video_path"] = self.default_video_path.get()
            self.bot.config["headless"] = self.headless_var.get()
            
            self.bot.save_config()
            self.log("✅ Configuración guardada exitosamente")
            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
        except Exception as e:
            self.log(f"❌ Error guardando configuración: {str(e)}")
            messagebox.showerror("Error", f"Error guardando configuración: {str(e)}")
            
    def start_posting(self, platform):
        """Iniciar publicación en hilo separado"""
        if not self.video_path.get():
            messagebox.showerror("Error", "Selecciona un video primero")
            return
            
        if not os.path.exists(self.video_path.get()):
            messagebox.showerror("Error", "El archivo de video no existe")
            return
            
        # Guardar configuración antes de publicar
        self.save_config()
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.post_content, args=(platform,))
        thread.daemon = True
        thread.start()
        
    def post_content(self, platform):
        """Publicar contenido en las plataformas seleccionadas"""
        video_path = self.video_path.get()
        description = self.description.get()
        
        try:
            if platform in ["instagram", "both"]:
                success, message = self.bot.post_to_instagram(video_path, description)
                
            if platform in ["youtube", "both"]:
                success, message = self.bot.post_to_youtube(video_path, description, description)
                
            self.log("🎉 Proceso completado")
            
        except Exception as e:
            self.log(f"❌ Error durante la publicación: {str(e)}")
            
    def log(self, message):
        """Agregar mensaje al log"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Ejecutar en el hilo principal de tkinter
        self.root.after(0, self._update_log, log_message)
        
    def _update_log(self, message):
        """Actualizar el widget de texto (debe ejecutarse en el hilo principal)"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        # Verificar dependencias
        try:
            import selenium
            import tkinter
        except ImportError as e:
            print(f"Error: Faltan dependencias. Instala con: pip install selenium")
            return
            
        app = BotGUI()
        app.run()
        
    except Exception as e:
        print(f"Error iniciando la aplicación: {e}")

if __name__ == "__main__":
    main()