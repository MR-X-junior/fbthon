import re
import requests

from . import utils
from . import exceptions
from .login import Cookie_Login
from datetime import datetime
from bs4 import BeautifulSoup as bs4


class CreateAccount(Cookie_Login):

  HEADERS = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','User-Agent':'Mozilla/5.0 (Mobile; rv:48.0; A405DL) Gecko/48.0 Firefox/48.0 KAIOS/2.5'}

  def __init__(self, firstname, lastname, email, gender, date_of_birth, password, headers = {}, save_login = True, free_facebook = False):
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    self.gender = gender
    self.date_of_birth = (date_of_birth if isinstance(date_of_birth,datetime) else datetime.strptime(date_of_birth,'%d/%m/%Y'))
    self.password = password
    self.headers = headers
    self.save_login = save_login
    self.free_facebook = free_facebook

    self.__session = requests.Session()
    self.__session.headers.update(self.HEADERS)
    self.__session.headers.update(self.headers)
    self.__host = "https://mbasic.facebook.com"
    gender_value = {'female':'1','male':'2','custom':'-1'}

    req = self.__session.get(self.__host)
    res = bs4(req.text,'html.parser')
    err_req = res.find('div', attrs = {'class':True, 'id':'root','role':'main'})
    signup_form = res.find('form', action = re.compile('^\/login\/device-based\/regular'))

    if err_req is not None and signup_form is None:
      err_req_div = err_req.find('div', attrs = {'class':True})
      err_req_msg = (err_req_div.get_text(separator = '\n') if err_req_div is not None else "Terjadi kesalahan:(")
      raise exceptions.FacebookError(err_req_msg)

    signup_data = {i.get('name'):i.get('value') for i in signup_form.findAll('input', attrs = {'type':'hidden'})}
    signup_form_value = signup_form.find('input', attrs = {'name':'sign_up','type':'submit'})
    if signup_form_value is None: raise exceptions.FacebookError('Untuk Saat ini fitur "CreateAccount" tidak mendukung pada facebook mobile, untuk mengatasi masalah ini coba ganti User-Agent yang sedang anda gunakan :)')
    signup_data['sign_up'] = signup_form_value.get('value')
    signup_submit = self.__session.post(self.__host + signup_form['action'], data = signup_data)
    signup_response = bs4(signup_submit.text,'html.parser')

    self.register_form = signup_response.find('form', action = re.compile('^https:\/\/(?:mbasic\.facebook\.com|((.*?)\.facebook\.com|facebook\.com))\/reg\/submit'))
    self.register_data = {chaa.get('name'):chaa.get('value') for chaa in self.register_form.findAll('input', attrs = {'type':'hidden'})}
    self.full_name_input = self.register_form.find('input', attrs = {'name':'lastname'}) is None

    if self.full_name_input:
      self.register_data['firstname'] = "%s %s" % (self.firstname,self.lastname)
    else:
      self.register_data['firstname'] = self.firstname
      self.register_data['lastname'] = self.lastname

    self.register_data['reg_email__'] = self.email
    self.register_data['sex'] = (gender_value[self.gender.lower()] if self.gender.lower() in gender_value.keys() else '-1')
    self.register_data['birthday_day'] = self.date_of_birth.day
    self.register_data['birthday_month'] = self.date_of_birth.month
    self.register_data['birthday_year'] = self.date_of_birth.year
    self.register_data['reg_passwd__'] = self.password
    self.register_submit = self.__session.post(self.register_form['action'], data = self.register_data)
    self.register_response = bs4(self.register_submit.text,'html.parser')
    self.register_error = self.register_response.find('div', attrs = {'id':'registration-error'})

    if self.register_error is not None: raise exceptions.FacebookError(self.register_error.text)
    if ('/recover/code/' in self.register_submit.url or 'home.php' in self.register_submit.url) and 'confirmemail' not in self.register_submit.url: raise exceptions.FacebookError("Gagal membuat akun Facebook, sepertinya anda sudah memiliki akun facebook dengan alamat email \"%s\"" % (email))
    if 'checkpoint' in self.__session.cookies.get_dict().keys() or 'checkpoint' in self.register_submit.url: raise exceptions.AccountCheckPoint('Akun Anda Terkena Checkpoint :(')

    if save_login and 'login/save-device/' in self.register_submit.url:
      savelogin_form = self.register_response.find('form',action = re.compile("/login/\w+"))
      url = self.__host + savelogin_form['action']
      data = {moya.get('name'):moya.get('value') for moya in savelogin_form.findAll('input', attrs = {'type':'hidden'})}

      self.register_submit = self.__session.post(url, data = data)
      self.register_response = bs4(self.register_submit.text,'html.parser')

    elif not save_login and 'login/save-device/' in self.register_submit.url:
      url = self.__host + self.register_response.find('a', href = re.compile('/login/save-device/cancel'))['href']
      data = {}
      for i in self.submit_res.findAll('input'):
        if i.get('name') in ['fb_dtsg', 'jazoest', 'flow', 'next', 'nux_source']: data[i.get('name')] = i.get('value')

      self.register_submit = self.__session.post(url, data = data)
      self.register_response = bs4(self.register_submit.text,'html.parser')

  def __str__(self):
    return "Facebook CreateAccount: firstname=%s, lastname=%s, email=%s gender=%s, date_of_birth=%s, password=%s" % (self.firstname, self.lastname, self.email, self.gender, self.date_of_birth.strftime('%d/%m/%Y'),self.password)

  def __repr__(self):
    return "Facebook CreateAccount: firstname=%s, lastname=%s, email=%s gender=%s, date_of_birth=%s, password=%s" % (self.firstname, self.lastname, self.email, self.gender, self.date_of_birth.strftime('%d/%m/%Y'),self.password)

  def confirm_account(self, verification_code):
    form_confirm = self.register_response.find('form', action = re.compile('^\/confirmemail\.php'))

    if 'confirmemail.php' in self.register_submit.url or form_confirm is not None:
      data_confirm = {khaneysia.get('name'):khaneysia.get('value') for khaneysia in form_confirm.findAll('input', attrs = {'type':'hidden'})}
      data_confirm['c'] = verification_code
      url_confirm = self.__host + form_confirm['action']
      submit_confirm = self.__session.post(url_confirm, data = data_confirm)
      response_confirm = bs4(submit_confirm.text,'html.parser')
      error_confirm = response_confirm.find('div', attrs = {'id':'m_conf_cliff_root_id'})

      if error_confirm is not None:
        err_div = error_confirm.find('div', string = True)
        err_msg = (err_div.text if err_div is not None else "Kode Verifikasi Salah :(")

        raise exceptions.FacebookError(err_msg)

      self.register_submit = submit_confirm
      self.register_response = bs4(submit_confirm.text,'html.parser')

      cookie_str = ''.join(["%s=%s;" % (keys, value) for keys,value in self.__session.cookies.get_dict().items()])
      super().__init__(cookies = cookie_str, free_facebook = self.free_facebook, headers = self.__session.headers)

      return submit_confirm.ok
    else:
      raise exceptions.FacebookError('Tidak dapat mengkonfirmasi akun :(')

  def resend_code(self):
    submit_resend = self.register_response.find('input', attrs = {'name':False,'class':True, 'type':'submit'})

    if submit_resend is not None:
      form_resend = submit_resend.find_previous('form', action = re.compile('^\/confirmemail\.php'))
      form_resend_data = {chaa.get('name'):chaa.get('value') for chaa in form_resend.findAll('input', attrs = {'type':'hidden'})}
      form_resend_url = self.__host + form_resend['action']

      resend = self.__session.post(form_resend_url, data = form_resend_data)

      return resend.ok
    else:
      raise exceptions.FacebookError('Tidak dapat mengirim ulang kode konfirmasi :(')

