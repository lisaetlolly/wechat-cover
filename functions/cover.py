import json
import re
import requests

def handler(event, context):
    # 获取前端传来的 URL
    params = event.get('queryStringParameters', {})
    article_url = params.get('url')

    if not article_url:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': '请提供 URL'})
        }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(article_url, headers=headers)
        html_content = response.text
        
        # 核心正则匹配
        cover_match = re.search(r'var msg_cdn_url = "(.*?)";', html_content)
        
        if cover_match:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'url': cover_match.group(1)})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': '未找到封面图'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }