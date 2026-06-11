import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class MovieTicketSystem:
    def __init__(self):
        self.current_user = None
        self.current_user_type = None
        self.login_attempts = {}
        # 数据文件
        self.users_file = "users.json"
        self.movies_file = "movies.json"
        self.orders_file = "orders.json"
        self.halls_file = "halls.json"
        self.reviews_file = "reviews.json"
        self.favorites_file = "favorites.json"
        # 加载所有数据
        self.load_users()
        self.load_halls()
        self.load_movies()
        self.load_orders()
        self.load_reviews()
        self.load_favorites()
    
    # ==================== 数据加载与保存 ====================
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        else:
            self.users = {
                "admin": {
                    "password": "admin123",
                    "email": "admin@example.com",
                    "phone": "13800000000",
                    "user_type": "admin",
                    "register_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            }
            self.save_users()
    
    def save_users(self):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def load_halls(self):
        if os.path.exists(self.halls_file):
            with open(self.halls_file, 'r', encoding='utf-8') as f:
                self.halls = json.load(f)
        else:
            # 预置影厅
            self.halls = {
                "hall_1": {"id": "hall_1", "name": "1号厅", "capacity": 100, "type": "标准厅"},
                "hall_2": {"id": "hall_2", "name": "2号厅", "capacity": 80, "type": "3D厅"},
                "hall_3": {"id": "hall_3", "name": "3号厅", "capacity": 60, "type": "VIP厅"}
            }
            self.save_halls()
    
    def save_halls(self):
        with open(self.halls_file, 'w', encoding='utf-8') as f:
            json.dump(self.halls, f, ensure_ascii=False, indent=2)
    
    def load_movies(self):
        if os.path.exists(self.movies_file):
            with open(self.movies_file, 'r', encoding='utf-8') as f:
                self.movies = json.load(f)
        else:
            # 预置电影数据，关联影厅ID
            self.movies = {
                "m001": {
                    "id": "m001",
                    "title": "阿凡达：水之道",
                    "genre": "科幻/动作",
                    "duration": 192,
                    "release_date": "2024-12-16",
                    "director": "詹姆斯·卡梅隆",
                    "description": "《阿凡达》续作，讲述杰克和奈蒂莉组建家庭后的故事。",
                    "poster": "avatar2.jpg",
                    "status": "上映中",
                    "sessions": [
                        {
                            "session_id": "s001",
                            "datetime": "2025-01-20 14:00:00",
                            "hall_id": "hall_1",
                            "price": 60,
                            "seats": self.init_seats(10, 10)
                        },
                        {
                            "session_id": "s002",
                            "datetime": "2025-01-20 19:30:00",
                            "hall_id": "hall_2",
                            "price": 65,
                            "seats": self.init_seats(10, 10)
                        }
                    ]
                },
                "m002": {
                    "id": "m002",
                    "title": "流浪地球3",
                    "genre": "科幻/灾难",
                    "duration": 165,
                    "release_date": "2025-01-28",
                    "director": "郭帆",
                    "description": "太阳即将毁灭，人类带着地球继续流浪。",
                    "poster": "wandering3.jpg",
                    "status": "即将上映",
                    "sessions": []
                },
                "m003": {
                    "id": "m003",
                    "title": "热辣滚烫",
                    "genre": "喜剧/剧情",
                    "duration": 129,
                    "release_date": "2024-02-10",
                    "director": "贾玲",
                    "description": "一个女孩通过拳击找到自我价值的故事。",
                    "poster": "hot.jpg",
                    "status": "上映中",
                    "sessions": [
                        {
                            "session_id": "s003",
                            "datetime": "2025-01-21 15:30:00",
                            "hall_id": "hall_3",
                            "price": 50,
                            "seats": self.init_seats(8, 8)
                        }
                    ]
                }
            }
            self.save_movies()
    
    def init_seats(self, rows: int, cols: int) -> List[List[str]]:
        return [['O' for _ in range(cols)] for _ in range(rows)]
    
    def save_movies(self):
        with open(self.movies_file, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)
    
    def load_orders(self):
        if os.path.exists(self.orders_file):
            with open(self.orders_file, 'r', encoding='utf-8') as f:
                self.orders = json.load(f)
        else:
            self.orders = []
            self.save_orders()
    
    def save_orders(self):
        with open(self.orders_file, 'w', encoding='utf-8') as f:
            json.dump(self.orders, f, ensure_ascii=False, indent=2)
    
    def load_reviews(self):
        if os.path.exists(self.reviews_file):
            with open(self.reviews_file, 'r', encoding='utf-8') as f:
                self.reviews = json.load(f)
        else:
            self.reviews = []
            self.save_reviews()
    
    def save_reviews(self):
        with open(self.reviews_file, 'w', encoding='utf-8') as f:
            json.dump(self.reviews, f, ensure_ascii=False, indent=2)
    
    def load_favorites(self):
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, 'r', encoding='utf-8') as f:
                self.favorites = json.load(f)
        else:
            self.favorites = {}
            self.save_favorites()
    
    def save_favorites(self):
        with open(self.favorites_file, 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=2)
    
    # ==================== 界面主流程（省略重复部分，仅显示改动） ====================
    def clear_screen(self):
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

    def show_main_menu(self):
        while True:
            self.clear_screen()
            print("\n" + "="*50)
            print("       🎬 欢迎使用电影订票管理系统")
            print("="*50)
            print("1. 🔐 登录")
            print("2. 📝 注册")
            print("3. 🚪 退出系统")
            print("="*50)
            choice = input("请选择操作 (1-3): ").strip()
            if choice == '1':
                if self.login():
                    self.ticket_booking_menu()
            elif choice == '2':
                self.register()
            elif choice == '3':
                print("\n✨ 感谢使用，再见！")
                break
            else:
                print("\n❌ 输入无效，请选择1-3之间的选项！")
                input("按回车键继续...")
    
    def login(self):
        self.clear_screen()
        print("\n" + "-"*50)
        print("          🔐 用户登录")
        print("-"*50)
        max_attempts = 3
        for attempt in range(max_attempts):
            username = input("\n请输入用户名: ").strip()
            if not username:
                print("❌ 用户名不能为空！")
                continue
            if username in self.login_attempts and self.login_attempts[username] >= 5:
                print(f"❌ 用户 {username} 已被锁定，请稍后再试！")
                return False
            password = input("请输入密码: ").strip()
            if username in self.users:
                if self.users[username]["password"] == password:
                    self.current_user = username
                    if username == "admin":
                        self.users[username]["user_type"] = "admin"
                        self.save_users()
                    self.current_user_type = self.users[username].get("user_type", "normal")
                    self.login_attempts[username] = 0
                    self.users[username]["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_users()
                    type_display = {"admin": "管理员", "vip": "VIP用户", "normal": "普通用户"}.get(self.current_user_type, "普通用户")
                    print(f"\n✅ 登录成功！")
                    print(f"👋 欢迎回来，{username}！")
                    print(f"🏷️  用户类型：{type_display}")
                    print(f"📅 上次登录：{self.users[username].get('last_login', '首次登录')}")
                    input("\n按回车键进入系统...")
                    return True
                else:
                    self.login_attempts[username] = self.login_attempts.get(username, 0) + 1
                    remaining = 5 - self.login_attempts[username]
                    if remaining > 0:
                        print(f"❌ 密码错误！还剩 {remaining} 次尝试机会")
                    else:
                        print(f"❌ 密码错误次数过多，用户 {username} 已被临时锁定！")
                    continue
            else:
                print(f"❌ 用户名 '{username}' 不存在！")
                if attempt < max_attempts - 1:
                    choice = input("\n是否立即注册？(y/n): ").strip().lower()
                    if choice == 'y':
                        self.register()
                        return False
        print("\n❌ 登录失败次数过多，请稍后再试！")
        input("按回车键返回主菜单...")
        return False
    
    def register(self):
        self.clear_screen()
        print("\n" + "-"*50)
        print("          📝 新用户注册")
        print("-"*50)
        while True:
            username = input("用户名 (3-20个字符): ").strip()
            if not username:
                print("❌ 用户名不能为空！")
                continue
            if username in self.users:
                print("❌ 用户名已存在！")
                continue
            if len(username) < 3 or len(username) > 20:
                print("❌ 用户名长度必须在3-20个字符之间！")
                continue
            if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', username):
                print("❌ 用户名只能包含字母、数字、下划线或中文！")
                continue
            
            print("\n请选择用户类型：")
            print("1. 普通用户")
            print("2. VIP用户")
            type_choice = input("请选择 (1-2): ").strip()
            user_type = "vip" if type_choice == '2' else "normal"
            type_name = "VIP用户" if user_type == "vip" else "普通用户"
            
            print("\n密码要求：6-20个字符，建议包含大小写字母、数字和特殊字符")
            password = input("请输入密码: ").strip()
            if len(password) < 6 or len(password) > 20:
                print("❌ 密码长度必须在6-20个字符之间！")
                continue
            confirm = input("请再次输入密码: ").strip()
            if password != confirm:
                print("❌ 两次输入的密码不一致！")
                continue
            
            email = input("电子邮箱 (可选): ").strip()
            if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                print("❌ 邮箱格式不正确！")
                continue
            phone = input("手机号码 (可选): ").strip()
            if phone and not re.match(r'^1[3-9]\d{9}$', phone):
                print("❌ 手机号码格式不正确！")
                continue
            
            self.users[username] = {
                "password": password,
                "email": email,
                "phone": phone,
                "user_type": user_type,
                "register_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.save_users()
            print("\n" + "="*50)
            print("✅ 注册成功！")
            print(f"🎉 欢迎 {username} 加入！")
            print(f"🏷️  用户类型：{type_name}")
            if user_type == "vip":
                print("✨ VIP用户可享受9折购票优惠！")
            print("="*50)
            choice = input("\n是否立即登录？(y/n): ").strip().lower()
            if choice == 'y':
                if self.login():        # 如果登录成功
                    self.ticket_booking_menu()   # 直接进入主菜单
                break
            else:
                break
    
    # ==================== 用户主菜单 ====================
    def ticket_booking_menu(self):
        while True:
            self.clear_screen()
            type_display = {"admin": "管理员", "vip": "VIP用户", "normal": "普通用户"}.get(self.current_user_type, "普通用户")
            print("\n" + "="*50)
            print(f"      🎬 电影订票系统 - {self.current_user} ({type_display})")
            print("="*50)
            print("1. 🎬 浏览电影列表")
            print("2. 🔍 搜索电影")
            print("3. 🎫 购买电影票")
            print("4. 📋 查看我的订单")
            print("5. ❌ 取消订单")
            print("6. 💬 电影评价")
            print("7. ⭐ 我的收藏")
            print("8. 👤 个人信息")
            print("9. 🚪 退出登录")
            if self.current_user_type == "vip":
                print("10. ✨ VIP专享优惠")
            if self.current_user_type == "admin":
                print("11. ⚙️ 管理员功能")
            print("="*50)
            choice = input("请选择操作: ").strip()
            if choice == '1':
                self.browse_movies()
            elif choice == '2':
                self.search_movies()
            elif choice == '3':
                self.purchase_ticket()
            elif choice == '4':
                self.view_orders()
            elif choice == '5':
                self.cancel_order()
            elif choice == '6':
                self.review_menu()
            elif choice == '7':
                self.favorite_menu()
            elif choice == '8':
                self.user_profile()
            elif choice == '9':
                print(f"\n👋 {self.current_user} 已退出登录")
                self.current_user = None
                self.current_user_type = None
                break
            elif choice == '10' and self.current_user_type == "vip":
                self.vip_benefits()
            elif choice == '11' and self.current_user_type == "admin":
                self.admin_menu()
            else:
                print("❌ 无效选择！")
                input("按回车键继续...")
    
    # ==================== 电影浏览 ====================
    def browse_movies(self, genre_filter=None):
        self.clear_screen()
        """浏览所有电影，可按类型筛选"""
        print("\n" + "="*50)
        if genre_filter:
            print(f"          🎬 {genre_filter}类型电影")
        else:
            print("          🎬 全部电影")
        print("="*50)
        # 获取所有电影
        movies_list = list(self.movies.values())
        if genre_filter:
            movies_list = [m for m in movies_list if genre_filter.lower() in m['genre'].lower()]
        # 分类显示
        showing = [m for m in movies_list if m.get("status") == "上映中" and m.get("sessions")]
        upcoming = [m for m in movies_list if m.get("status") == "即将上映"]
        print("\n【正在上映】")
        if showing:
            for m in showing:
                print(f"  [{m['id']}] {m['title']} | {m['genre']} | {m['duration']}分钟 | 导演：{m['director']}")
                print(f"      简介：{m['description'][:50]}...")
                for sess in m['sessions']:
                    hall_name = self.halls.get(sess['hall_id'], {}).get('name', sess['hall_id'])
                    dt = sess['datetime']
                    price = sess['price']
                    print(f"      场次：{dt} {hall_name} 票价：{price}元")
        else:
            print("  暂无上映电影")
        print("\n【即将上映】")
        if upcoming:
            for m in upcoming:
                print(f"  [{m['id']}] {m['title']} | {m['genre']} | {m['duration']}分钟 | 上映日期：{m['release_date']}")
        else:
            print("  暂无即将上映电影")
        # 提供按类型筛选的快捷方式
        if not genre_filter:
            print("\n提示：输入「类型」可筛选电影（如：科幻、喜剧）")
            cmd = input("按回车返回，或输入类型筛选: ").strip()
            if cmd:
                self.browse_movies(genre_filter=cmd)
            else:
                return
        else:
            input("\n按回车键继续...")
    
    def search_movies(self):
        self.clear_screen()
        """搜索电影"""
        print("\n" + "-"*40)
        print("          🔍 搜索电影")
        print("-"*40)
        keyword = input("请输入搜索关键词（片名、类型或导演）: ").strip()
        if not keyword:
            print("❌ 关键词不能为空")
            input("按回车键继续...")
            return
        results = []
        for m in self.movies.values():
            if (keyword.lower() in m['title'].lower() or 
                keyword.lower() in m['genre'].lower() or
                keyword.lower() in m['director'].lower()):
                results.append(m)
        if results:
            print(f"\n找到 {len(results)} 部相关电影：")
            for m in results:
                print(f"  [{m['id']}] {m['title']} | {m['genre']} | {m['status']}")
                if m['sessions']:
                    for sess in m['sessions']:
                        hall_name = self.halls.get(sess['hall_id'], {}).get('name', sess['hall_id'])
                        print(f"      场次：{sess['datetime']} {hall_name} 票价：{sess['price']}元")
        else:
            print("❌ 未找到相关电影")
        input("\n按回车键继续...")
    
    # ==================== 购票 ====================
    def purchase_ticket(self):
        self.clear_screen()
        print("\n" + "="*50)
        print("          🎫 购买电影票")
        print("="*50)
        showing = {mid: m for mid, m in self.movies.items() if m.get("status") == "上映中" and m.get("sessions")}
        if not showing:
            print("❌ 当前没有上映的电影，无法购票")
            input("按回车键继续...")
            return
        print("\n可购票的电影：")
        for mid, m in showing.items():
            print(f"  {mid} - {m['title']}")
        movie_id = input("\n请输入电影ID: ").strip()
        if movie_id not in showing:
            print("❌ 电影ID无效或暂无场次")
            input("按回车键继续...")
            return
        movie = showing[movie_id]
        sessions = movie['sessions']
        print(f"\n电影《{movie['title']}》场次：")
        for idx, sess in enumerate(sessions, 1):
            hall_name = self.halls.get(sess['hall_id'], {}).get('name', sess['hall_id'])
            dt = sess['datetime']
            price = sess['price']
            available = sum(row.count('O') for row in sess['seats'])
            print(f"  {idx}. {dt} | {hall_name} | 票价:{price}元 | 余座:{available}")
        choice = input("请选择场次(序号): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(sessions):
            print("❌ 无效选择")
            input("按回车键继续...")
            return
        session = sessions[int(choice)-1]
        session_id = session['session_id']
        # 座位选择
        print("\n座位图（O=可选，X=已售）：")
        seats = session['seats']
        rows = len(seats)
        cols = len(seats[0]) if rows > 0 else 0
        print("     " + " ".join([f"{i+1:2}" for i in range(cols)]))
        for i, row in enumerate(seats):
            row_label = chr(65+i)
            print(f"{row_label}   " + "  ".join(row))
        print("\n请输入座位号，如 A5 表示第A排第5座")
        seat_input = input("座位号: ").strip().upper()
        if len(seat_input) < 2:
            print("❌ 座位格式错误")
            input("按回车键继续...")
            return
        row_char = seat_input[0]
        col_str = seat_input[1:]
        if not col_str.isdigit():
            print("❌ 列号必须是数字")
            input("按回车键继续...")
            return
        row_idx = ord(row_char) - ord('A')
        col_idx = int(col_str) - 1
        if row_idx < 0 or row_idx >= rows or col_idx < 0 or col_idx >= cols:
            print("❌ 座位超出范围")
            input("按回车键继续...")
            return
        if seats[row_idx][col_idx] == 'X':
            print("❌ 该座位已被预订")
            input("按回车键继续...")
            return
        base_price = session['price']
        if self.current_user_type == "vip":
            final_price = base_price * 0.9
            print(f"\n✨ VIP用户享受9折优惠，原价{base_price}元 → 现价{final_price:.2f}元")
        else:
            final_price = base_price
            print(f"\n票价：{base_price}元")
        print(f"\n购票信息：")
        print(f"电影：{movie['title']}")
        print(f"场次：{session['datetime']} {self.halls.get(session['hall_id'], {}).get('name', session['hall_id'])}")
        print(f"座位：{seat_input}")
        print(f"实付金额：{final_price:.2f}元")
        confirm = input("\n确认购买？(y/n): ").strip().lower()
        if confirm != 'y':
            print("已取消购票")
            input("按回车键继续...")
            return
        seats[row_idx][col_idx] = 'X'
        self.save_movies()
        order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{len(self.orders)+1:04d}"
        order = {
            "order_id": order_id,
            "username": self.current_user,
            "user_type": self.current_user_type,
            "movie_id": movie_id,
            "movie_title": movie['title'],
            "session_id": session_id,
            "session_datetime": session['datetime'],
            "hall_id": session['hall_id'],
            "seat": seat_input,
            "original_price": base_price,
            "paid_price": final_price,
            "status": "已支付",
            "purchase_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cancel_deadline": (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        }
        self.orders.append(order)
        self.save_orders()
        print("\n✅ 购票成功！")
        print(f"订单号：{order_id}")
        input("按回车键继续...")
    
    # ==================== 订单管理 ====================
    def view_orders(self):
        self.clear_screen()
        user_orders = [o for o in self.orders if o['username'] == self.current_user]
        if not user_orders:
            print("\n📭 您还没有任何订单")
            input("按回车键继续...")
            return
        print("\n" + "="*60)
        print(f"            📋 我的订单 (共{len(user_orders)}笔)")
        print("="*60)
        for o in user_orders:
            status = o['status']
            status_emoji = "✅" if status == "已支付" else "❌"
            print(f"\n订单号：{o['order_id']} {status_emoji} {status}")
            print(f"电影：{o['movie_title']}")
            hall_name = self.halls.get(o.get('hall_id', ''), {}).get('name', o.get('hall', '未知影厅'))
            print(f"场次：{o['session_datetime']} {hall_name}")
            print(f"座位：{o['seat']}")
            print(f"原价：{o['original_price']}元 | 实付：{o['paid_price']:.2f}元")
            if o['status'] == "已支付":
                print(f"可取消截止时间：{o['cancel_deadline']}")
            print("-"*40)
        input("按回车键继续...")
    
    def cancel_order(self):
        # 更新座位的影厅关联
        self.clear_screen()
        print("\n" + "-"*40)
        print("          ❌ 取消订单")
        print("-"*40)
        active_orders = [o for o in self.orders if o['username'] == self.current_user and o['status'] == "已支付"]
        if not active_orders:
            print("没有可取消的订单")
            input("按回车键继续...")
            return
        print("\n您的有效订单：")
        for idx, o in enumerate(active_orders, 1):
            print(f"{idx}. 订单号：{o['order_id']} | {o['movie_title']} | {o['session_datetime']} | {o['seat']}")
        choice = input("请选择要取消的订单序号(输入0返回): ").strip()
        if choice == '0':
            return
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(active_orders):
            print("❌ 无效选择")
            input("按回车键继续...")
            return
        order = active_orders[int(choice)-1]
        session_time = datetime.strptime(order['session_datetime'], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        if session_time <= now:
            print("❌ 电影场次已经开始，无法取消订单")
            input("按回车键继续...")
            return
        if (session_time - now).total_seconds() / 60 < 30:
            print("❌ 距离电影开场不足30分钟，无法取消")
            input("按回车键继续...")
            return
        confirm = input(f"确认取消订单 {order['order_id']}？(y/n): ").strip().lower()
        if confirm != 'y':
            print("取消操作已终止")
            input("按回车键继续...")
            return
        # 释放座位
        movie = self.movies.get(order['movie_id'])
        if movie:
            for sess in movie['sessions']:
                if sess['session_id'] == order['session_id']:
                    seat = order['seat']
                    row_char = seat[0]
                    col_str = seat[1:]
                    row_idx = ord(row_char) - ord('A')
                    col_idx = int(col_str) - 1
                    if 0 <= row_idx < len(sess['seats']) and 0 <= col_idx < len(sess['seats'][0]):
                        sess['seats'][row_idx][col_idx] = 'O'
                    self.save_movies()
                    break
        order['status'] = "已取消"
        self.save_orders()
        print(f"✅ 订单 {order['order_id']} 已取消")
        input("按回车键继续...")
    
    # ==================== 新增：评价管理 ====================
    def review_menu(self):
        self.clear_screen()
        """评价功能菜单"""
        while True:
            self.clear_screen()
            print("\n" + "-"*40)
            print("          💬 电影评价")
            print("-"*40)
            print("1. 发表评价")
            print("2. 查看我的评价")
            print("3. 查看电影评价")
            print("4. 返回上级菜单")
            choice = input("请选择: ").strip()
            if choice == '1':
                self.add_review()
            elif choice == '2':
                self.view_my_reviews()
            elif choice == '3':
                self.view_movie_reviews()
            elif choice == '4':
                break
            else:
                print("无效选择")
    
    def add_review(self):
        self.clear_screen()
        """用户对已观看过的电影发表评价"""
        # 获取用户已购票且已观看（场次时间已过）的电影
        now = datetime.now()
        watched_movies = set()
        for order in self.orders:
            if order['username'] == self.current_user and order['status'] == "已支付":
                session_time = datetime.strptime(order['session_datetime'], "%Y-%m-%d %H:%M:%S")
                if session_time < now:
                    watched_movies.add(order['movie_id'])
        if not watched_movies:
            print("您还没有观看过任何电影，无法评价")
            input("按回车键继续...")
            return
        print("\n您已观看过的电影：")
        movie_list = []
        for mid in watched_movies:
            m = self.movies.get(mid)
            if m:
                movie_list.append(m)
                print(f"  {mid} - {m['title']}")
        movie_id = input("请选择要评价的电影ID: ").strip()
        if movie_id not in watched_movies:
            print("无效选择或未观看该电影")
            input("按回车键继续...")
            return
        # 检查是否已经评价过
        for r in self.reviews:
            if r['movie_id'] == movie_id and r['username'] == self.current_user:
                print("您已经评价过这部电影了")
                input("按回车键继续...")
                return
        rating = input("评分(1-5星，输入数字): ").strip()
        if not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            print("评分无效")
            input("按回车键继续...")
            return
        content = input("评价内容: ").strip()
        if not content:
            print("内容不能为空")
            input("按回车键继续...")
            return
        review = {
            "review_id": f"rev_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.reviews)+1}",
            "movie_id": movie_id,
            "movie_title": self.movies[movie_id]['title'],
            "username": self.current_user,
            "rating": int(rating),
            "content": content,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "replies": []  # 管理员回复列表
        }
        self.reviews.append(review)
        self.save_reviews()
        print("✅ 评价已提交")
        input("按回车键继续...")
    
    def view_my_reviews(self):
        self.clear_screen()
        my_reviews = [r for r in self.reviews if r['username'] == self.current_user]
        if not my_reviews:
            print("您还没有发表过评价")
            input("按回车键继续...")
            return
        print("\n我的评价：")
        for r in my_reviews:
            print(f"\n电影：{r['movie_title']} | 评分：{'★'*r['rating']}{'☆'*(5-r['rating'])} | 时间：{r['time']}")
            print(f"内容：{r['content']}")
            if r['replies']:
                print("管理员回复：")
                for rep in r['replies']:
                    print(f"  {rep['admin']}: {rep['content']} ({rep['time']})")
        input("按回车键继续...")
    
    def view_movie_reviews(self):
        self.clear_screen()
        """查看某部电影的所有评价（普通用户可见）"""
        movie_id = input("请输入电影ID查看评价: ").strip()
        if movie_id not in self.movies:
            print("电影不存在")
            input("按回车键继续...")
            return
        movie = self.movies[movie_id]
        reviews = [r for r in self.reviews if r['movie_id'] == movie_id]
        if not reviews:
            print(f"《{movie['title']}》暂无评价")
            input("按回车键继续...")
            return
        print(f"\n《{movie['title']}》观众评价：")
        for r in reviews:
            print(f"  {r['username']} | 评分：{'★'*r['rating']}{'☆'*(5-r['rating'])} | {r['time']}")
            print(f"  内容：{r['content']}")
            if r['replies']:
                print("  管理员回复：")
                for rep in r['replies']:
                    print(f"    {rep['admin']}: {rep['content']} ({rep['time']})")
        input("按回车键继续...")
    
    # ==================== 新增：收藏管理 ====================
    def favorite_menu(self):
        self.clear_screen()
        while True:
            self.clear_screen()
            print("\n" + "-"*40)
            print("          ⭐ 我的收藏")
            print("-"*40)
            print("1. 查看收藏列表")
            print("2. 添加收藏")
            print("3. 删除收藏")
            print("4. 返回上级菜单")
            choice = input("请选择: ").strip()
            if choice == '1':
                self.view_favorites()
            elif choice == '2':
                self.add_favorite()
            elif choice == '3':
                self.remove_favorite()
            elif choice == '4':
                break
            else:
                print("无效选择")
    
    def view_favorites(self):
        self.clear_screen()
        favs = self.favorites.get(self.current_user, [])
        if not favs:
            print("暂无收藏电影")
            input("按回车键继续...")
            return
        print("\n您的收藏：")
        for mid in favs:
            m = self.movies.get(mid)
            if m:
                print(f"  [{mid}] {m['title']} | {m['genre']} | {m['status']}")
                # 显示最近一场次信息
                if m['sessions']:
                    sess = m['sessions'][0]
                    hall_name = self.halls.get(sess['hall_id'], {}).get('name', sess['hall_id'])
                    print(f"      最近场次：{sess['datetime']} {hall_name} 票价{sess['price']}元")
        input("按回车键继续...")
    
    def add_favorite(self):
        self.clear_screen()
        movie_id = input("请输入要收藏的电影ID: ").strip()
        if movie_id not in self.movies:
            print("电影不存在")
            input("按回车键继续...")
            return
        if self.current_user not in self.favorites:
            self.favorites[self.current_user] = []
        if movie_id in self.favorites[self.current_user]:
            print("已经收藏过了")
        else:
            self.favorites[self.current_user].append(movie_id)
            self.save_favorites()
            print("✅ 已添加收藏")
        input("按回车键继续...")
    
    def remove_favorite(self):
        self.clear_screen()
        favs = self.favorites.get(self.current_user, [])
        if not favs:
            print("暂无收藏")
            input("按回车键继续...")
            return
        print("当前收藏：")
        for idx, mid in enumerate(favs, 1):
            m = self.movies.get(mid)
            if m:
                print(f"{idx}. {mid} - {m['title']}")
        choice = input("请输入要删除的序号(0返回): ").strip()
        if choice == '0':
            return
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(favs):
            print("无效选择")
        else:
            del self.favorites[self.current_user][int(choice)-1]
            self.save_favorites()
            print("✅ 已删除收藏")
        input("按回车键继续...")
    
    # ==================== 个人信息 ====================
    def user_profile(self):
        self.clear_screen()
        while True:
            self.clear_screen()
            user_info = self.users[self.current_user]
            type_display = {"admin": "管理员", "vip": "VIP用户", "normal": "普通用户"}.get(user_info.get("user_type", "normal"), "普通用户")
            print("\n" + "-"*50)
            print(f"          👤 {self.current_user} 的个人信息")
            print("-"*50)
            print(f"用户名：{self.current_user}")
            print(f"用户类型：{type_display}")
            print(f"密码：{'*' * len(user_info.get('password', ''))}")
            print(f"电子邮箱：{user_info.get('email', '未设置')}")
            print(f"手机号码：{user_info.get('phone', '未设置')}")
            print(f"注册时间：{user_info.get('register_time', '未知')}")
            print(f"上次登录：{user_info.get('last_login', '暂无')}")
            print("-"*50)
            print("1. 修改密码")
            print("2. 修改邮箱")
            print("3. 修改手机号")
            if self.current_user_type == "normal":
                print("4. 升级为VIP会员")
            print("5. 返回上级菜单")
            choice = input("请选择: ").strip()
            if choice == '1':
                self.change_password()
            elif choice == '2':
                self.change_email()
            elif choice == '3':
                self.change_phone()
            elif choice == '4' and self.current_user_type == "normal":
                self.upgrade_to_vip()
            elif choice == '5':
                break
            else:
                print("无效选择")
    
    def change_password(self):
        self.clear_screen()
        old = input("请输入原密码: ").strip()
        if self.users[self.current_user]["password"] != old:
            print("❌ 原密码错误")
            input("按回车键...")
            return
        new = input("请输入新密码(6-20字符): ").strip()
        if len(new) < 6 or len(new) > 20:
            print("❌ 密码长度错误")
            input("按回车键...")
            return
        confirm = input("请再次输入新密码: ").strip()
        if new != confirm:
            print("❌ 两次输入不一致")
            input("按回车键...")
            return
        self.users[self.current_user]["password"] = new
        self.save_users()
        print("✅ 密码修改成功")
        input("按回车键...")
    
    def change_email(self):
        self.clear_screen()
        new = input("请输入新邮箱: ").strip()
        if new and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', new):
            print("❌ 邮箱格式错误")
            input("按回车键...")
            return
        self.users[self.current_user]["email"] = new
        self.save_users()
        print("✅ 邮箱修改成功")
        input("按回车键...")
    
    def change_phone(self):
        self.clear_screen()
        new = input("请输入新手机号: ").strip()
        if new and not re.match(r'^1[3-9]\d{9}$', new):
            print("❌ 手机号格式错误")
            input("按回车键...")
            return
        self.users[self.current_user]["phone"] = new
        self.save_users()
        print("✅ 手机号修改成功")
        input("按回车键...")
    
    def upgrade_to_vip(self):
        self.clear_screen()
        confirm = input("升级VIP需支付98元/年（演示环境免费），是否确认？(y/n): ").strip().lower()
        if confirm == 'y':
            self.users[self.current_user]["user_type"] = "vip"
            self.current_user_type = "vip"
            self.save_users()
            print("✅ 恭喜您成为VIP会员！")
        else:
            print("升级取消")
        input("按回车键...")
    
    def vip_benefits(self):
        self.clear_screen()
        print("\n" + "="*50)
        print("          ✨ VIP专享优惠 ✨")
        print("="*50)
        print("1. 🎁 购票9折优惠")
        print("2. 💺 优先选座服务")
        print("3. 🍿 赠送小份爆米花（限每月一次）")
        print("4. 🎂 生日月双倍积分")
        print("5. 📱 专属客服通道")
        print("="*50)
        input("按回车键继续...")
    
    # ==================== 管理员功能（扩展） ====================
    def admin_menu(self):
        self.clear_screen()
        while True:
            self.clear_screen()
            print("\n" + "-"*50)
            print("          ⚙️ 管理员功能")
            print("-"*50)
            print("1. 用户管理")
            print("2. 影片信息管理")
            print("3. 影票价格管理")
            print("4. 影厅管理")
            print("5. 账单管理")
            print("6. 评价管理（回复/删除）")
            print("7. 返回上级菜单")
            choice = input("请选择: ").strip()
            if choice == '1':
                self.user_management()
            elif choice == '2':
                self.movie_management()
            elif choice == '3':
                self.price_management()
            elif choice == '4':
                self.hall_management()
            elif choice == '5':
                self.bill_management()
            elif choice == '6':
                self.admin_review_management()
            elif choice == '7':
                break
            else:
                print("无效选择")
    
    def user_management(self):
        self.clear_screen()
        while True:
            self.clear_screen()
            print("\n用户管理")
            print("1. 查看所有用户")
            print("2. 删除用户")
            print("3. 修改用户类型")
            print("4. 返回")
            sub = input("请选择: ").strip()
            if sub == '1':
                self.list_all_users()
            elif sub == '2':
                self.delete_user()
            elif sub == '3':
                self.change_user_type()
            elif sub == '4':
                break
            else:
                print("无效")
    
    def list_all_users(self):
        self.clear_screen()
        print("\n" + "="*80)
        print(f"{'用户名':<15} {'类型':<8} {'邮箱':<25} {'注册时间':<20}")
        print("="*80)
        for name, info in self.users.items():
            u_type = info.get('user_type', 'normal')
            type_cn = {'admin':'管理员','vip':'VIP','normal':'普通'}.get(u_type,'普通')
            email = info.get('email', '无')[:24]
            reg = info.get('register_time', '未知')[:19]
            print(f"{name:<15} {type_cn:<8} {email:<25} {reg:<20}")
        input("\n按回车键继续...")
    
    def delete_user(self):
        self.clear_screen()
        name = input("请输入要删除的用户名: ").strip()
        if name not in self.users:
            print("用户不存在")
        elif name == self.current_user:
            print("不能删除自己")
        elif name == "admin":
            print("不能删除默认管理员")
        else:
            del self.users[name]
            self.save_users()
            print(f"用户 {name} 已删除")
        input("按回车键...")
    
    def change_user_type(self):
        self.clear_screen()
        name = input("请输入用户名: ").strip()
        if name not in self.users:
            print("用户不存在")
            input("按回车键...")
            return
        current = self.users[name].get('user_type', 'normal')
        print(f"当前类型：{current}")
        print("可选类型：1.普通 2.VIP 3.管理员")
        opt = input("请选择(1-3): ").strip()
        new_type = {'1':'normal','2':'vip','3':'admin'}.get(opt)
        if not new_type:
            print("无效选择")
        else:
            self.users[name]['user_type'] = new_type
            self.save_users()
            print(f"已将 {name} 类型改为 {new_type}")
        input("按回车键...")
    
    # ==================== 影片信息管理 ====================
    def movie_management(self):
        self.clear_screen()
        while True:
            self.clear_screen()
            print("\n影片信息管理")
            print("1. 添加电影")
            print("2. 修改电影信息")
            print("3. 删除电影")
            print("4. 查找电影")
            print("5. 管理电影场次")
            print("6. 返回")
            sub = input("请选择: ").strip()
            if sub == '1':
                self.add_movie()
            elif sub == '2':
                self.modify_movie()
            elif sub == '3':
                self.delete_movie()
            elif sub == '4':
                self.search_movie_admin()
            elif sub == '5':
                self.manage_sessions()
            elif sub == '6':
                break
            else:
                print("无效")
    
    def add_movie(self):
        self.clear_screen()
        print("\n添加新电影")
        movie_id = input("电影ID (如 m004): ").strip()
        if movie_id in self.movies:
            print("电影ID已存在")
            input("按回车键...")
            return
        title = input("片名: ").strip()
        genre = input("类型(如 喜剧/动作): ").strip()
        duration = input("时长(分钟): ").strip()
        if not duration.isdigit():
            print("时长必须是数字")
            input("按回车键...")
            return
        release = input("上映日期(YYYY-MM-DD): ").strip()
        director = input("导演: ").strip()
        description = input("简介: ").strip()
        status = input("状态(上映中/即将上映): ").strip()
        self.movies[movie_id] = {
            "id": movie_id,
            "title": title,
            "genre": genre,
            "duration": int(duration),
            "release_date": release,
            "director": director,
            "description": description,
            "poster": "",
            "status": status,
            "sessions": []
        }
        self.save_movies()
        print("✅ 电影添加成功")
        # 可立即添加场次
        if input("是否立即添加场次？(y/n): ").strip().lower() == 'y':
            self.manage_sessions(movie_id)
        input("按回车键...")
    
    def modify_movie(self):
        self.clear_screen()
        movie_id = input("请输入要修改的电影ID: ").strip()
        if movie_id not in self.movies:
            print("电影不存在")
            input("按回车键...")
            return
        movie = self.movies[movie_id]
        print(f"当前信息：{movie}")
        print("留空表示不修改")
        new_title = input(f"片名({movie['title']}): ").strip()
        if new_title:
            movie['title'] = new_title
        new_genre = input(f"类型({movie['genre']}): ").strip()
        if new_genre:
            movie['genre'] = new_genre
        new_duration = input(f"时长({movie['duration']}): ").strip()
        if new_duration and new_duration.isdigit():
            movie['duration'] = int(new_duration)
        new_release = input(f"上映日期({movie['release_date']}): ").strip()
        if new_release:
            movie['release_date'] = new_release
        new_director = input(f"导演({movie['director']}): ").strip()
        if new_director:
            movie['director'] = new_director
        new_desc = input(f"简介({movie['description'][:30]}...): ").strip()
        if new_desc:
            movie['description'] = new_desc
        new_status = input(f"状态({movie['status']}): ").strip()
        if new_status:
            movie['status'] = new_status
        self.save_movies()
        print("✅ 电影信息已更新")
        input("按回车键...")
    
    def delete_movie(self):
        self.clear_screen()
        movie_id = input("请输入要删除的电影ID: ").strip()
        if movie_id not in self.movies:
            print("电影不存在")
        else:
            # 检查是否有订单关联
            related_orders = [o for o in self.orders if o['movie_id'] == movie_id]
            if related_orders:
                print("该电影已有订单记录，不能删除")
            else:
                del self.movies[movie_id]
                self.save_movies()
                print("✅ 电影已删除")
        input("按回车键...")
    
    def search_movie_admin(self):
        self.clear_screen()
        keyword = input("请输入搜索关键词(片名/导演/类型): ").strip()
        results = []
        for m in self.movies.values():
            if (keyword.lower() in m['title'].lower() or 
                keyword.lower() in m['director'].lower() or
                keyword.lower() in m['genre'].lower()):
                results.append(m)
        if results:
            print(f"找到 {len(results)} 部电影：")
            for m in results:
                print(f"  [{m['id']}] {m['title']} | {m['genre']} | {m['status']} | 导演：{m['director']}")
        else:
            print("未找到")
        input("按回车键...")
    
    def manage_sessions(self, specific_movie_id=None):
        self.clear_screen()
        if specific_movie_id:
            movie_id = specific_movie_id
        else:
            print("\n可选电影：")
            for mid, m in self.movies.items():
                print(f"{mid} - {m['title']}")
            movie_id = input("请输入电影ID: ").strip()
        if movie_id not in self.movies:
            print("电影不存在")
            input("按回车键...")
            return
        movie = self.movies[movie_id]
        print(f"\n电影《{movie['title']}》当前场次：")
        for idx, s in enumerate(movie['sessions'], 1):
            hall_name = self.halls.get(s['hall_id'], {}).get('name', s['hall_id'])
            print(f"{idx}. {s['datetime']} {hall_name} 票价{s['price']}元")
        print("\n1. 添加场次  2. 删除场次  3. 返回")
        act = input("请选择: ").strip()
        if act == '1':
            # 先列出影厅
            print("可用影厅：")
            for hid, h in self.halls.items():
                print(f"{hid} - {h['name']} (容量{h['capacity']})")
            hall_id = input("请选择影厅ID: ").strip()
            if hall_id not in self.halls:
                print("影厅不存在")
                input("按回车键...")
                return
            dt = input("场次时间(YYYY-MM-DD HH:MM:SS): ").strip()
            price = input("票价(数字): ").strip()
            if not price.replace('.','').isdigit():
                print("票价格式错误")
                input("按回车键...")
                return
            price = float(price)
            session_id = f"s{datetime.now().strftime('%Y%m%d%H%M%S')}"
            # 根据影厅容量动态生成座位（假设行数=ceil(capacity/10)，列数=10）
            capacity = self.halls[hall_id]['capacity']
            rows = (capacity + 9) // 10
            cols = 10
            seats = self.init_seats(rows, cols)
            movie['sessions'].append({
                "session_id": session_id,
                "datetime": dt,
                "hall_id": hall_id,
                "price": price,
                "seats": seats
            })
            self.save_movies()
            print("✅ 场次添加成功")
        elif act == '2':
            if not movie['sessions']:
                print("没有场次可删除")
            else:
                idx = input("请输入要删除的场次序号: ").strip()
                if idx.isdigit() and 1 <= int(idx) <= len(movie['sessions']):
                    # 检查是否有订单
                    sess_id = movie['sessions'][int(idx)-1]['session_id']
                    related = [o for o in self.orders if o.get('session_id') == sess_id]
                    if related:
                        print("该场次已有订单，不能删除")
                    else:
                        del movie['sessions'][int(idx)-1]
                        self.save_movies()
                        print("✅ 场次已删除")
                else:
                    print("无效序号")
        input("按回车键...")
    
    # ==================== 影票价格管理 ====================
    def price_management(self):
        self.clear_screen()
        print("\n影票价格管理")
        movie_id = input("请输入电影ID: ").strip()
        if movie_id not in self.movies:
            print("电影不存在")
            input("按回车键...")
            return
        movie = self.movies[movie_id]
        if not movie['sessions']:
            print("该电影没有场次")
            input("按回车键...")
            return
        print(f"\n电影《{movie['title']}》场次：")
        for idx, sess in enumerate(movie['sessions'], 1):
            hall_name = self.halls.get(sess['hall_id'], {}).get('name', sess['hall_id'])
            print(f"{idx}. {sess['datetime']} {hall_name} 当前票价：{sess['price']}元")
        choice = input("请选择要调整价格的场次序号: ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(movie['sessions']):
            print("无效选择")
            input("按回车键...")
            return
        sess = movie['sessions'][int(choice)-1]
        new_price = input(f"请输入新价格（当前{sess['price']}元）: ").strip()
        if not new_price.replace('.','').isdigit():
            print("价格必须是数字")
        else:
            sess['price'] = float(new_price)
            self.save_movies()
            print("✅ 票价已更新")
        input("按回车键...")
    
    # ==================== 影厅管理 ====================
    def hall_management(self):
        self.clear_screen()
        while True:
            self.clear_screen()
            print("\n影厅管理")
            print("1. 查看所有影厅")
            print("2. 添加影厅")
            print("3. 修改影厅信息")
            print("4. 删除影厅")
            print("5. 返回")
            sub = input("请选择: ").strip()
            if sub == '1':
                self.list_halls()
            elif sub == '2':
                self.add_hall()
            elif sub == '3':
                self.modify_hall()
            elif sub == '4':
                self.delete_hall()
            elif sub == '5':
                break
            else:
                print("无效")
    
    def list_halls(self):
        self.clear_screen()
        print("\n" + "="*60)
        print(f"{'ID':<10} {'名称':<10} {'容量':<8} {'类型':<10}")
        print("="*60)
        for hid, h in self.halls.items():
            print(f"{hid:<10} {h['name']:<10} {h['capacity']:<8} {h['type']:<10}")
        input("按回车键继续...")
    
    def add_hall(self):
        self.clear_screen()
        hid = input("影厅ID (如 hall_4): ").strip()
        if hid in self.halls:
            print("ID已存在")
            input("按回车键...")
            return
        name = input("影厅名称: ").strip()
        capacity = input("座位容量: ").strip()
        if not capacity.isdigit():
            print("容量必须是数字")
            input("按回车键...")
            return
        htype = input("影厅类型(如 标准厅/3D厅/VIP厅): ").strip()
        self.halls[hid] = {"id": hid, "name": name, "capacity": int(capacity), "type": htype}
        self.save_halls()
        print("✅ 影厅添加成功")
        input("按回车键...")
    
    def modify_hall(self):
        self.clear_screen()
        hid = input("请输入要修改的影厅ID: ").strip()
        if hid not in self.halls:
            print("影厅不存在")
            input("按回车键...")
            return
        hall = self.halls[hid]
        print(f"当前信息：{hall}")
        new_name = input(f"名称({hall['name']}): ").strip()
        if new_name:
            hall['name'] = new_name
        new_cap = input(f"容量({hall['capacity']}): ").strip()
        if new_cap and new_cap.isdigit():
            hall['capacity'] = int(new_cap)
        new_type = input(f"类型({hall['type']}): ").strip()
        if new_type:
            hall['type'] = new_type
        self.save_halls()
        print("✅ 影厅信息已更新")
        input("按回车键...")
    
    def delete_hall(self):
        self.clear_screen()
        hid = input("请输入要删除的影厅ID: ").strip()
        if hid not in self.halls:
            print("影厅不存在")
        else:
            # 检查是否有电影场次使用该影厅
            used = False
            for m in self.movies.values():
                for sess in m['sessions']:
                    if sess['hall_id'] == hid:
                        used = True
                        break
                if used:
                    break
            if used:
                print("该影厅有场次在使用，不能删除")
            else:
                del self.halls[hid]
                self.save_halls()
                print("✅ 影厅已删除")
        input("按回车键...")
    
    # ==================== 账单管理 ====================
    def bill_management(self):
        self.clear_screen()
        while True:
            self.clear_screen()
            print("\n账单管理")
            print("1. 影片收款统计")
            print("2. 客户往来款项查询")
            print("3. 实时票房统计")
            print("4. 返回")
            sub = input("请选择: ").strip()
            if sub == '1':
                self.movie_revenue()
            elif sub == '2':
                self.user_transactions()
            elif sub == '3':
                self.box_office()
            elif sub == '4':
                break
            else:
                print("无效")
    
    def movie_revenue(self):
        self.clear_screen()
        """统计每部影片的收款总额"""
        revenue = {}
        for order in self.orders:
            if order['status'] == "已支付":
                mid = order['movie_id']
                revenue[mid] = revenue.get(mid, 0) + order['paid_price']
        print("\n影片收款统计：")
        print(f"{'电影ID':<10} {'片名':<20} {'总收款(元)':<12}")
        print("-"*50)
        for mid, total in revenue.items():
            title = self.movies.get(mid, {}).get('title', '未知')
            print(f"{mid:<10} {title:<20} {total:<12.2f}")
        input("按回车键继续...")
    
    def user_transactions(self):
        self.clear_screen()
        """查询客户往来款项（每个用户的购票总额）"""
        user_total = {}
        for order in self.orders:
            if order['status'] == "已支付":
                uname = order['username']
                user_total[uname] = user_total.get(uname, 0) + order['paid_price']
        print("\n客户往来款项：")
        print(f"{'用户名':<15} {'消费总额(元)':<12}")
        print("-"*30)
        for uname, total in user_total.items():
            print(f"{uname:<15} {total:<12.2f}")
        input("按回车键继续...")
    
    def box_office(self):
        self.clear_screen()
        """实时票房统计（每部影片已支付订单总额）"""
        revenue = {}
        for order in self.orders:
            if order['status'] == "已支付":
                mid = order['movie_id']
                revenue[mid] = revenue.get(mid, 0) + order['paid_price']
        print("\n实时票房统计（单位：元）：")
        sorted_rev = sorted(revenue.items(), key=lambda x: x[1], reverse=True)
        for mid, total in sorted_rev:
            title = self.movies.get(mid, {}).get('title', '未知')
            print(f"{title:<20} 票房：{total:.2f} 元")
        if not sorted_rev:
            print("暂无票房数据")
        input("按回车键继续...")
    
    # ==================== 管理员评价管理 ====================
    def admin_review_management(self):
        self.clear_screen()
        """管理员回复或删除评价"""
        while True:
            self.clear_screen()
            print("\n评价管理")
            print("1. 查看所有评价")
            print("2. 回复评价")
            print("3. 删除评价")
            print("4. 返回")
            sub = input("请选择: ").strip()
            if sub == '1':
                self.list_all_reviews()
            elif sub == '2':
                self.reply_review()
            elif sub == '3':
                self.delete_review_admin()
            elif sub == '4':
                break
            else:
                print("无效")
    
    def list_all_reviews(self):
        self.clear_screen()
        if not self.reviews:
            print("暂无评价")
            input("按回车键...")
            return
        print("\n所有评价：")
        for r in self.reviews:
            print(f"\n评价ID: {r['review_id']} | 电影：{r['movie_title']} | 用户：{r['username']}")
            print(f"评分：{'★'*r['rating']}{'☆'*(5-r['rating'])} | 时间：{r['time']}")
            print(f"内容：{r['content']}")
            if r['replies']:
                print("已有回复：")
                for rep in r['replies']:
                    print(f"  {rep['admin']}: {rep['content']} ({rep['time']})")
        input("按回车键继续...")
    
    def reply_review(self):
        self.clear_screen()
        review_id = input("请输入要回复的评价ID: ").strip()
        review = None
        for r in self.reviews:
            if r['review_id'] == review_id:
                review = r
                break
        if not review:
            print("评价不存在")
            input("按回车键...")
            return
        print(f"正在回复 {review['username']} 对《{review['movie_title']}》的评价：{review['content']}")
        reply_content = input("请输入回复内容: ").strip()
        if not reply_content:
            print("回复内容不能为空")
            input("按回车键...")
            return
        reply = {
            "admin": self.current_user,
            "content": reply_content,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        review['replies'].append(reply)
        self.save_reviews()
        print("✅ 回复已添加")
        input("按回车键...")
    
    def delete_review_admin(self):
        self.clear_screen()
        review_id = input("请输入要删除的评价ID: ").strip()
        for i, r in enumerate(self.reviews):
            if r['review_id'] == review_id:
                del self.reviews[i]
                self.save_reviews()
                print("✅ 评价已删除")
                input("按回车键...")
                return
        print("评价不存在")
        input("按回车键...")

# ==================== 启动程序 ====================
if __name__ == "__main__":
    system = MovieTicketSystem()
    system.show_main_menu()