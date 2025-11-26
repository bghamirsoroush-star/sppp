from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import threading
import time
import random
import sys
import concurrent.futures

# میم‌های فارسی و انگلیسی
NAMES = [
    "۲۶", "۲۶۰", "۶۶۶", "۴۲۰", "۱۴", "۴۰", "۱۹", "۲۵", "۶۱", "۶۷", "۶۹",
    "سیکتیر", "داشاق", "علی", "پروین", "سگ", "خره", "گاو", "گاد", "نولایف",
    "کیر", "کص", "کونی", "حرومزاده", "بی‌ناموس", "بی‌غیرت", "پدرسوخته",
    "مادرجنده", "لاشی", "جنده", "فحش", "ننت", "بابات", "خواهرت", "برادرت",
    "sybau", "fuck", "bitch", "ass", "dick", "pussy", "motherfucker",
    "shit", "bastard", "whore", "slut", "nigga", "nigger", "faggot",
    "retard", "idiot", "stupid", "moron", "cunt", "cock", "piss"
]

SPAM_MESSAGES = [
    "۲۶ به ازای هر چیزی", "۲۶۰ ماشین سوار", "۶۶۶ شیطانی", "۴۲۰ حال کن",
    "سیکتیر از این کلاس", "داشاق چطوری", "علی پروین گاد", "سگ باز کن",
    "کیرم تو کلاس", "کص نگو بچه", "حرومزاده بازی درنیار",
    "ننتو میگام", "باباتو کردم", "کیرم دهنت", "کصخل بگو چیه",
    "sybau motherfucker", "fuck this class", "bitch ass teacher",
    "asshole students", "dickhead professor", "pussy moderator",
    "motherfucker admin", "shit class", "bastard system"
]

class UbuntuSkyRoomSpammer:
    def __init__(self):
        self.drivers = []
        self.success_count = 0
        self.spam_count = 0
        self.lock = threading.Lock()
        self.active_threads = 0
        self.max_threads = 8  # کاهش thread برای سرور
        self.start_time = None
        self.target_users = 0
        self.attempt_count = 0
        
    def setup_driver(self):
        """تنظیمات کروم برای سرور اوبونتو"""
        chrome_options = Options()
        
        # تنظیمات برای سرور بدون GUI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")  # فعال کردن headless برای سرور
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # تنظیمات performance
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2,
        })
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(15)
            return driver
        except Exception as e:
            print(f"❌ Error creating Chrome driver: {e}")
            return None

    def join_class(self, name, user_id, total_users, skyroom_link):
        """ورود به کلاس"""
        driver = self.setup_driver()
        if not driver:
            return False
            
        try:
            print(f"🎯 User {user_id}/{total_users}: {name}")
            
            # مرحله ۱: لود صفحه
            print(f"   📍 Loading page...")
            driver.get(skyroom_link)
            time.sleep(3)
            
            # مرحله ۲: پیدا کردن دکمه مهمان
            print(f"   🔍 Finding guest button...")
            guest_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "btn_guest"))
            )
            guest_btn.click()
            print(f"   ✅ Guest button clicked")
            time.sleep(2)
            
            # مرحله ۳: وارد کردن نام
            print(f"   ⌨️ Entering name...")
            name_field = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']"))
            )
            name_field.clear()
            
            # تایپ آهسته‌تر برای سرور
            for char in name:
                name_field.send_keys(char)
                time.sleep(0.1)
            time.sleep(1)
            
            # مرحله ۴: کلیک تأیید
            print(f"   ✅ Clicking confirm...")
            confirm_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'تأیید') or contains(., 'Confirm') or contains(., 'ورود')]"))
            )
            confirm_btn.click()
            print(f"   🎉 Confirm clicked")
            time.sleep(5)
            
            # چک کردن موفقیت
            if self.check_join_success(driver):
                print(f"✅ SUCCESS - User {user_id} joined")
                with self.lock:
                    self.success_count += 1
                
                self.start_spam(driver, name, user_id, total_users)
                return True
            else:
                print(f"❌ User {user_id} failed to join")
                return False
                
        except Exception as e:
            print(f"❌ Error user {user_id}: {str(e)}")
            return False
        finally:
            with self.lock:
                self.active_threads -= 1

    def check_join_success(self, driver):
        """چک کردن موفقیت در ورود"""
        try:
            # چک کردن URL
            current_url = driver.current_url.lower()
            if "skyroom" in current_url:
                # چک کردن عناصر مختلف
                indicators = [
                    "video", "canvas", ".video-", "#localVideo", 
                    ".participant", ".user-", ".room-", ".meeting-"
                ]
                
                for indicator in indicators:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, indicator)
                        if len(elements) > 0:
                            return True
                    except:
                        continue
                
                # اگر URL تغییر کرده
                if "ch/" in current_url or "room" in current_url:
                    return True
                    
            return False
        except:
            return False

    def start_spam(self, driver, name, user_id, total_users):
        """شروع اسپم"""
        print(f"🔥 User {user_id} starting spam")
        
        try:
            for i in range(random.randint(8, 20)):
                message = random.choice(SPAM_MESSAGES)
                if self.send_chat_message(driver, message):
                    with self.lock:
                        self.spam_count += 1
                    print(f"💬 User {user_id} message {self.spam_count}: {message}")
                
                time.sleep(random.uniform(0.5, 2))
            
            print(f"🎊 User {user_id} spam completed")
            
        except Exception as e:
            print(f"⚠️ Spam error user {user_id}: {e}")
        
        self.keep_online(driver, user_id)

    def send_chat_message(self, driver, message):
        """ارسال پیام در چت"""
        try:
            # پیدا کردن فیلد چت
            chat_selectors = [
                "div[contenteditable='true']",
                "input[type='text']",
                "textarea",
                ".chat-input",
                "#chat-input",
                "[contenteditable='true']"
            ]
            
            for selector in chat_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            element.click()
                            time.sleep(0.5)
                            
                            if element.get_attribute('contenteditable') == 'true':
                                driver.execute_script("arguments[0].innerHTML = '';", element)
                            else:
                                element.clear()
                            
                            element.send_keys(message)
                            time.sleep(0.5)
                            element.send_keys(Keys.ENTER)
                            time.sleep(1)
                            return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            return False

    def keep_online(self, driver, user_id):
        """نگه داشتن کاربر آنلاین"""
        print(f"💚 Keeping user {user_id} online")
        
        try:
            online_time = random.randint(180, 600)  # 3-10 دقیقه
            start_time = time.time()
            
            while time.time() - start_time < online_time:
                time.sleep(15)
                if not self.check_join_success(driver):
                    print(f"⚠️ User {user_id} disconnected")
                    break
            
            print(f"👋 User {user_id} leaving")
            
        except Exception as e:
            print(f"❌ Online error user {user_id}: {e}")
        finally:
            try:
                driver.quit()
            except:
                pass

    def run_ubuntu_attack(self, user_count, skyroom_link):
        """اجرای حمله روی اوبونتو"""
        print("🚀 UBUNTU SERVER ATTACK STARTED")
        print(f"🎯 TARGET: {user_count} users")
        print(f"🔗 LINK: {skyroom_link}")
        print("=" * 50)
        
        self.start_time = time.time()
        self.target_users = user_count
        
        # مانیتور
        monitor_thread = threading.Thread(target=self.ubuntu_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # اجرای کارگران
        self.ubuntu_workers(user_count, skyroom_link)
        
        self.final_ubuntu_report()

    def ubuntu_workers(self, user_count, skyroom_link):
        """کارگران برای اوبونتو"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            
            for i in range(user_count):
                if self.success_count >= user_count:
                    break
                    
                name = random.choice(NAMES)
                user_id = i + 1
                
                future = executor.submit(self.ubuntu_worker, name, user_id, user_count, skyroom_link)
                futures.append(future)
                
                time.sleep(1.5)  # فاصله بیشتر برای سرور
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"❌ Worker error: {e}")

    def ubuntu_worker(self, name, user_id, total_users, skyroom_link):
        """کارگر اوبونتو"""
        with self.lock:
            self.active_threads += 1
            self.attempt_count += 1
            
        success = self.join_class(name, user_id, total_users, skyroom_link)
        
        # تلاش مجدد در صورت شکست
        if not success and self.success_count < total_users:
            time.sleep(3)
            print(f"🔄 Retry user {user_id}")
            self.join_class(name, user_id, total_users, skyroom_link)

    def ubuntu_monitor(self):
        """مانیتور اوبونتو"""
        try:
            while self.success_count < self.target_users or self.active_threads > 0:
                elapsed = int(time.time() - self.start_time)
                success_rate = (self.success_count / self.target_users) * 100 if self.target_users > 0 else 0
                
                print(f"\n📊 UBUNTU STATUS - {elapsed}s")
                print(f"   ✅ JOINED: {self.success_count}/{self.target_users}")
                print(f"   💬 MESSAGES: {self.spam_count}")
                print(f"   🧵 ACTIVE: {self.active_threads}")
                print(f"   🔄 ATTEMPTS: {self.attempt_count}")
                print(f"   📈 SUCCESS RATE: {success_rate:.1f}%")
                
                # محاسبه ETA
                if success_rate > 0 and elapsed > 30:
                    remaining = self.target_users - self.success_count
                    rate = self.success_count / (elapsed / 60)
                    if rate > 0:
                        eta = remaining / rate
                        print(f"   ⏱️ ETA: {eta:.1f} minutes")
                
                print("-" * 40)
                time.sleep(10)
                
        except Exception as e:
            print(f"❌ Monitor error: {e}")

    def final_ubuntu_report(self):
        """گزارش نهایی"""
        total_time = int(time.time() - self.start_time)
        success_rate = (self.success_count / self.target_users) * 100
        
        print("\n" + "=" * 60)
        print("🎉 UBUNTU MISSION COMPLETED!")
        print("=" * 60)
        print(f"📊 FINAL RESULTS:")
        print(f"   👥 TARGET: {self.target_users}")
        print(f"   ✅ SUCCESS: {self.success_count}")
        print(f"   💬 MESSAGES: {self.spam_count}")
        print(f"   ⏱️ TIME: {total_time}s ({total_time/60:.1f}m)")
        print(f"   🎯 RATE: {success_rate:.1f}%")
        
        if success_rate >= 80:
            status = "💀 EXCELLENT"
        elif success_rate >= 60:
            status = "🔥 GOOD" 
        elif success_rate >= 40:
            status = "⚠️ AVERAGE"
        else:
            status = "❌ POOR"
            
        print(f"   📈 STATUS: {status}")
        print("=" * 60)

    def close_all(self):
        """بستن درایورها"""
        print("\n🔒 Closing browsers...")
        for driver in self.drivers:
            try:
                driver.quit()
            except:
                pass
        print("✅ Cleanup done")

def main():
    """تابع اصلی"""
    print("🎪 SKYROOM SPAMMER - UBUNTU SERVER EDITION")
    print("=" * 45)
    
    try:
        skyroom_link = input("Enter Skyroom class link: ").strip()
        if not skyroom_link:
            print("❌ Please enter a valid link!")
            return
            
        try:
            user_count = int(input("Enter number of users: "))
            if user_count <= 0:
                print("❌ Number must be greater than 0!")
                return
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        print(f"\n⚠️ CONFIRM UBUNTU ATTACK:")
        print(f"   Users: {user_count}")
        print(f"   Link: {skyroom_link}")
        confirm = input("✅ Type 'y' to start: ")
        
        if confirm.lower() != 'y':
            print("❌ Cancelled!")
            return
            
        bot = UbuntuSkyRoomSpammer()
        
        try:
            bot.run_ubuntu_attack(user_count, skyroom_link)
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user!")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            bot.close_all()
            
        input("\nPress Enter to exit...")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
