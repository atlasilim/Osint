import time
import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import geocoder
from bs4 import BeautifulSoup
import whois
import os
import webbrowser
import threading

# Sosyal medya platformları
platforms = {
    "Instagram": "https://www.instagram.com/",
    "Twitter": "https://twitter.com/",
    "Facebook": "https://www.facebook.com/",
    "Discord": "https://discord.com/"
}

# Telefon numarasının ait olduğu ülkeyi bulma
def get_phone_country(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        country = geocoder.region_code_for_number(parsed_number)
        return country
    except phonenumbers.phonenumberutil.NumberParseException:
        return None

# Telefon numarası geçerli mi kontrol et
def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

# E-posta adresini doğrula
def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        return False

# Web sitesi çalışıyor mu kontrol et
def validate_website(website_url):
    try:
        response = requests.get(website_url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Alan adı WHOIS sorgulama
def get_domain_whois(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        return f"Alan Adı Bilgileri:\n{domain_info}"
    except Exception as e:
        return f"[!] Hata: {str(e)}"

# Sosyal medya platformlarında kullanıcı araması
def search_user_on_platform(platform, username):
    options = Options()
    options.headless = False  # Tarayıcıyı görünür yapar
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    search_url = platforms.get(platform, "") + username

    driver.get(search_url)
    time.sleep(3)

    search_result = ""
    try:
        if platform == "Instagram" and "Page Not Found" not in driver.title:
            search_result = f"[+] Instagram Kullanıcı Adı Bulundu: {username}"
        elif platform == "Twitter" and "User not found" not in driver.page_source:
            search_result = f"[+] Twitter Kullanıcı Adı Bulundu: {username}"
        elif platform == "Facebook" and "Page Not Found" not in driver.title:
            search_result = f"[+] Facebook Kullanıcı Adı Bulundu: {username}"
        elif platform == "Discord" and "404 Not Found" not in driver.title:
            search_result = f"[+] Discord Kullanıcı Adı Bulundu: {username}"
        else:
            search_result = f"[-] {platform} Kullanıcı Adı Bulunamadı: {username}"
    except Exception as e:
        search_result = f"[!] Hata oluştu: {str(e)}"

    driver.quit()
    return search_result

# E-posta adresi araması (isim ve soyadına göre)
def search_email_by_name(first_name, last_name):
    example_emails = [
        f"{first_name.lower()}{last_name.lower()}@gmail.com",
        f"{first_name.lower()}.{last_name.lower()}@outlook.com",
        f"{first_name.lower()}_{last_name.lower()}@yahoo.com"
    ]
    return example_emails

# Kişiye özel sorgulama (PeekYou araması)
def search_person_by_name(first_name, last_name):
    print(f"[+] {first_name} {last_name} kişisini PeekYou'da arıyorsunuz...")
    search_url = f"https://www.peekyou.com/{first_name}_{last_name}"
    webbrowser.open(search_url)

# Şifre güvenliği kontrolü (Sadece siteye yönlendirir)
def redirect_to_password_leak_check():
    url = "https://cybernews.com/password-leak-check/"
    webbrowser.open(url)

# Paket yükleme (API Sorgusu için)
def pip_package_search(package_name):
    try:
        response = requests.get(f"https://pypi.org/project/{package_name}/")
        if response.status_code == 200:
            return f"[+] Paket Bulundu: {package_name}\nURL: {response.url}"
        else:
            return f"[-] Paket Bulunamadı: {package_name}"
    except Exception as e:
        return f"[!] Hata: {str(e)}"

# Sonuçları TXT dosyasına kaydetme
def save_results_to_txt(results):
    one_drive_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Masaüstü", "OSINT_Arama_Sonuclari.txt")

    try:
        with open(one_drive_path, "w", encoding="utf-8") as file:
            file.write("OSINT Arama Sonuçları\n")
            file.write("---------------------------\n")
            for result in results:
                file.write(f"{result}\n")
        print(f"[+] Sonuçlar kaydedildi: {one_drive_path}")
    except Exception as e:
        print(f"[-] TXT kaydedilirken hata oluştu: {e}")

# Menü işlevi
def display_menu():
    print("----------------------------------")
    print("Hoşgeldiniz! OSINT Geliştirme Aracına.")
    print("1. Sosyal Medya Kullanıcı Araması")
    print("2. Telefon Numarası Doğrulama")
    print("3. E-posta Adresi Doğrulama")
    print("4. Web Sitesi Durum Kontrolü")
    print("5. WHOIS Alan Adı Sorgulama")
    print("6. İsim ve Soyisim ile E-posta Araması")
    print("7. Kişiye Özel Sorgulama (PeekYou Araması)")
    print("8. Şifre Güvenliği Kontrolü")
    print("9. PIP Paketi Sorgulama")
    print("10. Çıkış")

# Kullanıcıdan giriş alma
def main():
    results = []
    while True:
        display_menu()
        choice = input("Bir işlem seçin (1-10): ")

        if choice == "1":
            platform_choice = input("Platform seçin (Instagram/Twitter/Facebook/Discord): ").capitalize()
            username = input(f"{platform_choice} kullanıcı adı nedir?: ")
            result = search_user_on_platform(platform_choice, username)
            if result:
                print(result)
                results.append(result)

        elif choice == "2":
            phone_number = input("Telefon numarası: ")
            if validate_phone_number(phone_number):
                country = get_phone_country(phone_number)
                result = f"[+] Telefon numarası geçerli: {phone_number}, {country} ülkesi."
            else:
                result = f"[-] Geçersiz telefon numarası: {phone_number}"
            print(result)
            results.append(result)

        elif choice == "3":
            email = input("E-posta adresi: ")
            if validate_email_address(email):
                result = f"[+] Geçerli e-posta adresi: {email}"
            else:
                result = f"[-] Geçersiz e-posta adresi: {email}"
            print(result)
            results.append(result)

        elif choice == "4":
            website_url = input("Web sitesi URL: ")
            if validate_website(website_url):
                result = f"[+] Web sitesi çalışıyor: {website_url}"
            else:
                result = f"[-] Web sitesi çalışmıyor: {website_url}"
            print(result)
            results.append(result)

        elif choice == "5":
            domain_name = input("Alan adı girin: ")
            result = get_domain_whois(domain_name)
            print(result)
            results.append(result)

        elif choice == "6":
            first_name = input("İsim: ")
            last_name = input("Soyisim: ")
            emails = search_email_by_name(first_name, last_name)
            for email in emails:
                print(f"[+] Önerilen E-posta: {email}")
                results.append(email)

        elif choice == "7":
            first_name = input("İsim: ")
            last_name = input("Soyisim: ")
            search_person_by_name(first_name, last_name)
            results.append(f"[+] {first_name} {last_name} PeekYou'da arandı.")

        elif choice == "8":
            redirect_to_password_leak_check()
            results.append("[+] Şifre kontrolü için siteye yönlendirildi.")

        elif choice == "9":
            package_name = input("PIP paketi adı: ")
            result = pip_package_search(package_name)
            print(result)
            results.append(result)

        elif choice == "10":
            save_results_to_txt(results)
            print("[+] Çıkılıyor...")
            break

        else:
            print("[!] Geçersiz seçenek!")

if __name__ == "__main__":
    main()
