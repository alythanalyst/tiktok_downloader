import json
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def get_full_tiktok_link(short_link):
    try:
        response = requests.get(short_link, allow_redirects=True)
        response.raise_for_status()
        return response.url
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def extract_video_id(url):
    try:
        match = re.search(r"/(\d+)", url)
        if match:
            return match.group(1)
        match = re.search(r"(?:item_id|video_id)=(\d+)", url)
        if match:
            return match.group(1)
        match = re.search(r"#(?:item_id|video_id)=(\d+)", url)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        print(f"Error extracting video ID: {e}")
        return None

def handler(event, context):  # Netlify Function handler
    if event['httpMethod'] == 'POST':
        try:
            data = json.loads(event['body'])
            tiktok_url = data.get('videoUrl')

            if tiktok_url:
                full_url = get_full_tiktok_link(tiktok_url)
                if full_url:
                    video_id = extract_video_id(full_url)
                    if video_id:
                        download_url = f"https://tikmate.app/download/wBnUQMyuh1w-zErZu2WMwPGKTkv1FeqLacxz64YoORm5Quh3Lqa2ZEuLZLFdHRpBD1r8hWuDSvE9QUcq/{video_id}.mp4?hd=1"
                        return {
                            'statusCode': 200,
                            'body': download_url
                        }
                    else:
                        return {
                            'statusCode': 200,
                            'body': "Could not extract video ID."
                        }
                else:
                    return {
                        'statusCode': 200,
                        'body': "Could not get full TikTok link."
                    }
            else:
                return {
                    'statusCode': 200,
                    'body': "No video URL provided."
                }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f"An error occurred: {str(e)}"
            }
    else: #Handles GET requests
        return {
            'statusCode': 405,  # Method Not Allowed
            'body': "Method Not Allowed"
        }