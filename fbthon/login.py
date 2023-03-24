"""
fbthon.login
--------------
Module Ini Di gunakan untuk login ke akun Facebook
"""

import re
import requests

from . import settings
from . import exceptions
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs4
from http.cookiejar import CookieJar
from http.cookies import SimpleCookie

class Cookie_Login:

  # Gunakan Cookie String Untuk Login Ke Akun #

  def __init__(self, cookies, free_facebook = False, headers = {}):
    self.free_facebook = free_facebook
    self.__cookies = cookies

    self.__host = ("https://free.facebook.com" if free_facebook else "https://mbasic.facebook.com")
    self.__session = requests.Session()
#    self.__session.max_redirects = 60

    self.head = {"Host":("free.facebook.com" if free_facebook else "mbasic.facebook.com"),"cache-control":"max-age=0","upgrade-insecure-requests":"1","user-agent":"Mozilla/5.0 (Linux; Android 9; SM-N976V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Mobile Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","accept-encoding":"gzip, deflate","accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,"} #,"Cookie":cookies}
    self.head.update(headers)
    self.default_head = {'User-Agent':self.head['user-agent']}

    self.__session.headers.update(self.head)

    kuki_dict = self.get_cookie_dict()

   # Set Cookie

    for key,value in kuki_dict.items():
      self.__session.cookies[key] = value
    else:
      self.__session.cookies['domain'] = '.facebook.com'
      self.__session.cookies['path'] = '/'

    url = self.__host + '/login.php?next='+self.__host +'/' + (kuki_dict['c_user'] if 'c_user' in kuki_dict.keys() else 'home.php')

    try:
      req = self.__session.get(url, allow_redirects = True)
    except requests.exceptions.TooManyRedirects:
      self.__session.headers.clear()
      self.__session.headers.update(self.default_head)
      req = self.__session.get(url, allow_redirects = True)

    if 'checkpoint' in req.url:
      raise exceptions.AccountCheckPoint('Akun Anda Terkena Checkpoint')
    elif 'login.php' in req.url:
      raise exceptions.InvalidCookies('Cookie Tidak Valid!')

    form_zero = bs4(req.text,'html.parser').find('form', action = re.compile('\/zero\/optin\/write'))
    zero_data = {}

    if form_zero is not None and free_facebook:
      for x in form_zero.findAll('input'): zero_data[x.get('name')] = x.get('value')
      self.__session.post(self.__host + form_zero['action'], data = zero_data)

    if form_zero is not None and not free_facebook:
      data_mode = bs4(self.__session.get(self.__host + form_zero.find('a', href = re.compile('^\/zero\/optin\/write'))['href']).text,'html.parser')
      data_form = data_mode.find('form', action = re.compile('^\/zero\/optin\/write(.*)action=confirm'))

      if data_form is not None:
        data_data = {i.get('name'):i.get('value') for i in data_form.findAll('input')} #:v
        self.__session.post(self.__host + data_form['action'], data = data_data)

  def __str__(self):
    return "Facebook Cookie_Login: cookies='%s' free_facebook=%s" % (self.__cookies, self.free_facebook)

  def __repr__(self):
    return "Facebook Cookie_Login: cookies='%s' free_facebook=%s" % (self.__cookies, self.free_facebook)


  @property
  def _session(self):
    return self.__session

  @property
  def _host(self):
    return self.__host

  def get_cookie_dict(self):
    simple_kue = SimpleCookie()
    simple_kue.load(self.__cookies)

    if len(simple_kue.items()) != 0:
      cookie_dict = {k: v.value for k, v in simple_kue.items()}
    else:
      cookie_dict = (dict(i.split('=', 1) for i in self.__cookies.split('; ')))

    return cookie_dict

  def get_cookie_str(self):
    return self.__cookies

  def get_token(self):
    data = {'user-agent': self.__session.headers['User-Agent'],'referer':'https://www.facebook.com/','host' : 'business.facebook.com','origin':'https://business.facebook.com','upgrade-insecure-requests':'1','accept-language':'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7','cache-control':'max-age=0','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','content-type':'text/html; charset=utf-8'}
    cookies = {'cookie':self.get_cookie_str()}

    req = requests.get('https://business.facebook.com/business_locations', data = data, cookies = cookies)
    token = re.search('(EAAG\w+)', req.text)

    return None if token is None else token.group(1)

  def logout(self, save_device = True):
    data = {}

    req = self.__session.get(self.__host + '/menu/bookmarks')
    res = bs4(req.text,'html.parser')
    link = res.find('a', id = 'mbasic_logout_button')

    if link is not None:
      log = bs4(self.__session.get(self.__host + link['href']).text,'html.parser')
      form = log.findAll('form')

      out = form[0] if save_device else form[1]

      for i in out.findAll('input'):
        data[i.get('name')] = i.get('value')

      khaneysia = self.__session.post(self.__host + out['action'], data = data)

      return khaneysia.ok


class Web_Login(Cookie_Login):

  def __init__(self, email, password, save_login = True,free_facebook = False, headers = {}):
    """

    email -> Gunakan alamat email pada akun facebook, anda juga bisa menggunakan id akun facebook / username akun facebook sebagai pengganti alamat email
    password -> Password Akun Facebook anda
    save_login -> Gunakan True jika ingin menyimpan informasi login
    free_facebook -> Gunakan True jika ingin menggukan web https://free.facebook.com
    headers -> 

    """

    self.save_login = save_login
    self.free_facebook = free_facebook

    self.host_parsed = urlparse("https://mbasic.facebook.com")

    header = {"Host":self.host_parsed.netloc,"cache-control":"max-age=0","upgrade-insecure-requests":"1","user-agent":"Mozilla/5.0 (Linux; Android 9; SM-N976V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Mobile Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","accept-encoding":"gzip, deflate","accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"}
    header.update(headers)

    if free_facebook:
      self.__host = self.host_parsed._replace(netloc = 'free.facebook.com').geturl()
    else:
      self.__host = self.host_parsed.geturl()

    self.__session = requests.Session()
    self.__session.headers.update(header)

    req = bs4(self.__session.get(self.__host).text,'html.parser')

    self.__data = {}

    for i in req.findAll('input'):
      if i.get('name') in ['lsd', 'jazoest', 'm_ts', 'li', 'try_number', 'unrecognized_tries', 'email', 'pass', 'login', 'bi_xrwh','_fb_noscript']: self.__data[i.get('name')] = i.get('value')

    self.email = email
    self.password = password

    self.__data.update({'email':self.email,'pass':self.password})

    action = req.find('form',action = re.compile('/login/device-based/regular/\w+'))
    url = self.__host + (action['action'] if action is not None else "/login.php")

    self.submit = self.__session.post(url, data = self.__data, allow_redirects=True)
    self.submit_res = bs4(self.submit.text,'html.parser')

    if 'checkpoint' in self.__session.cookies.get_dict().keys(): 
      raise exceptions.AccountCheckPoint('Akun Anda Terkena Checkpoint')
    elif 'c_user' not in self.__session.cookies.get_dict().keys():
      raise exceptions.LoginFailed('Gagal Login Ke akun, pastikan email atau password anda sudah benar!')

    if save_login and 'login/save-device/' in self.submit.url:
      form = self.submit_res.find('form',action = re.compile("/login/\w+"))
      url = self.__host + form['action']
      data = {}

      for i in form.findAll('input'):
        data[i.get('name')] = i.get('value')

      self.__session.post(url, data = data)

    elif not save_login and 'login/save-device/' in self.submit.url:
      url = self.__host + self.submit_res.find('a', href = re.compile('/login/save-device/cancel'))['href']
      data = {}

      for i in self.submit_res.findAll('input'):
        if i.get('name') in ['fb_dtsg', 'jazoest', 'flow', 'next', 'nux_source']: data[i.get('name')] = i.get('value')

      self.__session.post(url, data = data)

    cookie_dict = self.__session.cookies.get_dict()
    cookie_keys = cookie_dict.keys()
    self.__cookies = ''.join(["%s=%s;" % (i,cookie_dict[i]) for i in cookie_keys])

    super().__init__(cookies = self.__cookies, free_facebook = free_facebook, headers = headers)

  def __str__(self):
    return "Facebook Web_Login: email='%s' password='%s' save_login=%s free_facebook=%s" % (self.email, self.password, self.save_login, self.free_facebook)

  def __repr__(self):
    return "Facebook Web_Login: email='%s' password='%s' save_login=%s free_facebook=%s" % (self.email, self.password, self.save_login, self.free_facebook)

