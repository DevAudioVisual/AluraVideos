
"""
python -m nuitka --onefile --run --windows-file-version=0.0.4 --windows-product-version=0.0.4 --include-data-dir=./ffmpeg=ffmpeg --include-data-dir=./Config=Config --include-data-dir=./Templates=Templates --include-data-dir=./Assets=Assets --windows-icon-from-ico=./Assets/Icons/icon.ico --windows-company-name=SamuelMariano --windows-product-name=AluraVideos --output-dir=dist --output-filename=AluraVideos.exe --enable-plugin=pyqt6 --lto=yes --full-compat --follow-imports --remove-output --windows-console-mode=disable Main.py
"""

from plyer import notification

notification.notify(
    title='Título da Notificação',
    message='Esta é uma notificação de exemplo usando Plyer',
    app_name='Meu App',  # Nome do seu aplicativo (opcional)
    app_icon=None,  # Caminho para um ícone personalizado (opcional)
    
)