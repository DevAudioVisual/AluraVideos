import logging
import os
import signal
import sys
import threading
from Modelos.Interface import Interface
from Config import LoadConfigCache, LoadConfigCriarProjeto, LoadConfigInterface, LoadConfigAtalhos
from Util import Util
from logging.handlers import TimedRotatingFileHandler

from z_Testes import InterfaceConfig

titulo = "S_AluraVideos " + Util.version
InterfacePrincipal = None


def main():
    global InterfacePrincipal
    setup_signal_handlers()
    setup_logging()

    LoadConfigInterface.iniciarConfig()
    LoadConfigAtalhos.iniciarConfig()
    LoadConfigCache.iniciarConfig()
    LoadConfigCriarProjeto.IniciarConfig()
    InterfaceP()
    pass


def setup_signal_handlers():
    signal.signal(signal.SIGINT, handle_interrupt)


def handle_interrupt(signum, frame):
    print("Programa interrompido.")
    sys.exit(0)


def setup_logging():
    log_dir = os.path.join(os.path.expanduser(
        "~"), "Documents", "S_AluraVideos", "Logs")
    os.makedirs(log_dir, exist_ok=True)

    # Nome base do arquivo de log
    log_file = os.path.join(log_dir, "s_AluraVideos.log")
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=15
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.suffix = "%Y-%m-%d"  # Sufixo para incluir a data no nome do arquivo

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
    logging.error("Exceção não tratada", exc_info=(
        exc_type, exc_value, exc_traceback))


def thread_exception_handler(args):
    logging.error("Exceção não tratada em thread", exc_info=(
        args.exc_type, args.exc_value, args.exc_traceback))


def InterfaceP():
    InterfacePrincipal = Interface.App()
    InterfacePrincipal.carregarInterfacePrincipal()
    # InterfaceConfig.GerenciadorAtalhos(Interface.root)
    InterfacePrincipal.getRoot().mainloop()


if __name__ == '__main__':
    main()
