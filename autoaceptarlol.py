#  Auto-Accept LOL
#  V. 1.1.1
#  Arturo Jorge

import tkinter as tk
import pyautogui as pya
from ctypes import windll
from threading import Thread
from pynput.mouse import Listener

pick_color = False
pick_button = False

#region Set
def set_color(x, y):
    global pos
    pos = (x, y)
    pick_color = True
    

def set_button(x, y):
    global posclick
    posclick = (x, y)
    pick_button = True

#endregion

#region mouse input
def on_click_color(x, y, button, pressed):
    if pressed:
        set_color(x, y)
        return False
def on_click_button(x, y, button, pressed):
    if pressed:
        set_button(x, y)
        return False
    
def leer_color():
    # Crear un listener para el evento de clic del ratón
    with Listener(on_click=on_click_color) as listener:
        listener.join()  # Inicia el listener

def leer_click():
    # Crear un listener para el evento de clic del ratón
    with Listener(on_click=on_click_button) as listener:
        listener.join()  # Inicia el listener

#endregion

#region auto-accept match
def accept_match(stop, waiting_window):
    hdc = windll.user32.GetDC(0)
    found_color = 1591641
    
    while stop[0]:
        if pick_color:
            pixel_color = windll.gdi32.GetPixel(hdc, pos[0], pos[1])
        else:
            pixel_color = windll.gdi32.GetPixel(hdc, 1314, 126)
        if pixel_color == found_color:
            if pick_button:
                for i in range(0, 30):
                    pya.click(posclick[0], posclick[1])
                    i += 1
            else:
                for i in range(0, 30):
                    pya.click(955, 793)
                    i += 1
                            
            stop[0] = False
        else:
            pass
    
    
    waiting_window.destroy()

def exec_and_return():
    stop = [True]
    waiting_window = show_waiting(stop)
    Thread(target=accept_match, args=(stop, waiting_window)).start()

#endregion

#region gui
def show_waiting(stop):
    def detener():
        stop[0] = False
        waiting_window.destroy()

    waiting_window = tk.Toplevel(root)
    waiting_window.title("Esperando...")
    waiting_window.geometry("400x300")
    waiting_window.config(bg="#2B2B2B")  # Dark background

    waiting_label = tk.Label(waiting_window, text="Esperando...", font=("Arial", 12), bg="#2B2B2B", fg="#0080FF")  # Texto celeste sobre fondo oscuro
    waiting_label.pack(padx=50, pady=50)

    cancel_button = tk.Button(waiting_window, text="Cancelar", command=detener, bg="#444444", fg="white")  # Botón oscuro con texto blanco
    cancel_button.pack()

    waiting_window.protocol("WM_DELETE_WINDOW", detener)

    

    return waiting_window



# Creates the main interface
root = tk.Tk()
root.title("Auto-aceptar partidas")
root.geometry("400x400")
root.config(bg="#2B2B2B")  # Dark background
main_label = tk.Label(root, text="Auto-aceptar partidas de lol", font=("Arial", 12), bg="#2B2B2B", fg="white")  # Text
main_label.pack(padx=50, pady=50)

# Buttons

define_color_btn = tk.Button(root, text="Definir color", command=leer_color, bg="#444444", fg="white")  
define_color_btn.pack()
define_place_to_click_btn = tk.Button(root, text="Definir aceptar", command=leer_click, bg="#444444", fg="white")  
define_place_to_click_btn.pack()
wait_btn = tk.Button(root, text="Esperar partida", command=exec_and_return, bg="#444444", fg="white")  # Start Button
wait_btn.pack()
#endregion

root.mainloop()
