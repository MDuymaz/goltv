# Verilerinizi içeren dosya adlarını belirtiyoruz
input_file = "son_m3u.txt"
output_file = "gol.m3u"  # Çıktı dosyasının adı 'gol.m3u' olarak değiştirildi
link_file = "ana_link.txt"  # Ana linki bu dosyadan alacağız

# ana_link.txt dosyasındaki ana URL'yi alıyoruz
with open(link_file, "r", encoding="utf-8") as file:
    referrer_url = file.read().strip()  # Dosyadan URL'yi alıp boşlukları temizliyoruz

# son_m3u.txt dosyasındaki verileri okuyoruz
with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Veriyi işleyip uygun formata dönüştürüyoruz
formatted_data = []

# Dosya başında #EXTM3U etiketinin olup olmadığını kontrol edeceğiz
extm3u_added = False

# Satırları işleyeceğiz
i = 0
while i < len(lines):
    try:
        # Boş satırları atlıyoruz
        if not lines[i].strip():
            i += 1
            continue

        # MatchType, Text ve Url satırlarını alıyoruz
        if lines[i].startswith('MatchType:') and lines[i + 1].startswith('Text:') and lines[i + 2].startswith('Url:'):
            match_type = lines[i].strip().replace('MatchType: ', '').replace('"', '')  # MatchType
            text = lines[i + 1].strip().replace('Text: ', '').replace('"', '')  # Text
            url = lines[i + 2].strip()  # URL

            # Eğer #EXTM3U daha önce eklenmediyse, ilk başta ekliyoruz
            if not extm3u_added:
                formatted_data.append("#EXTM3U\n")
                extm3u_added = True

            # Verinin düzgün olduğundan emin olduktan sonra formatlıyoruz
            formatted_entry = f"""
#EXTINF:-1 tvg-name="{text}" tvg-language="Turkish" tvg-country="TR" group-title="{match_type}",{text}
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)
#EXTVLCOPT:http-referrer={referrer_url}
{url}
"""
            formatted_data.append(formatted_entry)
            i += 3  # Bir sonraki MatchType, Text ve Url için 3 satır ilerliyoruz
        else:
            # Eğer veriler uyumsuzsa, bir sonraki satıra geçiyoruz
            print(f"⚠️ Eksik veya hatalı veri tespit edildi. Atlanıyor: {lines[i:i+3]}")
            i += 1
    except IndexError:
        # Eğer bir hata oluşursa, sadece eksik veriler olduğunda bunu atlıyoruz
        print(f"⚠️ Veriler eksik veya hatalı: {lines[i:i+3]}")
        break

# Veriyi output dosyasına yazıyoruz
with open(output_file, "w", encoding="utf-8") as file:
    file.writelines(formatted_data)

print(f"Veriler başarıyla '{output_file}' dosyasına kaydedildi.")
