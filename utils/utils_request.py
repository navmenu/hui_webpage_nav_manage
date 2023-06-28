import logging

import requests

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, prefix: str, token: str):
        self.prefix = prefix
        self.token = token

    def ping(self, value="msg") -> (str, int):
        params = {"value": value}
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.get(self.prefix + 'ping', params=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return str(response.text), 200

    def get_admin(self) -> (dict, int):
        params = {}
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.get(self.prefix + 'get_admin', params=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def admin_login(self, username, password):
        params = {"username": username, "password": password}
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.post(self.prefix + 'admin_login', json=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def create_admin(self, **kw):
        params = {**kw}
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.post(self.prefix + 'create_admin', json=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def list_admin(self):
        params = {}
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.get(self.prefix + 'list_admin', params=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def list_admin_of_mine(self):
        params = {}
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.get(self.prefix + 'list_admin_of_mine', params=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def list_navi(self):
        params = {}
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.get(self.prefix + 'list_navi', params=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def create_navi(self, name, parent_nvid):
        params = {
            "name": name,
            "parent_nvid": parent_nvid,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.post(self.prefix + 'create_navi', json=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def delete_navi(self, name, force):
        params = {
            "name": name,
            "force": force,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.post(self.prefix + 'delete_navi', json=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def sort_navi(self, items):
        params = {
            "items": items,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.post(self.prefix + 'sort_navi', json=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def list_navi_lvl2(self, navi_name):
        params = {
            "navi_name": navi_name,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.get(self.prefix + 'list_navi_lvl2', params=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def delete_navi_lvl2(self, navi_name, name):
        params = {
            "navi_name": navi_name,
            "name": name,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.post(self.prefix + 'delete_navi_lvl2', json=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def create_navi_lvl2(self, navi_name, name, text, link, is_escrow):
        params = {
            "navi_name": navi_name,
            "name": name,
            "text": text,
            "link": link,
            "is_escrow": is_escrow,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.post(self.prefix + 'create_navi_lvl2', json=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200

    def sort_navi_lvl2(self, navi_name, items):
        params = {
            "navi_name": navi_name,
            "items": items,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'admin_manage_token': self.token,
        }
        response = requests.post(self.prefix + 'sort_navi_lvl2', json=params, headers=headers)
        if response.status_code != 200:
            return response.reason, response.status_code
        return response.json(), 200
