# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 01:33:47 2023

@author: EUROCOM
"""
import requests
import json
import datetime
#'2023-01-01T12:00:00.000Z'
data="{'url': 'test', 'data': 'string', 'priority': 0, 'start_datetime': null, 'check_condition_request_url': '/api/v1/test_condition', 'method': 'POST'}"

data={'url': 'test', 'data': {}, 'priority': 0, 'start_datetime': '2023-01-01T12:00:00.000Z', 'check_condition_request_url': '/api/v1/test_condition', 'method': 'POST'}

requests.post(url="http://127.0.0.1:10102/api/v1/jobs",data=json.dumps(data))