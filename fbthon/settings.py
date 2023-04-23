import re
import requests

from . import utils
from . import exceptions
from bs4 import BeautifulSoup as bs4

def SetFacebookSite(fbobj, set_to):
  site_list = ['reguler','basic']
  default_head = {'User-Agent':fbobj._session.headers['User-Agent']}

  if set_to not in site_list: raise exceptions.FacebookError('Facebook Site tidak valid!!')

  try:
    a = fbobj._session.get(fbobj._host + '/settings/site')
  except requests.exceptions.TooManyRedirects:
    fbobj._session.headers.clear()
    fbobj._session.headers.update(default_head)
    a = fbobj._session.get(fbobj._host + '/settings/site')

  b = bs4(a.text,'html.parser')
  c = b.find('form', action = re.compile('^\/a\/preferences\.php')) # form
  d = {i.get('name'):i.get('value') for i in c.findAll('input')} #Data
  e = c.findAll('input', attrs = {'name':'basic_site_devices'})
  f = e[site_list.index(set_to.lower())]
  d[f.get('name')] = f.get('value')

  r = fbobj._session.post(fbobj._host + c['action'], data = d)

  return r.ok


def SetLanguage(fbobj, locale):
  a = fbobj._session.get(fbobj._host + '/language')
  b = bs4(a.text,'html.parser')
  c = b.find('form', action = re.compile('^\/intl\/save_locale\/\?loc=' + locale))

  if c is None: raise exceptions.FacebookError('Locale tidak valid, pastikan locale yang anda massukan sudah benar :)')

  d = {i.get('name'):i.get('value') for i in c.findAll('input')}

  r = fbobj._session.post(fbobj._host + c['action'], data = d)

  return r.ok

def GetLocale(fbobj):
  khaneysia = {} # :)

  a = fbobj._session.get(fbobj._host + '/language')
  b = bs4(a.text,'html.parser')
  c = b.findAll('form', action = re.compile('^\/intl\/save_locale\/\?loc='))

  for i in c:
    locale = re.search('loc=(.*?)&',i['action']).group(1)
    value = i.find('input', attrs = {'type':'submit'}).get('value')

    khaneysia[value] = locale

  return khaneysia

def SwitchMode(fbobj, set_to):
  a = fbobj._session.get(fbobj._host + '/home.php')
  b = bs4(a.text,'html.parser')

  if set_to.lower() == 'basic':
    zero = b.find('a', href = re.compile('^\/zero\/toggle\/settings\/confirm'))

    if zero is not None:
      zero_confirm = fbobj._session.get(fbobj._host + zero['href'])

      return zero_confirm.ok
    else:
      return False

  elif set_to.lower() == 'reguler':
    upsell = b.find('a', href = re.compile('^\/upsell\/advanced_upsell\/in_line'))

    if upsell is not None:
      confirm_upsell = fbobj._session.get(fbobj._host + upsell['href'])
      form_upsell = bs4(confirm_upsell.text,'html.parser').find('form', action = re.compile('^\/upgrade\/upsell\/'))
      data_upsell = {}

      data_upsell['fb_dtsg'] = form_upsell.find('input', attrs = {'name':'fb_dtsg'}).get('value')
      data_upsell['jazoest'] = form_upsell.find('input', atrrs = {'name':'jazoest'}).get('value')
      data_upsell['data_pack_selection'] = 'upgrade_to_paid'

      r = fbobj._session.post(fbobj._host + form_upsell['action'], data = data_upsell)

      return r.ok

    else:
      return False

def ChangePassword(fbobj, old_pass, new_pass, keep_session = False):
  a = fbobj._session.get(fbobj._host + '/settings/security/password')
  b = bs4(a.text,'html.parser')
  c = b.find('form', action = re.compile('^\/password\/change')) # form

  if c is not None:
    d = {i.get('name'):i.get('value') for i in c.findAll('input')} # Data
    d['password_old'] = old_pass
    d['password_new'] = new_pass
    d['password_confirm'] = new_pass

    e = fbobj._session.post(fbobj._host + c['action'], data = d)

    if '/settings/security/password' in e.url:
      err = "Terjadi Kesalahan!"
      div_err = bs4(e.text,'html.parser').find('div', id = 'root', class_ = True)
      if div_err is not None:
        msg_err = div_err.find('div', class_ = True, text = True)
        if msg_err is not None:
          err = msg_err.text

      raise exceptions.FacebookError(err)
    else:
      form = bs4(e.text,'html.parser').find('form', action = re.compile('^\/settings\/account\/password\/survey'))
      data = {i.get('name'):i.get('value') for i in form.findAll('input')}
      url = fbobj._host + form['action']
      data['session_invalidation_options'] = ('keep_sessions' if keep_session else 'review_sessions')

      req = fbobj._session.post(url, data = data)
      res = bs4(req.text,'html.parser')

      if keep_session:
        return req.ok
      else:
        last_req = fbobj._session.get(fbobj._host + res.find('a', href = re.compile('^\/settings\/security_login\/sessions\/log_out_all\/confirm'))['href'])
        return last_req.ok

def UpdateProfilePicture(fbobj, photo):
  a = fbobj._session.get(fbobj._host + '/me?v=info')
  b = bs4(a.text,'html.parser')
  c = b.find('a', href = re.compile('^\/profile_picture(\?|\/\?)'))

  if c is not None:
    d = fbobj._session.get(fbobj._host + c['href'])
    e = bs4(d.text,'html.parser')
  else:
    c = b.find('a', href = re.compile('^\/photo\.php(\?|\/\?)'), attrs = {'id':True})
    if c is None: raise exceptions.FacebookError('Tidak dapat mengganti Poto Profile')
    d = bs4(fbobj._session.get(fbobj._host + c['href']).text,'html.parser').find('a', href = re.compile('^\/photos\/change\/profile_picture'))
    e = bs4(fbobj._session.get(fbobj._host + d['href']).text,'html.parser')

  upload = e.find('a', href = re.compile('^\/photos\/upload(\?|\/\?)profile_pic'))
  if upload is not None: e = bs4(fbobj._session.get(fbobj._host + upload['href']).text,'html.parser')

  form = e.find('form', action = re.compile('https:\/\/(z-upload\.facebook\.com|upload\.facebook\.com)'))
  data = {moya.get('name'):moya.get('value') for moya in form.findAll('input', attrs = {'type':'hidden'})}
  kirim = utils.upload_photo(requests_session = fbobj._session, upload_url = form['action'], input_file_name = 'pic', file_path = photo, fields = data)

  return kirim.ok
