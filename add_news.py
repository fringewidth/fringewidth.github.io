import json
import datetime

def add_news():
    now = datetime.datetime.now()
    current_year = str(now.year)
    current_month = str(now.month).zfill(2)
    current_day = str(now.day).zfill(2)

    year = input(f"Enter year [{current_year}]: ").strip() or current_year
    month = input(f"Enter month [{current_month}]: ").strip() or current_month
    day = input(f"Enter day [{current_day}]: ").strip() or current_day

    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    headline = input("Enter news headline: ").strip()

    if not headline:
        print("Error: Headline cannot be empty")
        return

    try:
        with open('news.json', 'r') as f:
            news_list = json.load(f)
    except FileNotFoundError:
        return 

    new_item = {
        "date": date_str,
        "headline": headline
    }
    news_list.append(new_item)

    news_list.sort(key=lambda x: x["date"], reverse=True)

    with open('news.json', 'w') as f:
        json.dump(news_list, f, indent=2)

    print(f"Added news item for {date_str}")

if __name__ == "__main__":
    add_news()
