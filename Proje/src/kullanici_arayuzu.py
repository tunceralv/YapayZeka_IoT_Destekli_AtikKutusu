import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import customtkinter as ctk
from threading import Thread
from PIL import Image, ImageTk
from Tespit import AtikTespit
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from utils.json_loader import kullanici_yukle_by_name,kullanici_yukle,sehir_ekle

class Gui:
    def __init__(self, root):
        self.root = root
        self.yolo=None
        
        # Ekran çözünürlüğü sabit ve optimum
        self.root.geometry("900x700")
        self.root.title("Otomatik Atık Tanıma Sistemi")

        # Tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Frame'leri önce tanımla
        self.content_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#f8f8f8")
        self.content_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.frame_home = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color="white")
        self.frame_help = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color="white")

        self.frames = {
            "home": self.frame_home,
            "help": self.frame_help
        }

        # Ana sayfa slider verileri
        self.slider_images = [
            ("C:\\Users\\Tuncer\\Desktop\\Desktop\\PROJELER\\B211210074_Tasarim\\AtikTespit\\images\\slider1.jpg", "Geri dönüşüm doğal kaynakları korur ve atıkları azaltır."),
            ("C:\\Users\\Tuncer\\Desktop\\Desktop\\PROJELER\\B211210074_Tasarim\\AtikTespit\\images\\slider2.jpg", "Bir alüminyum kutu geri dönüşümü, enerjinin %95'ini tasarruf eder."),
            ("C:\\Users\\Tuncer\\Desktop\\Desktop\\PROJELER\\B211210074_Tasarim\\AtikTespit\\images\\slider3.jpg", "1 ton kağıt geri dönüşümü, 17 ağacın kesilmesini engeller."),
            ("C:\\Users\\Tuncer\\Desktop\\Desktop\\PROJELER\\B211210074_Tasarim\\AtikTespit\\images\\slider4.jpg", "1 ton kağıt geri dönüşümü, 17 ağacın kesilmesini engeller."),
        ]
        self.current_slide = 0

        # Menü sonra oluşturulmalı çünkü build_home içinde referans verilen widget'lar var
        self.menu_frame = ctk.CTkFrame(self.root, width=200, corner_radius=15, fg_color="#f2f2f2")
        self.menu_frame.pack(side="left", fill="y", padx=10, pady=10)

     
        # Tüm frame'leri oluştur
        self.build_menu()
        self.build_home()
        self.build_help()

        # Slider başlat
        Thread(target=self.update_slider, daemon=True).start()
        self.show_frame("home")
    def update_slider(self):
        while True:
            img_path, info = self.slider_images[self.current_slide]
            try:
                image = Image.open(img_path).resize((600, 300))
                photo = ImageTk.PhotoImage(image)
                self.lbl_slider_image.configure(image=photo)
                self.lbl_slider_image.image = photo
                self.lbl_slider_text.configure(text=info)
            except FileNotFoundError:
                self.lbl_slider_text.configure(text="Resim bulunamadı!")

            self.current_slide = (self.current_slide + 1) % len(self.slider_images)
            time.sleep(5)    

    def build_menu(self):
        ctk.CTkButton(self.menu_frame, text="Ana Sayfa", command=lambda: self.show_frame("home"),
              fg_color="#1e5631", hover_color="#145c2a").pack(pady=10, fill="x")
        ctk.CTkButton(self.menu_frame, text="Yardım", command=lambda: self.show_frame("help"),
              fg_color="#1e5631", hover_color="#145c2a").pack(pady=10, fill="x")
        ctk.CTkButton(self.menu_frame, text="Çıkış", command=self.root.quit,
              fg_color="#8B0000", hover_color="#B22222").pack(pady=40, fill="x")

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def build_home(self):
        self.lbl_slider_image = ctk.CTkLabel(self.frame_home, text="")
        self.lbl_slider_image.pack(pady=10)

        self.lbl_slider_text = ctk.CTkLabel(
        self.frame_home,
        text="",
        font=("Segoe UI", 16),
        wraplength=600,
        justify="center"
    )
        self.lbl_slider_text.pack(pady=10)
        # 📌 Metin kutusu ekleniyor
        metin = (
            "Geri Dönüşüm: Geleceğe Umutla Bakmanın İlk Adımı\n\n"
            "Geri dönüşüm, sadece atıkların dönüştürülmesi değil; aynı zamanda doğal kaynakların korunması, enerji tasarrufu "
            "sağlanması ve çevrenin gelecek nesillere temiz bir şekilde aktarılması için atılan en önemli adımlardan biridir. "
            "Bir ton kağıdın geri dönüşümüyle 17 ağacın kesilmesi engellenirken, bir alüminyum kutunun geri dönüşümüyle enerjinin "
            "%95’i tasarruf edilir. Küçük bir hareketin, büyük etkiler yaratabileceğini görmek, geri dönüşümü yalnızca bir sorumluluk "
            "değil, aynı zamanda bir fırsat haline getirir.\n\n"
            "Geri dönüşüm, aynı zamanda çevre kirliliğini azaltır ve daha az atık oluşmasını sağlar. Plastik, kağıt, cam gibi malzemelerin "
            "doğru şekilde geri kazanımı, okyanuslarımızı, ormanlarımızı ve yaşadığımız çevreyi koruma altına alır. Her bir geri dönüşüm "
            "hareketi, sadece doğayı korumakla kalmaz; aynı zamanda geleceğe duyduğumuz umudu da güçlendirir.\n\n"
            "Unutmayın, her geri dönüşüm hareketi bir değişimin başlangıcıdır. Bugün attığınız adımlar, yarın daha yeşil, daha yaşanabilir "
            "bir dünya demektir. Dünyayı değiştirmek için ihtiyacınız olan tek şey, bir adımla başlamak!"
        )

        # Scrollable metin kutusu (read-only)
        textbox = ctk.CTkTextbox(self.frame_home, width=700, height=250, font=("Segoe UI", 14), wrap="word",fg_color="#DCDADA")
        textbox.insert("0.0", metin)
        textbox.configure(state="disabled")  # Kullanıcının düzenlemesini engelle
        textbox.pack(pady=20)
        self.marquee_label = ctk.CTkLabel(
        self.frame_home,
        text="✅ Lütfen kartınızı okutunuz",
        font=("Segoe UI", 16, "bold"),
        text_color="green"
        )
        self.marquee_label.pack(pady=(10, 20))

        # Kayan yazıyı başlat
        self.marquee_text = "✅ Lütfen kartınızı okutunuz     "
        self.marquee_index = 0
        self.animate_marquee()
 
    def build_help(self):
        ctk.CTkLabel(self.frame_help, text="Yardım ve Kullanım Kılavuzu", font=("Segoe UI", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self.frame_help, text="1. Kamerayı başlatmak için 'Canlı Tespit' sekmesine geçin.", wraplength=700, justify="left").pack(pady=10)
        ctk.CTkLabel(self.frame_help, text="2. Ayarlar sekmesinden tema değiştirebilirsiniz.", wraplength=700, justify="left").pack(pady=10)

    def animate_marquee(self):
        display_text = self.marquee_text[self.marquee_index:] + self.marquee_text[:self.marquee_index]
        self.marquee_label.configure(text=display_text)
        self.marquee_index = (self.marquee_index + 1) % len(self.marquee_text)
        self.root.after(150, self.animate_marquee)
    
    def kart_okundu(self, kullanici_adi):
        self.root.withdraw()
        user_data, uid = kullanici_yukle_by_name(kullanici_adi)

        if user_data:
            sehir_ekle(uid)  
            yolo = AtikTespit(uid=uid)
            self.yolo = yolo
            SecimPenceresi(self.root, yolo)
        else:
            print("⚠ Kullanıcı JSON'da tanımlı değil.")

class SecimPenceresi(ctk.CTkToplevel):
    def __init__(self, master=None,yolo=None):
        super().__init__(master)
        self.yolo=yolo
        user_data, _ = kullanici_yukle(yolo.uid)
        kullanici_adi = user_data.get("isim", "Kullanıcı") 
        self.title("İşlem Seçimi")
        self.geometry("900x600")
        self.configure(fg_color="#f0f0f0")
        self.resizable(False, False)
        

        # Hoşgeldiniz başlığı
        self.hosgeldiniz_label = ctk.CTkLabel(
            self,
            text=f"Hoşgeldin {kullanici_adi}",
            font=("Segoe UI", 28, "bold")
        )
        self.hosgeldiniz_label.pack(pady=(40, 10))
        # Kayan yazı
        self.kayan_yazi = ctk.CTkLabel(self, text="", font=("Segoe UI", 18),text_color="green")
        self.kayan_yazi.pack(pady=(10, 30))
        self.mesaj = "Lütfen yapmak istediğiniz işlemi seçin..."
        self.kayan_index = 0
        self.kayan_yazi_guncelle()

        # Butonlar
          # Ortalanmış butonlar için bir alt çerçeve
        btn_container = ctk.CTkFrame(self, fg_color="transparent")
        btn_container.pack(pady=(10, 10))

        buton_genislik = 240
        buton_yukseklik = 55

        self.btn_geri_donustur = ctk.CTkButton(
            btn_container,
            text="♻️ Geri Dönüştür",
            font=("Segoe UI", 18),
            width=buton_genislik,
            height=buton_yukseklik,
            fg_color="#145c2a",
            command=self.geri_donustur
        )
        self.btn_geri_donustur.pack(pady=8)

        self.btn_gecmis_analiz = ctk.CTkButton(
            btn_container,
            text="📊 Geçmiş Analizlerim",
            font=("Segoe UI", 18),
            width=buton_genislik,
            height=buton_yukseklik,
            fg_color="#145c2a",
            command=self.gecmis_analiz
        )
        self.btn_gecmis_analiz.pack(pady=8)

        self.btn_bakiye = ctk.CTkButton(
            btn_container,
            text="💰 Bakiye Bilgisi",
            font=("Segoe UI", 18),
            width=buton_genislik,
            height=buton_yukseklik,
            fg_color="#145c2a",
            command=self.bakiye_bilgisi
        )
        self.btn_bakiye.pack(pady=8)

        self.btn_cikis = ctk.CTkButton(
            btn_container,
            text="🚪 Çıkış",
            font=("Segoe UI", 18),
            width=buton_genislik,
            height=buton_yukseklik,
            fg_color="#8B0000",
            hover_color="#B22222",
            command=self.cikis_yap
        )
        self.btn_cikis.pack(pady=8)
       
    def kayan_yazi_guncelle(self):
        gösterilecek = self.mesaj[:self.kayan_index] + ("|" if self.kayan_index % 2 == 0 else "")
        self.kayan_yazi.configure(text=gösterilecek)
        self.kayan_index = (self.kayan_index + 1) % (len(self.mesaj) + 1)
        self.after(150, self.kayan_yazi_guncelle)
    
    def bakiye_bilgisi(self):
     BakiyeBilgisiPenceresi(self.master, self.yolo)

    def geri_donustur(self):
        self.destroy()
        CanliTespitSayfasi(self.master, self.yolo)

    def gecmis_analiz(self):
     GecmisAnalizPenceresi(self.master, self.yolo)

    
    def cikis_yap(self):
     self.destroy()
     self.master.destroy()  # Ana pencereyi de kapatır (program tamamen sonlanır)


class CanliTespitSayfasi(ctk.CTkToplevel):
    def __init__(self, master, yolo):
        super().__init__(master)
        self.title("Canlı Tespit")
        self.geometry("1000x700")
        self.yolo = yolo

        self.configure(fg_color="#f4f4f4")

        self.label = ctk.CTkLabel(self, text="Canlı Tespit Ekranı", font=("Segoe UI", 20, "bold"),text_color="green")
        self.label.pack(pady=10)

        self.camera_frame = ctk.CTkFrame(self, fg_color="#e0e0e0", width=800, height=500)
        self.camera_frame.pack(pady=10)
        
        self.camera_label = ctk.CTkLabel(self.camera_frame, text="Kamera bekleniyor...", width=800, height=500)
        self.camera_label.pack()

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame, text="▶ Kamerayı Başlat",
            command=lambda: Thread(target=self.yolo.start).start(),
            fg_color="#28a745", hover_color="#1e7e34"
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            btn_frame, text="⛔ Kamerayı Durdur",
            command=self.yolo.stop,
            fg_color="#dc3545", hover_color="#a71d2a"
        ).pack(side="left", padx=20)

        # Görüntüyü güncelleme bağlaması
        self.yolo.display_callback = self.update_camera_view

                # Butonlar
        ctk.CTkButton(
        self,
        text="🔙 Geri",
        font=("Segoe UI", 14),
        command=self.geri_don,
        fg_color="#8B0000", hover_color="#B22222"
        ).pack(pady=(10, 5))

    def geri_don(self):
        self.destroy()
        SecimPenceresi(self.master,self.yolo)  # Tekrar işlem seçimi menüsüne dön

    def update_camera_view(self, imgtk):
        if imgtk is None:
            self.camera_label.configure(image="", text="Kamera durdu.")
        else:
            self.camera_label.configure(image=imgtk, text="")
            self.camera_label.imgtk = imgtk

class GecmisAnalizPenceresi(ctk.CTkToplevel):
    def __init__(self, master, yolo):
        super().__init__(master)
        self.yolo=yolo
        self.title("Geçmiş Analizler")
        self.geometry("600x500")
        self.configure(fg_color="#f8f8f8")
        self.yolo = yolo

        ctk.CTkLabel(self, text="Atık Türlerine Göre Tespit Grafiği", font=("Segoe UI", 20, "bold"),text_color="green").pack(pady=10)
        ctk.CTkButton(self, text="🔙 Geri", command=self.destroy,fg_color="#8B0000", hover_color="#B22222").pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

        self.after(1000, self.update_graph)  # İlk güncelleme 1 saniyede başlar

    def update_graph(self):
        user_data, _ = kullanici_yukle(self.yolo.uid)
        sayaclar = user_data.get("sayaclar", {"plastik":0, "cam":0, "kağıt":0, "metal":0})

        self.ax.clear()
        labels = ["Plastik", "Cam", "Kagit", "Metal"]
        values = [sayaclar["plastik"], sayaclar["cam"], sayaclar["kagit"], sayaclar["metal"]]
        colors = ["#007bff", "#28a745", "#ffc107", "#6f42c1"]

        self.ax.bar(labels, values, color=colors)
        self.ax.set_ylabel("Tespit Sayısı")
        self.ax.set_ylim(0, max(values + [1]) * 1.2)
        self.ax.set_title("Canlı Tespit Grafiği")
        plt.tight_layout()

        self.canvas.draw()
        self.after(2000, self.update_graph)

class BakiyeBilgisiPenceresi(ctk.CTkToplevel):
    def __init__(self, master, yolo):
        super().__init__(master)
        self.title("Bakiye Bilgisi")
        self.geometry("500x400")
        self.configure(fg_color="#f8f8f8")
        self.yolo = yolo

        ctk.CTkLabel(self, text="💰 Kart Bakiyesi", font=("Segoe UI", 22, "bold"),text_color="green").pack(pady=20)

        # Bilgi kutusu
        self.text_box = ctk.CTkTextbox(self, width=400, height=200, font=("Segoe UI", 14), wrap="word", fg_color="#E6E6E6")
        self.text_box.pack(pady=10)
        self.text_box.configure(state="disabled")

        # Geri butonu
        ctk.CTkButton(self, text="🔙 Geri", command=self.destroy, fg_color="#8B0000", hover_color="#B22222").pack(pady=10)

        # İlk veriyi yükle ve döngü başlat
        self.update_bakiye()

    def update_bakiye(self):
        user_data, _ = kullanici_yukle(self.yolo.uid)
        sayaclar = user_data.get("sayaclar", {"plastik": 0, "cam": 0, "kağıt": 0, "metal": 0})
        bakiye = user_data.get("bakiye", 0)

        # Gösterilecek yeni metni oluştur
        detaylar = (
            f"Toplam Bakiye: {bakiye} Puan\n\n"
            f"🏷 Plastik: {sayaclar.get('plastik', 0)} x 4 = {sayaclar.get('plastik', 0)*4}\n"
            f"🍾 Cam: {sayaclar.get('cam', 0)} x 2 = {sayaclar.get('cam', 0)*2}\n"
            f"📄 Kağıt: {sayaclar.get('kağıt', 0)} x 1 = {sayaclar.get('kağıt', 0)*1}\n"
            f"🛠 Metal: {sayaclar.get('metal', 0)} x 3 = {sayaclar.get('metal', 0)*3}\n"
        )

        self.text_box.configure(state="normal")
        self.text_box.delete("0.0", "end")
        self.text_box.insert("0.0", detaylar)
        self.text_box.configure(state="disabled")

        # Her 2 saniyede bir güncelle
        self.after(2000, self.update_bakiye)

