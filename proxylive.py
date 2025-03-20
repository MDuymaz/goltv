from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

# Chrome başsız mod ayarları
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# WebDriver başlatma
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://playerpro.live/')

# Dosyalardan linkleri okuma
with open("m3u_link_alındı.txt", "r") as file:
    links = [line.strip() for line in file.readlines()]

with open("ana_link.txt", "r") as file:
    ana_link = file.read().strip()

# Çıktı dosyasını aç
with open("son_m3u_link_tamam.txt", "w") as file:
    for link in links:
        # Eğer satır boşsa atla
        if not link:
            continue  

        # Eğer "LİNK BULUNAMADI" yazısı varsa ya da link "https://playerpro.live" ile başlıyorsa, direkt dosyaya yaz
        if "LİNK BULUNAMADI" in link or link.startswith("https://playerpro.live"):
            file.write(f"{link}\n")
            print(f"Kaydedildi: {link}")
            continue  # Bu durumda işlem yapmadan sonraki linke geç

        # Eğer gerçek bir URL değilse, sadece yazıyı dosyaya kaydet
        if not link.startswith("http"):
            file.write(f"{link}\n")
            print(f"Kaydedildi: {link}")
            continue  # Bu durumda işlem yapmadan sonraki linke geç

        # Diğer linkler için formu doldurma
        inputs = driver.find_elements(By.CSS_SELECTOR, 'form input')
        if len(inputs) >= 3:
            inputs[0].clear()
            inputs[0].send_keys(link)
            inputs[1].clear()
            inputs[1].send_keys(ana_link)
            inputs[2].clear()
            inputs[2].send_keys(ana_link)

        # Butona tıklama
        button = driver.find_element(By.CSS_SELECTOR, 'form button')
        ActionChains(driver).move_to_element(button).click().perform()

        # Bekleme süresi
        time.sleep(5)  

        # Ağ trafiği loglarını al ve sadece proxy.php URL'lerini kontrol et
        logs = driver.get_log('performance')
        found_proxy_url = False  # Fazladan yazmamak için kontrol değişkeni

        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log.get('method') == 'Network.responseReceived':
                url = log.get('params', {}).get('response', {}).get('url', '')
                # Eğer URL 'proxy.php' içeriyorsa, sadece bu URL'yi kaydet
                if "proxy.php" in url:
                    if not found_proxy_url:  # Sadece ilk proxy linkini al
                        file.write(f"{url}\n")
                        print(f"Proxy URL kaydedildi: {url}")
                        found_proxy_url = True  # Daha fazla yazmamak için işaret koy
                    break  # Bir tane bulunca döngüyü kır

        # Sayfayı yeniden yükle
        driver.get('https://playerpro.live/')
        time.sleep(3)

# Tarayıcıyı kapat
driver.quit()
