# Verilerinizi içeren dosya adlarını belirtiyoruz
input_file = "son_m3u.txt"
output_file = "gol.m3u"  # Çıktı dosyasının adı
link_file = "ana_link.txt"  # Ana linki bu dosyadan alacağız

# ana_link.txt dosyasındaki ana URL'yi alıyoruz
with open(link_file, "r", encoding="utf-8") as file:
    referrer_url = file.read().strip()

# son_m3u.txt dosyasındaki verileri okuyoruz
with open(input_file, "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file if line.strip()]  # Boş satırları temizle

# Veriyi işleyip uygun formata dönüştürüyoruz
formatted_data = []
extm3u_added = False  # #EXTM3U eklenip eklenmediğini takip etmek için

# Satırları üçlü gruplar halinde işle
i = 0
while i < len(lines):
    try:
        if lines[i].startswith("MatchType:") and i+2 < len(lines):
            match_type = lines[i].replace('MatchType: ', '').replace('"', '')
            text = lines[i + 1].replace('Text: ', '').replace('"', '')
            url = lines[i + 2]  # Üçüncü satırı URL olarak al
            
            # Eğer URL beklenen formatta değilse atla
            if not url.startswith("http"):
                print(f"⚠️ Geçersiz URL atlandı: {url}")
                i += 3
                continue
            
            # Eğer ilk kez ekliyorsak #EXTM3U başlığını ekleyelim
            if not extm3u_added:
                formatted_data.append("#EXTM3U\n")
                extm3u_added = True

            # Formatlı M3U satırlarını oluştur
            formatted_entry = f"""
#EXTINF:-1 tvg-name="{text}" tvg-language="Turkish" tvg-country="TR" group-title="{match_type}",{text}
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)
#EXTVLCOPT:http-referrer={referrer_url}
{url}
"""
            formatted_data.append(formatted_entry)
            i += 3  # Sonraki üçlüye geç
        else:
            print(f"⚠️ Eksik veya hatalı veri bulundu, atlanıyor: {lines[i]}")
            i += 1  # Sonraki satıra geç
    except IndexError:
        print(f"⚠️ Veriler eksik, işleme devam ediliyor...")
        break

# Veriyi output dosyasına yaz
with open(output_file, "w", encoding="utf-8") as file:
    file.writelines(formatted_data)

print(f"✅ Veriler başarıyla '{output_file}' dosyasına kaydedildi.")
