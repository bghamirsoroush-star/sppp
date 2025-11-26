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
        self.max_threads = 50  # افزایش threadها برای سرعت بیشتر
        self.start_time = None
        
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
        chrome_options.add_argument("--max_old_space_size=1024")
        
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2,
        })
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(15)  # کاهش بیشتر timeout
        driver.set_script_timeout(15)
        self.drivers.append(driver)
        return driver

    def join_class(self, name, user_id, total_users, skyroom_link):
        """ورود به کلاس - فوق سریع"""
        driver = self.setup_driver()
        try:
            print(f"🎯 کاربر {user_id} از {total_users}: {name}")
            
            # مرحله ۱: رفتن به لینک با timeout کوتاه
            driver.get(skyroom_link)
            time.sleep(1)  # کاهش زمان انتظار
            
            # مرحله ۲: کلیک مهمان با انتظار کوتاه
            guest_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "btn_guest"))
            )
            guest_btn.click()
            time.sleep(0.5)
            
            # مرحله ۳: وارد کردن نام سریع
            name_field = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.full-width[type='text']"))
            )
            name_field.clear()
            
            # تایپ فوق سریع
            name_field.send_keys(name)
            time.sleep(0.3)
            
            # مرحله ۴: کلیک تأیید
            confirm_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'تأیید')]]"))
            )
            confirm_btn.click()
            time.sleep(1.5)  # کاهش زمان انتظار برای ورود
            
            print(f"✅ کاربر {user_id} از {total_users} وارد شد: {name}")
            with self.lock:
                self.success_count += 1
            
            # شروع اسپم سریع
            self.turbo_spam(driver, name, user_id, total_users)
            
        except Exception as e:
            print(f"❌ خطا در کاربر {user_id}: {str(e)[:50]}...")
            try:
                driver.quit()
            except:
                pass
        finally:
            with self.lock:
                self.active_threads -= 1

    def turbo_spam(self, driver, name, user_id, total_users):
        """اسپم توربو با پیام‌های زیاد"""
        print(f"🔥 کاربر {user_id} از {total_users} شروع اسپم توربو کرد!")
        
        session_count = 0
        max_sessions = random.randint(3, 8)  # افزایش sessions
        
        while session_count < max_sessions:
            try:
                chat_element = self.find_chat_element(driver)
                if chat_element:
                    # افزایش تعداد پیام‌ها در هر session
                    messages_count = random.randint(8, 20)
                    
                    for i in range(messages_count):
                        message = random.choice(SPAM_MESSAGES)
                        if self.send_turbo_message(driver, chat_element, message):
                            with self.lock:
                                self.spam_count += 1
                            print(f"💬 کاربر {user_id} پیام {self.spam_count}: {message}")
                        
                        time.sleep(random.uniform(0.05, 0.2))  # کاهش فاصله
                    
                    session_count += 1
                    print(f"🎯 کاربر {user_id} session {session_count} تمام شد - {messages_count} پیام")
                
                # فاصله کوتاه بین sessionها
                break_time = random.randint(2, 6)
                time.sleep(break_time)
                
            except Exception as e:
                print(f"⚠️ خطا در اسپم کاربر {user_id}: {str(e)[:50]}...")
                time.sleep(1)
        
        print(f"🎊 کاربر {user_id} از {total_users} اسپم تمام کرد! ({session_count} session)")
        
        # ماندن در کلاس برای مدت بیشتر
        self.keep_alive_turbo(driver, name, user_id, total_users)

    def find_chat_element(self, driver):
        """پیدا کردن فیلد چت - سریع"""
        selectors = [
            "div[contenteditable='true']",
            "input[type='text']", 
            "textarea",
            "[contenteditable='true']",
            ".chat-input",
            "#chat-input",
            "input.chat-input"
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
        """ارسال پیام فوق سریع"""
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
        """نگه داشتن کاربر در کلاس - بهینه"""
        counter = 0
        max_time = random.randint(300, 600)  # 5-10 دقیقه
        
        try:
            start_time = time.time()
            while time.time() - start_time < max_time:
                time.sleep(20)  # چک هر 20 ثانیه
                counter += 1
                if counter % 3 == 0:
                    print(f"💚 کاربر {user_id} از {total_users} آنلاین ({counter} چک)")
        except:
            pass

    def run_turbo_spam(self, user_count, skyroom_link):
        """اجرای توربو اسپم"""
        print(f"🚀 شروع اسپم توربو با {user_count} کاربر")
        print(f"🎯 لینک: {skyroom_link}")
        print("👻 حالت مخفی: فعال")
        print("⚡ حالت توربو: فعال")
        print("🔥 میم‌های فارسی/انگلیسی فعال شد!")
        print("💀 حالت شیطانی: فعال")
        print("=" * 50)
        
        self.start_time = time.time()
        
        # استفاده از ThreadPoolExecutor برای مدیریت بهتر
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for i in range(user_count):
                name = random.choice(NAMES)
                future = executor.submit(self.quick_turbo_join, name, i+1, user_count, skyroom_link)
                futures.append(future)
                time.sleep(0.05)  # فاصله بسیار کم
            
            concurrent.futures.wait(futures)
        
        self.final_report(user_count)

    def quick_turbo_join(self, name, user_id, total_users, skyroom_link):
        """ورود توربو کاربر"""
        with self.lock:
            self.active_threads += 1
            
        self.join_class(name, user_id, total_users, skyroom_link)

    def progress_monitor(self, user_count):
        """مانیتور پیشرفت پیشرفته"""
        try:
            while self.active_threads > 0:
                elapsed = int(time.time() - self.start_time)
                success_rate = (self.success_count / user_count) * 100
                
                print(f"\n📊 گزارش توربو ({elapsed} ثانیه):")
                print(f"   ✅ کاربران موفق: {self.success_count}/{user_count} ({success_rate:.1f}%)")
                print(f"   💬 پیام‌های ارسالی: {self.spam_count}")
                print(f"   🧵 کاربران فعال: {self.active_threads}")
                if elapsed > 0:
                    rate_per_min = self.spam_count / (elapsed/60)
                    print(f"   ⚡ سرعت: {rate_per_min:.1f} پیام/دقیقه")
                    print(f"   🎯 موفقیت: {success_rate:.1f}%")
                print("-" * 40)
                
                time.sleep(8)  # گزارش هر 8 ثانیه
                
        except KeyboardInterrupt:
            print("\n🛑 توقف توسط کاربر...")

    def final_report(self, user_count):
        """گزارش نهایی توربو"""
        total_time = int(time.time() - self.start_time)
        success_rate = (self.success_count / user_count) * 100
        messages_per_minute = self.spam_count / (total_time/60) if total_time > 0 else 0
        
        print("\n" + "=" * 60)
        print("🎊 عملیات توربو کامل شد!")
        print("=" * 60)
        print(f"📈 نتایج نهایی توربو:")
        print(f"   👥 تعداد کاربران درخواستی: {user_count}")
        print(f"   ✅ کاربران موفق: {self.success_count} ({success_rate:.1f}%)")
        print(f"   💬 مجموع پیام‌ها: {self.spam_count}")
        print(f"   ⏱️ زمان کل: {total_time} ثانیه ({total_time/60:.1f} دقیقه)")
        print(f"   🚀 میانگین پیام در دقیقه: {messages_per_minute:.1f}")
        print(f"   💀 کارایی: {'عالی' if success_rate > 80 else 'خوب' if success_rate > 60 else 'متوسط'}")
        print("=" * 60)

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
    """تابع اصلی"""
    print("🎪 اسکریپت اسپم اسکای روم - نسخه توربو شیطانی")
    print("💀 مجهز به میم‌های فارسی و انگلیسی پیشرفته")
    print("=" * 50)
    
    try:
        # دریافت لینک اسکای روم
        skyroom_link = input("🔗 لینک اسکای روم را وارد کنید: ").strip()
        
        if not skyroom_link.startswith('http'):
            print("❌ لینک نامعتبر! لطفاً یک لینک کامل وارد کنید.")
            return
        
        # دریافت تعداد کاربران
        user_count = int(input("👥 تعداد کاربران مورد نظر را وارد کنید: "))
        
        if user_count <= 0:
            print("❌ تعداد باید بیشتر از ۰ باشد!")
            return
        
        if user_count > 100:
            print("⚠️ اخطار: تعداد بالا ممکن است باعث کندی شود!")
        
        # تأیید نهایی
        print(f"\n⚠️ آیا مطمئنید می‌خواهید {user_count} کاربر وارد کلاس شوند؟")
        print("💀 این عمل ممکن است باعث اختلال در کلاس شود!")
        confirm = input("✅ برای تأیید 'y' را وارد کنید، برای لغو هر کلید دیگر: ")
        
        if confirm.lower() != 'y':
            print("❌ عملیات لغو شد!")
            return
        
        # اجرای اسکریپت
        bot = SkyRoomTurboSpam()
        
        # شروع مانیتور
        monitor_thread = threading.Thread(target=bot.progress_monitor, args=(user_count,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        bot.run_turbo_spam(user_count, skyroom_link)
        
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
