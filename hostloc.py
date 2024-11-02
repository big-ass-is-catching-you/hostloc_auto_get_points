import requests
import time
import re
from datetime import date
username = ''  # 论坛账户
password = ''  # 论坛密码
login_url = "https://hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes"
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
# 登录请求
request = requests.post(login_url, data={"username": username, 'password': password}, headers = user_agent)
print(f"{date.today()} 登录状态码: {request.status_code}")  # 打印登录状态码
# 检查登录是否成功
if request.status_code != 200:
    print("登录请求失败，请检查用户名和密码。")
    exit()

# 获取用户积分中心
user_info = requests.get('https://hostloc.com/home.php?mod=spacecp&ac=credit', headers = user_agent, cookies=request.cookies).text
# 打印返回的 HTML 以调试
#print(user_info)

# 尝试获取金钱信息
match = re.search(r'金钱: </em>(\d+).+?</li>', user_info)
if match:
    Current_money = match.group(1)
    print(f"用户 {username}, 你的金钱为 {Current_money}")
else:
    print("未找到金钱信息，请检查网页结构。")
    exit()

# 正题，刷积分
for i in range(20359, 20390):
    request1 = requests.get(f'https://hostloc.com/space-uid-{i}.html', headers = user_agent, cookies=request.cookies)
    user_title = re.search(r'<title>(.+?)全球主机交流论坛', request1.text)
    
    if user_title:
        print(user_title.group(1))  # 获取访问的空间标题
    else:
        print(f"未找到用户 {i} 的空间标题。")

    time.sleep(6)  # 可选的延时
    new_money_info = requests.get('https://hostloc.com/home.php?mod=spacecp&ac=credit', headers = user_agent, cookies=request.cookies).text
    new_money_match = re.search(r'金钱: </em>(\d+).+?</li>', new_money_info)
    
    if new_money_match:
        new_money = new_money_match.group(1)
        print(f"金钱为 {new_money}")
    else:
        print("未找到更新后的金钱信息。")
