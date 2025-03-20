from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

# Başsız modda Chrome ayarlarını yapma
chrome_options = Options()
chrome_options.add_argument("--headless")  # Başsız modda çalıştır
chrome_options.add_argument("--no-sandbox")  # GitHub Actions ortamı için güvenlik ayarı
chrome_options.add_argument("--disable-dev-shm-usage")  # GitHub Actions ortamı için performans ayarı

# Ağ trafiği loglama için capabilities ayarlarını yapmak
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# ChromeDriver'ı başlatma
driver = webdriver.Chrome(options=chrome_options)

# Web sayfasına gitme
driver.get('https://playerpro.live/')

# Verileri m3u_link_alındı.txt dosyasından okuma (birden fazla link)
with open("m3u_link_alındı.txt", "r") as file:
    links = file.readlines()

# ana_link.txt'yi okuma
with open("ana_link.txt", "r") as file:
    ana_link = file.read().strip()

# son_m3u_link_tamam.txt dosyasını sıfırlıyoruz (baştan yazılmasını sağlıyoruz)
with open("son_m3u_link_tamam.txt", "w") as file:
    # Her link için işlemi yapalım
    for link in links:
        link = link.strip()  # Linki temizle (başta/sonda boşlukları kaldır)

        # Eğer link içinde 'playlist' kelimesi varsa, bu linki direkt yazıyoruz
        if "playlist" in link:
            file.write(f'Url: "{link}"\n')  # Linki doğrudan dosyaya ekliyoruz
            print(f"Playlist URL kaydedildi: {link}")
        else:
            # HTML elemanlarına erişip formu dolduruyoruz
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/form/div[1]/input').send_keys(link)
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/form/div[2]/input').send_keys(ana_link)
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/form/div[3]/input').send_keys(ana_link)

            # Buton üzerinde tıklama işlemi yapmak için ActionChains kullanıyoruz
            button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/form/button')
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()

            # Bir süre bekleyelim çünkü ağ istekleri biraz zaman alabilir
            time.sleep(5)

            # Ağ trafiği loglarını al
            logs = driver.get_log('performance')

            # URL'yi almak için logları kontrol et
            referer_url = None
            for entry in logs:
                log = json.loads(entry['message'])['message']

                # Sadece 'Network.responseReceived' mesajlarına bakıyoruz
                if 'method' in log and log['method'] == 'Network.responseReceived':
                    # 'response' anahtarının varlığını kontrol ediyoruz
                    if 'response' in log['params']:
                        url = log['params']['response'].get('url', '')
                        # Buradaki URL'yi istenilen linki kontrol ederek alabilirsiniz
                        if "proxy.php" in url:
                            print(f"Found URL: {url}")
                            
                            # referer parametresini URL'den dinamik olarak alıyoruz
                            referer_url = log['params']['response'].get('url', '')
                            if "referer=" in referer_url:
                                referer = referer_url.split('referer=')[1].split('&')[0]

                                # URL'yi güncelliyoruz, sadece bir kez referer ve origin parametrelerini ekliyoruz
                                url = url.split('&referer=')[0]  # Eğer referer zaten varsa, onu çıkarıyoruz
                                url += f"&referer={referer}&origin={referer}"  # Aynı değeri origin parametresine de ekliyoruz

                                # Yeni URL'yi dosyaya kaydediyoruz
                                file.write(f'Url: "{url}"\n')  # Yeni URL'yi dosyaya ekliyoruz
                                
                                print(f"URL kaydedildi: {url}")
                            break

            # Sayfayı yeniden yükleyerek işlemi sıfırlıyoruz
            driver.get('https://playerpro.live/')  # Sayfayı yeniliyoruz
            time.sleep(3)  # Sayfanın yeniden yüklenmesi için biraz bekliyoruz

# Tarayıcıyı kapatma
driver.quit()
