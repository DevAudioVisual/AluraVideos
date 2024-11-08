import os
import sys
import signal
import logging
import ctypes
import threading
from logging.handlers import TimedRotatingFileHandler
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QLocale
from Models.AutoUpdate import AutoUpdate
from QtInterfaces.Interfaces.LoadingScreen.LoadingScreen import LoadingScreen, LoadingThread
from QtInterfaces.Interfaces.MainWindow import MainWindow
import qtsass
from Util import Tokens
from dotenv import load_dotenv

# Metadados da aplicação
__version__ = "V1.1.0"
__company_name__ = "DevAudioVisual"
__copyright__ = "Copyright 2024"
__author__ = "Samuel Mariano"

# Função para verificar se o usuário possui permissões de administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Reinicia o programa como administrador caso necessário
def run_as_admin():
    if not is_admin():
        executable = sys.executable
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
        sys.exit()

# Função principal da aplicação
def main():
    #run_as_admin()
    load_dotenv()
    # Configurações de inicialização
    setup_signal_handlers()
    setup_logging()
    
    # Cria a aplicação e define a localidade para Português (Brasil)
    app = QApplication(sys.argv)
    locale = QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil)
    QLocale.setDefault(locale)
    
    # Compila o arquivo .scss para .qss e aplica o estilo
    try:
        qtsass.compile_filename(r'styles\style.scss', r'styles\style.qss')
    except Exception as e:
        import Util.Util as util
        util.LogError("QtSass", e, False)
        
    # Carrega e define a folha de estilo da aplicação
    try:
        with open(r"styles\style.qss", "r") as f:
            stylesheet = f.read()
        app.setStyleSheet(stylesheet)
    except Exception as e:
        util.LogError("SetStyleSheet", f"Ocorreu um erro ao definir a estilização:\n{e}", False)
    
    # Inicializa a tela de carregamento e a thread associada
    loading_screen = LoadingScreen()
    loading_screen.show()
    loading_thread = LoadingThread()
    
    # Conecta sinais de progresso e atualizações de etapas
    loading_thread.progress_updated.connect(loading_screen.update_progress)
    loading_thread.etapa.connect(loading_screen.update_etapa)
    
    # Executa a verificação de atualização em thread principal, se chaves forem carregadas      
    loading_thread.execute_in_main_thread.connect(lambda: AutoUpdate.app().check_updates())

    # Finaliza tela de carregamento e inicializa a janela principal
    loading_thread.finished.connect(loading_screen.close)
    loading_thread.finished.connect(MainWindow.create_main_window)
    
    # Conecta sinal para encerrar a thread ao fechar o aplicativo
    app.aboutToQuit.connect(loading_thread.quit)
    loading_thread.start()

    sys.exit(app.exec())

# Configura sinais de interrupção para encerrar o programa com segurança
def setup_signal_handlers():
    signal.signal(signal.SIGINT, handle_interrupt)

# Função para lidar com interrupções do sistema
def handle_interrupt(signum, frame):
    print("Programa interrompido.")
    sys.exit(0)

# Configura o sistema de logging
def setup_logging():
    # Cria diretório de logs e configura o arquivo de log rotativo
    log_dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos", "Logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "AluraVideos.log")
    
    # Configuração do handler de arquivo
    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=15
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.suffix = "%Y-%m-%d.log" 

    # Configuração do handler de saída de console
    stream_handler = logging.StreamHandler()

    # Configuração do sistema de log
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[file_handler, stream_handler]
    )

    # Define handlers de exceção para logs de erros
    sys.excepthook = handle_exception
    threading.excepthook = thread_exception_handler

# Tratamento de exceções globais
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Exceção não tratada", exc_info=(exc_type, exc_value, exc_traceback))

# Tratamento de exceções para threads
def thread_exception_handler(args):
    logging.error("Exceção não tratada em thread", exc_info=(args.exc_type, args.exc_value, args.exc_traceback))

# Ponto de entrada da aplicação
if __name__ == '__main__':
    main()
