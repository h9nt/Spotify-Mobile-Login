from uuid       import uuid4
from pyproto    import ProtoBuf # pip install python-protobuf (Thanks to @xtekky btw for the lib)
from requests   import post
from binascii   import hexlify


def get_cl_token() -> str:
    "Just for testing, not working idkkk"
    payload = {
        1: 1,
        2: {
            1: "9.0.14.561",
            2: "9a8d2f0ce77a4e248bb71fefcb557637",
            3: {
                1: {
                    1: {
                        1: {1: 720, 2: 1280, 3: 480, 4: 240, 5: 240},
                        2: 9,
                        3: 28,
                        4: "SM-G935F",
                        5: "SM-G935F",
                        6: "samsung",
                        7: "samsung",
                        8: 32,
                        9: "com.spotify.music/d6a6dced4a85f24204bf9505ccc1fce114cadb32/761e89f2-1f10-44b8-afc3-33d5fe9d9fb1",
                    }
                },
                2: "55f9bd0ec8e77641",
            },
        },
    }

    cl_v1 = post("https://clienttoken.spotify.com/v1/clienttoken", headers= {
        "Accept": "application/x-protobuf",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-protobuf",
        "Host": "clienttoken.spotify.com",
        "User-Agent": "Spotify/9.0.14.561 Android/28 (SM-G935F)"
    }, data=ProtoBuf(payload).toBuf())

    cl_first = ProtoBuf(cl_v1.content).getProtoBuf(3).getBytes(1).decode("utf-8")

    v2payload = {
        1: 2,
        3: {
            1: cl_first,
            2: {
                1: 3,
                4: {
                    1: "95601890AFE2DEF500000000000AD7EC"
                }
            }
        }
    }

    cl_final = post("https://clienttoken.spotify.com/v1/clienttoken", headers= {
        "Accept": "application/x-protobuf",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-protobuf",
        "Host": "clienttoken.spotify.com",
        "User-Agent": "Spotify/9.0.14.561 Android/28 (SM-G935F)"
    }, data=ProtoBuf(v2payload).toBuf())

    final = ProtoBuf(cl_final.content).getProtoBuf(2).getBytes(1).decode("utf-8") # if response empty, give out 400

    if not final:
        return None
    else:
        return {
            "cl_token": final
        }


def get_body(username: str, password: str) -> str:
    payload = {
        1: {1: "9a8d2f0ce77a4e248bb71fefcb557637", 2: "55f9bd0ec8e77641"},
        4: {
            2: {
                1: 1,
                2: "https://auth-callback.spotify.com/r/android/music/login",
                3: f"{str(uuid4())}",  # str(uuid4) / 73f8985a-8d04-4f04-902b-5902313b7475
                4: 1,
            },
            3: {1: "en"},
        },
        109: {
            1: f"{str(username.lower())}",  # username/email
            2: f"{str(password.lower())}",  # password
            3: ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",  # ???
        },
    }
    return ProtoBuf(payload).toBuf()

def get_captcha(response: bytes) -> str:
    try:
        return ProtoBuf(response).getProtoBuf(3).getProtoBuf(1).getProtoBuf(3).getProtoBuf(1).getBytes(1).decode("utf-8")
    except Exception:
        print("No Captcha response.")
        raise SystemExit


def raw_res(response: bytes) -> str:
    try:
        return ProtoBuf(response).getInt(2)
    except Exception:
        print("Error!")
        raise SystemExit
