from requests   import post
from utils.body import get_body, get_captcha, raw_res
from colorama   import init
from os         import system

init(autoreset=True)
system('cls')

username = input("\n Username >>> ")
password = input("\n Password >>> ")

url = "https://login5.spotify.com/v4/login"

headers = {
    "client-token": "AACSi2Ydr2091VRyM2HyLyGnMSrACJPVAtKLPftGWGTOn8DrRrTuYiA/JpEVap3JtGkiqyGoo/FEcVJ3mDmKUnQK6cthMsORJngYcPWXfeviup/GV2eIZspqIv4tA3VzXW1xLicyw3+Iij147bX5vfdJRb20Qhp22RU17s/SANxeJ/6rhRHqspOPThEZ+JwrtdHPeRP7U3ZnhqzJ5c06yeKJwkwV7ugtc+KD+Cjd4K22gSwSQVC1BYQW8kiLXKuKP89jBV55lNEJDf9k3F/jhPscuheD3h80QG4mRNzWIwg+fA9UCHxmRnh+WLgb5J7HxaUC8zu7ZeY9EfvM8jSTptFe/hNkrWzkYreo7ZgrnohR25jyOcIMMZtn2SfB8O+g",
    "Connection": "Keep-Alive",
    "Content-Type": "application/x-protobuf",
    "Host": "login5.spotify.com",
    "User-Agent": "Spotify/9.0.14.561 Android/28 (SM-G935F)",
    "X-Retry-Count": "0",
}

response = post(url, headers=headers, data=get_body(username, password))

is_captcha = get_captcha(response.content)
pw_false = raw_res(response.content)

if is_captcha:
    res = {
        "status": False,
        "message": "Captcha detected!",
        "captcha_url": f"{is_captcha}"
    }
    print(res)
elif pw_false:
    res = {
        "status": False,
        "message": "Password or username wrong"
    }
    print(res)
else:
    print("IDK No response or soemthing")
