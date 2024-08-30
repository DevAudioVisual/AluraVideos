import tkinter as tk
import pyautogui
import cv2
import numpy as np

#TODO integrar a print no chatbot do gemini

def selecionar_roi():
    # Capturar a tela inteira
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Função para desenhar o retângulo de seleção
    def desenhar_retangulo(event, x, y, flags, param):
        nonlocal x1, y1, x2, y2, desenhando
        if event == cv2.EVENT_LBUTTONDOWN:
            desenhando = True
            x1, y1 = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if desenhando:
                x2, y2 = x, y
                img_copia = img.copy()
                cv2.rectangle(img_copia, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.imshow('Selecione a ROI', img_copia)
        elif event == cv2.EVENT_LBUTTONUP:
            desenhando = False
            x2, y2 = x, y
            cv2.destroyAllWindows()

    # Criar a janela para seleção da ROI
    cv2.namedWindow('Selecione a ROI')
    cv2.setMouseCallback('Selecione a ROI', desenhar_retangulo)
    cv2.imshow('Selecione a ROI', img)

    # Aguardar a seleção da ROI
    x1, y1, x2, y2 = 0, 0, 0, 0
    desenhando = False
    cv2.waitKey(0)

    # Recortar a ROI e salvar a imagem
    roi = img[y1:y2, x1:x2]
    cv2.imwrite('roi.png', roi)

# Interface Tkinter
selecionar_roi()