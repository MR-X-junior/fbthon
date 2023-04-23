import re
import codecs
import requests

from . import utils
from . import exceptions
from bs4 import BeautifulSoup as bs4

class Comments:

  def __init__(self, comments_html, request_sessions):
    self.__html = str(comments_html)
    self.__html_parser = bs4(self.__html,'html.parser')
    self.__react_type = {'1':'like','2':'love','3':'wow','4':'haha','7':'sad','8':'angry','16':'care'}

    self.__session = request_sessions
    self.__host = ('https://'+self.__session.headers['host'] if 'host' in self.__session.headers.keys() else "https://mbasic.facebook.com")

    if self.__html_parser.find('div') is None: raise exceptions.FacebookError('"%s" Invalid HTML Comment!!!' % (comments_html))

    self.__comment_info = {'author':None,
                           'usermame':None,
                           'comment_text':'',
                           'media':None,
                           'user_tag':[],
                           'time':None}

    author = self.__html_parser.find('a', href = re.compile('^\/(profile\.php\?id=|[a-zA-Z0-9_.-]+\?eav=)'))
    comment_text = self.__html_parser.find('h3').find_next('div', class_ = True)
    waktu = self.__html_parser.find('abbr')

    media_mp4 = self.__html_parser.find('a', href = re.compile('^\/video_redirect\/'))
    media_jpeg = self.__html_parser.find('a', href = re.compile('^\/photo\.php\?'))

    if author is not None:
      self.__comment_info['author'] = author.text
      self.__comment_info['username'] = re.search('^\/(([a-zA-Z0-9_.-]+)\?eav|profile\.php\?id=(\d+))',author['href']).group(2 if 'profile.php' not in author['href'] else 3)

    if comment_text is not None:
      for br in comment_text.find_all('br'):
        br.replace_with("\n")

      self.__comment_info['comment_text'] = comment_text.text
      self.__comment_info['user_tag'].extend([{'name':i.text,'username':re.search('^\/(([a-zA-Z0-9_.-]+)\?eav|profile\.php\?id=(\d+))',i['href']).group(2 if 'profile.php' not in i['href'] else 3)} for i in comment_text.findAll('a', href = re.compile('^\/([a-zA-Z0-9_.-]+\?eav|profile\.php)'))])

    if waktu is not None: self.__comment_info['time'] = waktu.text

    if media_mp4 is not None:
      rahmet_data = {'link':None, 'id':None, 'preview':None, 'content-type':'video/mp4'}
      video = re.search('src=(.*)', requests.utils.unquote(media_mp4['href']))
      preview = media_mp4.find_next('img', src = re.compile('^https:\/\/z-m-scontent(\.fbpn4-1\.fna\.fbcdn\.net|\.fsri(.*?)\.fna\.fbcdn\.net)'))

      if video is not None:
        rahmet_data['link'] = video.group(1)
        rahmet_data['id'] = re.search('&id=(\d+)',video.group(1)).group(1)

      if preview is not None: rahmet_data['preview'] = preview['src']

      self.__comment_info['media'] = rahmet_data

    if media_jpeg is not None:
      khaneysia_data = {'link':None, 'id':None, 'preview':None, 'content-type':'image/jpeg'}
      photo = self.__host + media_jpeg['href']
      thubmnail = media_jpeg.find_next('img', src = re.compile('^https:\/\/z-m-scontent(\.fbpn4-1\.fna\.fbcdn\.net|\.fsri(.*?)\.fna\.fbcdn\.net)'))

      req_photo = self.__session.get(photo)
      res_photo = bs4(req_photo.text,'html.parser')

      link_photo = res_photo.find('img', src = re.compile('^https:\/\/z-m-scontent(\.fbpn4-1\.fna\.fbcdn\.net|\.fsri(.*?)\.fna\.fbcdn\.net)'))

      if link_photo is not None: khaneysia_data['link'] = link_photo['src']
      if thubmnail is not None: khaneysia_data['preview'] = thubmnail['src']
      if link_photo is not None: khaneysia_data['id'] = re.search("(\d+_\d+_\d+)",link_photo['src']).group(1)

      self.__comment_info['media'] = khaneysia_data

    self.author = self.__comment_info['author']
    self.username = self.__comment_info['username']
    self.comment_text = self.__comment_info['comment_text']
    self.media = self.__comment_info['media']
    self.user_tag = self.__comment_info['user_tag']
    self.time = self.__comment_info['time']

  @property
  def _comment_info(self):
    return self.__comment_info.copy()

  def __getitem__(self, item):
    return (self.__comment_info[item] if item in self.__comment_info.keys() else None)

  def __str__(self):
    return "Facebook Comments: author='%s' username='%s' comment_text='%r' user_tag=%s time='%s'" % (self.__comment_info['author'],self.__comment_info['username'],self.__comment_info['comment_text'],self.__comment_info['user_tag'],self.__comment_info['time'])

  def __repr__(self):
    return "Facebook Comments: author='%s' username='%s' comment_text='%r' user_tag=%s time='%s'" % (self.__comment_info['author'],self.__comment_info['username'],self.__comment_info['comment_text'],self.__comment_info['user_tag'],self.__comment_info['time'])

  def reply(self, message):
    reply_url = self.__html_parser.find('a', href = re.compile('^\/comment\/replies\/'))
    if reply_url is None: raise exceptions.FacebookError('Tidak dapat membalas komentar '+ str(self['author']))
    message = codecs.decode(codecs.encode(message,'unicode_escape'),'unicode_escape')

    a = self.__session.get(self.__host + reply_url['href'])
    b = bs4(a.text,'html.parser')
    c = b.find('form', action = re.compile('\/a\/comment\.php\?'))
    d = {i.get('name'):i.get('value') for i in c.findAll('input')}
    d['comment_text'] = message

    kirim = self.__session.post(self.__host + c['action'], data = d)

    return kirim.ok

  def send_react(self, react_type):
    react_list = ['like','love','care','haha','wow','sad','angry']
    react_url = self.__html_parser.find('a', href = re.compile('^\/reactions\/picker\/\?ft_id=\d+'))

    if react_type.lower() not in react_list: raise TypeError('Invalid react type')

    if react_url is not None:
      a = self.__session.get(self.__host + react_url['href'])
      b = bs4(a.text,'html.parser')

      get_react = b.findAll('a', href = re.compile('\/ufi\/reaction'))

      kirim = self.__session.get(self.__host + get_react[react_list.index(react_type.lower())]['href'])

      return kirim.ok

  def get_reply(self, limit = 10):
    reply_data = []
    reply_url = self.__html_parser.find('a', href = re.compile('^\/comment\/replies(.*)count=\d+'))


    if reply_url is not None:
      while len(reply_data) < limit:
        reply_link = self.__host + reply_url['href']

        a = self.__session.get(reply_link)
        b = bs4(a.text,'html.parser')

        for i in b.findAll('h3', class_ = False)[1:]:
          div_komen = i.find_previous('div')
          if div_komen is None: continue
          reply_data.append(Comments(str(div_komen), self.__session))

        next_uri = b.find('a', href = re.compile('^\/comment\/replies(.*)pc=\d'))
        if next_uri is None or len(reply_data) >= limit: break

        reply_url = self.__host + next_uri['href']


    return reply_data[0:limit]

  def get_react(self):
    ufi = self.__html_parser.find('a', href = re.compile('^\/ufi\/reaction\/profile\/browser'))
    react_data = {i:0 for i in self.__react_type.values()}

    if ufi is not None:
      a = self.__session.get(self.__host + ufi['href'])
      b = bs4(a.text,'html.parser')
      c = b.findAll('a', href = re.compile('^\/ufi\/reaction\/profile(.*)reaction_type=\d(.*)total_count=\d'))
      
      for k,v in enumerate(c[1:]):
        total = int(re.search('total_count=(\d+)',v['href']).group(1))
        rct_type = re.search('reaction_type=(\d+)',v['href']).group(1)
        if rct_type not in self.__react_type.keys():continue
        react_data[self.__react_type[rct_type]] = total


    return react_data
