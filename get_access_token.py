# -*- coding: utf-8 -*-
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

flow = flow_from_clientsecrets(
            './client_secrets.json',
            scope = 'https://www.googleapis.com/auth/chromewebstore',
            redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        )

print 'AUTHORIZE URL: ' + flow.step1_get_authorize_url()

code = raw_input('CODE: ')
credentials = flow.step2_exchange(code)

storage = Storage('./credentials.json')
storage.put(credentials)

print 'OK!'
