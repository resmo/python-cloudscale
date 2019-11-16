#!/usr/bin/env python

from __future__ import print_function

import os
import json
import requests
from urllib import urlencode

class RestAPI(object):

    def __init__(self, endpoint, api_key):
        '''
        '''
        self.endpoint = endpoint
        self.headers = {
            'Authorization': 'Bearer %s' % api_key,
            'Content-type': 'application/json',
        }

    def _return_result(self, r):
        '''
        '''

        result = {
            'status_code': r.status_code,
        }

        try:
            result['data'] = r.json()
        except ValueError:
            result['data'] = None

        return result

    def get_resources(self, resource, payload=None, resource_id=None):
        '''
        '''

        if not resource:
            return {}

        query_url = self.endpoint + '/' + resource
        if resource_id:
            query_url = query_url + '/' + resource_id

        # TODO: make this less ugly
        if payload:
            for k, v in payload.items():
                if v is not None:
                    data = "%s=%s" % (k, v)
                else:
                    data = k
                break

            query_url = query_url + '?' + data

        r = requests.get(query_url, headers=self.headers)
        return self._return_result(r)

    def post_patch_resource(self, resource, payload, resource_id=None):
        '''
        '''

        if not resource:
            return {}

        # Ignore None values
        data = dict()
        for k, v in payload.items():
            if v is not None:
                data[k] = v

        query_url = self.endpoint + '/' + resource
        print(json.dumps(data))
        if resource_id:
            query_url = query_url + '/' + resource_id
            r = requests.patch(query_url, json=data, headers=self.headers)

        else:
            r = requests.post(query_url, json=data, headers=self.headers)

        return self._return_result(r)

    def delete_resource(self, resource, resource_id):
        '''
        '''

        if not resource:
            return {}

        query_url = self.endpoint + '/' + resource + '/' + resource_id
        r = requests.delete(query_url, headers=self.headers)
        return self._return_result(r)
