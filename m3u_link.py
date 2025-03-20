import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time
import psutil
import atexit
import warnings

# Tarayıcı seçeneklerini ayarlıyoruz
options = Options()
options.add_argument("--headless")  # Tarayıcıyı başsız çalıştır
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Tarayıcıyı başlatıyoruz
driver = uc.Chrome(options=options)

# Tarayıcıyı kapatma fonksiyonu
def close_driver():
    try:
        time.sleep(2)  # Tarayıcı kapanmadan önce bekleme ekledik
        driver.quit()  # Tarayıcıyı kapatıyoruz
    except Exception as e:
        print(f"Tarayıcıyı kapatma hatası (görmezden gelindi): {e}")

# Program sonlanmadan önce driver'ı kapatmak için exit işlemi ekliyoruz
atexit.register(close_driver)

# Hata mesajlarını bastırıyoruz
warnings.filterwarnings("ignore", category=UserWarning, message=".*undetected_chromedriver.*")

# m3u_link.txt dosyasındaki URL'leri okuma
with open("m3u_link.txt", "r", encoding="utf-8") as file:
    urls = file.readlines()

# URL'leri tek tek kontrol etme ve video URL'lerini alma
all_video_urls = []

for url in urls:
    url = url.strip()  # URL'deki boşlukları temizliyoruz
    if url:  # Boş satırlar varsa, onları geçiyoruz
        try:
            print(f"🔍 {url} sayfası açılıyor...")
            driver.get(url)  # URL'yi açıyoruz

            # Sayfanın yüklenmesi için bir süre bekliyoruz
            time.sleep(5)

            # Ağ isteklerini takip etmek için tarayıcı konsolunu kullanıyoruz
            logs = driver.execute_script("return performance.getEntriesByType('resource');")

            # Video URL'lerini topluyoruz
            video_urls = []
            for log in logs:
                video_url = log['name']
                if video_url.endswith('.m3u8') or video_url.endswith('.mp4'):
                    video_urls.append(video_url)

            # Eğer birden fazla video URL'si varsa, sadece en uzun olanı alıyoruz
            if video_urls:
                longest_video_url = max(video_urls, key=len)  # En uzun URL'yi seçiyoruz
                all_video_urls.append(longest_video_url)
                print(f"🎥 En uzun video URL'si bulundu: {longest_video_url}")
            else:
                print("⚠️ Bu sayfada video URL'si bulunamadı.")
                all_video_urls.append("LİNK BULUNAMADI")

        except Exception as e:
            print(f"❌ {url} sayfasında hata oluştu: {e}")
            all_video_urls.append("LİNK BULUNAMADI")

# Video URL'lerini m3u_link_alındı.txt dosyasına kaydediyoruz
with open("m3u_link_alındı.txt", "w", encoding="utf-8") as file:
    for video_url in all_video_urls:
        file.write(f"{video_url}\n")

print("🎉 Video URL'leri m3u_link_alındı.txt dosyasına kaydedildi.")

# Tarayıcıyı kapatma işlemi
try:
    time.sleep(3)
    process = psutil.Process(driver.service.process.pid)
    process.terminate()  # Selenium processini manuel olarak sonlandırıyoruz
    print("Tarayıcı başarıyla kapatıldı.")
except Exception as e:
    print(f"Selenium processini sonlandırma hatası (görmezden gelindi): {e}")
