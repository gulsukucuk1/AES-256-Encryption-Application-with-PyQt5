import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class ProfesyonelDosyaKasasi(QWidget):

    def __init__(self):
        super().__init__()
        self.secili_dosya_yolu = ""
        self.sifre_gorunur = False 
        self.init_ui()

    def init_ui(self):

        self.setWindowTitle("AES-256 Güvenli Dosya Şifreleme/Çözme")
        self.setGeometry(100, 100, 500, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Şifreleme Anahtarı:"))
        sifre_layout = QHBoxLayout()
        
        self.ent_anahtar = QLineEdit()
        self.ent_anahtar.setEchoMode(QLineEdit.Password) 
        self.ent_anahtar.setPlaceholderText("Şifre giriniz...")
        
        self.btn_goz = QPushButton("Gör")
        self.btn_goz.setFixedWidth(60)
        
        sifre_layout.addWidget(self.ent_anahtar)
        sifre_layout.addWidget(self.btn_goz)
        layout.addLayout(sifre_layout)

        layout.addWidget(QLabel("İşlem Yapılacak Dosya:"))
        self.btn_dosya_sec = QPushButton("Bilgisayardan Dosya Seç")
        self.btn_dosya_sec.setFixedHeight(35)
        layout.addWidget(self.btn_dosya_sec)

        self.lbl_dosya_bilgi = QLabel("Seçilen: Yok")
        self.lbl_dosya_bilgi.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.lbl_dosya_bilgi)

        buton_grubu = QHBoxLayout()
        self.btn_sifrele = QPushButton("Şifrele ve Koru")
        self.btn_coz = QPushButton("Şifreyi Çöz ve Aç")
        self.btn_sifrele.setStyleSheet("background-color: #2c3e50; color: white; height: 40px; font-weight: bold;")
        self.btn_coz.setStyleSheet("background-color: #27ae60; color: white; height: 40px; font-weight: bold;")
        
        buton_grubu.addWidget(self.btn_sifrele)
        buton_grubu.addWidget(self.btn_coz)
        layout.addLayout(buton_grubu)

        self.setLayout(layout)
        self.btn_goz.clicked.connect(self.sifre_goster_gizle)
        self.btn_dosya_sec.clicked.connect(self.dosya_sec)
        self.btn_sifrele.clicked.connect(self.sifrele_islem)
        self.btn_coz.clicked.connect(self.coz_islem)

    def sifre_goster_gizle(self):
        if self.sifre_gorunur:
            self.ent_anahtar.setEchoMode(QLineEdit.Password)
            self.btn_goz.setText("Gör")
            self.sifre_gorunur = False
        else:
            self.ent_anahtar.setEchoMode(QLineEdit.Normal)
            self.btn_goz.setText("Gizle")
            self.sifre_gorunur = True

    def dosya_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Tüm Dosyalar (*.*)")
        if dosya:
            self.secili_dosya_yolu = dosya
            self.lbl_dosya_bilgi.setText(f"Seçilen: {os.path.basename(dosya)}")

    def anahtar_hazirla(self):
        return self.ent_anahtar.text().encode('utf-8').ljust(32)[:32]

    def alanlari_temizle(self):
        self.ent_anahtar.clear()
        self.secili_dosya_yolu = ""
        self.lbl_dosya_bilgi.setText("Seçilen: Yok")

    def sifrele_islem(self):
        if not self.secili_dosya_yolu or not self.ent_anahtar.text():
            QMessageBox.warning(self, "Hata", "Eksik veri girişi!")
            return

        try:
            anahtar = self.anahtar_hazirla()
            with open(self.secili_dosya_yolu, "rb") as f:
                veri = f.read()

            cipher = AES.new(anahtar, AES.MODE_CBC)
            islenmis = cipher.iv + cipher.encrypt(pad(veri, AES.block_size))
            
            cikti = self.secili_dosya_yolu + ".sifreli"
            with open(cikti, "wb") as f:
                f.write(islenmis)

            QMessageBox.information(self, "Bilgi", "Dosya şifrelendi.")
            self.alanlari_temizle()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def coz_islem(self):

        if not self.secili_dosya_yolu.endswith(".sifreli"):
            QMessageBox.warning(self, "Uyarı", "Geçersiz dosya formatı!")
            return

        try:
            anahtar = self.anahtar_hazirla()
            with open(self.secili_dosya_yolu, "rb") as f:
                veri = f.read()

            iv = veri[:16]
            asıl_veri = veri[16:]
            cipher = AES.new(anahtar, AES.MODE_CBC, iv)
            cozulmus = unpad(cipher.decrypt(asıl_veri), AES.block_size)
            eski_ad = self.secili_dosya_yolu.replace(".sifreli", "")
            klasor, dosya_adi = os.path.split(eski_ad)
            cikti = os.path.join(klasor, "Cozuldu_" + dosya_adi)

            with open(cikti, "wb") as f:
                f.write(cozulmus)

            QMessageBox.information(self, "Bilgi", "Dosya çözüldü.")
            self.alanlari_temizle()
        except:
            QMessageBox.critical(self, "Hata", "Hatalı şifre girişi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ProfesyonelDosyaKasasi()
    ex.show()
    sys.exit(app.exec_())