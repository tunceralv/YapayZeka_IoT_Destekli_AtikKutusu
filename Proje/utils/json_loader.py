import json
import os
import geocoder

DOSYA_YOLU = "Data/kullanicilar.json"

def kullanici_yukle(uid):
    if not os.path.exists(DOSYA_YOLU):
        with open(DOSYA_YOLU, "w") as f:
            json.dump({}, f)

    with open(DOSYA_YOLU, "r") as f:
        data = json.load(f)

    if uid in data:
        return data[uid], uid
    else:
        print("⚠ Tanımsız kart.")
        return None, None

def sayac_arttir(uid, kategori):
    with open(DOSYA_YOLU, "r") as f:
        data = json.load(f)

    if uid not in data:
        print("⚠ Tanımsız UID, sayaç güncellenemedi.")
        return

    if kategori in data[uid]["sayaclar"]:
        data[uid]["sayaclar"][kategori] += 1
    else:
        print("⚠ Geçersiz kategori:", kategori)
        return

    with open(DOSYA_YOLU, "w") as f:
        json.dump(data, f, indent=4)

def yeni_kullanici_ekle(uid, isim):
    with open(DOSYA_YOLU, "r") as f:
        data = json.load(f)

    if uid not in data:
        data[uid] = {
            "isim": isim,
            "sayaclar": {
                "plastik": 0,
                "cam": 0,
                "kağıt": 0,
                "metal": 0
            },
            "bakiye":0
        }
        with open(DOSYA_YOLU, "w") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Yeni kullanıcı eklendi: {isim}")
    else:
        print("ℹ Zaten kayıtlı kullanıcı.")

def kullanici_yukle_by_name(name):
    if not os.path.exists(DOSYA_YOLU):
        return None, None

    with open(DOSYA_YOLU, encoding='utf-8') as f:
     data = json.load(f)

    for uid, bilgiler in data.items():
        if bilgiler.get("isim", "").upper() == name.upper():
            return bilgiler, uid

    return None, None

def bakiye_arttir(uid, kategori):
    puanlar = {
        "plastik": 4,
        "metal": 3,
        "cam": 2,
        "kağıt": 1
    }

    with open(DOSYA_YOLU, "r") as f:
        data = json.load(f)

    if uid not in data:
        print("⚠ Tanımsız UID, bakiye güncellenemedi.")
        return

    if kategori in puanlar:
        data[uid]["bakiye"] += puanlar[kategori]
    else:
        print("⚠ Geçersiz kategori:", kategori)
        return

    with open(DOSYA_YOLU, "w") as f:
        json.dump(data, f, indent=4)

def sehir_ekle(uid):
    try:
        g = geocoder.ip('me')
        sehir = g.city if g.ok else "Bilinmiyor"

        with open(DOSYA_YOLU, "r+", encoding="utf-8") as f:
            data = json.load(f)
            if uid in data:
                data[uid]["sehir"] = sehir
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()
                print(f"✅ Şehir bilgisi ({sehir}) eklendi.")
            else:
                print("⚠ UID bulunamadı.")
    except Exception as e:
        print(f"Hata (şehir ekleme): {str(e)}")