# -*- coding: utf-8 -*-
import sys
import httplib2
import json
from oauth2client.file import Storage

storage = Storage('./credentials.json') # 取得したアクセストークン
credentials = storage.get()

http = credentials.authorize(httplib2.Http())

with open(sys.argv[2], 'rb') as f:

    # PUTでzipを送りつければアップロードできる
    response = http.request(
                'https://www.googleapis.com/upload/chromewebstore/v1.1/items/' + sys.argv[1],
                method = 'PUT',
                body = f
            )

    json = json.loads(response[1])

    # 結果の表示
    print 'State: ' + json['uploadState']
    if 'itemError' in json:
        print 'Error:'
        for err in json['itemError']:
            print err
    else:
        print 'Success!'
