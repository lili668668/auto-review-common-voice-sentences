import time
import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("username")
parser.add_argument("authorization")
parser.add_argument("reviewNumber")
args = parser.parse_args()

username = args.username
authorization = args.authorization
reviewNumber = 25

response = requests.get('https://kinto.mozvoice.org/v1/buckets/App/collections/Sentences_Meta_zh-TW/records?has_Sentences_Meta_UserVote_{username}=false&has_approved=false&_sort=createdAt'.format(username=username))
sentences = json.loads(response.text)['data']

if args.reviewNumber is 'all':
  reviewNumber = len(sentences)
else:
  reviewNumber = int(args.reviewNumber)

postData = {
  'defaults': {
    'headers': {
      'Authorization': authorization
    }
  },
  'requests': []
}
timestamp = str(time.time()).split('.')[0]


def send(cnt):
  global postData
  headers = {
    'Authorization': authorization,
    'Content-Type': 'application/json',
    'Content-Length': str(len(json.dumps(postData))),
    'Host': 'kinto.mozvoice.org',
    'Origin': 'https://common-voice.github.io',
    'Referer': 'https://common-voice.github.io/sentence-collector/',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
  }

  result = requests.post('https://kinto.mozvoice.org/v1/batch', headers=headers, data=json.dumps(postData))
  print('{}: {}'.format(str(int(cnt / 24)), result.url))
  if 'error' in json.loads(result.text):
    print(result.text)

  postData = {
    'defaults': {
      'headers': {
        'Authorization': authorization
      }
    },
    'requests': []
  }
  timestamp = str(time.time()).split('.')[0]

for cnt in range(0, reviewNumber):
  template = {
    'body': {
      'data': {
        'createdAt': sentences[cnt]['createdAt'],
        'id': sentences[cnt]['id'],
        'invalid': [],
        'valid': [],
        'last_modified': sentences[cnt]['last_modified'],
        'sentence': sentences[cnt]['sentence'],
        'source': sentences[cnt]['source'],
        'username': sentences[cnt]['username']
      }
    },
    'headers': {
      'If-Match': '"{}"'.format(sentences[cnt]['last_modified'])
    },
    'method': 'PUT',
    'path': '/buckets/App/collections/Sentences_Meta_zh-TW/records/{}'.format(sentences[cnt]['id'])
  }
  for name in sentences[cnt]['valid']:
    template['body']['data']['Sentences_Meta_UserVote_{}'.format(name)] = True
    template['body']['data']['Sentences_Meta_UserVoteDate_{}'.format(name)] = sentences[cnt]['Sentences_Meta_UserVoteDate_{}'.format(name)]
    template['body']['data']['valid'].append(name)

  template['body']['data']['Sentences_Meta_UserVote_{}'.format(username)] = True
  template['body']['data']['Sentences_Meta_UserVoteDate_{}'.format(username)] = timestamp
  template['body']['data']['valid'].append(username)

  postData['requests'].append(template)

  if cnt % 24 is 0 and cnt is not 0:
    send(cnt)

send(reviewNumber + 24)

