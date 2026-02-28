import requests

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"Status: {r.status_code}")
        print(r.text[:5000]) # Print first 5000 chars
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("--- YUANJISONG ---")
    fetch_html("https://www.yuanjisong.com/job/all/all-all-all-all/page1/")
    print("\n\n --- SHIXIAN ---")
    fetch_html("https://shixian.com/projects")
