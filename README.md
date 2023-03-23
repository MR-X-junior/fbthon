# fbthon

**fbthon** adalah library sederhana yang di gunakan untuk scraping web Facebook

# Informasi Library
*Author :* [**Rahmat adha**](https://facebook.com/Anjay.pro098)\
*Library :* [**fbthon**](https://github.com/MR-X-Junior/fbthon)\
*License:* [**MIT License**](https://github.com/MR-X-junior/fbthon/blob/main/LICENSE)\
*Release:* **23**/03/20**23**\
*Version :* **0.0.1**

Di karenakan library ini masih versi pertama, pasti bakal banyak error/bug nya, jika menemukan error/bug pada library ini bisa langsung posting di [Issues](https://github.com/MR-X-junior/fbthon/issues) akun github saya :)

## Contoh Cara Penggunaan

### Pertama-tama buat dulu object `Facebook`

```python
>>> from fbthon import Facebook
>>> cookie = Cookie_akun_facebook
>>> fb = Facebook(cookie)
```

### Jika tidak tidak mempunyai Cookie akun facebook, kamu bisa coba cara di bawah ini

```python
>>> from fbthon import Facebook
>>> from fbthon.login import Web_Login
>>> email = "example@gmail.com" # Ganti email ini dengan email akun Facebook kamu
>>> password = "Banteng merah no counter321" # Ganti password ini dengan password Akun Facebook kamu
>>> login = Web_Login(email,password)
>>> cookie = login.get_cookie_str() # Ini adalah cookie akun Facebook kamu
>>> fb = Facebook(cookie)
```

Cara di [atas](#Jika-tidak-tidak-mempunyai-Cookie-akun-facebook-kamu-bisa-coba-cara-di-bawah-ini) akan login ke akun facebook, cara ini mungkin akan membuat akun facebook kamu terkena checkpoint.

Untuk mengurangi risiko akun terkena checkpoint, kamu hanya perlu mengganti user-agent yang sama dengan perangkat yang terakhir kali di gunakan untuk login akun facebook.

```python
>>> from fbthon import Facebook
>>> from fbthon.login import Web_Login
>>> user_agent = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0.1; SM-J510GN Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36'}
>>> email = "example@gmail.com" # Ganti email ini dengan email akun Facebook kamu
>>> password = "Banteng merah no counter321" # Ganti password ini dengan password Akun Facebook kamu
>>> login = Web_Login(email,password, headers = user_agent)
>>> cookie = login.get_cookie_str() # Ini adalah cookie akun Facebook kamu
>>> fb = Facebook(cookie)
```

#### Optional Parameter
*(Untuk `Web_Login` class)*.

- **email**: Email akun Facebook, kamu juga bisa menggunakan id atau username sebagai pengganti email
- **password**: Password akun Facebook
- **save_login**:  Menyimpan informasi login, default argument ini adalah `True`
- **free_facebook**: Gunakan `True` jika ingin menggukan web [free.facebook.com](https://free.facebook.com), default argument ini adalah `False`
- **headers**: ini  yang akan di gunakan untuk headers `requests`

### Extract Profile

Method `get_profile` dapat mengekstrak informasi dari akun facebook, Method ini akan mengembalikan object `User`

```python
>>> zuck = fb.get_profile('zuck')
>>> zuck.name
'Mark Zuckerberg'
>>> zuck.id
4
>>> zuck._user_info
{'name': 'Mark Zuckerberg', 'first_name': 'Mark', 'middle_name': '', 'last_name': 'Zuckerberg', 'alternate_name': '', 'about': "I'm trying to make the world a more open place.", 'username': '/zuck', 'id': '4', 'contact_info': {'Facebook': '/zuck'}, 'profile_pict': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t39.30808-1/312257846_10114737758665291_6588360857015169674_n.jpg?stp=cp0_dst-jpg_e15_q65_s480x480&_nc_cat=1&ccb=1-7&_nc_sid=dbb9e7&efg=eyJpIjoiYiJ9&_nc_eui2=AeFzbmHFWdaxFtpefl6HFZsab3tzEriMmA5ve3MSuIyYDvNS3CLUOOX_Yzt_U3wSA0jeUIi3OK41Qr4CDF_Yeuxd&_nc_ohc=_tOCG5VpSrsAX8FPoj-&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfDS8wxbStTclGwnoPxoTGde0VDzjBQPguHMx3zTJulmkw&oe=6412E91E', 'basic_info': {'Tanggal Lahir': '14 Mei 1984', 'Jenis Kelamin': 'Laki-laki', 'Bahasa': 'English language dan Mandarin Chinese'}, 'education': [{'name': 'Harvard University', 'type': 'Computer Science and Psychology', 'study': '', 'time': '30 Agustus 2002 - 30 April 2004'}, {'name': 'Phillips Exeter Academy', 'type': 'Classics', 'study': '', 'time': 'Angkatan 2002'}, {'name': 'Ardsley High School', 'type': 'SMA', 'study': '', 'time': 'September 1998 - Juni 2000'}], 'work': [{'name': 'Chan Zuckerberg Initiative', 'time': '1 Desember 2015 - Sekarang'}, {'name': 'Meta', 'time': '4 Februari 2004 - Sekarang'}], 'living': [{'Kota Saat Ini': 'Palo Alto, California', 'Kota asal': 'Dobbs Ferry, New York'}], 'relationship': 'Berkeluarga dengan  Priscilla Chan  sejak 19 Mei 2012', 'other_name': [], 'family': [], 'year_overviews': [{'year': '2017', 'overviews': ['August Was Born', 'Harvard Degree']}, {'year': '2015', 'overviews': ['Memulai Pekerjaan Baru di Chan Zuckerberg Initiative', 'Max Lahir']}, {'year': '2012', 'overviews': ['Menikah dengan Priscilla Chan', 'Peristiwa Hidup Lain']}, {'year': '2011', 'overviews': ['Menjadi Vegetarian']}, {'year': '2010', 'overviews': ['Mulai Belajar Mandarin Chinese']}, {'year': '2009', 'overviews': ['Wore a Tie for a Whole Year']}, {'year': '2006', 'overviews': ['Launched News Feed']}, {'year': '2004', 'overviews': ['Launched the Wall', 'Memulai Pekerjaan Baru di Meta', 'Keluar dari Harvard University']}, {'year': '2002', 'overviews': ['Mulai Kuliah di Harvard University', 'Lulus dari Phillips Exeter Academy']}, {'year': '2000', 'overviews': ['Mulai Kuliah di Phillips Exeter Academy', 'Keluar dari Ardsley High School']}, {'year': '1998', 'overviews': ['Mulai Kuliah di Ardsley High School']}], 'quote': '"Fortune favors the bold."\n - Virgil, Aeneid X.284\n \n "All children are artists. The problem is how to remain an artist once you grow up." \n - Pablo Picasso\n \n "Make things as simple as possible but no simpler."\n - Albert Einstein'}
```

**Gunakan `me` jika ingin mengekstrak informasi dari akun kamu**\
**Contoh**: 

```python
>>> my_profile = fb.get_profile('me')
>>> my_profile.name
Rahmat
>>> my_profile.id
100053033144051
>>> my_profile.username
/Anjay.pro098
>>> my_profile._user_info
{'name': 'Rahmat', 'first_name': 'Rahmat', 'middle_name': '', 'last_name': '', 'alternate_name': 'Mat', 'about': '', 'username': '/Anjay.pro098', 'id': '100053033144051', 'contact_info': {'Ponsel': '0857-5462-9509', 'Facebook': '/Anjay.pro098', 'GitHub': 'MR-X-Junior', 'LinkedIn': 'rahmat-adha', 'Email': 'rahmadadha11@gmail.com'}, 'profile_pict': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t39.30808-1/279908382_524601785984255_7727931677642432211_n.jpg?stp=cp0_dst-jpg_e15_p480x480_q65&_nc_cat=109&ccb=1-7&_nc_sid=dbb9e7&efg=eyJpIjoiYiJ9&_nc_eui2=AeEUCqxtmlmkSmx4EruhJj1ZoWFvcSuRApChYW9xK5ECkKEzjdDols3I7WDmPnas34nC8SsOQFYFy3zM38AIJfS1&_nc_ohc=XqfoPIkQwfkAX9oxiI4&tn=CoPUyHV9TcgsBjnY&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfByqAVLNVMSOfwr6pe43Iwr3HpWeVg0qImeiROkpw53rw&oe=63FCE8CF', 'basic_info': {'Tanggal Lahir': '13 Januari 2006', 'Jenis Kelamin': 'Laki-laki'}, 'education': [{'name': '', 'type': '', 'study': '', 'time': ''}], 'work': [], 'living': [{'Kota Saat Ini': 'Muaraancalung, Kalimantan Timur, Indonesia', 'Kota asal': 'Muaraancalung, Kalimantan Timur, Indonesia'}], 'relationship': 'Lajang', 'other_name': {'Nama panggilan': 'Met'}, 'family': [{'name': 'Pahrul Aguspriana XD.', 'username': '/PahrulXD', 'designation': 'Adik laki-laki', 'profile_pict': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t39.30808-1/331028920_3040847712882567_3539568768564278719_n.jpg?stp=c0.0.320.320a_cp0_dst-jpg_e15_p320x320_q65&_nc_cat=101&ccb=1-7&_nc_sid=dbb9e7&efg=eyJpIjoiYiJ9&_nc_eui2=AeEW2pBM_jo0ZzypEALp1QB7eG7Nm80Gj5J4bs2bzQaPkmGYk_gZVtPSzsrb1SX796_BwslIoWRa_4yIuFC3x1Fh&_nc_ohc=NjtS1hHD7GcAX9Sp4HY&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfBGUpSnDzv3tHfsng6gWLn2ZGjNwSaFXzDLeCnlWv9Lsg&oe=63FDEBC2'}], 'year_overviews': [], 'quote': "i know i'm not alone"}
```

### Get Posts

Method `get_posts`, akan mengumpulkan postingan dan mengekstrak postingan tersebut, method ini akan mengembalikan `list` yang di dalam nya terdapat sekumpulan object  `Posts`

**CATATAN: METHOD INI HANYA BISA MENGUMPULKAN POSTINGAN DARI AKUN PENGGUNA, TIDAK BISA MENGUMPULKAN POSTINGAN DARI GROUP ATAU HALAMAN.**
```python
for x in fb.get_posts('zuck', limit = 2):
   print("Author : "+x.author)
   print("Caption: "+x.caption)
   print("Upload Time "+ x.upload_time + "\n\n")
```

#### Output
```python
Author : Mark Zuckerberg
Caption: When Priscilla and I started working on the Chan Zuckerberg Initiative's science mission to help cure, prevent or manage all diseases, our first major project was launching the Biohub. It has been very successful, so today we're launching a second Biohub in Chicago that will engineer miniaturized sensors to instrument living tissues to help scientists see and understand how cells work together. We're going to start by instrumenting skin and heart tissues with an initial focus on measuring inflammation. About 50% of deaths are caused by diseases related to inflammation, like cancer and heart disease, so we're hopeful the technology created at the Chicago Biohub will have broad applications for science and health similar to the San Francisco Biohub.
Upload Time 2 Maret pukul 16.00


Author : Mark Zuckerberg
Caption: We're creating a new top-level product group at Meta focused on generative AI to turbocharge our work in this area. We're starting by pulling together a lot of the teams working on generative AI across the company into one group focused on building delightful experiences around this technology into all of our different products. In the short term, we'll focus on building creative and expressive tools. Over the longer term, we'll focus on developing AI personas that can help people in a variety of ways. We're exploring experiences with text (like chat in WhatsApp and Messenger), with images (like creative Instagram filters and ad formats), and with video and multi-modal experiences. We have a lot of foundational work to do before getting to the really futuristic experiences, but I'm excited about all of the new things we'll build along the way.
Upload Time 27 Februari pukul 20.50
```

### Post Parser

Method `post_parser` di gunakan untuk mengekstrak postingan, method ini akan mengembalikan object `Posts`

```python
>>> post = fb.post_parser("https://m.facebook.com/story.php?story_fbid=pfbid02kbL4vnSF4Ex88nBQrMZdvjUoWV7hhznHZ8BpMcFAJzjL2CEoBCAHeHEk4Y8DLAQ5l&id=100053033144051&mibextid=Nif5oz")
>>> post.author
Rahmat
>>> post.caption
Hello World 🌍
>>> post.post_file
{'image': [{'link': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t39.30808-6/241434705_371774571266978_6844800659294160676_n.jpg?stp=cp0_dst-jpg_e15_fr_q65&_nc_cat=104&ccb=1-7&_nc_sid=110474&efg=eyJpIjoiYiJ9&_nc_eui2=AeE-bGgqsChJWa0bm9hnBZ-c9HuYP8xaWmP0e5g_zFpaYypDCKSWUSxTvpaIdTGIXCGEzD4653spgkhYVI1L37UK&_nc_ohc=3B_9FgPbsqgAX_k1QAl&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_zt=23&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfB8x_I9eObguAKc3CVt2A1dYWAYrLDpzMOnD3CnvfM4wg&oe=641513CF', 'id': '241434705_371774571266978_6844800659294160676', 'preview': 'https://z-m-scontent.fsri1-1.fna.fbcdn.net/v/t39.30808-6/241434705_371774571266978_6844800659294160676_n.jpg?stp=cp0_dst-jpg_e15_p526x296_q65&_nc_cat=104&ccb=1-7&_nc_sid=110474&efg=eyJpIjoiYiJ9&_nc_eui2=AeE-bGgqsChJWa0bm9hnBZ-c9HuYP8xaWmP0e5g_zFpaYypDCKSWUSxTvpaIdTGIXCGEzD4653spgkhYVI1L37UK&_nc_ohc=3B_9FgPbsqgAX_k1QAl&_nc_ad=z-m&_nc_cid=1225&_nc_eh=4613fe15e78ad080e57d79ac328ba3a7&_nc_zt=23&_nc_rml=0&_nc_ht=z-m-scontent.fsri1-1.fna&oh=00_AfD3FkrA5grtqsZFr7LoQKSVpQToVBhEXRqC3ntmUjB5Hw&oe=641513CF', 'content-type': 'image/jpeg'}], 'video': []}
>>> post.upload_time
17 Mei 2021 pukul 13.15
>>> post.post_datetime
datetime.datetime(2021, 5, 17, 21, 15, 17)
>>> post.get_react()
{'like': 5652, 'love': 310, 'care': 9, 'haha': 6, 'wow': 252, 'sad': 0, 'angry': 1}
```

#### Mengirim Komentar

Kamu bisa menggunakan method `send_comment` untuk mengirim komentar.
Method `send_comment` akan mengembalikan `True` Jika berhasil mengirim komentar.

**Contoh:**

```python
>>> post = fb.post_parser('https://m.facebook.com/story.php?story_fbid=pfbid0h1BPgqZsa4seKWoqn7c6GqDyAD3vKUePuasDRHuZCyN46M4uuAVy4m4fAukRvaojl&id=100053033144051&mibextid=Nif5oz')
>>> post.send_comment('Hallo kak '+post.author +'\n\nKomentar ini di tulis menggunakan library fbthon :)')
True
```

##### Hasilnya
**Liat Komentar paling bawah**

![Contoh cara mengirim komentar](https://i.ibb.co/QFDpnw9/Screenshot-20230322-064024.jpg)

#### Memberikan react pada postingan

Kamu bisa menggunakan method `send_react` untuk memberikan react pada postingan.
Method ini akan mengembalikan `True` jika berhasil memberikan react pada postingan.

```python
>>> post = fb.post_parser(Link_post_facebook)
>>> post.send_react(react_type)
True
```

Terdapat 7 React Type, di antaranya : 
- Like
- Love
- Care
- Haha
- Wow
- Sad
- Angry

**Contoh Cara mengirim react:**
```python
>>> post = fb.post_parser('https://m.facebook.com/story.php?story_fbid=pfbid0h1BPgqZsa4seKWoqn7c6GqDyAD3vKUePuasDRHuZCyN46M4uuAVy4m4fAukRvaojl&id=100053033144051&mibextid=Nif5oz')
>>> post.send_react('Wow')
True
```

##### Hasilnya
![Contoh cara memberikan react ke postingan](https://i.ibb.co/SPXGWJJ/Screenshot-2023-0322-065521.png)

### Messenger

object `Messenger` bisa di gunakan untuk mengirim/menerima chat.\
Terdapat 2 cara untuk membuat Object `Messenger`

**Cara 1**

```python
>>> msg = fb.Messenger()
```
**Cara 2**

```python
>>> from fbthon.messenger import Messenger
>>> msg = Messenger(Cookie_Akun_Facebook_kamu)
```


#### Mendapatkan Pesan Baru
Method `get_new_message` bisa di gunakan untuk mendapatkan pesan baru:)

```python

for x in msg.get_new_message(limit = 3):
   print ("Nama : "+ x['name'])
   print ("Id Akun : "+x['id'])
   print ("Last Chat : "+ x['last_chat'])
   print ("Time : "+x['time'] + "\n\n")

```

##### Output

```python
Nama : Khaneysia                        
Id Akun : 1000xxxxxxxxxxx
Last Chat : Good Night sayang :)
Time : 5 menit lalu

Nama : Rahmat
Id Akun : 100053033144051
Last Chat : Hallo Kak Rahmat:)
Time : 11 menit lalu

Nama : Mark Zuckerberg
Id Akun : 4
Last Chat : Ban Akun aku dong om                          
Time : 4 Mar
```

Method `get_new_chat` juga bisa di gunakan untuk mendapatkan pesan baru, tetapi method ini berbeda dengan method `get_new_message`

```python
>>> msg.get_new_message(limit = 3)
[{'name': 'Khaneysia', 'id': '1000xxxxxxxxxxx', 'last_chat': 'Good Night sayang :)', 'time': '23 menit lalu'}, {'name': 'Rahmat', 'id': '100053033144051', 'last_chat': 'Hallo Kak Rahmat:)', 'time': '34 menit lalu'}, {'name': 'Mark Zuckerberg', 'id': '4', 'last_chat': 'Hello Mark Zuckerberg', 'time': '4 Mar'}]
>>> msg.get_new_chat(limit = 3)
[Facebook Chats : name='Mark Zuckerberg' id=4 chat_id=4:100090156622219 type='user', Facebook Chats : name='Khaneysia' id=1000xxxxxxxxxxx chat_id=1000xxxxxxxxxxx:100090156622219 type='user', Facebook Chats : name='Rahmat' id=100053033144051 chat_id=100053033144051:100090156622219 type='user']
```

Dari code di atas kita sudah bisa menyimpulkan perbedaan method `get_new_message` dan method `get_new_chat`. 

Method `get_new_message` akan mengembalikan `list` yang di dalam nya terdapat sekumpulan `dict`, sedangkan method `get_new_chat` akan mengembalikan `list` yang di dalam nya terdapat sekumpulan object `Chats`.

#### Mengirim Pesan

Kamu bisa menggunakan method `new_chat` untuk mengirim pesan, method ini akan mengembalikan object `Chats`

```python
with msg.new_chat('zuck') as chat:
  chat.send_text('Assalamualaikum')
  chat.send_text('Hallo om '+ chat.name)
  chat.send_text('Apa kabar?')
  chat.send_text('Pesan ini di kirim menggunakan library fbthon:)\n\nTerima kasih Sudah membaca chat saya.')
```

##### Hasilnya
![Contoh Cara Mengirim Pesan](https://i.ibb.co/fQHtDmb/Screenshot-20230317-222932.jpg)

## Membuat Postingan
method `create_timeline` bisa di gunakan untuk membuat postingan, method ini akan mengembalikan `True` jika berhasil membuat postingan.

### Membuat Postingan (Hanya Caption)

```python
>>> fb.create_timeline(target = 'me', message = 'Postingan Ini di buat menggunakan library fbthon\n\nHehe :>')
True
```

#### Hasilnya
![Membuat Postingan (Hanya Caption)](https://i.ibb.co/wB998Yd/Screenshot-2023-0317-224853.png)

### Membuat Postingan di akun teman
Untuk membuat postingan di akun teman, kamu hanya perlu mengganti argumen dari parameter `target` menjadi id atau username teman kamu:)

**Contoh:**

```python
>>> fb.create_timeline(target = 'Id atau username akun teman', message = 'Postingan Ini di buat menggunakan library fbthon\n\nHehe :>')
True
```

#### Hasilnya
![Membuat Postingan (Hanya caption) di akun teman Facebook](https://i.ibb.co/cTwRYDh/IMG-20230318-181857.jpg)

### Membuat Postingan (Tag Teman)
Untuk menandai teman pada postingan, kamu bisa menggunakan argumen `users_with`.

```python
>>> fb.create_timeline(target = 'me', message = 'Postingan Ini di buat menggunakan library fbthon\n\nHehe :>', users_with = 'id akun teman fb lu')
True
```

#### Hasilnya
![Membuat Postingan (Tag Teman)](https://i.ibb.co/tbHKb0x/IMG-20230322-072612.jpg)

### Membuat Postingan (Dengan Foto)
Kamu bisa menggunakan argumen `file` untuk menambahkan foto pada postingan:)

```python
>>> fb.create_timeline(target = 'me', message = ' Alhamdulillah :)', file = '/sdcard/Pictures/Certificate/mimo-certificates-125_page-0001.jpg')
True
```

#### Hasilnya
![Membuat Postingan (Dengan Foto)](https://i.ibb.co/d4nKvVr/Screenshot-2023-0318-151426.png)

Oh iya, kamu bisa menggunakan argumen `filter_type` untuk mengatur filter pada foto yang akan kamu upload.

```python
>>> fb.create_timeline(target = 'me', message = ' Alhamdulillah :)', file = '/sdcard/Pictures/Certificate/mimo-certificates-125_page-0001.jpg', filter_type='1')
True
```

Dan Ini hasil nya:

![Mengatur filter pada foto](https://i.ibb.co/twf0tnc/Screenshot-2023-0323-082948.png)

**Ada beberapa tipe filter yang bisa kamu coba, di antaranya:**
- Tanpa Filter = -1
- Hitam Putih = 1
- Retro = 2

### Membuat Postingan (Dengan Lokasi)
Kamu bisa menggunakan argumen `location` untuk menambahkan lokasi pada postingan

```python
>>> fb.create_timeline(target = 'me', message = 'Postingan Ini di buat menggunakan library fbthon\n\nHehe :>', location = 'Muaraancalung, Kalimantan Timur')
True
```

#### Hasilnya
![Membuat Postingan (Dengan Lokasi)](https://i.ibb.co/vh5zh05/Screenshot-2023-0318-145829.png)

### Membuat Postingan (Dengan Feeling)
Kamu bisa menggunakan argumen `feeling` untuk menambahkan feeling pada postingan

```python
>>> fb.create_timeline(target = 'me', message = 'Postingan Ini di buat menggunakan library fbthon\n\nHehe :>', feeling = 'Happy')
True
```

#### Hasilnya
![Membuat Postingan (Dengan Feeling)](https://i.ibb.co/n7yp62b/Screenshot-2023-0318-152335.png)

# Cara Install

**fbthon** sudah tersedia di PyPi

```console
$ python -m pip install fbthon
```

**fbthon** bisa install di Python versi 3.7+

# Donate
[![Donate for Rahmat adha](https://i.ibb.co/PwYMWsK/Saweria-Logo.png)](https://saweria.co/rahmatadha)