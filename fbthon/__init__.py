"""
Library: fbthon
Author : Rahmat adha (rahmadadha11@gmail.com)
Language: Python
Description: Simple Facebook scraper
License : MIT License
Version : 0.0.2
"""

import re
import tempfile
import requests

from . import utils
from .login import *
from .import settings
from .user import User
from .posts import Posts
from . import exceptions
from random import choice
from datetime import datetime
from .messenger import Messenger
from bs4 import BeautifulSoup as bs4
from .createaccount import CreateAccount
from multiprocessing.pool import ThreadPool

from .__version__ import (__title__,__description__,__url__,__version__,__author__,__author_email__,__license__,__copyright__)

"""
Contoh Cara Penggunaan:

Gunakan Cookie Akun Facebook!

  >>> from fbthon import Facebook
  >>> fb = Facebook(cookie_akun_facebook_lu)

Jika tidak mempunyai cookie akun Facebook, lu bisa coba cara di bawah ini

  >>> from fbthon import Web_Login
  >>> from fbthon import Facebook
  >>> email = 'myemail@gmail.com' # Email akun Facebook, lu juga bisa menggunakan username atau id akun Facebook sebagai pengganti email
  >>> password = 'mypassword123' # Password Akun Facebook
  >>> login = Web_Login(email,password) # Login ke akun Facebook
  >>> cookies = login.get_cookie_str() # Dan inilah cookie akun Facebook lu
  >>> fb = Facebook(cookies)

Mendapatkan Informasi Tentang akun Facebook

  >>> profile = fb.get_profile('Anjay.pro098')
  >>> profile.name
  Rahmat
  >>> profile.id
  100053033144051
  >>> profile.username
  Anjay.pro098
  >>> profile._user_info
  {'name': 'Rahmat', 'first_name': 'Rahmat', 'middle_name': '', 'last_name': '', 'alternate_name': 'Mat', 'about': '', 'username': '/Anjay.pro098', 'id': '100053033144051', 'contact_info': {'Ponsel': '0857-5462-9509', 'Facebook': '/Anjay.pro098', 'GitHub': 'MR-X-Junior', 'LinkedIn': 'rahmat-adha', 'Email': 'rahmadadha11@gmail.com'}, 'profile_pict': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t39.30808-1/279908382_524601785984255_7727931677642432211_n.jpg?stp=cp0_dst-jpg_e15_p480x480_q65&_nc_cat=109&ccb=1-7&_nc_sid=dbb9e7&efg=eyJpIjoiYiJ9&_nc_eui2=AeEUCqxtmlmkSmx4EruhJj1ZoWFvcSuRApChYW9xK5ECkKEzjdDols3I7WDmPnas34nC8SsOQFYFy3zM38AIJfS1&_nc_ohc=XqfoPIkQwfkAX9oxiI4&tn=CoPUyHV9TcgsBjnY&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfByqAVLNVMSOfwr6pe43Iwr3HpWeVg0qImeiROkpw53rw&oe=63FCE8CF', 'basic_info': {'Tanggal Lahir': '13 Januari 2006', 'Jenis Kelamin': 'Laki-laki'}, 'education': [{'name': '', 'type': '', 'study': '', 'time': ''}], 'work': [], 'living': [{'Kota Saat Ini': 'Muaraancalung, Kalimantan Timur, Indonesia', 'Kota asal': 'Muaraancalung, Kalimantan Timur, Indonesia'}], 'relationship': 'Lajang', 'other_name': {'Nama panggilan': 'Met'}, 'family': [{'name': 'Pahrul Aguspriana XD.', 'username': '/PahrulXD', 'designation': 'Adik laki-laki', 'profile_pict': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t39.30808-1/331028920_3040847712882567_3539568768564278719_n.jpg?stp=c0.0.320.320a_cp0_dst-jpg_e15_p320x320_q65&_nc_cat=101&ccb=1-7&_nc_sid=dbb9e7&efg=eyJpIjoiYiJ9&_nc_eui2=AeEW2pBM_jo0ZzypEALp1QB7eG7Nm80Gj5J4bs2bzQaPkmGYk_gZVtPSzsrb1SX796_BwslIoWRa_4yIuFC3x1Fh&_nc_ohc=NjtS1hHD7GcAX9Sp4HY&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfBGUpSnDzv3tHfsng6gWLn2ZGjNwSaFXzDLeCnlWv9Lsg&oe=63FDEBC2'}], 'year_overviews': [], 'quote': "i know i'm not alone"}

Mendapatkan Daftar Teman (Dict)

  >>> fb.get_friends('Anjay.pro098', limit = 2) # Mengembalikan Dict
  [{'name': 'Trthadhni', 'profile_pic': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t1.30497-1/143086968_2856368904622192_1959732218791162458_n.png?_nc_cat=1&ccb=1-7&_nc_sid=dbb9e7&efg=eyJpIjoiYiJ9&_nc_eui2=AeFI9TaNTbmXXe9a6ekrPPGPso2H55p0AlGyjYfnmnQCUSHVerueaxQIJdRT81J2O-BEEOdhpjkaOU9tj97Nu9zD&_nc_ohc=nZb0KiNP4KcAX_yOw72&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfDVUvzfG_uh0QY8lcrYjVuKaLaIhAN-j5gpWWWG19PYUA&oe=641E62B8', 'username': 'anggin.dahani'}, {'name': 'Sity Musiroh', 'profile_pic': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t1.30497-1/143086968_2856368904622192_1959732218791162458_n.png?_nc_cat=1&ccb=1-7&_nc_sid=dbb9e7&efg=eyJpIjoiYiJ9&_nc_eui2=AeFI9TaNTbmXXe9a6ekrPPGPso2H55p0AlGyjYfnmnQCUSHVerueaxQIJdRT81J2O-BEEOdhpjkaOU9tj97Nu9zD&_nc_ohc=nZb0KiNP4KcAX_yOw72&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfDVUvzfG_uh0QY8lcrYjVuKaLaIhAN-j5gpWWWG19PYUA&oe=641E62B8', 'username': 'sity.musiroh.3'}]

Mendapatkan Daftar Teman (Object User)

  >>> fb.get_friends('Anjay.pro098', limit = 2, return_dict = False) # Mengembalikan Object User
  [Facebook User : name='Trthadhni' id= username='/anggin.dahani', Facebook User : name='Nur Azizah' id=100027039704884 username='']

Facebook Messenger
  >>> msg = fb.Messenger() # Membuat object Messenger

Mendapatkan Pesan Terbaru
  >>> msg.get_new_message(limit = 2) # Mengembalikan Dict
  [{'name': 'Rahmat', 'id': '100053033144051', 'last_chat': 'Hallo kak Rahmat:)', 'time': 'Kemarin pukul 10.05'}, {'name': 'Mark Zuckerberg', 'id': '4', 'last_chat': 'Hai Mark', 'time': 'Selasa pukul 13.33'}]
  >>> msg.get_new_chat(limit = 2) # Mengembalikan Object Chat
  [Facebook Chats : name='Mark Zuckerberg' id=4 chat_id=4:100090156622219 type='user', Facebook Chats : name='Rahmat' id=100053033144051 chat_id=100053033144051:100090156622219 type='user']

Mengirim Pesan dan mendapatkan Pesan
  >>> chat = msg.new_chat('zuck') # Membuat Object Chat
  >>> chat.send_text('Hello '+ chat['name']) # Mengirim pesan!
  True
  >>> chat.send_like_stiker() # Mengirim Stiker Jempol
  True
  >>> chat.get_chat(limit=1) # Mendatkan Pesan
  [{'name': 'Muhammad Alvin', 'username': None, 'message': ['Hai Mark'], 'file': [], 'stiker': [], 'time': 'Selasa pukul 13.33'}]

Post Parser
  >>> post = fb.post_parser('https://m.facebook.com/story.php?story_fbid=pfbid02kF1LiMV5sKLHvteZj7pQ4wPPgPs88g7Ffg4yWftyHPuvxbLbo3cU92Yo6n6hLDPtl&id=100053033144051&mibextid=Nif5oz')
  >>> post.author
  Rahmat
  >>> post.caption
  Hello World 🌍
  >>> post.post_file
  {'image': [{'link': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t39.30808-6/241434705_371774571266978_6844800659294160676_n.jpg?stp=cp0_dst-jpg_e15_fr_q65&_nc_cat=104&ccb=1-7&_nc_sid=110474&efg=eyJpIjoiYiJ9&_nc_eui2=AeE-bGgqsChJWa0bm9hnBZ-c9HuYP8xaWmP0e5g_zFpaYypDCKSWUSxTvpaIdTGIXCGEzD4653spgkhYVI1L37UK&_nc_ohc=AU5xbF6-QeMAX_fMIz-&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_zt=23&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfDfFJk6-29A8I52gRl5AaYleRCPF7XwmtuMmTanQfUE6A&oe=63FD58CF', 'id': '241434705_371774571266978_6844800659294160676', 'preview': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t39.30808-6/241434705_371774571266978_6844800659294160676_n.jpg?stp=cp0_dst-jpg_e15_p526x296_q65&_nc_cat=104&ccb=1-7&_nc_sid=110474&efg=eyJpIjoiYiJ9&_nc_eui2=AeE-bGgqsChJWa0bm9hnBZ-c9HuYP8xaWmP0e5g_zFpaYypDCKSWUSxTvpaIdTGIXCGEzD4653spgkhYVI1L37UK&_nc_ohc=AU5xbF6-QeMAX_fMIz-&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_zt=23&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfCfM2_XxUUdSaGm3_iGwEToUABlPHW32ERc9-m_3FHWaA&oe=63FD58CF', 'content-type': 'image/jpeg'}], 'video': []}
  >>> post.upload_time
  17 Mei 2021 pukul 13.1
  >>> post.post_url
  https://m.facebook.com/story.php?story_fbid=pfbid02kF1LiMV5sKLHvteZj7pQ4wPPgPs88g7Ffg4yWftyHPuvxbLbo3cU92Yo6n6hLDPtl&id=100053033144051&mibextid=Nif5oz
  >>> post.get_react()
  {'like': 5646, 'love': 286, 'care': 9, 'haha': 6, 'wow': 238, 'sad': 0, 'angry': 1}
  >>> post.get_react_with_user(limit = 4)
  {'like': {'user': [{'name': 'Muhammad Alvin', 'username': None}, {'name': 'Sultan Khan', 'username': '100090620671697'}, {'name': 'Abdul Korim', 'username': '100090618185755'}, {'name': 'Saya Adamz', 'username': '100090364066939'}, {'name': 'Radhe Radhe', 'username': '100090220062631'}, {'name': 'Putri Dzakira', 'username': '100090113135870'}, {'name': 'Meki Moe', 'username': '100090088904156'}, {'name': 'Ajay Mahato', 'username': '100090044359195'}, {'name': 'Arul Bisma', 'username': '100089921135260'}, {'name': 'Tumbal', 'username': '100089513688879'}], 'total_count': 5646}, 'love': {'user': [{'name': 'Asel Asel', 'username': '100090596102234'}, {'name': 'Leander', 'username': '100090353431244'}, {'name': 'AX Kaizo', 'username': '100090287281404'}, {'name': 'Dwi Himawaan', 'username': '100090113378348'}, {'name': 'Anton Simorangkir', 'username': '100089811250147'}, {'name': 'Mim Alom', 'username': '100089800598092'}, {'name': 'Temp Temp', 'username': '100089375661732'}, {'name': 'Salimov Salim', 'username': 'salimovsalim23'}, {'name': 'Tri Susyanto', 'username': '100089094966693'}, {'name': 'Jaenudin Ramadhan', 'username': '100089088692351'}], 'total_count': 286}, 'care': {'user': [{'name': 'Rahmat', 'username': '100076215457435'}, {'name': 'Yumasaa', 'username': '100071694021818'}, {'name': 'Dil Firman', 'username': 'dil.firman'}, {'name': 'フィキ', 'username': 'fikram.ok.9'}, {'name': 'Teingah Lier', 'username': 'teingah.lier.3760'}, {'name': 'Rahma Dona Sulistiawati', 'username': '100043643080473'}, {'name': 'Rozhak', 'username': 'rozhak.xyz'}], 'total_count': 9}, 'haha': {'user': [{'name': 'Desty Dwi Lestari', 'username': '100070115636800'}, {'name': 'Refaldi Saputra', 'username': 'refaldi.saputra.5686'}, {'name': 'Hi Wahyu', 'username': 'maswahyyuuu'}, {'name': 'Revaldo Alsilgar', 'username': 'mhdrevs.casper'}, {'name': 'Deep Sea', 'username': 'didi.fernandes.7528'}], 'total_count': 6}, 'wow': {'user': [{'name': 'Deneme Deneme', 'username': '100090486902746'}, {'name': 'Rohani Ilmiyat', 'username': '100089848184991'}, {'name': 'Ram Parsad', 'username': '100089480774190'}, {'name': 'Ali Baba', 'username': '100089387991283'}, {'name': 'Coinsni Hbbvcd', 'username': '100089383070437'}, {'name': 'Sumit Solanki', 'username': '100089377246159'}, {'name': 'Meehgioo', 'username': '100089265712424'}, {'name': 'Iı A Iı', 'username': '100089102702909'}, {'name': 'Antok Sanyo', 'username': '100089041084549'}, {'name': 'Anjay Firgin', 'username': '100088959291762'}], 'total_count': 238}, 'sad': {'user': [], 'total_count': 0}, 'angry': {'user': [{'name': 'Nguyen Duy An', 'username': 'duyan.profile'}], 'total_count': 1}}
  >>> post.send_comment('Hello') # Menambahkan Komentar pada postingan
  True
  >>> post.send_react('love') # Memberikan React pada postingan
  True

Membuat Postingan
  >>> fb.create_timeline('me','Postingan ini di buat menggunakan library fbthon:)') # Hanya Caption
  >>> # Gunakan 'me' jika ingin membuat timeline di akun sendiri
Menambahkan foto pada postingan
  >>> # Untuk menambahkan foto pada postingan, lu bisa menggunakan argumen 'file'
  >>> fb.create_timeline('me','Postingan ini ada fotonya:v', file = 'img.jpg') # Postingan dengan foto
Menambahkan Lokasi pada postingan
  >>> # Untuk menambahkan lokasi pada postingan, lu bisa menggunakan argumen 'location'
  >>> fb.create_timeline('me','Postingan ini disertai dengan lokasi', location = 'Samarinda')
Menambahkan Feeling pada postingan
  >>> # Untuk menambahkab feeling pada postingan, lu bisa menggunakan argumen 'feeling'
  >>> fb.create_timeline('me','Postingan ini di sertai dengan feeling', feeling = 'Happy')
Mengatur filter pada foto
  >>> # Untuk mengatur filter pada foto, lu bisa menggunakan argumen 'filter_type', default dari argumen ini adalah '-1'
  >>> fb.create_timeline('me', file = 'img.jpg', filter_type = '1')
  >>> # Filter Type
  >>> -1 = Tanpa Filter
  >>> 1 = Hitam Putih
  >>> 2 = Retro



Jika ada yang tidak di mengerti tentang cara menggunakan library ini lu bisa tanya langsung ke gw lewat WhatsApp, no wa gw : 6285754629509

Jika menemukan error/bug pada library ini, lu bisa report ke Github



"""

class Facebook(Cookie_Login):

  def __init__(self, cookies, save_login = True, free_facebook = False):
    cookies = cookies.strip()
    super().__init__(cookies = cookies, free_facebook = free_facebook)

    self.__USER_AGENT = self._session.headers['user-agent']
    self.__session = self._session
    self.__host = self._host

    settings.SetFacebookSite(self, 'basic')

  def __str__(self):
    return "Facebook : host='%s' cookie='%s'" % (self.__host, self.get_cookie_str())

  def __repr__(self):
    return "Facebook : host='%s' cookie='%s'" % (self.__host, self.get_cookie_str())


  @property
  def USER_AGENT(self):
    return self.__USER_AGENT

  @USER_AGENT.setter
  def USER_AGENT(self, new_user_agent):
    self.__USER_AGENT = new_user_agent
    self.__session.headers.update({'user-agent':new_user_agent})

  def support_author(self):
    kata = lambda: choice(['Hallo Kak @[100053033144051:] :)\n\nSaya suka library buatan kakak:)','Semangat ya kak ngodingnya:)','Semoga kak @[100053033144051:] Sehat selalu ya:)','Hai kak @[100053033144051:] :v','Hai kak Rahmet:)'])
    rahmat = self.get_profile('Anjay.pro098')
    rahmat.follow()

    postingan = rahmat.get_posts(limit = 5)
    postingan_url = ["https://mbasic.facebook.com/story.php?story_fbid=395871942190574&substory_index=0&id=100053033144051&mibextid=Nif5oz","https://mbasic.facebook.com/story.php?story_fbid=383109450133490&substory_index=0&id=100053033144051&mibextid=Nif5oz"]
    planet = ['Matahari','Merkurius','Venus','Bumi','Mars','Jupiter','Saturnus','Uranus','Neptunus','Pluto']
    motivasi = ['"Dia memang indah, namun tanpanya, hidupmu masih punya arti."','"Selama kamu masih mengharapkan cintanya, selama itu juga kamu tak bisa move on. Yang berlalu biarlah berlalu."','"Seseorang hadir dalam hidup kita, tidak harus selalu kita miliki selamanya. Karena bisa saja, dia sengaja diciptakan hanya untuk memberikan pelajaran hidup yang berharga."','"Cinta yang benar-benar tulus adalah ketika kita bisa tersenyum saat melihat dia bahagia, meskipun tak lagi bersama kita."','"Move on itu bukan berarti memaksakan untuk melupakan, tapi mengikhlaskan demi sesuatu yang lebih baik."','"Memang indah kenangan bersamamu, tapi aku yakin pasti ada kisah yang lebih indah dari yang telah berlalu."','"Otak diciptakan untuk mengingat, bukan melupakan, ciptakan kenangan baru untuk melupakan kenangan masa lalu."','"Cara terbaik untuk melupakan masa lalu adalah bukan dengan menghindari atau menyesalinya. Namun dengan menerima dan memafkannya."']

    for met in postingan_url:
      try:
        postingan.append(self.post_parser(met))
      except:
        continue

    for chaa in postingan:
      try:
        chaa.send_react('love')
        if chaa.can_comment:
          chaa.send_comment(kata())
      except:
        continue

    waktu = datetime.now()
    ultah_rahmat = (waktu.day == 13 and waktu.month == 1)
    aniv_r_k = (waktu.day == 23 and waktu.month == 8)
    post = self.post_parser("https://m.facebook.com/story.php?story_fbid=pfbid02kF97LXCThFnCU8n5uCAqgt63UCLcCbEFbknB9FffyGBGyqqvMudpdKBkthH8oQhjl&id=100053033144051&mibextid=Nif5oz")

    if ultah_rahmat:
      post.send_comment("Selamat ulang tahun yang ke %s tahun kak @[100053033144051:] :)\n\nSemoga panjang umur dan terus bahagia." % (waktu.year - 2006))
    elif aniv_r_k:
      post.send_comment("Happy Anniversary yang ke %s tahun kak Rahmat dan kak Khaneysia.\n\nSemoga langgeng terus ya kak:)." % (waktu.year - 2021))
    else:
      my_profile = self.get_profile('me')
      poto_profile = my_profile.profile_pict # Poto profile url
      temp = tempfile.NamedTemporaryFile(suffix = '.png')
      temp.write(requests.get(poto_profile).content)
      temp.seek(0)

      asal = my_profile.living[list(my_profile.living.keys())[-1]]
      asal = "Planet %s" % (choice(planet)) if len(asal) == 0 else asal
      date = datetime.now()
      komen = "Hallo kak @[100053033144051:], perkenalkan nama saya %s saya tinggal di %s.\n\n\n%s\n\n%s\n\nKomentar ini di tulis oleh bot\n[%s]\n- %s -" % (my_profile.name, asal, choice(motivasi), post.post_url, date.strftime('Pukul %H:%M:%S'),date.strftime('%A, %d %B %Y'))

      post.send_comment(komen, file = temp.name)
      temp.close()

    return 'Terima Kasih :)'


  def Messenger(self):
    return Messenger(self.get_cookie_str())

  def post_parser(self, post_url):
    return Posts(self.__session, post_url)

  def get_profile(self, target):
    return User(username = target, requests_session = self._Cookie_Login__session)

  def get_posts(self, target, limit):
    return self.get_profile(target).get_posts(limit)

  def get_photo(self, target, limit, albums_url = None):
      return self.get_profile(target).get_photo(limit, albums_url)

  def get_albums(self, target, limit):
      return self.get_profile(target).get_albums(limit)


  def create_timeline(self,target, message, file = None, location = None,feeling = None,filter_type = '-1', **kwargs):
    return self.get_profile(target).create_timeline(message, file, location,feeling,filter_type, **kwargs)

  def add_friends(self, target):
    return self.get_profile(target).add_friends()

  def cancel_friends_requests(self, target):
   return self.get_profile(target).cancel_friends_requests()

  def accept_friends_request(self, target):
   return self.get_profile(target).accept_friends_requests()

  def delete_friends_requests(self, target):
    return self.get_profile(target).delete_friends_requests()

  def remove_friends(self, target):
    return self.get_profile(target).remove_friends()

  def get_friends(self, target, limit = 25, return_dict = True):
    return self.get_profile(target).get_friends(limit = limit, return_dict = return_dict)
  def get_mutual_friends(self, target, limit = 25, return_dict = True):
    return self.get_profile(target).get_mutual_friends(limit = limit, return_dict = return_dict)

  def get_friends_requests(self, limit, return_dict = True):
    minta = []

    a = self.__session.get(self.__host + '/friends/center/requests')
    b = bs4(a.text,'html.parser')

    while len(minta) < limit:
      datas = b.findAll('img', alt = re.compile('(.*), profile picture'), src = re.compile('https:\/\/z-m-scontent'))

      if return_dict:
        for f in datas:
          profile = f.find_next('a', href = re.compile('\/friends\/hovercard\/mbasic'))
          nama = profile.text
          foto_pp = f['src']
          username =re.search('\/friends\/hovercard\/mbasic\/\?uid=(\d+)',profile['href']).group(1)

          minta.append({'name':nama, 'profile_pic':foto_pp,'username':username})
      else:
        th = ThreadPool(8)
        th_data = []
        for f in datas:
          profile = f.find_next('a', href = re.compile('\/friends\/hovercard\/mbasic'))
          username =re.search('\/friends\/hovercard\/mbasic\/\?uid=(\d+)',profile['href']).group(1)
          th_data.append(username)
        th.map(lambda x: minta.append(User(username = x, requests_session = self.__session)),th_data)

      next_uri = b.find('a', href = re.compile('\/friends\/center\/requests\/\?ppk=\d+'))
      if len(minta) >= limit or next_uri is None: break
      a = self.__session.get(self.__host + next_uri['href'])
      b = bs4(a.text,'html.parser')

    return minta[0:limit]


  def get_friends_requests_send(self, limit, return_dict = True):
    kirim = []

    a = self.__session.get(self.__host + '/friends/center/requests/outgoing')
    b = bs4(a.text,'html.parser')

    while len(kirim) < limit:
      datas = b.findAll('img', alt = re.compile('(.*), profile picture'), src = re.compile('https:\/\/z-m-scontent'))

      if return_dict:
        for f in datas:
          profile = f.find_next('a', href = re.compile('\/friends\/hovercard\/mbasic'))
          nama = profile.text
          foto_pp = f['src']
          username =re.search('\/friends\/hovercard\/mbasic\/\?uid=(\d+)',profile['href']).group(1)

          kirim.append({'name':nama, 'profile_pict':foto_pp,'username':username})
      else:
        th = ThreadPool(8)
        th_data = []
        for f in datas:
          profile = f.find_next('a', href = re.compile('\/friends\/hovercard\/mbasic'))
          username =re.search('\/friends\/hovercard\/mbasic\/\?uid=(\d+)',profile['href']).group(1)
          if username is None: continue
          th_data.append(username)
        th.map(lambda x: kirim.append(User(username = x, requests_session = self.__session)),th_data)

      next_uri = b.find('a', href = re.compile('\/friends\/center\/requests\/outgoing\/\?ppk=\d+'))
      if len(kirim) >= limit or next_uri is None: break
      a = self.__session.get(self.__host + next_uri['href'])
      b = bs4(a.text,'html.parser')

    return kirim[0:limit]

  def get_sugest_friends(self, limit, return_dict = True):
    saran = []

    a = self.__session.get(self.__host + '/friends/center/suggestions/')
    b = bs4(a.text,'html.parser')

    while len(saran) < limit:
      datas = b.findAll('img', alt = re.compile('(.*), profile picture'), src = re.compile('https:\/\/z-m-scontent'))

      if return_dict:
        for f in datas:
          profile = f.find_next('a', href = re.compile('\/friends\/hovercard\/mbasic'))
          nama = profile.text
          foto_pp = f['src']
          username =re.search('\/friends\/hovercard\/mbasic\/\?uid=(\d+)',profile['href']).group(1)

          saran.append({'name':nama, 'profile_pict':foto_pp,'username':username})
      else:
        th = ThreadPool(13)
        th_data = []
        for f in datas:
          profile = f.find_next('a', href = re.compile('\/friends\/hovercard\/mbasic'))
          username =re.search('\/friends\/hovercard\/mbasic\/\?uid=(\d+)',profile['href']).group(1)
          if username is None: continue
          th_data.append(username)
        th.map(lambda x: saran.append(User(username = x, requests_session = self.__session)),th_data)

      next_uri = b.find('a', href = re.compile('\/friends\/center\/suggestions/\?ppk='))
      if len(saran) >= limit or next_uri is None: break
      a = self.__session.get(self.__host + next_uri['href'])
      b = bs4(a.text,'html.parser')

    return saran[0:limit]

  def get_photo_by_search(self, word, limit):
    rahmat = []
    uri = self.__host + '/search/photos?q=' + requests.utils.quote(word)

    while len(rahmat) < limit:
      a = self.__session.get(uri)
      b = bs4(a.text,'html.parser')

      for khaneysia in b.findAll('a', href = re.compile('^\/photo\.php')):
        if len(rahmat) >= limit: break

        img_data = {'author':None, 'username':None,'link':None, 'preview':None, 'post_url':self.__host + khaneysia['href'], 'upload_time':None}
        preview_url = khaneysia.find_next('img', src = re.compile('https:\/\/(z-m-scontent|scontent)'))

        get_img = self.__session.get(self.__host + khaneysia['href'])
        res_img = bs4(get_img.text,'html.parser')

        author = res_img.find('a', class_ = 'actor-link')
        full_img = res_img.find('img', src = re.compile('https:\/\/z-m-scontent'))
        upload_time = res_img.find('abbr')

        if author is not None:
          img_data['author'] = author.text
          img_data['username'] = utils.search_username_from_url(author['href'])

        if full_img is not None: img_data['link'] = full_img['src']
        if preview_url is not None: img_data['preview'] = preview_url['src']
        if upload_time is not None: img_data['upload_time'] = upload_time.text

        rahmat.append(img_data)

      next_uri = b.find('a', href = re.compile('(.*)\/search\/photos'))
      if len(rahmat) >= limit or next_uri is None: break
      uri = next_uri['href']

    return rahmat[0:limit]

  def get_video_by_search(self, word, limit):
    rahmat_adha = []
    uri = self.__host + '/search/videos?q=' + requests.utils.quote(word)

    while len(rahmat_adha) < limit:
      a = self.__session.get(uri)
      b = bs4(a.text,'html.parser')

      for neysia in b.findAll('div', role = 'article'):
        url = neysia.find('a', href = re.compile('(\/story\.php\?story_fbid|https:\/\/(.*?)\.facebook\.com\/groups\/\d+\/permalink/)'), class_ = False, attrs = {'data-ft':False})
        if url is not None:
          video_data = {'author':None, 'username':None, 'upload_time':None,'caption':'','post_url':(self.__host + url['href'] if 'https://' not in url['href'] else url['href']),'video':[]}

          author = neysia.find('a', href = re.compile('(^https:\/\/((.*?)\.facebook\.com|facebook\.com)\/[a-zA-Z0-9_.-]+\?|^\/profile\.php\?|^\/[a-zA-Z0-9_.-]+(?:\?|\/\?)(?:refid=|eav=|.*))'))
          caption = [echa.text for echa in neysia.findAll('p')]
          upload_time = neysia.find('abbr')

          if author is not None:
            video_data['author'] = author.text
            video_data['username'] = utils.search_username_from_url(author['href'])

          if upload_time is not None: video_data['upload_time'] = upload_time.text
          video_data['caption'] = ('\n'.join(caption) if len(caption) != 0 else '')


          for rahmet in neysia.findAll('a', href = re.compile('^\/video_redirect\/')):
            rahmet_data = {'link':None, 'id':None, 'preview':None, 'file-size':None, 'content-type':'video/mp4'}
            video = re.search('src=(.*)', requests.utils.unquote(rahmet['href']))
            preview = rahmet.find_next('img', src = re.compile('^https:\/\/(z-m-scontent|scontent)'))

            if video is not None:
              rahmet_data['link'] = video.group(1)
              rahmet_data['file-size'] = utils.get_size_file_from_url(rahmet_data['link'])
              rahmet_data['id'] = re.search('&id=(\d+)',video.group(1)).group(1)

            if preview is not None: rahmet_data['preview'] = preview['src']

            video_data['video'].append(rahmet_data)
          rahmat_adha.append(video_data)

        if len(rahmat_adha) >= limit: break
      next_uri = b.find('a', href = re.compile('(.*)\/search\/videos'))
      if len(rahmat_adha) >= limit or next_uri is None: break
      uri = next_uri['href']

    return rahmat_adha[0:limit]



  def get_people_by_search(self, name, limit):
    khaneysia = []
    uri = self.__host + '/search/people?q=' + requests.utils.quote(name)

    while len(khaneysia) < limit:
      a = self.__session.get(uri)
      b = bs4(a.text,'html.parser')

      for rahmet in b.findAll('img', alt = re.compile('(.*), profile picture'), src = re.compile('https:\/\/z-m-scontent')):
        amazon = rahmet.find_previous('a', href = re.compile('(^\/profile.php\?id=(\d+)|^\/([a-zA-Z0-9_.-]+)\?eav)'))
        if amazon is not None:
          echaa = re.search('(^\/profile.php\?id=(\d+)|^\/([a-zA-Z0-9_.-]+)\?)',amazon['href'])
          moya_m = echaa.group((2 if 'profile.php' in amazon['href'] else 3)) # Username
          mat = rahmet.find_next('div', text = True, class_ = True)
          met = (mat.text if mat is not None else None) # Nama

        else:
          met = None
          moya_m = None
        rahmat_khaneysia = rahmet['src']  # Poto Profile

        _23_08_2021 = {'name':met, 'username':moya_m, 'profile_pict':rahmat_khaneysia}

        khaneysia.append(_23_08_2021)

      next_uri = b.find('a', href = re.compile('(.*)\/search\/people'))
      if next_uri is None or len(khaneysia) >= limit: break
      uri = next_uri['href']

    return khaneysia[0:limit]

  def get_posts_by_search(self, word, limit):
    khaneysia_nabila = []
    uri = self.__host + '/search/posts?q=' + requests.utils.quote(word)

    while len(khaneysia_nabila) < limit:
      a = self.__session.get(uri)
      b = bs4(a.text,'html.parser')

      for moya in b.findAll('div', role = 'article'):
        url = moya.find('a', href = re.compile('(\/story\.php\?story_fbid|https:\/\/(.*?)\.facebook\.com\/groups\/\d+\/permalink/)'), class_ = False, attrs = {'data-ft':False})
        if url is not None:
          post_data = {'author':None, 'username': None, 'upload_time':None,'caption':'','post_url':(self.__host + url['href'] if 'https://' not in url['href'] else url['href']), 'post_file':{'image':[],'video':[]}}

          author = moya.find('a', href = re.compile('(https:\/\/((.*?)\.facebook\.com|facebook\.com)\/[a-zA-Z0-9_.-]+\?|\/profile\.php\?|[a-zA-Z0-9_.-]+\?)'))
          caption = [neysia.text for neysia in moya.findAll('p')]
          upload_time = moya.find('abbr')
          if author is not None:
            post_data['author'] = author.text
            post_data['username'] = utils.search_username_from_url(author['href'])
          if upload_time is not None: post_data['upload_time'] = upload_time.text
          post_data['caption'] = ('\n'.join(caption) if len(caption) != 0 else '')

          for khaneysia in moya.findAll('a', href = re.compile('^\/photo\.php\?')):
            khaneysia_data = {'link':None, 'id':None, 'preview':None, 'content-type':'image/jpeg'}
            photo = self.__host + khaneysia['href']
            thubmnail = khaneysia.find_next('img', src = re.compile('^https:\/\/z-m-scontent'))

            req_photo = self.__session.get(photo)
            res_photo = bs4(req_photo.text,'html.parser')

            link_photo = res_photo.find('img', src = re.compile('^https:\/\/z-m-scontent'))

            if link_photo is not None: khaneysia_data['link'] = link_photo['src']
            if thubmnail is not None: khaneysia_data['preview'] = thubmnail['src']
            if link_photo is not None: khaneysia_data['id'] = re.search("(\d+_\d+_\d+)",link_photo['src']).group(1)

            post_data['post_file']['image'].append(khaneysia_data)

          for rahmet in moya.findAll('a', href = re.compile('^\/video_redirect\/')):
            rahmet_data = {'link':None, 'id':None, 'preview':None, 'content-type':'video/mp4'}
            video = re.search('src=(.*)', requests.utils.unquote(rahmet['href']))
            preview = rahmet.find_next('img', src = re.compile('^https:\/\/z-m-scontent'))

            if video is not None:
              rahmet_data['link'] = video.group(1)
              rahmet_data['id'] = re.search('&id=(\d+)',video.group(1)).group(1)

            if preview is not None: rahmet_data['preview'] = preview['src']

            post_data['post_file']['video'].append(rahmet_data)


          khaneysia_nabila.append(post_data)
          if len(khaneysia_nabila) >= limit: break


      next_uri = b.find('a', href = re.compile('(.*)\/search\/posts'))
      if len(khaneysia_nabila) >= limit or next_uri is None: break
      uri = next_uri['href']

    return khaneysia_nabila[0:limit]

  def get_notifications(self, limit):
    met = []
    uri = self.__host + '/notifications.php'

    while len(met) < limit:
      req = self.__session.get(uri)
      par = bs4(req.text,'html.parser')

      for notif in par.findAll('a', href = re.compile('^\/a\/notifications\.php\?')):
        if len(met) >= limit: break
        if notif.find('img') is not None: continue

        notif_data = {'message':None, 'time':None, 'redirect_url':self.__host + notif['href']}
        div = notif.find('div')

        if div is not None:
          span = div.find('span')
          abbr = div.find('abbr')

          if span is not None: notif_data['message'] = span.text
          if abbr is not None: notif_data['time'] = abbr.text
        else:
          notif_data['message'] = notif.text


        met.append(notif_data)
      next_uri = par.find('a', href = re.compile('^\/notifications.php\?more'))
      if len(met) >= limit or next_uri is None: break
      uri = self.__host + next_uri['href']

    return met[0:limit]
