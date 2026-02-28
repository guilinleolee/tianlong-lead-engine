import requests
from bs4 import BeautifulSoup

def fetch_and_analyze(name, url):
    print(f"\n--- {name} ---")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://www.google.com/',
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.encoding = r.apparent_encoding
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Look for common project list patterns
            print("Title:", soup.title.string if soup.title else "No Title")
            
            # Shixian patterns
            if "shixian" in url:
                items = soup.select('.project-item, .item, .project, .row')
                print(f"Found {len(items)} potential items")
                for i, item in enumerate(items[:5]):
                    print(f"Item {i}: {str(item)[:500]}...")
            
            # Yuanjisong patterns
            if "yuanjisong" in url:
                items = soup.select('.job-list-item, .course-card, .job-item, .item')
                print(f"Found {len(items)} potential items")
                for i, item in enumerate(items[:5]):
                    print(f"Item {i}: {str(item)[:500]}...")
                    
        else:
            print("Response Preview:", r.text[:1000])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_analyze("YUANJISONG", "https://www.yuanjisong.com/job")
    fetch_and_analyze("SHIXIAN", "https://shixian.com/projects")
