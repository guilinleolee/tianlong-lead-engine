import requests
from bs4 import BeautifulSoup

def explore():
    url = "https://www.proginn.com/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a')
        print(f"Total links found: {len(links)}")
        for l in links:
            text = l.get_text(strip=True)
            href = l.get('href')
            if text and href:
                # Look for "项目", "抢单", "接单", "发现"
                keywords = ["项目", "接单", "任务", "外包", "整包"]
                if any(k in text for k in keywords):
                    print(f"{text}: {href}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    explore()
