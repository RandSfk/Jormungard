import requests, re, random, datetime, time, uuid, os
from fake_useragent import UserAgent
from requests.api import head
from faker import Faker
from rich import print
from rich.panel import Panel as pn
cp = 0
ok = 0
temp_mail = ""

no = 0

ua = UserAgent()
def ugenX():
    ualist = [ua.random for _ in range(50)]
    return str(random.choice(ualist))

req = requests.Session()
fake = Faker()


DefaultUAWindows   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
HeadersGetWindows  = lambda i=DefaultUAWindows : {'Host':'www.facebook.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9, id-ID,id;q=0.8','Cache-Control':'max-age=0','Dpr':'2','Pragma':'akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-get-request-id,akamai-x-get-nonces,akamai-x-get-client-ip,akamai-x-feo-trace','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not_A Brand";v="8", "Chromium";v="120"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Ch-Ua-Model':'','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','Priority':'u=0, i','User-Agent':ugenX()}
HeadersPostWindows = lambda i=DefaultUAWindows : {'Host':'www.facebook.com','Accept':'*/*','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9, id-ID,id;q=0.8','Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.facebook.com','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not_A Brand";v="8", "Chromium";v="120"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Ch-Ua-Model':'','Sec-Fetch-Site':'same-origin','User-Agent':ugenX()}

DefaultUAAndroid   = 'Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SQ3A.220705.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/407.0.0.0.65;]'
HeadersGetAndroid  = lambda i=DefaultUAAndroid : {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Cache-Control':'max-age=0','Dpr':'2','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?1','Sec-Ch-Ua-Model':'','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'none','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':i}
HeadersPostAndroid = lambda i=DefaultUAAndroid : {'Host':'m.facebook.com','Accept':'*/*','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9, id-ID,id;q=0.8','Content-Type':'application/x-www-form-urlencoded','Origin':'https://m.facebook.com','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not_A Brand";v="8", "Chromium";v="120"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'"Android"','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Ch-Ua-Model':'','Sec-Fetch-Site':'same-origin','User-Agent':i}




def GetEmail():
    global temp_mail
    ses = requests.Session()
    data = {
        "min_name_length": 10,
        "max_name_length": 10
    }
    pos = ses.post("https://api.internal.temp-mail.io/api/v3/email/new", data=data)
    email = pos.json()["email"]
    temp_mail = email
    return email

def GetCode(email):
    ses = requests.Session()
    pos = ses.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages")
    otp = re.search(r'"subject":"(\d{5}) is your confirmation code"', pos.text)
    if otp == None:
        return False
    return otp.group(1)

def confirm_id(mail, otp, data, uid):
    try:
        url = "https://m.facebook.com/confirmation_cliff/"
        params = {
        'contact': mail,
        'type': "submit",
        'is_soft_cliff': "false",
        'medium': "email",
        'code': otp}
        payload = {
        'fb_dtsg': 'NAcMC2x5X2VrJ7jhipS0eIpYv1zLRrDsb5y2wzau2bw3ipw88fbS_9A:0:0',
        'jazoest': re.search(r'"\d+"', data).group().strip('"'),
        'lsd': re.search(r'"LSD",\[\],{"token":"([^"]+)"}',str(data)).group(1),
        '__dyn': "",
        '__csr': "",
        '__req': "4",
        '__fmt': "1",
        '__a': "",
        '__user': uid}
        headers = {
        'User-Agent': "",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua-full-version-list': "",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Android WebView\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        'sec-ch-ua-model': "\"\"",
        'sec-ch-ua-mobile': "?1",
        'x-asbd-id': "129477",
        'x-fb-lsd': "KnpjLz-YdSXR3zBqds98cK",
        'sec-ch-prefers-color-scheme': "light",
        'sec-ch-ua-platform-version': "\"\"",
        'origin': "https://m.facebook.com",
        'x-requested-with': "mark.via.gp",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://m.facebook.com/confirmemail.php?next=https%3A%2F%2Fm.facebook.com%2F%3Fdeoia%3D1&soft=hjk",
        'accept-language': "en-GB,en-US;q=0.9,en;q=0.8",
        'priority': "u=1, i"}
        response = req.post(url, params=params, data=payload, headers=headers)
        if response.status_code == 200:
            print("Confirmed")
    except Exception as e:
        print(e)

def scrap_data(idf, pw, uid):
    global ok, cp
    requ = req.get("https://touch.alpha.facebook.com/login.php?")
    with open("dump.txt", "w") as file:
        file.write(requ.text)
    koki = (";").join([ "%s=%s" % (key, value) for key, value in requ.cookies.get_dict().items() ])
    if requ.status_code == 200:
        rr = random.randint
        headers = {
                'authority': 'touch.alpha.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'dpr': '1.600000023841858',
                'origin': 'https://touch.alpha.facebook.com',
                'referer': 'https://touch.alpha.facebook.com/',
                'accept-encoding': 'br, gzip',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': f'"Not.A/Brand";v="{str(rr(8,20))}", "Chromium";v="{str(rr(40,114))}", "Google Chrome";v="{str(rr(40,114))}"',
                'sec-ch-ua-full-version-list': f'"Not.A/Brand";v="{str(rr(8,20))}.0.0.0", "Chromium";v="{str(rr(40,114))}.0.{str(rr(2000,5999))}.{str(rr(10,399))}", "Google Chrome";v="{str(rr(40,114))}.0.{str(rr(2000,5999))}.{str(rr(10,399))}"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Linux"',
                'sec-ch-ua-platform-version': '""',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': ugenX(),
                'viewport-width': '980'
            }
        data = {
                'jazoest': re.search('name="jazoest" value="(.*?)"', str(requ.text)).group(1),
                'lsd': re.search('name="lsd" value="(.*?)"', str(requ.text)).group(1),
                'm_ts': re.search('name="m_ts" value="(.*?)"', str(requ.text)).group(1),
                'li': re.search('name="li" value="(.*?)"', str(requ.text)).group(1),
                'email': idf,
                'pass': pw,
                'next': ''
            }
        pos = req.post(random.choice(['https://www.facebook.com/login/device-based/regular/login/', 'https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110', 'https://www.facebook.com/login/?privacy_mutation_token=eyJ0eXBlIjowLCJjcmVhdGlvbl90aW1lIjoxNzM1NzQxNzE0LCJjYWxsc2l0ZV9pZCI6MzgxMjI5MDc5NTc1OTQ2fQ%3D%3D&next']), data=data, headers=headers, allow_redirects=False)
        if pos.status_code == 200:
            if "checkpoint" in pos.cookies.get_dict():
                print("[!] Akun Checkpoint")
                cp+=1
            else:
                print("[!] Akun Tidak Checkpoint")
                ok+=1
                print("Menunggu OTP")
                time.sleep(10)
                print("Mengirim OTP")
                otp = GetCode(temp_mail)
                user_id = uid
                confirm_id(temp_mail, otp, data, user_id)
        else:
            pass
    else:
        pass

def create():
    global no
    url = 'http://api.tuberboy.com/fb/reg'
    gend = random.randint(1, 2)
    data = {
        'name': fake.name_male() if gend == 2 else fake.name_female(), 
        'email': GetEmail(),
        'password': "rivalganteng",
        'gender': gend,
    }
    print(pn(f"Nama: {data['name']}\nEmail: {data['email']}\nPassword: {data['password']}\nGender: {'Pria' if data['gender'] == 2 else 'Wanita'}", title="[!] Membuat Akun Baru"))
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        try:
            result = response.json()
            if result['status']:
                print("Account created successfully:", result['message'])
                time.sleep(1)
                print(result)
                return {'e':result['email'], 'p':result['password'], 'u':result['user_id']}
            else:
                no+=1
                print(f'{result['message']}-+-{str(no)}')
                time.sleep(2)
                create()

        except ValueError:
            print("Response is not in JSON format:", response.text)
    else:
        print(f"Error {response.status_code}: {response.text}")
        
buat = create()
print(buat)
if buat:
    scrap_data(buat['e'], buat['p'], buat['u'])
