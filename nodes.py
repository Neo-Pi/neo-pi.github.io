import requests

proxies = [
    {"name": "🇭🇰 D00 香港HKT*", "server": "shark2.douyucdn.cn.0768eb49.ksyungslb.com.douyinvod.click", "port": 39275, "type": "ssr", "cipher": "chacha20-ietf",
        "password": "GhQrDS", "protocol": "auth_aes128_sha1", "obfs": "plain", "protocol-param": "143077:4y14lw3363", "obfs-param": "bilivideo.com", "udp": True},
    # Add more proxies here...
]


def test_proxy(proxy):
    proxy_url = f"{proxy['server']}:{proxy['port']}"
    proxies = {
        "http": f"socks5://{proxy_url}",
        "https": f"socks5://{proxy_url}"
    }
    url = "https://www.google.com"  # Change this to the URL you want to test
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy['name']} is working")
        else:
            print(f"Proxy {proxy['name']} is not working")
    except requests.exceptions.RequestException:
        print(f"Proxy {proxy['name']} is not working1")


# Test each proxy in the list
for proxy in proxies:
    test_proxy(proxy)
