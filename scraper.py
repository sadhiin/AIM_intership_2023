import json
import requests
import csv
import time
import os
# Facebook Graph API credentials
app_id = "YOUR_APP_ID"
app_secret = "YOUR_APP_SECRET"
page_id = "YOUR_PAGE_ID"

def get_access_token(app_id, app_secret):
    """ Get the access token from Facebook """
    payload = {
        'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret
    }
    response = requests.get("https://graph.facebook.com/oauth/access_token", params=payload)
    return response.json()['access_token']

def request_until_succeed(url):
    """ Make an API request and handle errors """
    success = False
    while not success:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                success = True
            else:
                print("Error:", response.status_code)
                print("Retrying in 5 seconds...")
                time.sleep(5)
        except Exception as e:
            print("Error:", str(e))
            time.sleep(5)
    return response.json()

def get_posts(page_id, access_token):
    """ Retrieve posts from the Facebook page """
    url = f"https://graph.facebook.com/v17.0/{page_id}/posts?access_token={access_token}"
    posts = request_until_succeed(url)
    return posts.get('data', [])

def get_comments(post_id, access_token):
    """ Retrieve comments from a post """
    url = f"https://graph.facebook.com/v17.0/{post_id}/comments?access_token={access_token}"
    comments = request_until_succeed(url)
    return comments.get('data', [])

def save_to_csv(filename, data):
    """ Save data to a CSV file """
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Post ID", "Comment ID", "Message"])
        for item in data:
            writer.writerow(item)

if __name__ == '__main__':
    try:

        access_token = get_access_token(app_id, app_secret)
        posts = get_posts(page_id, access_token)

        all_comments = []
        for post in posts:
            post_id = post['id']
            comments = get_comments(post_id, access_token)
            for comment in comments:
                all_comments.append([post_id, comment['id'], comment['message']])

        comment_file_name = "comments.csv"
        save_to_csv(comment_file_name, all_comments)
        print("All comments saved to {}".format(comment_file_name))

    except Exception as e:
        raise e