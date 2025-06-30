import json
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QMessageBox, QGroupBox, QPushButton,
    QHBoxLayout, QFileDialog, QGridLayout, QListWidgetItem, QStackedWidget, QApplication,QScrollArea,
)
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
import sys
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView

MAKINE_DOSYASI = "Data/makineler.json"
DOSYA_YOLU = "Data/kullanicilar.json"
ADMIN_DOSYASI = "Data/admin.json"

class ModelSonuclariPage(QWidget):
     def __init__(self):
        super().__init__()

        ana_layout = QVBoxLayout(self)

        # Scroll alanı oluştur
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # 👇 Scrollbar stilini buraya ekliyoruz
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 12px;
                margin: 10px 0 10px 0;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #8FBC8F, stop:1 #3CB371);
                min-height: 25px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.add_image_group(scroll_layout, "🎯 Precision-Confidence Eğrisi", 
                             "Her sınıf için doğruluk oranının güven skoru ile değişimi gösterilmiştir.", 
                             "images/P_curve.png")

        self.add_image_group(scroll_layout, "📈 Precision-Recall Eğrisi", 
                             "Modelin doğruluk ve geri çağırma başarımı sınıflara göre karşılaştırılmıştır.", 
                             "images/PR_curve.png")

        self.add_image_group(scroll_layout, "🔁 Recall-Confidence Eğrisi", 
                             "Modelin güven skoruna karşılık hatırlama başarımı görselleştirilmiştir.", 
                             "images/R_curve.png")

        self.add_image_group(scroll_layout, "🧮 Confusion Matrix", 
                             "Gerçek ve tahmin edilen değerlerin karşılaştırıldığı matris sunulmuştur.", 
                             "images/confusion_matrix.png")

        self.add_image_group(scroll_layout, "📊 F1-Confidence Eğrisi", 
                             "F1 skorlarının güven skoru ile değişimi sınıflara göre gösterilmiştir.", 
                             "images/F1_curve.png")

        scroll_area.setWidget(scroll_content)
        ana_layout.addWidget(scroll_area)

     def add_image_group(self, layout, title, description, image_path):
        group_box = QGroupBox(title)
        group_layout = QVBoxLayout()

        pixmap = QPixmap(image_path)
        image_label = QLabel()

        if pixmap.isNull():
            image_label.setText("❌ Görsel yüklenemedi: " + image_path)
            image_label.setAlignment(Qt.AlignCenter)
        else:
            image_label.setPixmap(pixmap.scaledToWidth(900, Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignCenter)

        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: black;
            padding-top: 5px;
        """)

        group_layout.addWidget(image_label)
        group_layout.addWidget(desc_label)
        group_box.setLayout(group_layout)

        group_box.setStyleSheet("""
            QGroupBox {
                border: 1px solid gray;
                border-radius: 10px;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 6px;
                background-color: #ddd;
                border-radius: 6px;
                font-weight: bold;
            }
        """)

        layout.addWidget(group_box)
class DashboardPage(QWidget):
    def __init__(self, filtered_users, admin_adi, admin_sehir, parent=None):
        super().__init__(parent)
        self.filtered_users = filtered_users
        self.admin_adi = admin_adi
        self.admin_sehir = admin_sehir
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel(f"👤 Hoşgeldin {self.admin_adi}  |  📍 Şehir: {self.admin_sehir}")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.grid = QGridLayout()
        layout.addLayout(self.grid)

        self.add_kullanici_listesi()
        self.add_sayisal_grafik()
        self.add_pasta_grafik()
        self.add_tasarruf_bilgisi()

        self.setLayout(layout)

    def styled_button(self, text, color, icon_path=None, callback=None):
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 12px;
                padding: 8px;
                font-weight: bold;
                
            }}
            QPushButton:hover {{
                background-color: {'#3CB371' if color == '#2E8B57' else '#B22222'};
            }}
        """)
        if icon_path:
            btn.setIcon(QIcon(icon_path))
        if callback:
            btn.clicked.connect(callback)
        return btn

    def styled_groupbox(self, title):
        box = QGroupBox(title)
        box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 10px;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 4px;
            }
        """)
        return box

    def add_kullanici_listesi(self):
        user_box = QGroupBox("📋 Lokasyondaki Kullanıcılar")
        vbox = QVBoxLayout()
        user_list = QListWidget()

        for uid, bilgiler in self.filtered_users.items():
            isim = bilgiler.get("isim", "Bilinmiyor")
            puan = bilgiler.get("bakiye", 0)
            user_list.addItem(f"{isim}  - {puan} Puan")

        vbox.addWidget(user_list)

        btns = QHBoxLayout()
        btns.addWidget(self.styled_button("Excel", "#2E8B57", "icons/excel.png"))
        btns.addWidget(self.styled_button("PDF", "#8B0000", "icons/pdf.png"))
        vbox.addLayout(btns)

        user_box.setLayout(vbox)
        self.grid.addWidget(user_box, 0, 0)

    def add_sayisal_grafik(self):
        self.chart_box = QGroupBox("📊 Sayısal Atık Grafiği")
        vbox = QVBoxLayout()
        self.fig1, self.ax1 = plt.subplots()
        self.canvas1 = FigureCanvas(self.fig1)
        vbox.addWidget(self.canvas1)

        btns = QHBoxLayout()
        btns.addWidget(self.styled_button("Excel", "#2E8B57", "icons/excel.png", self.export_chart_excel))
        btns.addWidget(self.styled_button("PDF", "#8B0000", "icons/pdf.png", self.export_chart_pdf_placeholder))
        vbox.addLayout(btns)

        self.chart_box.setLayout(vbox)
        self.grid.addWidget(self.chart_box, 0, 1)
        self.update_bar_chart()

    def add_pasta_grafik(self):
        self.pie_box = QGroupBox("🥧 Atık Yüzdesi")
        vbox = QVBoxLayout()
        self.fig2, self.ax2 = plt.subplots()
        self.canvas2 = FigureCanvas(self.fig2)
        vbox.addWidget(self.canvas2)

        btns = QHBoxLayout()
        btns.addWidget(self.styled_button("Excel", "#2E8B57", "icons/excel.png", self.export_pie_excel))
        btns.addWidget(self.styled_button("PDF", "#8B0000", "icons/pdf.png", self.export_pie_pdf_placeholder))
        vbox.addLayout(btns)

        self.pie_box.setLayout(vbox)
        self.grid.addWidget(self.pie_box, 1, 0)
        self.update_pie_chart()

    def add_tasarruf_bilgisi(self):
        self.info_box = QGroupBox("💡 Tasarruf Bilgisi")
        vbox = QVBoxLayout()
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        vbox.addWidget(self.info_label)

        btns = QHBoxLayout()
        btns.addWidget(self.styled_button("Excel", "#2E8B57", "icons/excel.png", self.export_pie_excel))
        btns.addWidget(self.styled_button("PDF", "#8B0000", "icons/pdf.png", self.export_tasarruf_pdf_placeholder))
        vbox.addLayout(btns)

        self.info_box.setLayout(vbox)
        self.grid.addWidget(self.info_box, 1, 1)
        self.update_savings_info()

    def update_bar_chart(self):
        toplam = {"Plastik": 0, "Cam": 0, "Kagit": 0, "Metal": 0}
        for bilgiler in self.filtered_users.values():
            for atik, sayi in bilgiler.get("sayaclar", {}).items():
                toplam[atik.capitalize()] += sayi
        self.ax1.clear()
        bars = self.ax1.bar(toplam.keys(), toplam.values(), color=['red', 'blue', 'gray', 'green'])
        self.ax1.set_title("SÜTUN GRAFİĞİ")
        self.ax1.set_ylabel("Miktar")
        self.ax1.set_xlabel("Atık Türü")
        for bar in bars:
            height = bar.get_height()
            self.ax1.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom')
        self.canvas1.draw()

    def update_pie_chart(self):
        toplam = {"Plastik": 0, "Cam": 0, "Kagit": 0, "Metal": 0}
        for bilgiler in self.filtered_users.values():
            for atik, sayi in bilgiler.get("sayaclar", {}).items():
                toplam[atik.capitalize()] += sayi
        self.ax2.clear()
        values = list(toplam.values())
        if sum(values) == 0:
            self.ax2.text(0.5, 0.5, "Veri bulunamadı", ha='center', va='center')
        else:
            self.ax2.pie(values, labels=toplam.keys(), autopct='%1.1f%%', startangle=90)
        self.canvas2.draw()

    def update_savings_info(self):
        katsayi = {"Plastik": 4, "Metal": 3, "Cam": 2, "Kagit": 1}
        toplam = {k: 0 for k in katsayi}
        puan = 0
        for bilgiler in self.filtered_users.values():
            for atik, sayi in bilgiler.get("sayaclar", {}).items():
                toplam[atik.capitalize()] += sayi

        text = ""
        for k in toplam:
            adet = toplam[k]
            text += f"{k}: {adet} x {katsayi[k]} = {adet * katsayi[k]}\n"
            puan += adet * katsayi[k]

        text += f"\nToplam Puan: {puan}\n"
        text += f"Yaklaşık {puan / 24:.1f} ağaç veya {puan * 8} Wh enerji tasarrufu."

        self.info_label.setText(text)

    def export_users_excel(self):
        df = pd.DataFrame([
            {"UID": uid, "İsim": data["isim"], "Puan": data["bakiye"]}
            for uid, data in self.filtered_users.items()
        ])
        yol, _ = QFileDialog.getSaveFileName(self, "Excel Kaydet", "kullanicilar.xlsx", "Excel Files (*.xlsx)")
        if yol:
            df.to_excel(yol, index=False)

    def export_users_pdf_placeholder(self):
        QMessageBox.information(self, "Bilgi", "PDF export yakında entegre edilecek.")

    def export_chart_excel(self):
        data = {"Plastik": 0, "Cam": 0, "Kagit": 0, "Metal": 0}
        for bilgiler in self.filtered_users.values():
            for k, v in bilgiler.get("sayaclar", {}).items():
                data[k.capitalize()] += v

        df = pd.DataFrame(list(data.items()), columns=["Atık Türü", "Adet"])
        yol, _ = QFileDialog.getSaveFileName(self, "Excel Kaydet", "sayisal_grafik.xlsx", "Excel Files (*.xlsx)")
        if yol:
            df.to_excel(yol, index=False)

    def export_chart_pdf_placeholder(self):
        QMessageBox.information(self, "Bilgi", "PDF export yakında entegre edilecek.")

    def export_pie_excel(self):
        self.export_chart_excel()

    def export_pie_pdf_placeholder(self):
        QMessageBox.information(self, "Bilgi", "PDF export yakında entegre edilecek.")

    def export_tasarruf_pdf_placeholder(self):
        QMessageBox.information(self, "Bilgi", "PDF export yakında entegre edilecek.")

class AdminDashboard(QMainWindow):
    def __init__(self, admin_info=None):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(100, 100, 1200, 800)

        # Admin bilgilerini al
        if admin_info is None:
            with open(ADMIN_DOSYASI, "r", encoding="utf-8") as f:
                admin_info = json.load(f)
        self.admin_info = admin_info

        # Kullanıcıları filtrele
        self.filtered_users = self.listele_kullanicilar()

        # ✅ Buton tabanlı sidebar oluştur
        self.sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        self.btn_dashboard = self.styled_menu_button("Admin Dashboard", "#2E8B57", self.show_dashboard)
        self.btn_model = self.styled_menu_button("Model Sonuçları", "#2E8B57", self.show_model_results)
        self.btn_makineler = self.styled_menu_button("Makineler", "#2E8B57", self.show_makineler)
        self.btn_exit = self.styled_menu_button("Çıkış", "#8B0000", self.close)

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_model)
        sidebar_layout.addWidget(self.btn_makineler)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_exit)

        self.sidebar.setLayout(sidebar_layout)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: #f0f0f0;")

        # 📄 Sayfaları gösteren stacked widget
        self.stacked_widget = QStackedWidget()
        self.dashboard_page = DashboardPage(
            self.filtered_users,
            admin_info["admin_Ad"],
            admin_info["admin_Sehir"]
        )
        self.model_page = ModelSonuclariPage()
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.model_page)
        self.makineler_page = MakinelerPage()  # 👈 eksik olan satır
        self.stacked_widget.addWidget(self.makineler_page)

        # 🔄 Ana layout
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stacked_widget)
        self.setCentralWidget(central_widget)

    def styled_menu_button(self, text, color, callback):
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {'#3CB371' if color != '#8B0000' else '#a00000'};
            }}
        """)
        btn.clicked.connect(callback)
        return btn

    def show_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_page)

    def show_model_results(self):
        self.stacked_widget.setCurrentWidget(self.model_page)
    
    def show_makineler(self):
        self.stacked_widget.setCurrentWidget(self.makineler_page)

    def listele_kullanicilar(self):
        result = {}
        try:
            with open(DOSYA_YOLU, "r", encoding="utf-8") as f:
                data = json.load(f)
            for uid, bilgiler in data.items():
                if bilgiler.get("sehir", "").lower() == self.admin_info["admin_Sehir"].lower():
                    result[uid] = bilgiler
        except FileNotFoundError:
            QMessageBox.critical(self, "Hata", "kullanicilar.json bulunamadı.")
        return result

class MakinelerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.map_view = QWebEngineView()
        layout.addWidget(self.map_view)
        self.setLayout(layout)
        self.yukle_harita()

    def yukle_harita(self):
        try:
            with open(MAKINE_DOSYASI, "r", encoding="utf-8") as f:
                makineler = json.load(f)

            # Harita merkezini ilk makinenin konumuna göre ayarla
            ilk_konum = next(iter(makineler.values()))["konum"]
            harita = folium.Map(location=ilk_konum, zoom_start=16, tiles="CartoDB positron")

            for id, veri in makineler.items():
                konum = veri["konum"]
                adres = veri["adres"]
                durum = veri["durum"]
                renk = "green" if durum.lower() == "aktif" else "red"

                folium.Marker(
                    location=konum,
                    popup=f"<b>{id}</b><br>{adres}<br><i>Durum: {durum}</i>",
                    icon=folium.Icon(color=renk)
                ).add_to(harita)

            harita.save("harita.html")
            self.map_view.load(QUrl.fromLocalFile(os.path.abspath("harita.html")))

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Harita yüklenemedi:\n{str(e)}")