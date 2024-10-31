from PyQt6.QtWidgets import QSlider,QMenu, QScrollArea, QGroupBox,QCheckBox, QTableWidgetItem, QStackedWidget, QProgressBar, QToolButton,QToolBar, QApplication, QMainWindow, QMessageBox, QListWidgetItem, QComboBox, QPushButton, QLabel, QSpacerItem, QVBoxLayout, QWidget, QGridLayout, QSizePolicy, QLineEdit, QTableWidget, QListWidget, QHBoxLayout
from PyQt6.QtGui import QCursor,QTransform
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, QSize

class Slider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class Menu(QMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ScrollArea(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class GroupBox(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CheckBox(QCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

class TableWidgetItem(QTableWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class StackedWidget(QStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ToolButton(QToolButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ToolBar(QToolBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ListWidgetItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
class ListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class LineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Label(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class PushButton(QPushButton):
    def __init__(self, *args, animacao=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.animacao = animacao
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.adjustSize()
        #self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        if self.animacao:
            self.anim = QPropertyAnimation(self, b'geometry')
            self.anim.setDuration(250)
            self.anim.setEasingCurve(QEasingCurve.Type.OutCurve)

    def enterEvent(self, event):
        if self.animacao:
            self.anim.setDirection(self.anim.Direction.Forward)
            if self.anim.state() == self.anim.State.Stopped:
                self.anim.setStartValue(self.geometry())
                width = self.geometry().width() + 4
                height = self.geometry().height() + 4
                x = self.x() - 2
                y = self.y() - 2
                self.anim.setEndValue(QRect(x, y, width, height))
                self.anim.start()
        QPushButton.enterEvent(self, event)

    def leaveEvent(self, event):
        if self.animacao:
            self.anim.setDirection(self.anim.Direction.Backward)
            if self.anim.state() == self.anim.State.Stopped:
                self.anim.start()
        QPushButton.leaveEvent(self, event)
        
class SpacerItem(QSpacerItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)          
             
class VBoxLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setContentsMargins(10, 10, 10, 10)
        
class HBoxLayout(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)      
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setContentsMargins(10, 10, 10, 10)  
        
class GridLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setContentsMargins(10, 10, 10, 10)
        
class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        
class SizePolicy(QSizePolicy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class alignWidget(QHBoxLayout):
    def __init__(self, widget):
        super().__init__()
        self.addWidget(widget)
        self.setCenter()
    def setCenter(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    def setCenterAndTop(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
class setSizePolicy():
    def __init__(self, widget):
        self.widget = widget
    def setFixed(self):
        self.widget.setSizePolicy(SizePolicy.Policy.Fixed, SizePolicy.Policy.Fixed)
    def setMaximum(self):
        self.widget.setSizePolicy(SizePolicy.Policy.Maximum, SizePolicy.Policy.Maximum)
        
def setGeometry(widget):
    widget.setGeometry(QRect())