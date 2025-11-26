from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
import random

# میم‌های فوق سریع فارسی
FAST_FARSI_NAMES = [
    "۲۶", "۲۶۰", "۶۶۶", "۴۲۰", "۱۴", "۴۰", "۱۹", "۲۵", "۶۱", "۶۷", "۶۹",
    "سیکتیر", "داشاق", "علی", "پروین", "سگ", "خره", "گاو", "گاد", "نولایف",
    "کیر", "کص", "کونی", "حرومزاده", "بی‌ناموس", "بی‌غیرت", "پدرسوخته",
    "مادرجنده", "لاشی", "جنده", "فحش", "ننت", "بابات", "خواهرت", "برادرت"
]

FAST_FARSI_MESSAGES = [
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
    "جن‌زده بازی درنیار", "صیک پاک کن", "گول نخور", "کلاه بذار", "لاواط کن", "گیم بزن"
]

class SkyRoomTurboSpammer:
    def __init__(self):
        self.success_count = 0
        self.spam_count = 0
        self.lock = threading.Lock()
        self.active_threads = 0
        
    def setup_driver(self):
        """تنظیمات کروم سریع"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-images")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(20)
        return driver

    def join_and_spam(self, name, user_id, total_users):
        """ورود و اسپم برای یک کاربر"""
        driver = self.setup_driver()
        try:
            print(f"🎯 کاربر {user_id} از {total_users}: {name}")
            
            # ورود سریع
            driver.get("https://www.skyroom.online/ch/soroushamir/riazi101101")
            time.sleep(2)
            
            driver.find_element(By.ID, "btn_guest").click()
            time.sleep(1)
            
            name_field = driver.find_element(By.CSS_SELECTOR, "input.full-width[type='text']")
            name_field.send_keys(name)
            time.sleep(0.5)
            
            driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'تأیید')]]").click()
            time.sleep(2)
            
            print(f"✅ کاربر {user_id} وارد شد: {name}")
            with self.lock:
                self.success_count += 1
            
            # اسپم سریع
            self.quick_spam(driver, user_id, total_users)
            
        except Exception as e:
            print(f"❌ خطا در کاربر {user_id}: {e}")
        finally:
            try:
                driver.quit()
            except:
                pass
            with self.lock:
                self.active_threads -= 1

    def quick_spam(self, driver, user_id, total_users):
        """اسپم سریع"""
        print(f"🔥 کاربر {user_id} شروع اسپم کرد!")
        
        spam_count = 0
        max_messages = random.randint(10, 25)
        
        while spam_count < max_messages:
            try:
                # پیدا کردن فیلد چت
                elements = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true'], input[type='text'], textarea")
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        element.click()
                        message = random.choice(FAST_FARSI_MESSAGES)
                        
                        if element.get_attribute('contenteditable') == 'true':
                            element.clear()
                        else:
                            element.clear()
                        
                        element.send_keys(message)
                        element.send_keys(Keys.ENTER)
                        
                        with self.lock:
                            self.spam_count += 1
                            spam_count += 1
                        
                        print(f"💬 کاربر {user_id} پیام {self.spam_count}: {message}")
                        time.sleep(random.uniform(0.1, 0.5))
                        break
            except:
                pass
        
        print(f"🎊 کاربر {user_id} اسپم تمام کرد! ({spam_count} پیام)")

    def run_multi_user_attack(self, user_count):
        """اجرای حمله چند کاربره"""
        print("🚀 شروع حمله چند کاربره اسکای روم")
        print(f"🎯 تعداد کاربران: {user_count}")
        print("🔗 لینک: https://www.skyroom.online/ch/soroushamir/riazi101101")
        print("⚡ حالت توربو: فعال")
        print("=" * 50)
        
        start_time = time.time()
        
        threads = []
        for i in range(user_count):
            while self.active_threads >= 10:  # حداکثر 10 thread همزمان
                time.sleep(0.5)
            
            name = random.choice(FAST_FARSI_NAMES)
            thread = threading.Thread(target=self.join_and_spam, args=(name, i+1, user_count))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            
            with self.lock:
                self.active_threads += 1
            
            time.sleep(0.3)  # فاصله بین شروع کاربران
        
        # منتظر ماندن برای اتمام تمام threads
        for thread in threads:
            thread.join()
        
        # گزارش نهایی
        total_time = time.time() - start_time
        print("\n" + "=" * 50)
        print("🎊 عملیات کامل شد!")
        print("=" * 50)
        print(f"📊 نتایج نهایی:")
        print(f"   👥 کاربران درخواستی: {user_count}")
        print(f"   ✅ کاربران موفق: {self.success_count}")
        print(f"   💬 پیام‌های ارسالی: {self.spam_count}")
        print(f"   ⏱️ زمان کل: {total_time:.1f} ثانیه")
        print(f"   🚀 میانگین پیام در ثانیه: {self.spam_count/total_time:.1f}")
        print("=" * 50)

def main():
    """تابع اصلی"""
    print("🎪 اسکریپت اسپم اسکای روم - نسخه توربو")
    print("=" * 40)
    
    try:
        # دریافت تعداد کاربران
        user_count = int(input("👉 چند تا کاربر می‌خوای؟ "))
        
        if user_count <= 0:
            print("❌ تعداد باید بیشتر از صفر باشه!")
            return
        
        print(f"\n🔥 آماده حمله با {user_count} کاربر...")
        time.sleep(1)
        
        # اجرای اسکریپت
        bot = SkyRoomTurboSpammer()
        bot.run_multi_user_attack(user_count)
        
    except ValueError:
        print("❌ لطفاً یک عدد معتبر وارد کن!")
    except KeyboardInterrupt:
        print("\n🛑 توسط کاربر متوقف شد!")
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")

if __name__ == "__main__":
    main()
