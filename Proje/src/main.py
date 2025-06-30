import customtkinter as ctk
import threading
import serial
import time
from kullanici_arayuzu import Gui
from Tespit import AtikTespit

gui = None

def rfid_listener(port='COM10', baud=9600):
    global gui
    try:
        ser = serial.Serial(port, baud, timeout=1)
        print("[INFO] RFID dinleniyor...")
        while True:
            line = ser.readline().decode(errors='ignore').strip()
            if line.startswith("CARD_DETECTED:"):
                isim = line.split(":")[1].strip().upper()  
                print(f"[INFO] Kart okundu → {isim}")
                gui.kart_okundu(isim)
                break
    except serial.SerialException as e:
        print(f"[HATA] Seri port hatası: {e}")


def main():
    global gui
    root = ctk.CTk()
    gui = Gui(root)
    thread = threading.Thread(target=rfid_listener, daemon=True)
    thread.start()
    root.mainloop()

if __name__ == "__main__":
    main()
