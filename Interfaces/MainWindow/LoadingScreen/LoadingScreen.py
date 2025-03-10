from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QLinearGradient,QColor
from PyQt6.QtWidgets import QWidget
import Util.CustomWidgets as cw
global Config

versao_effector = None
versao_ordinem = None
versao_notabillity = None

notes_effector = None
notes_ordinem = None
notes_notability = None

class LoadingScreen(cw.Widget):
    def __init__(self):
        super().__init__()
        #self.setFixedSize(500, 300)
        #self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint)
        
        layoutPrincipal = cw.HBoxLayout()
        self.setLayout(layoutPrincipal)
        
        class layoutEsquerda(QWidget):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)                    
                
                layout = cw.VBoxLayout()
                
                pixmap = QPixmap(r"Assets\Icons\icon.ico")  # Substitua "imagem.png" pelo caminho da sua imagem

                image_label = cw.Label()
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centraliza a imagem
                image_label.setObjectName("teste")
                import Main
                text_label = cw.Label(f"AluraVideos <font face='Helvetica' style='font-size: 13px;'>{Main.version}</font>")
                text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                text_label.setObjectName("extra-grande")
                
                text_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
                image_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
                
                layout.addWidget(text_label)
                layout.addWidget(image_label)
                
                self.setLayout(layout)
                
        
        layoutDireita = cw.VBoxLayout()
        layoutDireita.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layoutPrincipal.addWidget(layoutEsquerda())
        layoutPrincipal.addLayout(layoutDireita)

        self.label = cw.Label('Carregando')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(500)  # Atualiza a cada 500 milissegundos
        self.counter = 0
        
        self.etapa = cw.Label('Etapa atual: ')
        self.etapa.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.etapa.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.etapa.setMinimumWidth(250)

        self.progressBar = cw.ProgressBar()
        self.progressBar.setValue(0)
        
        layoutDireita.addWidget(self.label)
        layoutDireita.addWidget(self.etapa)
        layoutDireita.addWidget(self.progressBar)
        
    def update_text(self):
        self.counter += 1
        if self.counter > 3:
            self.counter = 0
        ponto = "." * self.counter
        self.label.setText(f"Carregando{ponto}")
    
    def update_etapa(self, etapa):
        self.etapa.setText(f"Etapa atual: {etapa}")
    def update_progress(self, value):
        self.progressBar.setValue(value)
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor(0x4C3BCF))  # Cor inicial
        gradient.setColorAt(1.0, QColor(0x6c757d))  # Cor final
        painter.fillRect(self.rect(), gradient)
    def showEvent(self, event):
        # Centralizar a janela no monitor atual após ela ser exibida
        qtRectangle = self.frameGeometry()
        centerPoint = self.window().windowHandle().screen().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        super().showEvent(event)
        

        

        