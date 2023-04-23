import re
import os
import codecs
import requests
import traceback

from . import utils
from . import exceptions
from bs4 import BeautifulSoup as bs4

class Chats:

  def __init__(self, chats_url,requests_session):
    self.__session = requests_session
    self.__host = ('https://'+self.__session.headers['host'] if 'host' in self.__session.headers.keys() else "https://mbasic.facebook.com")

    self.__chats_url = chats_url

    req = self.__session.get(self.__chats_url)
    self.__res = bs4(req.text,'html.parser')
    self.__send_url = self.__res.find('form', action = re.compile('\/messages\/send\/'))
    self.__action_redirect  = self.__res.find('form', action = re.compile('\/messages\/action_redirect'))

    if self.__send_url is not None: self.__send_url = self.__host + self.__send_url['action']
    if self.__action_redirect is not None: self.__action_redirect = self.__host + self.__action_redirect['action']

    self.__data = {}
    self.__chat_info = {}
    self.__data_other = {}

    for i in self.__res.findAll('input'):
      if i.get('name') not in ['search', 'search_source','query', 'like', 'send_photo','unread', 'delete', 'delete_selected', 'archive', 'ignore_messages', 'block_messages', 'message_frx','unarchive','unblock_messages','add_people','leave_conversation',None]:
        self.__data[i.get('name')] = i.get('value')
      else:
        self.__data_other[i.get('name')] = i.get('value')

    self.__chat_info['name'] = self.__res.find('title').text
    self.__chat_info['id'] = None
    self.__chat_info['chat_id'] = (re.search("tid=cid\.(.?)\.((\d+:\d+)|\d+)",requests.utils.unquote(chats_url)).group(2) if 'tid' in chats_url else None)
    self.__chat_info['chat_url'] = chats_url
    self.__chat_info['chat_type'] = ('group' if 'leave_conversation' in self.__data_other else 'user')
    self.__chat_info['blocked'] = 'unblock_messages' in self.__data_other.keys()

    for x in self.__data.keys():
      if re.match('ids\[\d+\]',x):
        self.__chat_info['id'] = self.__data[x]
        break

    self.name = self.__chat_info['name']
    self.id = self.__chat_info['id']
    self.chat_id = self.__chat_info['chat_id']
    self.chat_url = self.__chat_info['chat_url']
    self.chat_type = self.__chat_info['chat_type']
    self.blocked = self.__chat_info['blocked']

  @property
  def chat_info(self):
    return self.__chat_info.copy()

  def __str__(self):
    return "Facebook Chats : name='%s' id=%s chat_id=%s type='%s'" % (self.name, self.id, self.chat_id, self.chat_type)

  def __repr__(self):
    return "Facebook Chats : name='%s' id=%s chat_id=%s type='%s'" % (self.name, self.id, self.chat_id, self.chat_type)

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, tb):
    if exc_type is not None:
      traceback.print_exception(exc_type, exc_value, tb)

    return True

  def __getitem__(self, item):
    return (self.__chat_info[item] if item in self.__chat_info.keys() else None)

  def __get_messages(self, chat_url):
    data = {'chat':[]}

    req = self.__session.get(chat_url)

    self.__res_get_chat = bs4(req.text,'html.parser')

    ah = self.__res_get_chat.find('div', id = 'see_older')

    if ah is None:
      ah = self.__res_get_chat.find('div', id='messageGroup')

    if ah is None: return data

    chat = ah.find_next('div')

    for i in chat.contents:
      profile = i.find('a', href = re.compile('^\/([a-zA-Z0-9_.-]+|profile\.php)\?'))
      if profile is None: continue
      uh = {'name':None,'username':None, 'message':[], 'file':[],'stiker':[],'time':None}
      uh['name'] = profile.text
      if 'profile.php' not in profile['href']: uh['username'] = re.match('^\/([a-zA-Z0-9_.-]+)\?',profile['href']).group(1)
      content = profile.find_previous('div')

      for echa in content.findAll('img', src = re.compile(''), class_ = True, alt = True):
        stiker_url = echa['src']
        stiker_name = echa['alt']
        stiker = {'stiker_name':stiker_name, 'stiker_url':stiker_url}
        uh['stiker'].append(stiker)

      for br in content.findAll('br'):
        br.replace_with('\n')

      for y in content.findAll('span', attrs = {'aria-hidden':False, 'class':False}):
        if len(y.text) == 0: continue
        uh['message'].append(y.text)

      waktu = i.find('abbr')

      uh['time'] = waktu.text
      data['chat'].append(uh)

      for jpg in i.findAll('a', href = re.compile('\/messages\/attachment_preview')):
        link = jpg.find_next('img', src = re.compile('^https:\/\/z-m-scontent(\.fbpn4-1\.fna\.fbcdn\.net|\.fsri(.*?)\.fna\.fbcdn\.net)'))
        if link is None: continue
        content_id = re.search("(\d+_\d+_\d+)",link['src']).group(1)
        preview = self.__host + jpg['href']
        data['chat'][-1]['file'].append({'link':link['src'],'id':content_id, 'preview':preview,'content-type':'image/jpeg'})

      for mp4 in i.findAll('a', href = re.compile('\/video_redirect\/')):
        vidurl = re.search('src=(.*)',requests.utils.unquote(mp4['href'])).group(1)
        vidid = re.search('&id=(\d+)',vidurl).group(1)
        thumb_nail = mp4.find_next('img', src = re.compile('https:\/\/z-m-scontent\.(fbpn\d-\d|fsri\d-\d)\.fna\.fbcdn\.net'))['src']
        data['chat'][-1]['file'].append({'link':vidurl,'id':vidid,'preview':thumb_nail,'content-type':'video/mp4'})

    return data

  def get_chat(self, limit = 5, sort = True):
    data = []
    previos_chat = self.__chats_url

    while True:
      get = self.__get_messages(previos_chat)
      data.extend(get['chat'])
      previos_chat = self.__res_get_chat.find('div', id = 'see_older')
      if len(get['chat']) == 0 or previos_chat is None or len(data) >= limit: break
      previos_chat = self.__host + previos_chat.find_next('a')['href']

    if len(data) != 0 and sort: data.reverse()

    return data[0:limit]

  def send_text(self, message):
    if self['blocked']: raise exceptions.FacebookError('Pesan tidak bisa di kirim karena anda telah memblokir akun "%s"!!!' % (self['name']))
    if self.__send_url is None: raise exceptions.FacebookError('Tidak dapat mengirim pesan kepada %s' % (self.name))
    if not re.match('^\S',message): raise exceptions.FacebookError('Panjang pesan minimal 1 karakter, dan harus di awali dengan non-white space character!!.')

    message = codecs.decode(codecs.encode(message,'unicode_escape'),'unicode_escape')

    data = self.__data.copy()
    data.update({'body':message})
    res = self.__session.post(self.__send_url, data = data)
    html_res = bs4(res.text,'html.parser')

    if html_res.find('a', href = re.compile('\/home\.php\?rand=\d+')):
      err_div = html_res.find('div', id = 'root')
      err_msg = ("Terjadi Kesalahan!" if err_div is None else err_div.find('div', class_ = True).get_text(separator = '\n'))
      raise exceptions.FacebookError(err_msg)

    return res.ok

  def send_image(self, file, message = ''):
    if self['blocked']: raise exceptions.FacebookError('Pesan tidak bisa di kirim karena anda telah memblokir akun "%s"!!!' % (self['name']))
    if self.__send_url is None: raise exceptions.FacebookError('Tidak dapat mengirim pesan kepada %s' % (self.name))

    message = codecs.decode(codecs.encode(message,'unicode_escape'),'unicode_escape')
    form = self.__res.find('form', action = re.compile('https:\/\/(?:z-upload|upload)\.facebook\.com'))

    if form is None:
      data = self.__data.copy()
      data['send_photo'] = self.__data_other['send_photo']
      post = self.__session.post(self.__send_url, data = data)
      form = bs4(post.text,'html.parser').find('form', action = re.compile('https:\/\/(?:z-upload|upload)\.facebook\.com'))

    form_data = {i.get('name'):(None,i.get('value')) for i in form.findAll('input', attrs = {'name':True,'type':'hidden'})}
    form_data['body'] = (None, message)

    submit = utils.upload_photo(requests_session = self.__session, upload_url = form['action'], input_file_name = 'file1', file_path = file, fields = form_data)

    return submit.ok

  def send_like_stiker(self):
    if self.__send_url is None: raise exceptions.FacebookError('Tidak dapat mengirim pesan kepada %s' % (self.name))

    if self['blocked']: raise exceptions.FacebookError('Stiker tidak bisa di kirim karena anda telah memblokir akun "%s"!!!' % (self['name']))

    data = self.__data.copy()
    data['like'] = (self.__data_other['like'] if 'like' in self.__data_other.keys() else 'like')

    req = self.__session.post(self.__send_url, data = data)

    html_res = bs4(req.text,'html.parser')
    if html_res.find('a', href = re.compile('\/home\.php\?rand=\d+')):
      err_div = html_res.find('div', id = 'root')
      err_msg = ("Terjadi Kesalahan!" if err_div is None else err_div.find('div', class_ = True).get_text(separator = '\n'))
      raise exceptions.FacebookError(err_msg)

    return req.ok

  def mark_as_unread(self):

    if self.__action_redirect is None or 'unread' not in self.__data_other.keys(): return False

    data = self.__data.copy()
    data['unread'] = self.__data_other['unread']

    req = self.__session.post(self.__action_redirect, data = data)

    return req.ok

  def delete_chat(self):

    if self.__action_redirect is None or 'delete' not in self.__data_other.keys(): return False

    data = self.__data.copy()
    data['delete'] = self.__data_other['delete']

    a = self.__session.post(self.__action_redirect, data = data)
    b = bs4(a.text,'html.parser')

    url = self.__host + b.find('a', href = re.compile('\/messages\/action\/\?mm_action=delete'))['href']

    req = self.__session.get(url)

    return req.ok

  def archive_chat(self):
    if self.__action_redirect is None or 'archive' not in self.__data_other.keys(): return False

    data = self.__data.copy()
    data['archive'] = self.__data_other['archive']

    a = self.__session.post(self.__action_redirect, data = data)

    return a.ok

  def unarchive_chat(self):
    if self.__action_redirect is None or 'unarchive' not in self.__data_other.keys(): return False

    data = self.__data.copy()
    data['unarchive'] = self.__data_other['unarchive']

    a = self.__session.post(self.__action_redirect, data = data)

    return a.ok

  def ignore_chat(self):
    if self.__action_redirect is None or 'ignore_messages' not in self.__data_other.keys(): return False

    data = self.__data.copy()
    data['ignore_messages'] = self.__data_other['ignore_messages']

    a = self.__session.post(self.__action_redirect, data = data)
    b = bs4(a.text,'html.parser')

    url = self.__host + b.find('a', href = re.compile('(.*)\/ignore_messages\/'))['href']

    req = self.__session.get(url)

    return req.ok

  def block_chat(self):
    if self.__action_redirect is None or 'block_messages' not in self.__data_other.keys(): return False

    data = self.__data.copy()
    data['block_messages'] = self.__data_other['block_messages']

    a = self.__session.post(self.__action_redirect, data = data)
    b = bs4(a.text,'html.parser')

    url = self.__host + b.find('a', href = re.compile('(.*)\/block_messages\/'))['href']

    req = self.__session.get(url)

    self.refresh()

    return req.ok

  def unblock_chat(self):
    if self.__action_redirect is None or 'unblock_messages' not in self.__data_other.keys(): return False

    data = self.__data.copy()
    data['unblock_messages'] = self.__data_other['unblock_messages']

    a = self.__session.post(self.__action_redirect, data = data)
    b = bs4(a.text,'html.parser')

    url = self.__host + b.find('a', href = re.compile('(.*)\/unblock_messages\/'))['href']

    req = self.__session.get(url)

    self.refresh()

    return req.ok

  def refresh(self):
    self.__init__(self.__chats_url, self.__session)

