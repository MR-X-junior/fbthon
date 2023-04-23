"""
facebook.messenger
------------------
Module Ini Di gunakan untuk menggirim/menerima chat dari facebook
"""

import re
import requests

from . import exceptions
from .chats import Chats
from .login import Cookie_Login
from bs4 import BeautifulSoup as bs4
from multiprocessing.pool import ThreadPool

class Messenger:

  def __init__(self, cookies, headers = {}):
    login = Cookie_Login(cookies, headers = headers)

    self.__session = login._session
    self.__host = login._host

    req = self.__session.get(self.__host + '/messages')
    res = bs4(req.text,'html.parser')
    self.__new_messages = self.__host + res.find('a',href = re.compile('\/messages\/'))['href']

    a = self.__session.get(self.__new_messages)
    self.__res = bs4(a.text,'html.parser')

    self.__message_pending = self.__res.find('a', href = re.compile('\/messages\/\?folder=pending'))
    self.__message_filter = self.__res.find('a', href = re.compile('\/messages\/\?folder=other'))
    self.__message_archive = self.__res.find('a', href = re.compile('\/messages\/\?folder=action(.*)Aarchived'))
    self.__message_unread = self.__res.find('a', href = re.compile('\/messages\/\?folder=unread'))
    self.__message_spam = self.__res.find('a', href = re.compile('\/messages\/\?folder=spam'))

    self.__message_pending = self.__host + self.__message_pending['href'] if self.__message_pending is not None else None
    self.__message_filter = self.__host + self.__message_filter['href'] if self.__message_filter is not None else None
    self.__message_archive = self.__host + self.__message_archive['href'] if self.__message_archive is not None else None
    self.__message_unread = self.__host + self.__message_unread['href'] if self.__message_unread is not None else None
    self.__message_spam = self.__host + self.__message_spam['href'] if self.__message_spam is not None else None

  def new_chat(self, username):
    a = self.__session.get(self.__host + '/' + str(username))
    b = bs4(a.text,'html.parser')

    if b.find('a', href = re.compile('\/home\.php\?rand=\d+')): raise exceptions.PageNotFound("Akun dengan username \"%s\" Tidak di temukan!" % (username))

    chats_url = b.find('a', href = re.compile('\/messages\/thread\/\d+(.*)'))

    if chats_url is None: raise exceptions.FacebookError("Tidak Bisa mengirim chat ke %s" % (b.find('title').text))

    return Chats(self.__host + chats_url['href'], self.__session)

  def __get_chat(self, url, limit = 10):
    chat = []
    my_chat = []

    while True:

      a = self.__session.get(url)
      b = bs4(a.text,'html.parser')
      c = b.findAll('a',href = re.compile('\/messages\/read\/'))
      chat.extend(c[0:(limit - len(chat))])

      url = b.find('a', href = re.compile('\/messages\/\?pageNum=\d(.*)selectable'))

      if len(chat) >= limit or url is None:
        break
      else:
        url = self.__host + url['href']

    th = ThreadPool(6)
    th.map(lambda x: my_chat.append(Chats(self.__host + x['href'], self.__session)),chat[0:limit])

    return my_chat

  def __get_messages(self, url, limit):
    chat_ku = []

    for i in range(limit):
      a = self.__session.get(url)
      b = bs4(a.text,'html.parser')
      c = b.findAll('table', class_ = True, role = False)
      if len(c) <= 0: break

      for x in c:
        name = x.find('a', href = re.compile('^\/messages\/read'))
        message = x.find('span', class_ = True)
        waktu = x.find('abbr')
        uid = None

        if name is not None:
          uid = re.search('tid=cid\.(?:c|g)\.(\d+)',requests.utils.unquote(name['href'])).group(1)

        name = (name.text if name is not None else None)
        message = (message.text if message is not None else None)
        waktu = (waktu.text if waktu is not None else None)

        chat_ku.append({'name':name, 'id':uid, 'last_chat':message,'time':waktu})

      url = b.find('a', href = re.compile('\/messages\/\?pageNum=\d(.*)selectable'))
      if len(chat_ku) >= limit or url is None: break
      else:
        url = self.__host + url['href']


    return chat_ku[0:limit]

  def get_chat_pending(self, limit = 10):
    return self.__get_chat(url = self.__message_pending, limit = limit)

  def get_chat_filter(self, limit = 10):
    return self.__get_chat(url = self.__message_filter, limit = limit)

  def get_chat_archive(self, limit = 10):
    return self.__get_chat(url = self.__message_archive, limit = limit)

  def get_chat_unread(self, limit = 10):
    return self.__get_chat(url = self.__message_unread, limit = limit)

  def get_chat_spam(self, limit = 10):
    return self.__get_chat(url = self.__message_spam, limit = limit)

  def get_new_chat(self, limit = 10):
    return self.__get_chat(url = self.__new_messages, limit = limit)

  def get_new_message(self, limit = 10):
    return self.__get_messages(url = self.__new_messages, limit = limit)

  def get_message_spam(self, limit = 10):
    return self.__get_messages(url = self.__message_spam, limit = limit)

  def get_message_unread(self, limit = 10):
    return self.__get_messages(url = self.__message_unread, limit = limit)

  def get_message_archive(self, limit = 10):
    return self.__get_messages(url = self.__message_archive, limit = limit)

  def get_message_filter(self, limit = 10):
    return self.__get_messages(url = self.__message_filter, limit = limit)

  def get_message_pending(self, limit = 10):
    return self.__get_messages(url = self.__message_pending, limit = limit)



