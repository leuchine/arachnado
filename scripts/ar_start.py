# -*- coding: utf-8 -*-
import json
import logging
import requests


if __name__ == '__main__':
    url = 'http://127.0.0.1:8888/crawler/start'
    # url = 'https://54.200.77.2/crawler/start'
    headers = {'Authorization': 'Basic YWRtaW46bWVtZXhwYXNz',
                "Content-Type": "application/json"}
    logging.basicConfig(level=logging.INFO)
    sites = [
        {"domain":"spider://ar_vb",
        "options":{"args":{"start_urls":["http://www.firearmstalk.com/forums/"],
                                        "post_days":-1},"settings":{}}},
    ]
    for site in sites:
        r = requests.post(url, data=json.dumps(site),
                          headers=headers,
                          verify=False)
        print site["domain"]
        print r
        print r.text
        print "---------------------"
    print "Completed"