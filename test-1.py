from facebook_scraper import get_posts

for post in get_posts('nintendo', pages=20, youtube_dl = True):
    print(post['text'][:50])