class LoginFailed(Exception):
  '''Gagal Login Ke akun Facebook'''
  pass

class InvalidCookies(Exception):
  '''Coookie tidak valid'''
  pass

class AccountCheckPoint(Exception):
  '''Account terkena CheckPoint'''
  pass

class AccountTemporaryBanned(Exception):
  '''Akun Sementara di banned Sementara Oleh om mark'''
  pass

class AccountDisabled(Exception):
  '''Akun terkena Banned permanen oleh om Mark'''
  pass

class PageNotFound(Exception):
  '''Halaman Yang di tuju sudah kadaluarsa / URL tidak valid!'''
  pass

class SessionExpired(Exception):
  '''Sesi sudah kadaluarsa'''
  pass

class FacebookError(Exception):
  '''ususu'''
  pass
