#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser
import json
import os
from datetime import datetime
from collections import defaultdict

# RSS源配置
RSS_SOURCES = [
    "https://news.ycombinator.com/rss",
    "https://feeds.techcrunch.com/techcrunch/",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.arxiv.org/rss/cs.AI",
    "https://openai.com/blog/rss.xml",
    "https://www.deepmind.com/blog/rss.xml",
]

def fetch_news():
    """采集新闻"""
    articles = []
    
    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source)
            for entry in feed.entries[:5]:
                articles.append({
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', '#'),
                    'summary': entry.get('summary', '')[:200],
                    'source': feed.feed.get('title', 'Unknown'),
                    'published': entry.get('published', datetime.now().isoformat()),
                })
        except:
            pass
    
    return articles

def generate_html(articles):
    """生成HTML"""
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Agent - 自动化新闻资讯站</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; border-radius: 10px; margin-bottom: 30px; text-align: center; }
        header h1 { font-size: 2.5em; margin-bottom: 10px; }
        header p { font-size: 1.1em; opacity: 0.9; }
        .news-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .news-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; }
        .news-card:hover { transform: translateY(-5px); }
        .news-card h3 { color: #667eea; margin-bottom: 10px; font-size: 1.1em; }
        .news-card .source { color: #999; font-size: 0.9em; margin-bottom: 10px; }
        .news-card p { color: #666; line-height: 1.6; margin-bottom: 10px; }
        .news-card a { color: #667eea; text-decoration: none; }
        .news-card a:hover { text-decoration: underline; }
        footer { text-align: center; padding: 20px; color: #999; margin-top: 40px; border-top: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 AI News Agent</h1>
            <p>自动化新闻资讯站 - 每小时自动更新最新AI和科技新闻</p>
        </header>
        
        <div class="news-grid">
'''
    
    for article in articles:
        html += f'''        <div class="news-card">
            <h3>{article['title']}</h3>
            <div class="source">来源: {article['source']}</div>
            <p>{article['summary']}</p>
            <a href="{article['link']}" target="_blank">阅读全文 →</a>
        </div>
'''
    
    html += '''        </div>
        
        <footer>
            <p>AI News Agent - 自动化新闻资讯站</p>
            <p>最后更新: ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
            <p>© 2026 All rights reserved</p>
        </footer>
    </div>
</body>
</html>'''
    
    return html

def main():
    print("采集新闻...")
    articles = fetch_news()
    print(f"采集到 {len(articles)} 篇新闻")
    
    print("生成HTML...")
    html = generate_html(articles)
    
    print("保存文件...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ 完成！")

if __name__ == '__main__':
    main()
