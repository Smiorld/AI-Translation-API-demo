import random
from datetime import datetime
from models.models import db, CrawledText
TEXT_FILE = "local_texts.txt"  # 可以放在项目根目录

def fake_crawl(app):
    def job():
        with app.app_context():
            try:
                with open(TEXT_FILE, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]
                if not lines:
                    print("[FakeCrawler] No content found in file.")
                    return
                content = random.choice(lines)
                while content=="":
                    content = random.choice(lines)
                entry = CrawledText(content=content, source="local_file", status="new")
                db.session.add(entry)
                db.session.commit()
                print(f"[FakeCrawler] Added crawled text: {content[:40]}...")
            except Exception as e:
                print(f"[FakeCrawler] Error: {e}")

    return job