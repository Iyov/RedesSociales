from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional
import time
import os

class BrowserManager:
    """Gestor del navegador DuckDuckGo"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
    
    def start_browser(self):
        """Inicia el navegador Chrome con DuckDuckGo"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Para evitar detección de automation
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Ejecutar script para evitar detección
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        return self.driver
    
    def navigate_to_duckduckgo(self):
        """Navega a DuckDuckGo"""
        if not self.driver:
            self.start_browser()
        
        self.driver.get("https://duckduckgo.com")
        time.sleep(2)
        return self.driver
    
    def wait_for_element(self, by, value, timeout: int = 15):
        """Espera a que un elemento esté presente"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    def wait_for_element_clickable(self, by, value, timeout: int = 15):
        """Espera a que un elemento sea clickeable"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
    
    def find_element_safe(self, by, value, timeout: int = 5):
        """Encuentra un elemento de forma segura (no lanza excepción si no existe)"""
        try:
            return self.wait_for_element(by, value, timeout)
        except:
            return None
    
    def scroll_to_element(self, element):
        """Desplaza hasta un elemento"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
    
    def take_screenshot(self, filename: str = "screenshot.png"):
        """Toma una captura de pantalla"""
        self.driver.save_screenshot(filename)
        print(f"📸 Captura guardada: {filename}")
    
    def close(self):
        """Cierra el navegador"""
        if self.driver:
            self.driver.quit()