import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGroupBox
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
from admin_arayuzu import AdminDashboard  # Giriş sonrası panel


class AdminLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Giriş")
        self.setFixedSize(600, 400)
        


        # 🔹 Arka plan (net kalır)
        self.setAutoFillBackground(True)
        bg = QPixmap("Arka_plan/arka_plan1.jpg").scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(bg))
        self.setPalette(palette)

        # 🔹 Grup kutusu (panel)
        self.group = QGroupBox(self)
        self.group.setGeometry(150, 80, 300, 240)
        self.group.setStyleSheet("""
            QGroupBox {
                background-color: rgba(255, 255, 255, 90);
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 20px;
            }
        """)

        layout = QVBoxLayout()

        # 🔹 Başlık
        title = QLabel("🔐 Yetkili Girişi")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        # 🔹 Giriş bileşenleri
        self.username = QLineEdit()
        self.username.setPlaceholderText("Kullanıcı Adı")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Şifre")
        self.password.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Giriş Yap")
        self.login_btn.clicked.connect(self.check_login)

        # 🔹 Stil uygulama (Bileşenler oluşturulduktan sonra!)
        self.username.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 80);
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
            }
        """)
        self.password.setStyleSheet(self.username.styleSheet())

        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E8B57;
                color: white;
                border-radius: 12px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3CB371;
            }
        """)

        # 🔹 Bileşenleri ekle
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)

        self.group.setLayout(layout)

    def check_login(self):
        try:
            with open("C:\\Users\\Tuncer\\Desktop\\Desktop\\Proje\\Data\\admin.json", "r", encoding="utf-8") as file:
                admin_data = json.load(file)
        except FileNotFoundError:
            QMessageBox.critical(self, "Hata", "admin.json dosyası bulunamadı.")
            return

        username = self.username.text()
        password = self.password.text()

        if admin_data.get("admin_Ad") == username and admin_data.get("admin_Sifre") == password:
            QMessageBox.information(self, "Başarılı", f"Giriş başarılı! Hoşgeldiniz\n Lokasyon: {admin_data.get('admin_Sehir')}")
            self.close()
            self.open_dashboard(admin_data)
        else:
            QMessageBox.warning(self, "Hatalı Giriş", "Kullanıcı adı veya şifre yanlış.")

    def open_dashboard(self, admin_data):
        self.dashboard = AdminDashboard(admin_data)
        self.dashboard.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminLogin()
    window.show()
    sys.exit(app.exec_())
