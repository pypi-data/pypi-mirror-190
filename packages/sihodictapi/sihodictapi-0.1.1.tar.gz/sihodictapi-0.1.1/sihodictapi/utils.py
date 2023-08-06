import hashlib
import winreg

import requests

REG_KEY_INTERNET_SETTINGS = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,
                                             r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                             0, winreg.KEY_ALL_ACCESS)


def is_open_proxy() -> bool:
    """判断是否开启了代理"""
    try:
        if winreg.QueryValueEx(REG_KEY_INTERNET_SETTINGS, 'ProxyEnable')[0] == 1:
            return True
    except FileNotFoundError as err:
        print('没有找到代理信息：' + str(err))
    except Exception as err:
        print('有其他报错：' + str(err))
    return False


def get_proxy_url() -> str:
    """获取代理配置的url"""
    if is_open_proxy():
        try:
            return winreg.QueryValueEx(REG_KEY_INTERNET_SETTINGS, 'ProxyServer')[0]
        except FileNotFoundError as err:
            print('没有找到代理信息：' + str(err))
        except Exception as err:
            print('有其他报错：' + str(err))
    else:
        print('系统没有开启代理')
    return ''


def get_proxies():
    # if not is_open_proxy():
    #     return None
    # url = get_proxy_url()
    # return {'https': url} if url else None
    return {
        "http": None,
        "https": None,
    }


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


def request_get(url, params=None):
    return requests.get(url, params, headers=headers, proxies=get_proxies(), timeout=(5, 5))


def request_post(url, data=None, json=None):
    return requests.post(url, data, json, headers=headers, proxies=get_proxies(), timeout=(5, 5))


def md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()
