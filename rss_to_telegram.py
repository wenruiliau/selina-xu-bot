import feedparser
import requests
import html2text
import os
from dotenv import load_dotenv

def read_rss_feed(rss_url):
    feed = feedparser.parse(rss_url)
    return feed.entries

def send_to_telegram(bot_token, chat_id, message):
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(telegram_api_url, json=params)

    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)
    return response.json()

def html_to_markdown(html_content):
    return html2text.html2text(html_content)


def main():
    load_dotenv()
    rss_url = os.getenv('RSS_URL')
    bot_token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    entries = read_rss_feed(rss_url)
    
    try:
        text_file = open("latest_entry.txt", "r")
        latest_entry_id = text_file.read()
        text_file.close()
    except:
        raise ValueError('Cannot read text file')

    for entry in entries:
        if entry.link != latest_entry_id:
            markdown_summary = html_to_markdown(entry.summary)
            message = f"*New Article*\n\n[{entry.title}]({entry.link})\n\n{markdown_summary}"

            send_to_telegram(bot_token, chat_id, message)
            # Update the latest entry ID after successfully sending to Telegram
            latest_entry_id = entry.link
            text_file = open("latest_entry.txt", "w")
            text_file.write(latest_entry_id)
            text_file.close()
            break

if __name__ == "__main__":
    main()
