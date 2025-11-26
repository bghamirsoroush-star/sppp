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

# میم‌های فارسی خالص
NAMES = [
    "۲۶", "۲۶۰", "۶۶۶", "۴۲۰", "۱۴", "۴۰", "۱۹", "۲۵",
    "ادب", "ذات", "شرافت", "عقل", "حیا", "منطق", "اخلاق", "وجدان",
    "شرف", "ناموس", "غیرت", "مرام", "پارتی", "رانت", "فیلم سوپر",
    "کصشر", "مغز", "کلیه", "پول", "ماشین", "خونه", "زندونی",
    "تیک تاک", "اینستا", "شاد", "روبیکا", "ایتا", "بله", "گپ",
    "پیروز", "دخترخاله", "پسرخاله", "عمه", "خاله", "عمو", "دایی"
]

SPAM_MESSAGES = [
    "۲۶ به ازای هر چیزی", "۲۶۰ ماشین سوار", "۶۶۶ شیطانی", "۴۲۰ حال کن",
    "۱۴ معصوم", "۴۰ صیک", "۱۹ بهله", "۲۵ سالم",
    "ادب از که اموختی", "ذات ما همینه دیگه", "شرافت فروشی نکن", "عقل کل",
    "حیا کن دیگه", "منطق میخواد", "اخلاق هم چیز خوبیه", "وجدان بیدار",
    "شرف بزار کنار", "ناموس حرف نزن", "غیرت مردونه", "مرام بزار رو میز",
    "پارتی بازی درسته", "رانت خوری عالیه", "فیلم سوپر ندیدم", "کصشر نگو",
    "مغز داری استفاده کن", "کلیه اتو فروختی", "پول پارو میکنم", "ماشین مدل بالا",
    "خونه شمال شهر", "زندونی شدم", "تیک تاک بزن بریم", "اینستا فالو کن",
    "شاد باز کن", "روبیکا چت", "ایتا بیا پیوی", "بله آنلاین", "گپ گروهی",
    "پیروز نژاد", "دخترخاله ام", "پسرخاله شد", "عمه جون", "خاله خانم",
    "عمو سبزی فروش", "دایی جان", "صیک پاک کن", "گول نخور", "کلاه بذار"
]

class SkyRoomFarsiSpam:
    def __init__(self):
        self.drivers = []
        self.success_count = 0
        self.spam_count = 0
        self.lock = threading.Lock()
        self.active_threads = 0
        self.max_threads = 30
        self.start_time = None
        
    def setup_driver(self):
        """تنظیمات کروم بهینه‌شده"""
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
        
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
        })
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(20)
        self.drivers.append(driver)
        return driver

    def join_class(self, name, user_id, total_users, skyroom_link):
        """ورود به کلاس"""
        driver = self.setup_driver()
        try:
            print(f"🎯 کاربر {user_id} از {total_users}: {name}")
            
            # مرحله ۱: رفتن به لینک اسکای روم
            driver.get(skyroom_link)
            time.sleep(1.5)
            
            # مرحله ۲: کلیک مهمان
            guest_btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.ID, "btn_guest"))
            )
            guest_btn.click()
            time.sleep(1)
            
            # مرحله ۳: وارد کردن نام
            name_field = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.full-width[type='text']"))
            )
            name_field.clear()
            
            for char in name:
                name_field.send_keys(char)
                time.sleep(0.02)
            
            time.sleep(0.5)
            
            # مرحله ۴: کلیک تأیید
            confirm_btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'تأیید')]]"))
            )
            confirm_btn.click()
            time.sleep(2)
            
            print(f"✅ کاربر {user_id} از {total_users} وارد شد: {name}")
            with self.lock:
                self.success_count += 1
            
            # شروع اسپم
            self.farsi_spam(driver, name, user_id, total_users)
            
        except Exception as e:
            print(f"❌ خطا در کاربر {user_id}: {e}")
            try:
                driver.quit()
            except:
                pass
        finally:
            with self.lock:
                self.active_threads -= 1

    def farsi_spam(self, driver, name, user_id, total_users):
        """اسپم با میم‌های فارسی"""
        print(f"🔥 کاربر {user_id} از {total_users} شروع اسپم کرد!")
        
        session_count = 0
        max_sessions = random.randint(2, 5)
        
        while session_count < max_sessions:
            try:
                chat_element = self.find_chat_element(driver)
                if chat_element:
                    messages_count = random.randint(5, 12)
                    
                    for i in range(messages_count):
                        message = random.choice(SPAM_MESSAGES)
                        if self.send_farsi_message(driver, chat_element, message):
                            with self.lock:
                                self.spam_count += 1
                            print(f"💬 کاربر {user_id} پیام {self.spam_count}: {message}")
                        
                        time.sleep(random.uniform(0.1, 0.5))
                    
                    session_count += 1
                    print(f"🎯 کاربر {user_id} session {session_count} تمام شد")
                
                break_time = random.randint(3, 10)
                if break_time > 5:
                    print(f"⏳ کاربر {user_id} منتظر {break_time} ثانیه...")
                time.sleep(break_time)
                
            except Exception as e:
                print(f"⚠️ خطا در اسپم کاربر {user_id}: {e}")
                time.sleep(1)
        
        print(f"🎊 کاربر {user_id} از {total_users} اسپم تمام کرد!")
        
        self.keep_alive(driver, name, user_id, total_users)

    def find_chat_element(self, driver):
        """پیدا کردن فیلد چت"""
        selectors = [
            "div[contenteditable='true']",
            "input[type='text']", 
            "textarea",
            "[contenteditable='true']"
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

    def send_farsi_message(self, driver, chat_element, message):
        """ارسال پیام فارسی"""
        try:
            chat_element.click()
            time.sleep(0.05)
            
            if chat_element.get_attribute('contenteditable') == 'true':
                driver.execute_script("arguments[0].innerHTML = '';", chat_element)
            else:
                chat_element.clear()
            
            chat_element.send_keys(message)
            time.sleep(0.05)
            chat_element.send_keys(Keys.ENTER)
            time.sleep(0.1)
            
            return True
        except:
            return False

    def keep_alive(self, driver, name, user_id, total_users):
        """نگه داشتن کاربر در کلاس"""
        counter = 0
        try:
            while True:
                time.sleep(30)
                counter += 0.5
                if counter % 5 == 0:
                    print(f"💚 کاربر {user_id} از {total_users} آنلاین ({int(counter)} دقیقه)")
        except:
            pass

    def run_with_user_count(self, user_count, skyroom_link):
        """اجرای اصلی با لینک و تعداد کاربران انتخابی"""
        print(f"🚀 شروع اسپم با {user_count} کاربر")
        print(f"🎯 لینک: {skyroom_link}")
        print("👻 حالت مخفی: فعال")
        print("⚡ حالت توربو: فعال")
        print("🔥 میم‌های فارسی فعال شد!")
        print("=" * 50)
        
        self.start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for i in range(user_count):
                name = random.choice(NAMES)
                future = executor.submit(self.quick_join, name, i+1, user_count, skyroom_link)
                futures.append(future)
                time.sleep(0.1)
            
            concurrent.futures.wait(futures)
        
        self.final_report(user_count)

    def quick_join(self, name, user_id, total_users, skyroom_link):
        """ورود سریع کاربر"""
        with self.lock:
            self.active_threads += 1
            
        self.join_class(name, user_id, total_users, skyroom_link)

    def progress_monitor(self, user_count):
        """مانیتور کردن پیشرفت"""
        try:
            while self.active_threads > 0:
                elapsed = int(time.time() - self.start_time)
                success_rate = (self.success_count / user_count) * 100
                
                print(f"\n📊 گزارش فوری ({elapsed} ثانیه):")
                print(f"   ✅ کاربران موفق: {self.success_count}/{user_count} ({success_rate:.1f}%)")
                print(f"   💬 پیام‌های ارسالی: {self.spam_count}")
                print(f"   🧵 کاربران فعال: {self.active_threads}")
                if elapsed > 0:
                    print(f"   ⚡ میانگین پیام در دقیقه: {self.spam_count / (elapsed/60):.1f}")
                print("-" * 40)
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n🛑 توقف توسط کاربر...")

    def final_report(self, user_count):
        """گزارش نهایی"""
        total_time = int(time.time() - self.start_time)
        success_rate = (self.success_count / user_count) * 100
        messages_per_minute = self.spam_count / (total_time/60) if total_time > 0 else 0
        
        print("\n" + "=" * 50)
        print("🎊 عملیات کامل شد!")
        print("=" * 50)
        print(f"📈 نتایج نهایی:")
        print(f"   👥 تعداد کاربران درخواستی: {user_count}")
        print(f"   ✅ کاربران موفق: {self.success_count} ({success_rate:.1f}%)")
        print(f"   💬 مجموع پیام‌ها: {self.spam_count}")
        print(f"   ⏱️ زمان کل: {total_time} ثانیه")
        print(f"   🚀 میانگین پیام در دقیقه: {messages_per_minute:.1f}")
        print("=" * 50)

    def close_all(self):
        """بستن همه کروم‌ها"""
        print("\n🔒 در حال بستن کروم‌ها...")
        for driver in self.drivers:
            try:
                driver.quit()
            except:
                pass
        print("✅ تمام کروم‌ها بسته شدند")

def main():
    """تابع اصلی با دریافت لینک و تعداد کاربران"""
    print("🎪 اسکریپت اسپم اسکای روم - نسخه توربو")
    print("=" * 40)
    
    try:
        # دریافت لینک اسکای روم از کاربر
        skyroom_link = input("🔗 لینک اسکای روم را وارد کنید: ").strip()
        
        if not skyroom_link.startswith('http'):
            print("❌ لینک نامعتبر! لطفاً یک لینک کامل وارد کنید.")
            return
        
        # دریافت تعداد کاربران
        user_count = int(input("👥 تعداد کاربران مورد نظر را وارد کنید: "))
        
        if user_count <= 0:
            print("❌ تعداد باید بیشتر از ۰ باشد!")
            return
        
        # تأیید نهایی
        print(f"\n⚠️ آیا مطمئنید می‌خواهید {user_count} کاربر وارد کلاس شوند؟")
        confirm = input("✅ برای تأیید 'y' را وارد کنید، برای لغو هر کلید دیگر: ")
        
        if confirm.lower() != 'y':
            print("❌ عملیات لغو شد!")
            return
        
        # اجرای اسکریپت
        bot = SkyRoomFarsiSpam()
        
        # شروع مانیتور در thread جداگانه
        monitor_thread = threading.Thread(target=bot.progress_monitor, args=(user_count,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        bot.run_with_user_count(user_count, skyroom_link)
        
        input("\n⏹️ برای بستن Enter بزنید...")
        
    except ValueError:
        print("❌ لطفاً یک عدد معتبر وارد کنید!")
    except KeyboardInterrupt:
        print("\n🛑 توقف توسط کاربر...")
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")
    finally:
        try:
            bot.close_all()
        except:
            pass

if __name__ == "__main__":
    main()
