import tkinter as tk
import pyautogui as pya
from ctypes import windll
from threading import Thread
from pynput.mouse import Listener

def set_color(x, y):
    global pos
    pos = (x, y)

def set_click(x, y):
    global posclick
    posclick = (x, y)

def on_click_color(x, y, button, pressed):
    if pressed:
        set_color(x, y)
        return False
def on_click_click(x, y, button, pressed):
    if pressed:
        set_click(x, y)
        return False
    
def leer_color():
    # Crear un listener para el evento de clic del ratón
    with Listener(on_click=on_click_color) as listener:
        listener.join()  # Inicia el listener

def leer_click():
    # Crear un listener para el evento de clic del ratón
    with Listener(on_click=on_click_click) as listener:
        listener.join()  # Inicia el listener


def mostrar_esperando(stop):
    def detener():
        stop[0] = False
        waiting_window.destroy()

    waiting_window = tk.Toplevel(root)
    waiting_window.title("Esperando...")
    waiting_window.geometry("400x300")
    waiting_window.config(bg="#2B2B2B")  # Fondo oscuro

    waiting_label = tk.Label(waiting_window, text="Esperando...", font=("Arial", 12), bg="#2B2B2B", fg="#0080FF")  # Texto celeste sobre fondo oscuro
    waiting_label.pack(padx=50, pady=50)

    cancel_button = tk.Button(waiting_window, text="Cancelar", command=detener, bg="#444444", fg="white")  # Botón oscuro con texto blanco
    cancel_button.pack()

    waiting_window.protocol("WM_DELETE_WINDOW", detener)

    

    return waiting_window

def ejecutar_codigo(stop, waiting_window):
    hdc = windll.user32.GetDC(0)
    color_apagado = 1591641
    
    while stop[0]:
        color_actual = windll.gdi32.GetPixel(hdc, pos[0], pos[1])
        
        if color_actual == color_apagado:
            for i in range(0, 30):
                pya.click(posclick[0], posclick[1])
                i += 1
                
            stop[0] = False
        else:
            pass
    
    waiting_window.destroy()

def ejecutar_y_volver():
    stop = [True]
    waiting_window = mostrar_esperando(stop)
    Thread(target=ejecutar_codigo, args=(stop, waiting_window)).start()

# Crear la interfaz gráfica principal
root = tk.Tk()
root.title("Auto-aceptar partidas")
root.geometry("400x400")
root.config(bg="#2B2B2B")  # Fondo oscuro

# Botón para ejecutar el código
main_label = tk.Label(root, text="Auto-aceptar partidas de lol", font=("Arial", 12), bg="#2B2B2B", fg="white")  # Texto blanco sobre fondo oscuro
main_label.pack(padx=50, pady=50)
definir_btn = tk.Button(root, text="Definir color", command=leer_color, bg="#444444", fg="white")  # Botón oscuro con texto blanco
definir_btn.pack()
definir_click_btn = tk.Button(root, text="Definir aceptar", command=leer_click, bg="#444444", fg="white")  # Botón oscuro con texto blanco
definir_click_btn.pack()
ejecutar_btn = tk.Button(root, text="Esperar partida", command=ejecutar_y_volver, bg="#444444", fg="white")  # Botón oscuro con texto blanco
ejecutar_btn.pack()

root.mainloop()
