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
    "پیروز", "دخترخاله", "پسرخاله", "عمه", "خاله", "عمو", "دایی",
    "عشق", "هوش", "حافظه", "اراده", "صبر", "تحمل", "گذشت", "فداکاری"
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
    "عمو سبزی فروش", "دایی جان", "صیک پاک کن", "گول نخور", "کلاه بذار",
    "عشق یعنی این", "هوش مصنوعی", "حافظه تاریخی", "اراده آهنین", "صبر کن ببینم",
    "تحمل کن دیگه", "گذشت کن بابا", "فداکاری نکن", "ایران قوی", "ملت قهرمان"
]

class SkyRoomFarsiSpam:
    def __init__(self):
        self.drivers = []
        self.success_count = 0
        self.spam_count = 0
        self.lock = threading.Lock()
        self.active_threads = 0
        self.max_threads = 50  # افزایش قابل توجه threadهای همزمان
        self.start_time = None
        self.running = True
        
    def setup_driver(self):
        """تنظیمات کروم بهینه‌شده برای سرعت بالا"""
        chrome_options = Options()
        
        # تنظیمات اصلی
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        
        # بهینه‌سازی‌های سرعت
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--memory-pressure-off")
        chrome_options.add_argument("--max_old_space_size=4096")
        
        # تنظیمات performance
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.javascript": 1,
        })
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(15)  # کاهش بیشتر timeout
            driver.set_script_timeout(15)
            self.drivers.append(driver)
            return driver
        except Exception as e:
            print(f"❌ خطا در راه‌اندازی کروم: {e}")
            return None

    def join_class(self, name, user_id, total_users):
        """ورود به کلاس - فوق سریع"""
        driver = self.setup_driver()
        if not driver:
            return
            
        try:
            print(f"🎯 کاربر {user_id} از {total_users}: {name}")
            
            # مرحله ۱: رفتن به لینک با timeout بسیار کوتاه
            driver.get("https://www.skyroom.online/ch/soroushamir/riazi101101")
            time.sleep(1)  # کاهش شدید زمان انتظار
            
            # مرحله ۲: کلیک مهمان
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
            name_field.send_keys(name)  # ارسال مستقیم نام
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
            self.farsi_spam(driver, name, user_id, total_users)
            
        except Exception as e:
            print(f"❌ خطا در کاربر {user_id}: {str(e)[:100]}...")
            try:
                driver.quit()
                self.drivers.remove(driver)
            except:
                pass
        finally:
            with self.lock:
                self.active_threads -= 1

    def farsi_spam(self, driver, name, user_id, total_users):
        """اسپم با میم‌های فارسی - فوق سریع"""
        if not self.running:
            return
            
        print(f"🔥 کاربر {user_id} از {total_users} شروع اسپم کرد!")
        
        session_count = 0
        max_sessions = random.randint(2, 4)  # کاهش بیشتر sessions
        
        while session_count < max_sessions and self.running:
            try:
                # پیدا کردن فیلد چت
                chat_element = self.find_chat_element(driver)
                if chat_element:
                    # اسپم سریع در این session
                    messages_count = random.randint(3, 8)  # کاهش تعداد پیام‌ها
                    
                    for i in range(messages_count):
                        if not self.running:
                            break
                            
                        message = random.choice(SPAM_MESSAGES)
                        if self.send_farsi_message(driver, chat_element, message):
                            with self.lock:
                                self.spam_count += 1
                            
                            if self.spam_count % 10 == 0:  # چاپ هر 10 پیام
                                print(f"💬 پیام {self.spam_count} ارسال شد")
                        
                        time.sleep(random.uniform(0.05, 0.2))  # فاصله بسیار کم
                    
                    session_count += 1
                    if self.running:
                        print(f"🎯 کاربر {user_id} session {session_count} تمام شد")
                
                # فاصله کوتاه بین sessionها
                if self.running and session_count < max_sessions:
                    break_time = random.randint(2, 6)
                    time.sleep(break_time)
                
            except Exception as e:
                if self.running:
                    print(f"⚠️ خطا در اسپم کاربر {user_id}: {str(e)[:50]}...")
                time.sleep(1)
        
        if self.running:
            print(f"🎊 کاربر {user_id} از {total_users} اسپم تمام کرد!")
        
        # ماندن در کلاس
        self.keep_alive(driver, name, user_id, total_users)

    def find_chat_element(self, driver):
        """پیدا کردن فیلد چت - فوق سریع"""
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
                    try:
                        if element.is_displayed() and element.is_enabled():
                            return element
                    except:
                        continue
            except:
                continue
        return None

    def send_farsi_message(self, driver, chat_element, message):
        """ارسال پیام فارسی - فوق سریع"""
        try:
            chat_element.click()
            time.sleep(0.02)
            
            # پاک کردن محتوا
            if chat_element.get_attribute('contenteditable') == 'true':
                driver.execute_script("arguments[0].innerHTML = '';", chat_element)
            else:
                chat_element.clear()
            
            # ارسال پیام فوق سریع
            chat_element.send_keys(message)
            time.sleep(0.02)
            chat_element.send_keys(Keys.ENTER)
            time.sleep(0.05)
            
            return True
        except:
            return False

    def keep_alive(self, driver, name, user_id, total_users):
        """نگه داشتن کاربر در کلاس - سبک"""
        counter = 0
        try:
            while self.running and counter < 120:  # حداکثر 2 ساعت
                time.sleep(30)
                counter += 0.5
                if counter % 10 == 0 and self.running:
                    print(f"💚 کاربر {user_id} از {total_users} آنلاین ({int(counter)} دقیقه)")
        except:
            pass
        finally:
            try:
                driver.quit()
                self.drivers.remove(driver)
            except:
                pass

    def run_with_user_count(self, user_count):
        """اجرای اصلی با تعداد کاربران انتخابی - توربو"""
        print(f"🚀 شروع اسپم توربو با {user_count} کاربر")
        print("🎯 لینک: https://www.skyroom.online/ch/soroushamir/riazi101101")
        print("👻 حالت مخفی: فعال")
        print("⚡ حالت توربو: فعال")
        print("🔥 میم‌های فارسی: فعال")
        print("💨 سرعت: فوق سریع")
        print("=" * 60)
        
        self.start_time = time.time()
        self.running = True
        
        # شروع مانیتورینگ
        monitor_thread = threading.Thread(target=self.progress_monitor, args=(user_count,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # استفاده از ThreadPoolExecutor برای مدیریت فوق‌العاده threadها
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                # ارسال تمام کاربران به صورت فوق سریع
                futures = []
                for i in range(user_count):
                    if not self.running:
                        break
                        
                    name = random.choice(NAMES)
                    future = executor.submit(self.quick_join, name, i+1, user_count)
                    futures.append(future)
                    time.sleep(0.05)  # فاصله بسیار بسیار کم
                
                # منتظر ماندن برای اتمام
                for future in concurrent.futures.as_completed(futures):
                    if not self.running:
                        break
                    future.result()
                    
        except KeyboardInterrupt:
            print("\n🛑 توقف توسط کاربر...")
            self.running = False
        except Exception as e:
            print(f"❌ خطای غیرمنتظره: {e}")
            self.running = False
        finally:
            self.running = False
            time.sleep(2)
            self.final_report(user_count)

    def quick_join(self, name, user_id, total_users):
        """ورود فوق سریع کاربر"""
        with self.lock:
            self.active_threads += 1
            
        self.join_class(name, user_id, total_users)

    def progress_monitor(self, user_count):
        """مانیتور کردن پیشرفت - پیشرفته"""
        last_count = 0
        last_time = time.time()
        
        try:
            while self.running and (self.active_threads > 0 or time.time() - self.start_time < 30):
                current_time = time.time()
                elapsed = int(current_time - self.start_time)
                
                # محاسبه سرعت
                speed = self.spam_count - last_count
                last_count = self.spam_count
                
                if elapsed % 10 == 0:  # گزارش هر 10 ثانیه
                    success_rate = (self.success_count / user_count) * 100 if user_count > 0 else 0
                    
                    print(f"\n📊 گزارش لحظه‌ای ({elapsed} ثانیه):")
                    print(f"   ✅ کاربران موفق: {self.success_count}/{user_count} ({success_rate:.1f}%)")
                    print(f"   💬 پیام‌های ارسالی: {self.spam_count}")
                    print(f"   🧵 کاربران فعال: {self.active_threads}")
                    print(f"   ⚡ سرعت پیام/ثانیه: {speed / 10:.1f}")
                    if elapsed > 0:
                        print(f"   🚀 میانگین پیام در دقیقه: {self.spam_count / (elapsed/60):.1f}")
                    print("-" * 50)
                
                time.sleep(10)
                
        except Exception as e:
            if self.running:
                print(f"⚠️ خطا در مانیتورینگ: {e}")

    def final_report(self, user_count):
        """گزارش نهایی"""
        total_time = int(time.time() - self.start_time)
        success_rate = (self.success_count / user_count) * 100 if user_count > 0 else 0
        messages_per_minute = self.spam_count / (total_time/60) if total_time > 0 else 0
        
        print("\n" + "=" * 60)
        print("🎊 عملیات کامل شد!")
        print("=" * 60)
        print(f"📈 نتایج نهایی:")
        print(f"   👥 تعداد کاربران درخواستی: {user_count}")
        print(f"   ✅ کاربران موفق: {self.success_count} ({success_rate:.1f}%)")
        print(f"   💬 مجموع پیام‌ها: {self.spam_count}")
        print(f"   ⏱️ زمان کل: {total_time} ثانیه")
        print(f"   🚀 میانگین پیام در دقیقه: {messages_per_minute:.1f}")
        print(f"   ⚡ کارایی سیستم: {'عالی' if success_rate > 80 else 'خوب' if success_rate > 60 else 'متوسط'}")
        print("=" * 60)

    def stop(self):
        """توقف عملیات"""
        print("\n🛑 در حال توقف عملیات...")
        self.running = False
        time.sleep(2)
        self.close_all()

    def close_all(self):
        """بستن همه کروم‌ها"""
        print("\n🔒 در حال بستن کروم‌ها...")
        self.running = False
        
        for driver in self.drivers[:]:
            try:
                driver.quit()
            except:
                pass
        
        self.drivers.clear()
        print("✅ تمام کروم‌ها بسته شدند")

def main():
    """تابع اصلی با منوی پیشرفته"""
    print("🎪 اسکریپت اسپم اسکای روم - نسخه توربو پرو")
    print("=" * 50)
    print("🔥 قابلیت‌های ویژه:")
    print("   ⚡ سرعت فوق‌العاده در ورود کاربران")
    print("   🎯 مدیریت هوشمند منابع سیستم")
    print("   📊 مانیتورینگ لحظه‌ای پیشرفت")
    print("   🔥 میم‌های فارسی منتخب")
    print("   💨 قابلیت توقف اضطراری")
    print("=" * 50)
    
    # نمایش گزینه‌های از پیش تعریف شده
    print("\n🎯 گزینه‌های سریع:")
    print("   1. تست سبک (5 کاربر)")
    print("   2. اسپم متوسط (20 کاربر)") 
    print("   3. اسپم سنگین (50 کاربر)")
    print("   4. اسپم فوق سنگین (100 کاربر)")
    print("   5. اسپم حمله‌ای (200 کاربر)")
    print("   6. تعداد دلخواه")
    
    bot = None
    
    try:
        choice = input("\n🎲 گزینه مورد نظر را انتخاب کنید (1-6): ").strip()
        
        if choice == "1":
            user_count = 5
        elif choice == "2":
            user_count = 20
        elif choice == "3":
            user_count = 50
        elif choice == "4":
            user_count = 100
        elif choice == "5":
            user_count = 200
        elif choice == "6":
            user_count = int(input("👥 تعداد کاربران مورد نظر: "))
        else:
            print("❌ گزینه نامعتبر! استفاده از حالت پیش‌فرض (5 کاربر)")
            user_count = 5
            
        if user_count <= 0:
            print("❌ تعداد باید بیشتر از ۰ باشد!")
            return
        
        # هشدار برای تعداد بالا
        if user_count > 100:
            print(f"\n⚠️  هشدار: تعداد {user_count} کاربر ممکن است به منابع سیستم فشار وارد کند!")
            print("   💡 توصیه: سیستم با حداقل 8GB RAM و اینترنت پرسرعت")
        
        # تأیید نهایی
        print(f"\n⚠️ آیا مطمئنید می‌خواهید {user_count} کاربر وارد کلاس شوند؟")
        confirm = input("✅ برای تأیید 'y' را وارد کنید، برای لغو هر کلید دیگر: ")
        
        if confirm.lower() != 'y':
            print("❌ عملیات لغو شد!")
            return
        
        # اجرای اسکریпتب
        bot = SkyRoomFarsiSpam()
        
        # مدیریت توقف با Ctrl+C
        try:
            bot.run_with_user_count(user_count)
        except KeyboardInterrupt:
            bot.stop()
            
        input("\n⏹️ برای بستن Enter بزنید...")
        
    except ValueError:
        print("❌ لطفاً یک عدد معتبر وارد کنید!")
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")
    finally:
        if bot:
            bot.close_all()

if __name__ == "__main__":
    main()
