import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PIL import Image, ImageTk
import cv2
import threading
import time
from ultralytics import YOLO
from utils.json_loader import sayac_arttir,bakiye_arttir
import serial

# Arduino seri bağlantısı (örneğin COM3 olabilir)
arduino = serial.Serial('COM11', 9600, timeout=1)
time.sleep(2)  # Bağlantı stabil hale gelsin

class AtikTespit:
    def __init__(self,uid, display_callback=None, detect_callback=None):
        self.uid=uid
        self.model = YOLO("C:\\Users\\Tuncer\\Desktop\\Desktop\\Proje\\models\\best.pt")
        self.display_callback = display_callback
        self.detect_callback = detect_callback
        self.running = False

        self.sayaclar = {
            "plastik": 0,
            "cam": 0,
            "metal": 0,
            "kagit": 0
        }

        self.last_detection_time = time.time()  # Başlangıç zamanı → ilk 10 sn tespit yapılmaz

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._kamera_dongusu, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _kamera_dongusu(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Kamera açılamadı")
            return

        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue

            current_time = time.time()

            # İlk 10 saniye geçtikten sonra tespit yapılır
            if current_time - self.last_detection_time >= 10:
                self._tek_tespit(frame)
                self.last_detection_time = current_time

            # Kamera görüntüsünü göster
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            if self.display_callback:
                self.display_callback(imgtk)

        cap.release()
        print("Kamera kapatıldı")

    def _tek_tespit(self, frame):
        results = self.model.predict(source=frame, stream=True)
        for r in results:
            if r.boxes:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    class_name = self.model.names[cls_id].lower()

                    if class_name in ["plastik", "cam", "metal", "kagit"]:
                        sayac_arttir(self.uid, class_name)
                        bakiye_arttir(self.uid, class_name)
                        print(f"[Tespit] {class_name} bulundu → Sayaç güncellendi")
                        
                        if self.detect_callback:
                            self.detect_callback(class_name)

                        # ⬇️ Atık türüne göre komut belirle ve Arduino'ya gönder
                        if class_name == "plastik":
                            arduino.write(b'a')  # 90°
                        elif class_name == "cam":
                            arduino.write(b'b')  # 180°
                        elif class_name == "metal":
                            arduino.write(b'w')  # 270°
                        elif class_name == "kagit":
                            arduino.write(b's')  # 360°
                    else:
                        print(f"[UYARI] Tanımsız sınıf adı: {class_name}")