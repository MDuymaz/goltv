import urllib.parse
import re

# ana_link.txt dosyasından referer ve origin verilerini okuma
try:
    with open("ana_link.txt", "r") as file:
        lines = file.readlines()
        # Dosyada sadece bir satır varsa, bu satır her iki bilgi için kullanılacak
        if len(lines) >= 1:
            referer = lines[0].strip()  # Satırdaki tek veri hem referer hem origin olarak kullanılacak
            origin = referer
        else:
            raise ValueError("ana_link.txt dosyasındaki satır sayısı yetersiz. En az bir satır olmalıdır.")
except FileNotFoundError:
    print("ana_link.txt dosyası bulunamadı.")
    exit(1)

# son_m3u_link_tamam.txt dosyasından URL'leri alma
try:
    with open("son_m3u_link_tamam.txt", "r") as file:
        content = file.read()
# Base URL
base_url = "https://playerpro.live/proxy.php?url="

# final_url'leri depolamak için bir liste
final_urls = []

# URL'leri işleme
for original_url in urls:
    # Eğer URL, https://playerpro.live ile başlıyorsa, direkt ekle
    if original_url.startswith("https://playerpro.live"):
        final_urls.append(f'Url: "{original_url}"')
    else:
        # URL encode işlemi
        encoded_referer = urllib.parse.quote(referer, safe=":/?&=")  # referer için encode
        encoded_origin = urllib.parse.quote(origin, safe=":/?&=")    # origin için encode

        # original_url'yi encode etmeden kullanıyoruz çünkü zaten encode edilmiş
        final_url = f"{base_url}{urllib.parse.quote(original_url, safe=':/?&=')}&referer={encoded_referer}&origin={encoded_origin}"
        
        # final_url'yi listeye ekle
        final_urls.append(f'Url: "{final_url}"')

# final_url'leri final_url.txt dosyasına kaydetme
try:
    with open("final_url.txt", "w") as output_file:
        for url in final_urls:
            output_file.write(url + "\n")
    print("final_url başarıyla final_url.txt dosyasına kaydedildi.")
except Exception as e:
    print(f"final_url.txt dosyasına yazarken bir hata oluştu: {e}")
