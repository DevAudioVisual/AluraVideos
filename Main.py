import logging
from logging.handlers import TimedRotatingFileHandler
import os
import signal
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QLocale
from Models.AutoUpdate import AutoUpdate
from QtInterfaces.Interfaces.LoadingScreen.LoadingScreen import LoadingScreen, LoadingThread
from QtInterfaces.Interfaces.MainWindow import MainWindow
import ctypes
import sys
import qtsass
import os
from Util import Tokens

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        executable = sys.executable
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)      
        sys.exit()

def main():
    run_as_admin()
    setup_signal_handlers()
    setup_logging()
    
    app = QApplication(sys.argv) 
    #app.setStyle("Windows")
    locale = QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil)
    QLocale.setDefault(locale)
    
    qtsass.compile_filename(r'style.scss', r'style.qss')
    with open(r"style.qss", "r") as f:
             stylesheet = f.read()
    app.setStyleSheet(stylesheet)

    loading_screen = LoadingScreen()
    loading_screen.show()

    loading_thread = LoadingThread()

    loading_thread.progress_updated.connect(loading_screen.update_progress)
    loading_thread.etapa.connect(loading_screen.update_etapa)
    def _updates():
        if Tokens.LoadKeys():
            AutoUpdate.app().check_updates()
    loading_thread.execute_in_main_thread.connect(lambda: _updates())  
    loading_thread.finished.connect(loading_screen.close)
    loading_thread.finished.connect(MainWindow.create_main_window)

    # Conecta o sinal aboutToQuit ao slot que encerra a thread
    app.aboutToQuit.connect(loading_thread.quit)

    loading_thread.start()

    def on_message_received(message):
        print(f"Mensagem recebida na janela principal: {message}")
    # websocket_server = WebSocketServer()
    # websocket_server.message_received.connect(on_message_received)
    # websocket_server.start()


    sys.exit(app.exec())
    
def setup_signal_handlers():
    signal.signal(signal.SIGINT, handle_interrupt)


def handle_interrupt(signum, frame):
    print("Programa interrompido.")
    sys.exit(0)

def setup_logging():
    log_dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos", "Logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "AluraVideos.log")
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=15
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.suffix = "%Y-%m-%d.log" 

    stream_handler = logging.StreamHandler()

    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[file_handler, stream_handler]
    )

    sys.excepthook = handle_exception
    threading.excepthook = thread_exception_handler


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Exceção não tratada", exc_info=(exc_type, exc_value, exc_traceback))


def thread_exception_handler(args):
    logging.error("Exceção não tratada em thread", exc_info=(args.exc_type, args.exc_value, args.exc_traceback))

if __name__ == '__main__':
    main()