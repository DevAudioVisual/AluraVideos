import logging
from logging.handlers import TimedRotatingFileHandler
import os
import signal
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator,QLocale
from QtInterfaces.LoadingScreen.LoadingScreen import LoadingScreen, LoadingThread
from QtInterfaces.MainWindow import MainWindow
import ctypes
import sys
import os

def is_admin():
    """Verifica se o script está sendo executado como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Tenta reexecutar o script com permissões administrativas sem abrir o CMD"""
    if not is_admin():
        # Obter o caminho completo do executável do Python
        executable = sys.executable
        
        # Executa o script novamente como administrador, mas sem abrir o CMD
        params = ' '.join([f'"{arg}"' for arg in sys.argv])  # Junta os argumentos com aspas
        
        # Usar o comando ShellExecuteW com a flag 'runas' para privilégios administrativos
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", executable, params, None, 1)
        
        # Encerra o script atual, pois ele será reexecutado com privilégios elevados
        sys.exit()

def main():
    #run_as_admin()

    setup_signal_handlers()
    setup_logging()
    
    app = QApplication(sys.argv) 
    translator = QTranslator()
    if translator.load("qtbase_pt_BR", ":/translations"):  # Verifique o caminho correto para o arquivo de tradução
        app.installTranslator(translator)
    locale = QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil)
    QLocale.setDefault(locale)
    with open(r"Assets\styles\style.css", "r") as f:
             stylesheet = f.read()
    app.setStyleSheet(stylesheet)

    loading_screen = LoadingScreen()
    loading_screen.show()

    loading_thread = LoadingThread()

    loading_thread.progress_updated.connect(loading_screen.update_progress)
    loading_thread.etapa.connect(loading_screen.update_etapa)
    loading_thread.finished.connect(loading_screen.close)
    loading_thread.finished.connect(MainWindow.create_main_window)

    # Conecta o sinal aboutToQuit ao slot que encerra a thread
    app.aboutToQuit.connect(loading_thread.quit)

    loading_thread.start()

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