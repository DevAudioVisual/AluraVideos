import sys
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction

class SystemTrayIcon():
    def __init__(self, app):
      # Crie o ícone da bandeja
      self.app = app
      
      self.tray_icon = QSystemTrayIcon(QIcon(r"Assets\Icons\icon.ico"), app)
      self.tray_icon.activated.connect(lambda reason: self.left_click() if reason == QSystemTrayIcon.ActivationReason.Trigger else None)
      self.tray_icon.messageClicked.connect(self.left_click)
      self.tray_icon.setToolTip("AluraVideos")
      self.tray_icon.show()
      
      tray_menu = QMenu()
      tray_menu.addAction("Em breve")
      tray_menu.addAction("Em breve")
      self.tray_icon.setContextMenu(tray_menu)

      # Função para clique com o botão esquerdo
    def left_click(self):
        if self.app.isHidden():
          self.app.show()
        
        