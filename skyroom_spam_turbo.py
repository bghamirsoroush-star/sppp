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

# English names and messages
NAMES = [
    "John", "Mike", "Alex", "Sam", "Tom", "David", "Chris", "Ryan",
    "Bot1", "Bot2", "Bot3", "Bot4", "Bot5", "Bot6", "Bot7", "Bot8",
    "User1", "User2", "User3", "User4", "User5", "User6", "User7",
    "Test1", "Test2", "Test3", "Test4", "Test5", "Guest1", "Guest2"
]

SPAM_MESSAGES = [
    "Hello everyone!", "How are you?", "This is fun!",
    "Great class!", "Interesting topic!", "Thanks teacher!",
    "Can you repeat that?", "I have a question", "Well explained!",
    "Good point!", "I agree", "Nice presentation!",
    "Learning a lot!", "Keep going!", "Awesome!",
    "Thank you!", "Well done!", "Perfect!",
    "Amazing!", "Cool!", "Wow!", "Great job!",
    "I'm here!", "Listening!", "Watching!",
    "Good morning!", "Good afternoon!", "Hello teacher!"
]

class SkyRoomSpamBot:
    def __init__(self):
        self.drivers = []
        self.success_count = 0
        self.spam_count = 0
        self.lock = threading.Lock()
        self.active_threads = 0
        self.max_threads = 20
        self.start_time = None
        self.running = True
        self.skyroom_link = ""
        
    def setup_driver(self):
        """Setup Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        
        # Performance optimizations
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-plugins")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(20)
            self.drivers.append(driver)
            return driver
        except Exception as e:
            print(f"❌ Chrome driver error: {e}")
            return None

    def join_class(self, name, user_id, total_users):
        """Join SkyRoom class"""
        driver = self.setup_driver()
        if not driver:
            return
            
        try:
            print(f"🎯 User {user_id}/{total_users}: {name}")
            
            # Step 1: Go to SkyRoom link
            driver.get(self.skyroom_link)
            time.sleep(3)
            
            # Step 2: Click guest button
            guest_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn_guest"))
            )
            guest_btn.click()
            time.sleep(2)
            
            # Step 3: Enter name
            name_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.full-width[type='text']"))
            )
            name_field.clear()
            name_field.send_keys(name)
            time.sleep(1)
            
            # Step 4: Click confirm
            confirm_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'تأیید') or contains(text(), 'Confirm')]]"))
            )
            confirm_btn.click()
            time.sleep(3)
            
            print(f"✅ User {user_id}/{total_users} joined: {name}")
            with self.lock:
                self.success_count += 1
            
            # Start spamming
            self.start_spam(driver, name, user_id, total_users)
            
        except Exception as e:
            print(f"❌ Error with user {user_id}: {e}")
            try:
                driver.quit()
                if driver in self.drivers:
                    self.drivers.remove(driver)
            except:
                pass
        finally:
            with self.lock:
                self.active_threads -= 1

    def start_spam(self, driver, name, user_id, total_users):
        """Start spamming messages"""
        if not self.running:
            return
            
        print(f"🔥 User {user_id}/{total_users} started spamming!")
        
        session_count = 0
        max_sessions = random.randint(2, 4)
        
        while session_count < max_sessions and self.running:
            try:
                # Find chat element
                chat_element = self.find_chat_element(driver)
                if chat_element:
                    # Spam messages in this session
                    messages_count = random.randint(3, 8)
                    
                    for i in range(messages_count):
                        if not self.running:
                            break
                            
                        message = random.choice(SPAM_MESSAGES)
                        if self.send_message(driver, chat_element, message):
                            with self.lock:
                                self.spam_count += 1
                            
                            if self.spam_count % 10 == 0:
                                print(f"💬 Message {self.spam_count} sent")
                        
                        time.sleep(random.uniform(0.5, 1.5))
                    
                    session_count += 1
                    if self.running:
                        print(f"🎯 User {user_id} session {session_count} completed")
                
                # Break between sessions
                if self.running and session_count < max_sessions:
                    break_time = random.randint(5, 15)
                    print(f"⏳ User {user_id} waiting {break_time} seconds...")
                    time.sleep(break_time)
                
            except Exception as e:
                if self.running:
                    print(f"⚠️ Spam error user {user_id}: {e}")
                time.sleep(2)
        
        if self.running:
            print(f"🎊 User {user_id}/{total_users} finished spamming!")
        
        # Keep user in class
        self.keep_alive(driver, name, user_id, total_users)

    def find_chat_element(self, driver):
        """Find chat input field"""
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

    def send_message(self, driver, chat_element, message):
        """Send message to chat"""
        try:
            chat_element.click()
            time.sleep(0.2)
            
            # Clear content
            if chat_element.get_attribute('contenteditable') == 'true':
                driver.execute_script("arguments[0].innerHTML = '';", chat_element)
            else:
                chat_element.clear()
            
            # Send message
            chat_element.send_keys(message)
            time.sleep(0.2)
            chat_element.send_keys(Keys.ENTER)
            time.sleep(0.3)
            
            return True
        except:
            return False

    def keep_alive(self, driver, name, user_id, total_users):
        """Keep user in class"""
        counter = 0
        try:
            while self.running and counter < 60:  # Stay for 30 minutes max
                time.sleep(30)
                counter += 0.5
                if counter % 10 == 0 and self.running:
                    print(f"💚 User {user_id}/{total_users} online ({int(counter)} minutes)")
        except:
            pass
        finally:
            try:
                driver.quit()
                if driver in self.drivers:
                    self.drivers.remove(driver)
            except:
                pass

    def run_spam(self):
        """Main spam execution"""
        print("🚀 SkyRoom Spam Bot Started")
        print("=" * 50)
        
        # Get SkyRoom link
        self.skyroom_link = input("🔗 Enter SkyRoom link: ").strip()
        if not self.skyroom_link:
            print("❌ No link provided! Using default...")
            self.skyroom_link = "https://www.skyroom.online/ch/soroushamir/riazi101101"
        
        # Get number of users
        try:
            user_count = int(input("👥 Enter number of users: "))
            if user_count <= 0:
                print("❌ Number must be positive! Using 5 users...")
                user_count = 5
        except:
            print("❌ Invalid number! Using 5 users...")
            user_count = 5
        
        # Final confirmation
        print(f"\n⚠️  Start with {user_count} users?")
        confirm = input("✅ Confirm (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("❌ Operation cancelled!")
            return
        
        print(f"\n🎯 Starting spam with {user_count} users")
        print(f"🔗 Link: {self.skyroom_link}")
        print("👻 Headless mode: Active")
        print("⚡ Turbo mode: Active")
        print("=" * 50)
        
        self.start_time = time.time()
        self.running = True
        
        # Start monitoring
        monitor_thread = threading.Thread(target=self.progress_monitor, args=(user_count,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # Use ThreadPoolExecutor for efficient thread management
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                # Start all users quickly
                futures = []
                for i in range(user_count):
                    if not self.running:
                        break
                        
                    name = random.choice(NAMES)
                    future = executor.submit(self.quick_join, name, i+1, user_count)
                    futures.append(future)
                    time.sleep(0.3)  # Small delay between starting users
                
                # Wait for completion
                for future in concurrent.futures.as_completed(futures):
                    if not self.running:
                        break
                    future.result()
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user...")
            self.running = False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.running = False
        finally:
            self.running = False
            time.sleep(2)
            self.final_report(user_count)

    def quick_join(self, name, user_id, total_users):
        """Quick user join"""
        with self.lock:
            self.active_threads += 1
        self.join_class(name, user_id, total_users)

    def progress_monitor(self, user_count):
        """Monitor progress"""
        try:
            while self.running and (self.active_threads > 0 or time.time() - self.start_time < 30):
                elapsed = int(time.time() - self.start_time)
                
                if elapsed % 10 == 0:  # Report every 10 seconds
                    success_rate = (self.success_count / user_count) * 100 if user_count > 0 else 0
                    
                    print(f"\n📊 Progress Report ({elapsed} seconds):")
                    print(f"   ✅ Successful users: {self.success_count}/{user_count} ({success_rate:.1f}%)")
                    print(f"   💬 Messages sent: {self.spam_count}")
                    print(f"   🧵 Active users: {self.active_threads}")
                    if elapsed > 0:
                        print(f"   🚀 Messages per minute: {self.spam_count / (elapsed/60):.1f}")
                    print("-" * 40)
                
                time.sleep(10)
                
        except Exception as e:
            if self.running:
                print(f"⚠️ Monitor error: {e}")

    def final_report(self, user_count):
        """Final report"""
        total_time = int(time.time() - self.start_time)
        success_rate = (self.success_count / user_count) * 100 if user_count > 0 else 0
        messages_per_minute = self.spam_count / (total_time/60) if total_time > 0 else 0
        
        print("\n" + "=" * 50)
        print("🎊 Operation Complete!")
        print("=" * 50)
        print(f"📈 Final Results:")
        print(f"   👥 Requested users: {user_count}")
        print(f"   ✅ Successful users: {self.success_count} ({success_rate:.1f}%)")
        print(f"   💬 Total messages: {self.spam_count}")
        print(f"   ⏱️ Total time: {total_time} seconds")
        print(f"   🚀 Messages per minute: {messages_per_minute:.1f}")
        print("=" * 50)

    def stop(self):
        """Stop operation"""
        print("\n🛑 Stopping operation...")
        self.running = False
        self.close_all()

    def close_all(self):
        """Close all drivers"""
        print("\n🔒 Closing Chrome drivers...")
        self.running = False
        
        for driver in self.drivers[:]:
            try:
                driver.quit()
            except:
                pass
        
        self.drivers.clear()
        print("✅ All Chrome drivers closed")

def main():
    """Main function"""
    print("🎪 SkyRoom Spam Bot - English Version")
    print("=" * 40)
    print("🔥 Features:")
    print("   ⚡ Fast user joining")
    print("   🎯 Smart resource management")
    print("   📊 Real-time monitoring")
    print("   💨 Emergency stop capability")
    print("=" * 40)
    
    bot = None
    
    try:
        bot = SkyRoomSpamBot()
        bot.run_spam()
        
        input("\n⏹️ Press Enter to close...")
        
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if bot:
            bot.close_all()

if __name__ == "__main__":
    main()
