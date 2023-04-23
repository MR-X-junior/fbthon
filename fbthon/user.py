"""
fbthon.user
--------------
Mendapatkan Informasi Tentang Pengguna Facebook!
"""

import re
import os
import json
import codecs
import requests

from . import utils
from .posts import Posts
from . import exceptions
from .chats import Chats
from datetime import datetime
from .login import Cookie_Login
from bs4 import BeautifulSoup as bs4
from multiprocessing.pool import ThreadPool

class User:

  def __init__(self,username, requests_session):
    self.__usr = username

    self.__session = requests_session
    self.__host = "https://mbasic.facebook.com"

    self.__req = self.__session.get(self.__host + '/' + str(username) + '/about?v=info')
    self.__res = bs4(self.__req.text,'html.parser')

    if self.__res.find('a', href = re.compile('\/home\.php\?rand=\d+')): raise exceptions.PageNotFound("Akun dengan username \"%s\" Tidak di temukan!" % (username))

    self.__user_info = {
                       'name':'',
                       'first_name':'',
                       'middle_name':'',
                       'last_name':'',
                       'alternate_name':'',
                       'about':'',
                       'username':'',
                       'id':'',
                       'contact_info':{},
                       'profile_pict':'',
                       'basic_info':{},
                       'education':[],
                       'work':[],
                       'living':{},
                       'relationship':'',
                       'other_name':[],
                       'family':[],
                       'year_overviews':[],
                       'quote':''
                       }

    self.name = ''
    self.first_name = ''
    self.middle_name = ''
    self.last_name = ''
    self.alternate_name = ''
    self.about = ''
    self.username = ''
    self.id = ''
    self.contact_info = {}
    self.profile_pict = ''
    self.basic_info = {}
    self.education = []
    self.work = []
    self.living = {}
    self.relationship = ''
    self.other_name = []
    self.family = []
    self.year_overviews = []
    self.quote = ''

    # Foto Profile
    img = self.__res.find('img', alt = re.compile('.*, profile picture'))
    self.profile_pict = img['src']

    name = img.find_next('strong')

    # Nama
    if name is not None:
      alt_name = name.find('span', attrs = {'class':'alternate_name'})
      if alt_name is not None:
        self.alternate_name = re.sub('\(|\)$','',alt_name.text)
        alt_name.extract()
        pisah = name.text.split(' ')
        pisah.pop()
      else:
        pisah = name.text.split(' ')
    else:
      pisah = []

    if len(pisah) !=0: self.first_name = pisah[0]
    if len(pisah) > 2: self.middle_name = pisah[1]
    if len(pisah) >=2: self.last_name = pisah[-1]

    # Bio
    bio = self.__res.find('div', id = 'bio')

    if bio is not None:

      for x in bio.findAll('a', href = re.compile('\/profile\/edit')):
        x.extract()

      bio_ku = bio.findAll(text = True)
      self.about = bio_ku[-1]

    # User ID

    uid = self.__res.find('a', href = re.compile('(\/photo\.php|\/profile\/picture\/view)'))
    if uid is not None:
      ids = re.search('(.*)id=(\d+)&',uid['href'])
      if ids is not None: self.id = ids.group(2)

    # Informasi Tentang sekolah

    sekolah = self.__res.find('div', id = 'education')

    if sekolah is not None:
      gak_penting = sekolah.findAll('a', href = re.compile('(\/editprofile\/eduwork\/add\/|\/profile\/edit)'))

      for x in gak_penting:
        x.extract()

      for x in sekolah.findAll('img', src = re.compile('^https:\/\/z-m-scontent')):
        data_sekolah = x.find_next('div').findAll(text = True)
        length = len(data_sekolah)
        schol = {'name':'','type':'','study':'','time':''}

        if length == 3:
          schol.update({'name':data_sekolah[0],'type':data_sekolah[1],'time':data_sekolah[2]})
        elif length == 4:
          schol.update({'name':data_sekolah[0],'type':data_sekolah[1],'study':data_sekolah[2],'time':data_sekolah[3]})

        self.education.append(schol)

    # Informasi Tentang Pekerjaan
    kerja = self.__res.find('div', id = 'work')

    if kerja is not None:
      loker = kerja.findAll('img', alt = re.compile('(.*), profile picture'))

      for echa in loker:
        moya = echa.find_next('div')
        if moya is None: continue

        # Alay dikit gak papa lah:V
        rahmat_sayang_khaneysia = moya.findAll(text = True)
        rahmat_cinta_khaneysia = rahmat_sayang_khaneysia[0] # Nama Pekerjaan
        love_you_khaneysia = list(filter(lambda chaa: re.match('^(\d{1}|\d{2}|\u200f)(\d{1}|\d{2}|\s)(.*?)\s-(.*?)$',chaa),rahmat_sayang_khaneysia)) # Waktu Kerja
        love_you_khaneysia = (love_you_khaneysia[0] if len(love_you_khaneysia) != 0 else '')

        self.work.append({'name':rahmat_cinta_khaneysia,'time':love_you_khaneysia})

    # Informasi Tentang tempat tinggal
    rumah = self.__res.find('div', id = 'living')

    if rumah is not None:

      for rumah_mantan in rumah.findAll('a', href = re.compile('\/editprofile\.php')):
        rumah_mantan.extract()

      for span in rumah.findAll('span', attrs = {'aria-hidden':True}):
        span.extract()

      self.living.update(self.__list_to_dict([i.text for i in rumah.findAll('td')][2:]))

    # Informasi Tentang Nama Lain

    nama_lain = self.__res.find('div', id = 'nicknames')

    if nama_lain is not None:

      for y in nama_lain.findAll('span', attrs = {'aria-hidden':True}):
        y.extract()

      for x in nama_lain.findAll('a', href = re.compile('^\/profile\/edit\/info\/nicknames')):
        x.extract()

      nama_ku = nama_lain.findAll(text = True)
      nama_ku.pop(0)

      if len(nama_ku) % 2 == 1: nama_ku.pop(2)

      self.other_name = self.__list_to_dict(nama_ku)

    # Informasi tentang Hubungan Percintaan:V
    cinta = self.__res.find('div', id = 'relationship')

    if cinta is not None:
      for cinta_itu_palsu in cinta.findAll('a', href = re.compile('\/editprofile\.php')):
        cinta_itu_palsu.extract()

      cinta_ku = cinta.findAll(text = True)
      cinta_ku.pop(0)

      self.relationship = ' '.join(cinta_ku)

    # Informasi Tentang Anggota Keluarga
    # Harta Yang Paling Berharga Adalah Keluarga :) #
    keluarga = self.__res.find('div', id = 'family')

    if keluarga is not None:
      keluarga_ku = keluarga.findAll('img', alt = re.compile('(.*), profile picture'))

      for family in keluarga_ku:

        name = family.find_next('a')
        profile_pict = family["src"]
        username = re.search("^\/[a-zA-Z0-9_.-]+",name['href']).group(0)
        designation = name.find_next('h3')

        self.family.append({'name':name.text,'username':username,'designation':designation.text,'profile_pict':profile_pict})


    # Informasi Tentang Peristiawa Penting Dalam Hidup #
    kejadian = self.__res.find('div', id = 'year-overviews')

    if kejadian is not None:
      data_kejadian = {}
      tahun = kejadian.findAll('div', text = re.compile('\d{4}'))

      for y in tahun:
        div_kejadian = y.find_next('div', text = re.compile('\d{4}'))

        # 23-08-2021 #
        khaneysia = (div_kejadian.find_all_previous('a', href = re.compile('^\/[a-zA-Z0-9_.-]+\/(posts|timeline)')) if div_kejadian is not None else y.find_all_next('a', href = re.compile('^\/[a-zA-Z0-9_.-]+\/(posts|timeline)')))
        nabila = []
        zahra = y.text

        # Khaneysia Nabila Zahra, I Love you :) #
        khaneysia.reverse()

        for rahmet in khaneysia:
          nabila.append(rahmet.text)
          rahmet.extract()

        # 22/11/2021 #

        self.year_overviews.append({'year':zahra,'overviews':nabila})

    # Kutipan Favotite
    kutipan = self.__res.find('div', id = 'quote')

    if kutipan is not None:
      for x in kutipan.findAll('a', href = re.compile('^\/profile\/edit\/')):
        x.extract()

      content = kutipan.findAll(text = True)
      content.pop(0)
      if ' · ' in content: content.remove(' · ')

      self.quote = '\n'.join(content)

    # Informasi Kontak
    self.contact_info = self.__get_data_by_div(div_id = 'contact-info', tag_to_find = 'td', attrs = {'valign':'top'})
    if 'Facebook' in self.contact_info.keys(): self.username = self.contact_info['Facebook'].strip()

    # Informasi Umum
    self.basic_info = self.__get_data_by_div(div_id = 'basic-info', tag_to_find = 'td', attrs = {'valign':'top'})

    self.name = ' '.join(pisah)

    self.__user_info['name'] = self.name
    self.__user_info['first_name'] = self.first_name
    self.__user_info['middle_name'] = self.middle_name
    self.__user_info['last_name'] = self.last_name
    self.__user_info['alternate_name'] = self.alternate_name
    self.__user_info['about'] = self.about
    self.__user_info['username'] = self.username
    self.__user_info['id'] = self.id
    self.__user_info['contact_info'] = self.contact_info
    self.__user_info['profile_pict'] = self.profile_pict
    self.__user_info['basic_info'] = self.basic_info
    self.__user_info['education'] = self.education
    self.__user_info['work'] = self.work
    self.__user_info['living'] = self.living
    self.__user_info['relationship'] = self.relationship
    self.__user_info['other_name'] = self.other_name
    self.__user_info['family'] = self.family
    self.__user_info['year_overviews'] = self.year_overviews
    self.__user_info['quote'] = self.quote

    cookie_dict = self.__session.cookies.get_dict()
    self.__this_is_me = (self.id == cookie_dict['c_user'] if 'c_user' in cookie_dict.keys() else None)

  def __str__(self):
    return "Facebook User : name='%s' id=%s username='%s'" % (self.__user_info['name'], self.__user_info['id'], self.__user_info['username'])

  def __repr__(self):
    return "Facebook User : name='%s' id=%s username='%s'" % (self.__user_info['name'], self.__user_info['id'], self.__user_info['username'])

  def __getitem__(self, key):
    return (self._user_info[key] if key in self._user_info.keys() else None)

  @property
  def _user_info(self):
    return self.__user_info.copy()

  def __list_to_dict(self,list_):
   keys = []
   value = []
   data = {}

   for x in range(len(list_)):
     if x % 2 == 0:
       keys.append(list_[x])
     else:
       value.append(list_[x])

   for x in range(len(keys)):
     data.update({keys[x]:value[x]})

   return data

  def __get_data_by_div(self,div_id,tag_to_find, attrs = {}):
    data_info = self.__res.find('div', id = div_id)

    data_list = []

    if data_info is not None:
      for x in data_info.findAll(tag_to_find, attrs = attrs):
        data_list.append(re.sub('· (.*)','',x.text).strip())
      return self.__list_to_dict(data_list)

    else:
      return {}

  def __get_images(self, tag_object):
    data = {'thumbnail':None,'photo':None,'albums':None,'albums_url':None}

    try:
      thumbnail = tag_object.find('img')['src']
      photo_url = self.__host + tag_object['href']
      req = self.__session.get(photo_url)
      res = bs4(req.text,'html.parser')
      photo = res.find('img', src = re.compile('^https:\/\/(?:z-m-scontent|scontent)(.*)'))
      albums = res.find('a', href = re.compile('^\/[a-zA-Z0-9_.-]+\/albums'))

      if photo is not None: data.update({'photo':photo['src']})

      if albums is not None:
        data.update({'albums':albums.text})
        data.update({'albums_url':(self.__host + albums["href"])})

      data.update({'thumbnail':thumbnail})

    finally:
      return data

  def refresh(self):
    self.__init__(username = self.__usr, requests_session = self.__session)
    return True

  def get(self, item):
    return self[item]

  def poke(self):
    if self.__this_is_me: raise exceptions.FacebookError('Tidak dapat malakukan Poke ke akun anda!')

    colek = self.__res.find('a', href = re.compile('^\/pokes\/inline\/\?poke_target=\d+'))

    if colek is None: return False

    req = self.__session.get(self.__host + colek['href'])
    gagal = bs4(req.text,'html.parser').find(text = re.compile(self.name + '\s(.*?)$'))

    if gagal: raise exceptions.FacebookError(gagal)

    return req.ok

  def message(self):
    chat_url = self.__res.find('a', href = re.compile('^\/messages\/thread\/\d+(.*)'))

    if chat_url is None: raise exceptions.FacebookError("Tidak Bisa mengirim chat ke %s" % (self.name))

    return Chats(self.__host + chat_url['href'], self.__session)

  def send_text(self, message):
    return self.message().send_text(message)

  def block_user(self):
    if self.__this_is_me : raise exceptions.FacebookError('Hadeh, lu kira bisa apa ngeblokir akun sendiri???')

    block_url = self.__res.find('a', href = re.compile('^\/privacy\/touch\/block\/confirm'))

    if block_url is None: return False

    req = self.__session.get(self.__host + block_url['href'])
    res = bs4(req.text,'html.parser')

    form = res.find('form', action = re.compile('^\/privacy\/touch\/block\/'))
    data = {}

    for x in form.findAll('input'):
      if x.get('name') == 'canceled': continue
      data[x.get('name')] = x.get('value')

    req = self.__session.post(self.__host + form['action'], data = data)
    res = bs4(req.text,'html.parser')

    sukses = res.find('a', href = re.compile('^\/privacy\/touch\/block\/\?block_result=0'))

    hasil = (True if sukses else False)

    if hasil: self._user_info.clear()

    return hasil

  def __action_user(self, re_compiled):
    if self.__this_is_me:  raise exceptions.FacebookError("Tidak dapat melakukan tindakan yang anda minta!")

    acc = self.__res.find('a', href = re_compiled )

    if acc is None: return False

    data = {
            'jazoest': self.__res.find('input', attrs = {'name':'jazoest'}).get('value'),
            'fb_dtsg': self.__res.find('input', attrs = {'name':'fb_dtsg'}).get('value')
           }

    req = self.__session.get(self.__host + acc['href'], data = data)

    self.__res = bs4(req.text,'html.parser')

    return req.ok

  def add_friends(self):
    return self.__action_user(re_compiled = re.compile('^\/a\/friends\/profile\/add'))

  def cancel_friends_requests(self):
    return self.__action_user(re_compiled = re.compile('\/a\/friendrequest\/cancel\/\?subject_id=\d+'))

  def accept_friends_requests(self):
    return self.__action_user(re_compiled = re.compile('\/a\/friends\/profile\/add\/\?subject_id=\d+(.*)is_confirming'))


  def delete_friends_requests(self):
    return self.__action_user(re_compiled = re.compile('\/a\/(.*)\/friends\/reject\/\?subject_id=\d+'))

  def remove_friends(self):
    if self.__this_is_me: raise exceptions.FacebookError("Terjadi Kesalahan!")

    confirm_url = self.__res.find('a', href = re.compile('\/removefriend\.php\?friend_id=\d+'))

    if confirm_url is None: return False

    c = self.__session.get(self.__host + confirm_url['href'])
    d = bs4(c.text,'html.parser')

    form = d.find('form', action = re.compile('\/a\/friends\/remove\/\?subject_id=\d+'))
    remove_url = self.__host + form["action"]
    data = {}

    for x in form.findAll('input'):
      data[x.get('name')] = x.get('value')

    req = self.__session.post(remove_url, data = data)

    self.__res = bs4(req.text,'html.parser')

    return req.ok

  def follow(self):
    return self.__action_user(re_compiled = re.compile('^\/a\/subscribe\.php\?id=\d+'))

  def unfollow(self):
    return self.__action_user(re_compiled = re.compile('^\/a\/subscriptions\/remove\?(.*?)'))

  def get_friends(self, limit = 25, return_dict = True):
    teman = []
    url = self.__res.find('a', href = re.compile('\/((.*)\/friends\?lst=|profile\.php\?id=\d+(.*?)v=friends|profile\.php\?v=friends)'))

    if url is None:
      a = self.__session.get(self.__host + '/' + self.__usr)
      b = bs4(a.text,'html.parser')

      url = b.find('a', href = re.compile('\/((.*)\/friends\?lst=|profile\.php\?id=\d+(.*?)v=friends|profile\.php\?v=friends)'))

      if url is None: return teman

    c = self.__host + url['href']
    d = self.__session.get(c)
    e = bs4(d.text,'html.parser')

    while len(teman) < limit:
      datas = e.findAll('img', alt = re.compile('(.*), profile picture'), src = re.compile('https:\/\/z-m-scontent(.*)\.fbcdn\.net'))
      del datas[0]

      if return_dict:
        for f in datas:
          profile = f.find_next('a', href = re.compile('(^\/profile\.php|^\/(.*)\?)'))
          username = re.search('(^\/profile.php\?id=(\d+)|^\/([a-zA-Z0-9_.-]+))',profile['href']).group((2 if 'profile.php' in profile['href'] else 3))
          nama = profile.text
          foto_pp = f['src']
          teman.append({'name':nama, 'profile_pict':foto_pp,'username':username})
      else:
        th = ThreadPool(10)
        th_data = []

        for f in datas:
          profile = f.find_next('a', href = re.compile('(^\/profile\.php|^\/(.*)\?)'))
          username = re.search('(^\/profile.php\?id=(\d+)|^\/([a-zA-Z0-9_.-]+)\?)',profile['href'])
          if username is None: continue
          th_data.append(username.group((2 if 'profile.php' in profile['href'] else 3)))
        th.map(lambda x: teman.append(User(username = x, requests_session = self.__session)),th_data)

      next_uri = e.find('a', href = re.compile('^\/[a-zA-Z0-9_.-]+\/friends\?unit_cursor=\w+'))
      if len(teman) >= limit or next_uri is None: break
      d = self.__session.get(self.__host + next_uri['href'])
      e = bs4(d.text,'html.parser')

    return teman[0:limit]

  def get_mutual_friends(self, limit = 25, return_dict = True):
    if self.__this_is_me: raise exceptions.FacebookError('Terjadi Kesalahan!')

    sama = []

    a = self.__session.get(self.__host + '/' + str(self.__usr) +'?v=friends&mutual=1')
    b = bs4(a.text,'html.parser')

    if b.find('a', href = re.compile('\/home\.php\?rand=\d+')): raise exceptions.PageNotFound("Akun dengan username \"%s\" Tidak di temukan!" % (username))

    while len(sama) < limit:
      datas = b.findAll('img', alt = re.compile('(.*), profile picture'), src = re.compile('https:\/\/z-m-scontent(.*)\.fbcdn\.net'))

      if return_dict:
        for f in datas:
          profile = f.find_next('a', href = re.compile('(^\/profile\.php|^\/(.*)\?)'))
          username = re.search('(^\/profile.php\?id=(\d+)|^\/([a-zA-Z0-9_.-]+))',profile['href']).group((2 if 'profile.php' in profile['href'] else 3))
          nama = profile.text
          foto_pp = f['src']
          sama.append({'name':nama, 'profile_pic':foto_pp,'username':username})
      else:
        th = ThreadPool(8)
        th_data = []
        for f in datas:
          profile = f.find_next('a', href = re.compile('(^\/profile\.php|^\/(.*)\?)'))
          username = re.search('(^\/profile.php\?id=(\d+)|^\/([a-zA-Z0-9_.-]+)\?)',profile['href'])
          if username is None: continue
          th_data.append(username.group((2 if 'profile.php' in profile['href'] else 3)))
        th.map(lambda x: sama.append(User(username = x, requests_session = self.__session)),th_data)

      next_uri = b.find('a', href = re.compile('^\/[a-zA-Z0-9_.-]+\/friends\?startindex=\d+\&mutual=\d+'))
      if len(sama) >= limit or next_uri is None: break
      a = self.__session.get(self.__host + next_uri['href'])
      b = bs4(a.text,'html.parser')

    return sama[0:limit]

  def get_photo(self, limit = 5, albums_url = None):
    if albums_url is not None and not re.match('^https:\/\/(.*?)\.facebook\.com\/[a-zA-Z0-9_.-]+\/albums\/\d+\/(.*)',albums_url): raise exceptions.PageNotFound("URL Tidak Valid, Coba Periksa Kembali URL Anda!!!")

    my_photo = []

    if albums_url is None:
      a = self.__res.find('a', href = re.compile('^\/((.*?)\/photos\?(.*)|profile\.php\?id=\d+(.*)v=photos)'))

      if a is None: return my_photo

      b = self.__session.get(self.__host + a['href'])
      c = bs4(b.text,'html.parser')
    else:
      a = self.__session.get(albums_url)
      c = bs4(a.text,'html.parser')

      if c.find('a', href = re.compile('\/home\.php\?rand=\d+')): raise exceptions.PageNotFound("Oops!\nAlbums tidak di temukan, anda mungkin tidak memiliki akses untuk melihat album ini, atau mungkin album tersebut sudah di hapus!!")

    while len(my_photo) < limit:
      img = c.findAll('a', href = re.compile('^\/photo\.php'))
      if len(img) < 1: break
      img.pop(0)

      Thread = ThreadPool(8)

      my_photo.extend(Thread.map(self.__get_images, img))
      next_uri = c.find('a', href = re.compile('^\/[a-zA-Z0-9_.-]+\/photoset'))

      if next_uri is None or len(my_photo) >= limit: break

      b = self.__session.get(self.__host + next_uri['href'])
      c = bs4(b.text,'html.parser')

    return my_photo[0:limit]

  def get_albums(self, limit = 5):
    my_albums = []

    a = self.__res.find('a', href = re.compile('^\/((.*?)\/photos\?(.*)|profile\.php\?id=\d+(.*)v=photos)'))
    if a is None: return my_photo

    b = self.__session.get(self.__host + a['href'])
    c = bs4(b.text,'html.parser')

    while len(my_albums) < limit:
      album = c.findAll('a', href = re.compile('^\/[a-zA-Z0-9_.-]+\/albums\/'))

      for x in album:
        album_url = re.search("(^\/[a-zA-Z0-9_.-]+\/albums\/\d+\/)",x['href'])
        album_url = self.__host + (album_url.group(0) if album_url is not None else x['href'])

        album_name = x.text
        my_albums.append({'albums_name':album_name,'albums_url':album_url})

      next_uri = c.find('a', href = re.compile('^\/[a-zA-Z0-9_.-]+\/photos\/albums'))

      if next_uri is None or len(my_albums) >= limit: break

      b = self.__session.get(self.__host + next_uri['href'])
      c = bs4(b.text,'html.parser')

    return my_albums[0:limit]

  def get_posts(self, limit = 5):
    post_data = []

    timeline_url = self.__res.find('a', href = re.compile('^\/([a-zA-Z0-9_.-]+\?v=timeline|profile\.php\?id=\d+(.*?)v=timeline)'))
    timeline_url = (self.__host + timeline_url['href'] if timeline_url is not None else self.__host + '/' + str(self.__usr) + '?v=timeline')

    a = self.__session.get(timeline_url)

    while len(post_data) < limit:
      b = bs4(a.text,'html.parser')
      c = b.findAll('div', role = 'article')

      for d in c:
        url = d.find('a', href = re.compile('^\/(story\.php\?story_fbid|[a-zA-Z0-9_.-]+\/posts\/)'), class_ = False)
        if url is None: continue
        post_data.append(Posts(self.__session, self.__host + url['href'], json.loads(d.get('data-ft'))))
        if len(post_data) >= limit: break

      next_uri = b.find('a', href = re.compile('\/profile\/timeline\/stream\/\?cursor'))
      if len(post_data) >= limit or next_uri is None: break
      a = self.__session.get(self.__host + next_uri['href'])

    return post_data[0:limit]

  def create_timeline(self, message, file = None, location = None,feeling = None,filter_type = '-1', **kwargs):
    message = codecs.decode(codecs.encode(message,'unicode_escape'),'unicode_escape')

    form = self.__res.find('form', method = 'post', action = re.compile('^\/composer\/mbasic'))
    data = {}
    data_other = {}
    data_other_list_key = ['view_privacy','view_photo','view_mle','view_withtag','view_location','view_minutiae','view_album','view_post']

    if form is None:
      a = self.__session.get(self.__host + '/' + str(self.__usr) + '?v=timeline')
      b = bs4(a.text,'html.parser')
      form = b.find('form', method = 'post', action = re.compile('^\/composer\/mbasic'))

    if form is None: raise exceptions.FacebookError('Tidak dapat menulis timeline ke akun %s' % (self.name))

    for x in form.findAll("input"):
      if x.get('name') in data_other_list_key:
        data_other[x.get('name')] = x.get('value')
      else:
        data[x.get('name')] = x.get('value')

    timeline = self.__session.post(self.__host + form["action"], data = data)
    form = bs4(timeline.text,'html.parser').find('form', method = 'post', action = re.compile('^\/composer\/mbasic'))
    data_other_list_key.append('view_overview')

    for x in form.findAll("input"):
      if x.get('name') in data_other_list_key:
        data_other[x.get('name')] = x.get('value')
      else:
        data[x.get('name')] = x.get('value')

    submit_url = self.__host + form['action']
    submit_data = data

    if location is not None:
      location_data = data.copy()
      location_data['view_location'] = data_other['view_location']
      data_other_list_key.remove('view_location')

      lokasi_data = {}
      lokasi_url = self.__session.post(self.__host + form['action'], data = location_data)
      lokasi_parse = bs4(lokasi_url.text,'html.parser')

      lokasi_form = lokasi_parse.find('form', action = re.compile('^\/places\/selector'))
      for x in lokasi_form.findAll('input'): lokasi_data[x.get('name')] = x.get('value')

      lokasi_data.update({'query':location})
      cari_lokasi = self.__session.get(self.__host + lokasi_form['action'], params = lokasi_data)

      ketemu = bs4(cari_lokasi.text,'html.parser').find('a', href = re.compile('\/composer\/mbasic\/(.*)at=\d+'))
      if ketemu is None: raise exceptions.FacebookError("Lokasi dengan nama \"%s\" tidak di temukan!!!!" % (location))

      id_lokasi = re.search('at=(\d+)', ketemu['href']).group(1)
      submit_data.update({'at':id_lokasi})

    if feeling is not None:
      feeling = feeling.lower()
      feeling_data = data.copy()
      feeling_data['view_minutiae'] = data_other['view_minutiae']
      data_other_list_key.remove('view_minutiae')

      perasaan_data = {}
      perasaan_url = self.__session.post(self.__host + form['action'], feeling_data)
      perasaan_parse = bs4(perasaan_url.text,'html.parser')

      perasaan_ku = perasaan_parse.find('a', href = re.compile('\/composer\/mbasic\/\?ogaction=\d+'), attrs = {'aria-hidden':False})
      kunjungi_hati_ku = self.__session.get(self.__host + perasaan_ku['href'])
      hati_parse = bs4(kunjungi_hati_ku.text,'html.parser')
      perasaan_list = {i.text.lower():i['href'] for i in hati_parse.findAll('a', href = re.compile('\/composer\/mbasic\/\?ogaction='))}

      if feeling in perasaan_list.keys(): feeling_ku = self.__host + perasaan_list[feeling]
      else:
        perasaan_form = hati_parse.find('form', action = re.compile('\/composer\/mbasic'))
        params = {i.get('name'):i.get('value') for i in perasaan_form.findAll('input')}
        params['mnt_query'] = feeling

        cari_perasaan = self.__session.get(self.__host + perasaan_form["action"], params = params)
        feeling_ku = self.__host + bs4(cari_perasaan.text,'html.parser').find('a', href = re.compile('\/composer\/mbasic\/\?ogaction='), attrs = {'aria-hidden':False})['href']

      feeling_url = self.__session.get(feeling_ku)

      for x in bs4(feeling_url.text,'html.parser').findAll('input'):
        if x.get('name') in data_other_list_key: continue
        submit_data[x.get('name')] = x.get('value')


    if file is not None:
      file_data = data.copy()
      file_data['view_photo'] = data_other['view_photo']
      data_other_list_key.remove('view_photo')

      max_size = (1000000*4) # Maksimal Ukuran File
      support_file = ['.jpg','.png','.webp','.gif','.tiff','.heif']
      ext = os.path.splitext(file)[-1]
      if not ext in support_file: raise exceptions.FacebookError("Hanya bisa mengupload file dengan extensi \"%s\", tidak bisa mengupload file dengan extensi \"%s\"" % (', '.join([re.sub('^\.','',ext_file) for ext_file in support_file]),ext))
      if os.path.getsize(file) > max_size: raise exceptions.FacebookError('Ukuran file "%s"  terlalu besar, sehingga file tersebut tidak bisa di upload, File harus  berukuran kurang dari %s :)' % (os.path.realpath(file), utils.convert_size(max_size)))

      upload_data = {}
      upload_url = self.__session.post(self.__host + form['action'], data = file_data)
      upload_parse = bs4(upload_url.text,'html.parser')

      upload_form = upload_parse.find('form', action = re.compile('^\/composer\/mbasic'))

      for x in upload_form.findAll('input'): upload_data[x.get('name')] = x.get('value')

      upload_data.update({'filter_type':filter_type})

      upload_data['file1'] = os.path.basename(file)
      my_files = {'file1':open(file,'rb')}
      preview = self.__session.post(self.__host + upload_form['action'], data = upload_data, files = my_files)
      preview_form = bs4(preview.text,'html.parser').find('form', action = re.compile('\/composer\/mbasic'))
      preview_data = {}

      for x in preview_form.findAll('input'):
        if x.get('name') in data_other_list_key: continue
        preview_data[x.get('name')] = x.get('value')

      submit_url = self.__host + preview_form['action']
      submit_data.update(preview_data)

    for x in data_other_list_key:
      if not x in submit_data.keys(): continue
      submit_data.pop(x)

    submit_data.update({form.find('textarea').get('name'):message}) 
    submit_data.update({'view_post':data_other['view_post']})
    submit_data.update(kwargs)

    kirim = self.__session.post(submit_url, data = submit_data)

    urls = re.search("next=(.*)", kirim.url)
    if urls is not None: kirim = self.__session.get(requests.utils.unquote(urls.group(1)))

    return kirim.ok

