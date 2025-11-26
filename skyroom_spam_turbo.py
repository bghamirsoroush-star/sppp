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

# میم‌های فارسی و انگلیسی جدید
NAMES = [
    # فارسی
    "۲۶", "۲۶۰", "۶۶۶", "۴۲۰", "۱۴", "۴۰", "۱۹", "۲۵", "۶۱", "۶۷", "۶۹",
    "سیکتیر", "داشاق", "علی", "پروین", "سگ", "خره", "گاو", "گاد", "نولایف",
    "کیر", "کص", "کونی", "حرومزاده", "بی‌ناموس", "بی‌غیرت", "پدرسوخته",
    "مادرجنده", "لاشی", "جنده", "فحش", "ننت", "بابات", "خواهرت", "برادرت",
    "کیرم", "کصخل", "احمق", "نادان", "خرفت", "عقب‌مانده", "دیوث", "شومبول",
    "گوز", "عن", "گند", "کثافت", "چس", "پوف", "فاک", "شیطون", "جن‌زده",
    
    # انگلیسی
    "sybau", "fuck", "bitch", "ass", "dick", "pussy", "motherfucker",
    "shit", "bastard", "whore", "slut", "nigga", "nigger", "faggot",
    "retard", "idiot", "stupid", "moron", "cunt", "cock", "piss",
    "damn", "hell", "satan", "devil", "demon", "kill", "die", "dead",
    "sex", "porn", "dickhead", "asshole", "bullshit", "wanker", "twat",
    "waste", "trash", "garbage", "scum", "vermin", "rat", "worm",
    "666", "420", "69", "187", "911", "999", "111", "777", "888",
    "God", "Satan", "Lucifer", "Beelzebub", "Antichrist", "Evil"
]

SPAM_MESSAGES = [
    # فارسی
    "۲۶ به ازای هر چیزی", "۲۶۰ ماشین سوار", "۶۶۶ شیطانی", "۴۲۰ حال کن",
    "۱۴ معصوم", "۴۰ صیک", "۱۹ بهله", "۲۵ سالم", "۶۱ سیک", "۶۷ گاد", "۶۹ سکس",
    "سیکتیر از این کلاس", "داشاق چطوری", "علی پروین گاد", "سگ باز کن",
    "خره نگو", "گاو صفت", "گاد مود فعال", "نولایف چیه", "کیرم تو کلاس",
    "کص نگو بچه", "کونی بیا پایین", "حرومزاده بازی درنیار",
    "بی‌ناموس چرا اینجوری", "بی‌غیرت مثل پدرت", "پدرسوخته بگو چیه",
    "مادرجنده لاشی", "لاشی بازی درنیار", "جنده بازار", "فحش بده",
    "ننتو میگام", "باباتو کردم", "خواهرت حشریه", "برادرت کیریشو خوردم",
    "کیرم دهنت", "کصخل بگو چیه", "احمق نگو", "نادان مثل همیشه",
    "خرفت بازی درنیار", "عقب‌مانده ذهنی", "دیوث چرا اینجوری",
    "شومبول نخور", "گوز زیاد نده", "عنم گرفت", "گند بازی درنیار",
    "کثافت کاری نکن", "چس مگه داریم", "پوف نکن", "فاک یو", "شیطون بلا",
    "جن‌زده بازی درنیار",
    
    # انگلیسی
    "sybau motherfucker", "fuck this class", "bitch ass teacher",
    "asshole students", "dickhead professor", "pussy moderator",
    "motherfucker admin", "shit class", "bastard system", "whore university",
    "slut education", "nigga please", "nigger style", "faggot behavior",
    "retard students", "idiot teacher", "stupid system", "moron admin",
    "cunt class", "cock sucker", "piss off", "damn this shit", "hell yeah",
    "satan is here", "devil power", "demon mode", "kill yourself", "die already",
    "dead class", "sex education", "porn hub", "dickhead admin", "asshole system",
    "bullshit class", "wanker teacher", "twat face", "waste of time",
    "trash system", "garbage education", "scum university", "vermin students",
    "rat teacher", "worm admin", "666 satanic", "420 blaze it", "69 position",
    "187 murder", "911 emergency", "999 help", "111 angel", "777 lucky",
    "888 infinity", "God is dead", "Satan lives", "Lucifer king", "Beelzebub lord",
    "Antichrist here", "Evil rules",
    
    # ترکیبی
    "۲۶۰ sybau", "۶۶۶ satan", "۴۲۰ blaze", "سیکتیر bitch", "داشاق motherfucker",
    "علی پروین god", "سگ dog style", "گاو cow shit", "گاد mode on", "نولایف no life",
    "کیر dick", "کص pussy", "کونی faggot", "فحش curse", "ننت your mom",
    "بابات your dad", "خواهرت your sister", "کیرم my dick", "کصخل retard",
    "احمق idiot", "دیوث bastard", "شومبول balls", "گوز fart", "عن shit",
    "گند trash", "کثافت dirty", "چس kiss", "پوف puff", "فاک fuck"
]

class SkyRoomTurboSpam:
    def __init__(self):
        self.drivers = []
        self.success_count = 0
        self.spam_count = 0
        self.lock = threading.Lock()
        self.active_threads = 0
        self.max_threads = 50
        self.start_time = None
        self.target_users = 0
        self.attempt_count = 0
        
    def setup_driver(self):
        """تنظیمات کروم فوق سریع"""
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--memory-pressure-off")
        chrome_options.add_argument("--aggressive-cache-discard")
        
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2,
        })
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(15)
        driver.set_script_timeout(15)
        self.drivers.append(driver)
        return driver

    def join_class(self, name, user_id, total_users, skyroom_link):
        """ورود به کلاس - با قابلیت تلاش مجدد"""
        driver = self.setup_driver()
        max_attempts = 3  # حداکثر تلاش برای هر کاربر
        
        for attempt in range(max_attempts):
            try:
                print(f"🎯 User {user_id}/{total_users}: {name} (Attempt {attempt + 1})")
                
                # مرحله ۱: رفتن به لینک
                driver.get(skyroom_link)
                time.sleep(1.5)
                
                # مرحله ۲: کلیک مهمان
                guest_btn = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.ID, "btn_guest"))
                )
                guest_btn.click()
                time.sleep(0.8)
                
                # مرحله ۳: وارد کردن نام
                name_field = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.full-width[type='text']"))
                )
                name_field.clear()
                name_field.send_keys(name)
                time.sleep(0.5)
                
                # مرحله ۴: کلیک تأیید
                confirm_btn = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'تأیید')]]"))
                )
                confirm_btn.click()
                time.sleep(2.5)
                
                # چک کردن موفقیت آمیز بودن ورود
                if self.check_join_success(driver):
                    print(f"✅ SUCCESS - User {user_id}/{total_users} joined: {name}")
                    with self.lock:
                        self.success_count += 1
                    
                    # شروع اسپم
                    self.turbo_spam(driver, name, user_id, total_users)
                    return True
                else:
                    print(f"⚠️ Retrying user {user_id}...")
                    
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed for user {user_id}: {str(e)[:50]}...")
                if attempt < max_attempts - 1:
                    time.sleep(2)  # صبر قبل از تلاش مجدد
                else:
                    print(f"💀 User {user_id} failed after {max_attempts} attempts")
        
        try:
            driver.quit()
        except:
            pass
        
        with self.lock:
            self.active_threads -= 1
        return False

    def check_join_success(self, driver):
        """چک کردن موفقیت آمیز بودن ورود به کلاس"""
        try:
            # چک کردن عناصر مختلف که نشان دهنده ورود موفق هستند
            indicators = [
                "div[class*='user']",
                "div[class*='participant']", 
                "video",
                "canvas",
                "div[class*='video']",
                "div[class*='room']",
                "div[class*='meeting']"
            ]
            
            for indicator in indicators:
                elements = driver.find_elements(By.CSS_SELECTOR, indicator)
                if len(elements) > 0:
                    return True
            
            # چک کردن URL
            current_url = driver.current_url
            if "skyroom" in current_url and ("room" in current_url or "ch/" in current_url):
                return True
                
            return False
        except:
            return False

    def turbo_spam(self, driver, name, user_id, total_users):
        """اسپم توربو"""
        print(f"🔥 User {user_id}/{total_users} started turbo spam!")
        
        session_count = 0
        max_sessions = random.randint(3, 6)
        
        while session_count < max_sessions:
            try:
                chat_element = self.find_chat_element(driver)
                if chat_element:
                    messages_count = random.randint(10, 25)  # افزایش پیام‌ها
                    
                    for i in range(messages_count):
                        message = random.choice(SPAM_MESSAGES)
                        if self.send_turbo_message(driver, chat_element, message):
                            with self.lock:
                                self.spam_count += 1
                            print(f"💬 User {user_id} message {self.spam_count}: {message}")
                        
                        time.sleep(random.uniform(0.05, 0.15))
                    
                    session_count += 1
                    print(f"🎯 User {user_id} session {session_count} completed - {messages_count} messages")
                
                break_time = random.randint(2, 5)
                time.sleep(break_time)
                
            except Exception as e:
                print(f"⚠️ Spam error user {user_id}: {str(e)[:50]}...")
                time.sleep(1)
        
        print(f"🎊 User {user_id}/{total_users} spam completed! ({session_count} sessions)")
        
        # ماندن در کلاس
        self.keep_alive_turbo(driver, name, user_id, total_users)

    def find_chat_element(self, driver):
        """پیدا کردن فیلد چت"""
        selectors = [
            "div[contenteditable='true']",
            "input[type='text']", 
            "textarea",
            "[contenteditable='true']",
            ".chat-input",
            "#chat-input"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        return element
            except:
                continue
        return None

    def send_turbo_message(self, driver, chat_element, message):
        """ارسال پیام سریع"""
        try:
            chat_element.click()
            time.sleep(0.02)
            
            if chat_element.get_attribute('contenteditable') == 'true':
                driver.execute_script("arguments[0].innerHTML = '';", chat_element)
            else:
                chat_element.clear()
            
            chat_element.send_keys(message)
            time.sleep(0.02)
            chat_element.send_keys(Keys.ENTER)
            time.sleep(0.05)
            
            return True
        except:
            return False

    def keep_alive_turbo(self, driver, name, user_id, total_users):
        """نگه داشتن کاربر در کلاس"""
        counter = 0
        max_time = random.randint(300, 900)  # 5-15 دقیقه
        
        try:
            start_time = time.time()
            while time.time() - start_time < max_time:
                time.sleep(30)
                counter += 1
                if counter % 2 == 0:
                    print(f"💚 User {user_id}/{total_users} online ({counter * 0.5} min)")
        except:
            pass
        finally:
            try:
                driver.quit()
            except:
                pass
            with self.lock:
                self.active_threads -= 1

    def run_persistent_join(self, user_count, skyroom_link):
        """اجرای جوین مداوم تا رسیدن به تعداد مورد نظر"""
        print("🚀 STARTING PERSISTENT JOIN ATTACK")
        print(f"🎯 TARGET: {user_count} users")
        print(f"🔗 CLASS LINK: {skyroom_link}")
        print("⚡ TURBO MODE: ACTIVE")
        print("💀 SATANIC MODE: ENABLED")
        print("🔄 PERSISTENT JOIN: ENABLED")
        print("=" * 60)
        
        self.start_time = time.time()
        self.target_users = user_count
        
        # شروع مانیتور
        monitor_thread = threading.Thread(target=self.persistent_progress_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # حلقه جوین مداوم
        self.persistent_join_loop(user_count, skyroom_link)
        
        # گزارش نهایی
        self.final_persistent_report()

    def persistent_join_loop(self, user_count, skyroom_link):
        """حلقه جوین مداوم تا رسیدن به تعداد هدف"""
        while self.success_count < user_count:
            available_slots = self.max_threads - self.active_threads
            needed_users = user_count - self.success_count
            
            if available_slots > 0 and needed_users > 0:
                # تعداد threadهای جدید برای اجرا
                new_threads = min(available_slots, needed_users, 10)  # حداکثر 10 thread جدید همزمان
                
                for i in range(new_threads):
                    name = random.choice(NAMES)
                    user_id = self.success_count + self.active_threads + 1
                    
                    thread = threading.Thread(
                        target=self.persistent_join_worker,
                        args=(name, user_id, user_count, skyroom_link)
                    )
                    thread.daemon = True
                    thread.start()
                    
                    with self.lock:
                        self.active_threads += 1
                        self.attempt_count += 1
                    
                    time.sleep(0.1)  # فاصله کم بین شروع threadها
            
            time.sleep(1)  # چک هر 1 ثانیه

        print("🎉 TARGET USER COUNT REACHED! Waiting for active threads to complete...")
        
        # منتظر ماندن برای اتمام threadهای فعال
        while self.active_threads > 0:
            time.sleep(2)

    def persistent_join_worker(self, name, user_id, total_users, skyroom_link):
        """کارگر جوین مداوم"""
        try:
            self.join_class(name, user_id, total_users, skyroom_link)
        except Exception as e:
            print(f"💀 Worker error for user {user_id}: {e}")
        finally:
            with self.lock:
                self.active_threads -= 1

    def persistent_progress_monitor(self):
        """مانیتور پیشرفت جوین مداوم"""
        try:
            while self.success_count < self.target_users or self.active_threads > 0:
                elapsed = int(time.time() - self.start_time)
                success_rate = (self.success_count / self.target_users) * 100 if self.target_users > 0 else 0
                attempts_per_minute = self.attempt_count / (elapsed/60) if elapsed > 0 else 0
                
                print(f"\n📊 PERSISTENT JOIN STATUS - {elapsed}s")
                print(f"   ✅ SUCCESSFUL: {self.success_count}/{self.target_users} ({success_rate:.1f}%)")
                print(f"   💬 MESSAGES: {self.spam_count}")
                print(f"   🧵 ACTIVE: {self.active_threads}")
                print(f"   🔄 ATTEMPTS: {self.attempt_count}")
                if elapsed > 0:
                    print(f"   ⚡ SPEED: {attempts_per_minute:.1f} attempts/min")
                    print(f"   🎯 SUCCESS RATE: {success_rate:.1f}%")
                
                # پیش‌بینی زمان باقیمانده
                if success_rate > 0 and elapsed > 30:
                    remaining_users = self.target_users - self.success_count
                    users_per_minute = self.success_count / (elapsed/60)
                    if users_per_minute > 0:
                        eta_minutes = remaining_users / users_per_minute
                        print(f"   ⏱️ ETA: {eta_minutes:.1f} minutes")
                
                print("-" * 50)
                
                time.sleep(8)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user...")

    def final_persistent_report(self):
        """گزارش نهایی جوین مداوم"""
        total_time = int(time.time() - self.start_time)
        success_rate = (self.success_count / self.target_users) * 100
        messages_per_minute = self.spam_count / (total_time/60) if total_time > 0 else 0
        attempts_per_minute = self.attempt_count / (total_time/60) if total_time > 0 else 0
        
        print("\n" + "=" * 70)
        print("🎉 PERSISTENT JOIN ATTACK COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("📈 FINAL STATISTICS:")
        print(f"   👥 TARGET USERS: {self.target_users}")
        print(f"   ✅ SUCCESSFUL JOINS: {self.success_count} ({success_rate:.1f}%)")
        print(f"   💬 TOTAL MESSAGES: {self.spam_count}")
        print(f"   🔄 TOTAL ATTEMPTS: {self.attempt_count}")
        print(f"   ⏱️ TOTAL TIME: {total_time} seconds ({total_time/60:.1f} minutes)")
        print(f"   🚀 MESSAGES PER MINUTE: {messages_per_minute:.1f}")
        print(f"   ⚡ ATTEMPTS PER MINUTE: {attempts_per_minute:.1f}")
        print(f"   🎯 SUCCESS RATE: {success_rate:.1f}%")
        
        # رتبه‌بندی کارایی
        if success_rate >= 90:
            rating = "💀 LEGENDARY"
        elif success_rate >= 75:
            rating = "🔥 EXCELLENT" 
        elif success_rate >= 60:
            rating = "⭐ GOOD"
        elif success_rate >= 40:
            rating = "⚠️ AVERAGE"
        else:
            rating = "❌ POOR"
            
        print(f"   📊 PERFORMANCE: {rating}")
        print("=" * 70)

    def close_all(self):
        """بستن همه کروم‌ها"""
        print("\n🔒 Closing all browsers...")
        for driver in self.drivers:
            try:
                driver.quit()
            except:
                pass
        print("✅ All browsers closed successfully")

def main():
    """تابع اصلی"""
    print("🎪 SKYROOM TURBO SPAM - PERSISTENT JOIN EDITION")
    print("💀 Advanced Persian/English Meme Attack System")
    print("=" * 55)
    
    try:
        # دریافت لینک اسکای روم
        skyroom_link = input("Enter Skyroom class link: ").strip()
        
        if not skyroom_link.startswith('http'):
            print("❌ Invalid link! Please enter a complete URL.")
            return
        
        # دریافت تعداد کاربران
        user_count = int(input("Enter number of users to join: "))
        
        if user_count <= 0:
            print("❌ Number must be greater than 0!")
            return
        
        if user_count > 100:
            print("⚠️ Warning: High user count may cause performance issues!")
        
        # تأیید نهایی
        print(f"\n⚠️ CONFIRM PERSISTENT JOIN ATTACK")
        print(f"   Target: {user_count} users")
        print(f"   Link: {skyroom_link}")
        print("💀 This will continue until target user count is reached!")
        confirm = input("✅ Type 'y' to confirm, any other key to cancel: ")
        
        if confirm.lower() != 'y':
            print("❌ Operation cancelled!")
            return
        
        # اجرای اسکریپت
        bot = SkyRoomTurboSpam()
        
        try:
            bot.run_persistent_join(user_count, skyroom_link)
        except KeyboardInterrupt:
            print("\n🛑 Operation stopped by user!")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        finally:
            bot.close_all()
        
        input("\n⏹️ Press Enter to close...")
        
    except ValueError:
        print("❌ Please enter a valid number!")
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
