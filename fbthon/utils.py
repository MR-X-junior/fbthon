import os
import re
import math
import random
import string
import requests

from . import exceptions
from requests_toolbelt import MultipartEncoder

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"

   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)

   return "%s %s" % (s, size_name[i])

def get_size_file(file_path):
   return convert_size(os.path.getsize(file_path))

def get_size_file_from_url(url):
  return convert_size(int(requests.head(url).headers['Content-Length']))

def search_username_from_url(url):
  cari_username = re.search('^\/profile.php\?id=(\d+)|^\/([a-zA-Z0-9_.-]+)|https:\/\/(?:facebook.com|.*?\.facebook\.com)\/([a-zA-Z0-9_.-]+)\?',url).groups()
  result = next((x for x in cari_username if x is not None), None)

  return result

def upload_photo(requests_session, upload_url, input_file_name, file_path, fields = {}):
  max_size = (1000000*4)
  support_file = ['.jpg','.png','.webp','.gif','.tiff','.heif','.jpeg']
  mime = {'.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.gif': 'image/gif', '.tiff': 'image/tiff', '.heif': 'image/heif', '.jpeg': 'image/jpeg'}
  ext = os.path.splitext(file_path)[-1]

  if os.path.getsize(file_path) > max_size: raise exceptions.FacebookError('Ukuran file "%s"  terlalu besar, sehingga file tersebut tidak bisa di upload, File harus  berukuran kurang dari %s :)' % (os.path.realpath(file_path), convert_size(max_size)))
  if not ext in support_file: raise exceptions.FacebookError("Hanya bisa mengupload file dengan extensi \"%s\", tidak bisa mengupload file dengan extensi \"%s\"" % (', '.join([re.sub('^\.','',ext_file) for ext_file in support_file]),ext))

  data = {key:((None,value) if not isinstance(value,tuple) else value) for key,value in fields.items()}
  data[input_file_name] = (os.path.basename(file_path), open(file_path,'rb').read(),mime[ext])

  boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
  multipart = MultipartEncoder(fields=data,boundary=boundary)
  headers = {"content-type":multipart.content_type}

  submit = requests_session.post(upload_url, data = multipart, headers = headers)

  return submit
