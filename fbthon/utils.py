import os
import re
import math
import requests

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
