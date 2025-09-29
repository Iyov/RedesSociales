# 🤖 Redes Sociales Bot
Bot automatizado para publicar videos en Instagram Reels y YouTube Shorts.

## 🚀 Características
- 📱 Instagram Reels: Publicación automática en tu perfil
- 🎬 YouTube Shorts: Subida automática a tu canal
- 🔒 Chrome Incógnito: Navegación privada y segura
- ⚙️ Configuración persistente: Guarda tus credenciales
- 🎯 Video por defecto: Configura un video predeterminado
- 📊 Logs en tiempo real: Seguimiento del proceso

## 📦 Instalación
Instalar dependencias:
```
bash
pip install selenium
```
Ejecutar el bot:
```
bash
python main.py
```
## ⚙️ Configuración
Edita social_media_config.json o usa la interfaz gráfica:
```
json
{
    "instagram": {
        "username": "tu_usuario_instagram",
        "password": "tu_contraseña_instagram",
        "profile_url": "https://www.instagram.com/tu_usuario/"
    },
    "youtube": {
        "email": "tu_email_youtube@gmail.com",
        "password": "tu_contraseña_youtube",
        "channel_url": "https://www.youtube.com/@tu_usuario"
    },
    "chrome_path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "video_path": "C:\\Users\\TuUsuario\\Videos\\mi_reel.mp4",
    "headless": false
}
```
## 🎯 Uso
- Configura tus credenciales en la interfaz.
- Selecciona o configura un video por defecto.
- Haz clic en "Publicar en Instagram" o "Publicar en YouTube".
- ¡Listo! El bot hará todo automáticamente.

## 🔧 Requisitos
- Python 3.8+
- Chrome Browser
- Cuentas en Instagram y YouTube

## 📝 Notas
El bot funciona en modo incógnito para mayor privacidad.
Los videos deben cumplir con los requisitos de cada plataforma.
La primera ejecución puede ser más lenta mientras se cargan las dependencias.

### Desarrollado por Francisco Barrientos (https://github.com/Iyov)

