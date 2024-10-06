import getpass
from pyVim.connect import SmartConnect
import ssl


passwd = getpass.getpass()
s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode = ssl.CERT_NONE
si = SmartConnect(host="vcenter.alex.local", user="alex-adm@alex.local", pwd = passwd, sslContext = s)