from LonginusPyPiAlpha import Longinus
from Cryptodome.Cipher import AES #line:32
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
import subprocess,threading,sys,os,json
from socket import *
from getpass import *
from datetime import datetime
from datetime import timedelta
from asyncio import *
from hashlib import sha256
from argon2 import PasswordHasher
import re,base64,requests,struct,hmac,logging,pickle,secrets
import winreg
from multiprocessing import Process

__all__=['Server']


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
file_handler = logging.FileHandler('server.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Regedit:
    def __init__(self):
        self.Console_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console", 0, winreg.KEY_WRITE)
        self.logger=logger

    def _Set_Console_VirtualTerminalLevel(self,level=1):
        try:
            winreg.SetValueEx(self.Console_key, "VirtualTerminalLevel", 0, winreg.REG_DWORD, level)
            logger.info('[ Registry value change '+'\033[32m'+'succeeded'+'\033[0m'+' ] ==> VirtualTerminalLevel ')
        except Exception():
            logger.info('[ Registry value change '+'\033[31m'+'failed'+'\033[0m'+'  ] ==> VirtualTerminalLevel ')

class Server:
    c=''
    addr=''
    ip=''
    sessions = {}
    session_keys = {}
    login_sessions = {}
    login_session_keys = {}
    database = {}
    json_obj=''
    N=''
    col_ip=''
    sokt=socket()
    RSA_Key:dict=Longinus().Create_RSA_key()
    prv_key:str=open(RSA_Key['private_key']).read()
    pul_key:str=open(RSA_Key['public_key']).read()
    def __init__(self,version='0.4.6',port=9997,addres='0.0.0.0'):
        self.set_port=port;self.set_addr=addres;self.cipherdata=bytes();self.decrypt_data=bytes()
        self.set_version=version
        self.logger=logger;
        self.Lock=threading.Lock()

    def run(self):
        self.FileManagement().loader()
        
        Server.N=self.Network()
        self.N.bind_address(self.set_addr, self.set_port)
        Server.N.listen(0)
        self.run_service()

    def run_service(self):
        self.N=Server.N
        Server.N.accept_connection()
        threading.Thread(target=self.handler_connection).start()

    def handler_connection(self):
        while True:
            try:
                self.receive_function()
                self.protocol_execution()
            except Exception as e:
                self.logger.info('handler_connection')
                self.ERROR().error_handler(str(e))

    def receive_function(self):
        try:
            self.buffer_size=self.N.recv_head()
            self.recv_data=self.N.recv(self.buffer_size)
            self.obj=self.DATA(self.recv_data)
            self.json_obj,self.hmac_hash=self.obj.json_decompress()
        except Exception as e:
            self.logger.info('receive_function')
            self.ERROR().error_handler(str(e))

    def protocol_execution(self):
        try:
            self.SSL=self.SSLConnection('0.5.0',self.json_obj)
            self.handle=self.HANDLERS('0.5.0',self.json_obj)
            self.content_type=self.json_obj['request-head']['content-type']
            self.protocol=self.json_obj['request-head']['protocol']
            if (self.content_type == 'handshake' and self.protocol == 'client_hello'):
                self.SSL.server_hello()
            elif (self.content_type == 'handshake' and self.protocol == 'client_key_exchange'):
                self.session_id,self.master_key=self.SSL.Create_master_secret()
                self.SSL.ChangeCipherSpec_Finished(self.session_id)
            elif (self.content_type == 'client_master_secret' and self.protocol == 'Sign_Up'):
                self.handle.Sign_Up_handler()
            elif (self.content_type == 'client_master_secret' and self.protocol == 'login'):
                self.handle.login_handler()
            elif (self.content_type == 'client_master_secret' and self.protocol == 'request'):
                self.handle.request_handler()
            else: self.ERROR().error_handler('Abnormal access detected')
        except Exception as e:
            self.logger.info('protocol_execution')
            self.ERROR().error_handler(str(e))
        

#===================================================================================================================================#
#===================================================================================================================================#

    class Network:
        c=''
        addr=''
        col_addr=''
        def __init__(self):
            self.head=bytes()
            self.recv_datas=bytes()
            self.set_version=Server().set_version
            self.logger=logger
            self.s=Server.sokt

        def bind_address(self,set_addr, set_port):
            self.req = requests.get("http://ipconfig.kr")
            self.req = str(re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', self.req.text)[1])
            self.s.bind((set_addr, set_port))
            self.logger.info('[ Server started on '+'\033[32m'+'complete'+'\033[0m'+' ] ==> ' + self.req+':'+str(set_port))

        def listen(self,Volume):
            self.s.listen(Volume)

        def accept_connection(self):
            Server.Network.c, Server.Network.addr = self.s.accept()
            Server.Network.col_addr='\033[33m'+f'{self.addr}'+'\033[0m'
            Server.ip=str(self.addr).split("'")[1]
            Server.col_ip='('+'\033[38;5;214m'+Server.ip+'\033[0m'+')'
            self.logger.info('[ '+'\033[32m'+'Connected'+'\033[0m'+' with ] ==> '+Server.Network.col_addr)

        def recv_head(self):

            try:
                self.head = self.c.recv(4)
                self.head = int(struct.unpack("I", self.head)[0])
            except OSError as e:
                self.accept_connection()
                self.head = self.c.recv(4)
                self.head = int(struct.unpack("I", self.head)[0])
            self.logger.info(f'[ Header '+'\033[32m'+'received'+'\033[0m'+' ]'+Server.Network.col_addr+': '+str(self.head))
            return self.head

        def recv(self,buffer_size:int):
            self.head=buffer_size
            self.recv_datas = bytes()
            if self.head < 2048:
                self.recv_datas = self.c.recv(self.head)
            else:
                self.recv_datas = bytearray()
                for i in range(int(self.head / 2048)):
                    self.logger.info(f' ['+'\033[32m'+ 'Receiving data'+'%' +'\033[0m'+']'+Server.Network.col_addr+':' +'\033[32m'+ str(2048 * i / self.head * 100)+'%' +'\033[0m')
                    self.recv_datas += self.c.recv(2048)
                self.logger.info(f' [ Receiving data]: '+'\033[32m'+'100%'+'\033[0m')
            self.logger.info(f'[ Data '+'\033[32m'+'received'+'\033[0m'+' ]'+Server.Network.col_addr+': '+str(len(self.recv_datas))+' bytes')
            return self.recv_datas

        def send(self, data: bytes):
            head = struct.pack("I", len(data))
            self.c.sendall(head + data)
            self.logger.info(f'[ Data '+'\033[32m'+'sent'+'\033[0m'+' ]'+Server.Network.col_addr+': '+str(len(data))+' bytes')

        def send_and_close(self, data: bytes):
            head = struct.pack("I", len(data))
            self.c.sendall(head + data)
            self.logger.info(f'[ Data '+'\033[32m'+'sent'+'\033[0m'+' ]'+Server.Network.col_addr+': '+str(len(data))+' bytes')
            self.c.close()
            self.logger.info(f'[ socket '+'\033[31m'+'Closed'+'\033[0m'+' ]'+Server.Network.col_addr+'')


    class DATA:
        def __init__(self,data=bytes()):
            self.data=data
            self.hmac_hash =bytes()
            self.jsobj=str()
            self.logger=logger

        def json_decompress(self):
            try:
                self.compression_data = self.data
                if b'.' not in self.compression_data:
                    self.jsobj = base64.b85decode(self.compression_data).decode()
                    self.logger.info('[ Data decompressed '+'\033[32m'+'complete'+'\033[0m'+' ] ==> \n'+str(self.jsobj))
                    self.jsobj = json.loads(self.jsobj)
                else:
                    self.recv_obj=self.compression_data.decode().split('.')
                    self.jsobj = base64.b85decode(self.recv_obj[0].encode())
                    self.hmac_hash = base64.b85decode(self.recv_obj[1].encode())
                    self.logger.info('[ hmac hash found '+'\033[32m'+'successful'+'\033[0m'+' ]'+Server.col_ip+': '+str(self.hmac_hash))
                    self.jsobj = json.loads(self.jsobj)
                    if not self.request_credentials(self.hmac_hash,self.jsobj):
                        Server().ERROR().error_handler('Tampering, forged false request')
                        return 'Tampering, forged false request'
                return self.jsobj,self.hmac_hash
            except Exception as e:
                self.logger.info(str(e))
                self.logger.info(str(self.compression_data))
                Server().Network().send(b'thank you! Server test was successful thanks to you, This message is a temporary message written to convey thanks to you, and it is a disclaimer that the server is operating normally.')

        def master_key_selector(self,json_obj):
            self.session_id=json_obj['request-head']['session-id']
            self.login_id=json_obj['request-head']['login-id']
            if self.login_id !=None:
                self.master_key=Server.login_session_keys[json_obj['request-head']['login-id']]
                return self.master_key
            elif self.session_id !=None:
                self.master_key=Server.session_keys[self.session_id]
                return self.master_key
            else:
                return None

        def request_credentials(self,hmac_hash,json_obj):
            self.master_key=self.master_key_selector(json_obj)
            if (hmac_hash==hmac.digest(self.master_key,json.dumps(self.jsobj,indent=2).encode(),sha256)):
                logger.info(f'[ Session Credentials '+'\033[32m'+'complete'+'\033[0m'+' ]'+Server.col_ip+': '+str(hmac_hash))
                return True
            else:
                return False

        def Create_json_object(self,content_type=None,platform=None,version=None,
                                            protocol=None,random_token=None,random_token_length=None,
                                            public_key=None,public_key_length=None,server_error=None,
                                            session_id=None,session_id_length=None,master_secret=None,
                                            login_id=None,login_id_length=None):
            self.jsobj={
                'response-head':{
                    'content-type':content_type, 
                    'platform':platform,
                    'version':version,
                    'protocol':protocol,
                    'random_token':random_token,
                    'random_token_length':random_token_length,
                    'session-id':session_id,
                    'session-id_length':session_id_length,
                    'login-id':login_id,
                    'login-id_length':login_id_length,
                    },

                'response-body':{
                        'public-key':public_key,
                        'public-key_length':public_key_length,
                        'master_secret':master_secret,
                        'server_error':server_error
                        }
            }
            self.jsobj_dump= json.dumps(self.jsobj,indent=2)
            self.logger.info('[ Create json object '+'\033[32m'+'complete'+'\033[0m'+ ' ]'+Server.col_ip+f': \n {str(self.jsobj_dump)}')
            return self.jsobj_dump

#===================================================================================================================================#
#===================================================================================================================================#

    class SSLConnection:
        def __init__(self,set_version,json_obj):
            self.set_version=set_version
            self.SD=Server().DATA()
            Server.N=Server().Network()
            self.SC=Server().Crypto('')
            self.logger=logger
            self.json_obj=json_obj

        def server_hello(self):
            self.token=Longinus().Random_Token_generator()
            self.jsobj_dump=self.SD.Create_json_object(content_type='handshake',platform='server',version=self.set_version,
                                                protocol='server_hello',random_token=self.token.decode(),random_token_length=len(self.token),
                                                public_key=Server.pul_key,public_key_length=len(Server.pul_key))
            Server.N.send(base64.b85encode(self.jsobj_dump.encode()))
            self.logger.info(f'[ server hello transmission '+'\033[32m'+'complete'+'\033[0m'+']'+Server.col_ip)

        def Create_master_secret(self):
            self.master_key=self.SC._decrypt_rsa(Server.prv_key,base64.b85decode(self.json_obj['request-body']['pre_master_key']))
            self.session_id=Server().SessionManager(self.json_obj).session_creation(self.master_key)
            self.logger.info(f'[ Master secret creation '+'\033[32m'+'complete'+'\033[0m'+' ]'+Server.col_ip+': ' +str(self.session_id))
            return self.session_id,self.master_key

        def ChangeCipherSpec_Finished(self,session_id=None):
            self.jsobj_dump=self.SD.Create_json_object(content_type='handshake',platform='server',version=self.set_version,
                                                protocol='Change_Cipher_Spec',
                                                session_id=session_id,session_id_length=len(session_id))
            self.logger.info(f'[ Change Cipher Spec-'+'\033[32m'+'Finished'+'\033[0m'+' ]'+Server.col_ip+' ')
            Server.N.send_and_close(base64.b85encode(self.jsobj_dump.encode()))


#===================================================================================================================================#
#===================================================================================================================================#

    class HANDLERS:
        def __init__(self,set_version,json_obj):
            self.json_obj=json_obj
            self.session_id=json_obj['request-head']['session-id']
            self.master_key=Server().DATA().master_key_selector(json_obj)
            Server().FileManagement().loader()
            if (self.master_key!=None):
                self.UserID,self.Userpw=self.json_obj['request-body']['userid'],self.json_obj['request-body']['userpw']
                if not (self.Userpw==None or self.UserID==None):
                    self.UserID,self.Userpw=Server().Crypto(self.master_key).Decrypt_user_data(self.UserID,self.Userpw)
                    self.SU=Server().User(self.UserID.decode(),self.Userpw.decode())
                    self.verified_Userid,self.verified_Userpw=self.SU.verify_credentials()
            self.set_version = set_version
            self.logger=logger
            Server.N=Server().Network()
            self.SD=Server().DATA()

        def Sign_Up_handler(self):
            if self.SU._name_duplicate_check():
                Server().ERROR().error_handler("This user already exists.")
                return "This user already exists."
            self.verified_Userpw=self.SU.pwd_hashing(self.verified_Userpw)
            if (Server.sessions[self.session_id]['external_ip']==Server.ip):
                if Server().User(self.verified_Userid,self.verified_Userpw)._permission_checker(Server.ip):
                    Server().DBManagement(group='__administrator__').new_database_definition(self.verified_Userid,self.verified_Userpw,0)
                Server().DBManagement(group='__user__').new_database_definition(self.verified_Userid,self.verified_Userpw,1)
                Server().FileManagement().save_database()
                self.logger.info(f'[ User info update '+'\033[32m'+'complete'+'\033[0m'+' ]'+Server.col_ip+': '+self.verified_Userid)
                self.jsobj_dump=self.SD.Create_json_object(content_type='Sign_Up-report',platform='server',version=self.set_version,
                                            protocol='Sign_up_complete')
                self.verified_jsobj_dump=Server().Crypto(self.master_key).hmac_cipher(self.jsobj_dump.encode())
                Server.N.send_and_close(self.verified_jsobj_dump)

        def login_handler(self):                 
            for DB_id,DB_val in Server().database.items():
                if DB_val['user_id']==self.verified_Userid:
                    #try:
                        if PasswordHasher().verify(DB_val['user_pw'],self.verified_Userpw):
                            self.SM=Server().SessionManager(self.json_obj)
                            self.login_id=self.SM.login_session_creation(DB_id)
                            self.SM.discard_session(self.session_id)
                            Server().FileManagement().save_session()
                            self.jsobj_dump=self.SD.Create_json_object(content_type='login-report',platform='server',version=self.set_version,
                                                        protocol='welcome! ',
                                                        login_id=self.login_id,login_id_length=len(self.login_id))
                            self.verified_jsobj_dump=Server().Crypto(self.master_key).hmac_cipher(self.jsobj_dump.encode())
                            self.logger.info(f'[ Login '+'\033[32m'+'successful'+'\033[0m'+' ]'+Server.col_ip+': '+str(self.login_id))
                            Server.N.send_and_close(self.verified_jsobj_dump)
                    #except Exception: Server().ERROR().error_handler('The password does not match the supplied hash')
                else: Server().ERROR().error_handler('The user could not be found. Please proceed to sign up')

        def request_handler(self):
            self.reqdata=Server().Crypto(self.master_key)._decrypt_aes(base64.b85decode(self.json_obj['request-body']['master_secret']))
            self.logger.info('[ \033[32m'+'get request'+'\033[0m'+' ]'+Server.col_ip+':' f' {self.reqdata.decode()}')
            self.jsobj_dump=self.SD.Create_json_object(content_type='server_master_secret',platform='server',version=self.set_version,
                                        protocol='response',master_secret=base64.b85encode(Server().Crypto(self.master_key)._encrypt_aes(self.reqdata)).decode())
            self.verified_jsobj_dump=Server().Crypto(self.master_key).hmac_cipher(self.jsobj_dump.encode())
            Server.N.send_and_close(self.verified_jsobj_dump)

    class ERROR:
        def error_handler(self,msg,set_version=''):
            try:
                self.logger=logger
                Server.N=Server().Network()
                self.SD=Server().DATA()
                self.logger.info('[ '+'\033[31m'+'unexpected error'+'\033[0m'+ ' ]: ' +msg)
                self.jsobj_dump=self.SD.Create_json_object(content_type='return_error',platform='server',version=set_version,
                                                    protocol='error',
                                                    server_error=' [ unexpected error ]: '+msg)
                Server.N.send_and_close(self.jsobj_dump.encode())
            except Exception as e:
                self.logger.info('[ unexpected error ]:' ,e)

#===================================================================================================================================#
#===================================================================================================================================#

    class DBManagement:
        def __init__(self,group='__user__'):
            self.logger=logger
            self.group=group

        def new_database_definition(self,verified_UserID,verified_Userpw, permission_lv=1):
            self.verified_Userpw=verified_Userpw
            self.verified_UserID=verified_UserID
            self.permission_lv=permission_lv
            self.database_creation()

        def database_creation(self):
            token=Longinus().Random_Token_generator(8)
            new_database = {'user_id': self.verified_UserID, 'user_pw': self.verified_Userpw, 'permission_lv': self.permission_lv, 'group': self.group}
            Server.database[token.decode()]=new_database
            self.logger.info(f'[ New user database creation '+'\033[32m'+'complete'+'\033[0m'+' ] ==> '+str(new_database))
            return new_database

    class SessionManager:
        def __init__(self,json_obj):
            self.logger=logger
            self.json_obj=json_obj
            self.session_id=json_obj['request-head']['session-id']
            self.internal_ip=json_obj['request-head']['addres']

        def session_creation(self, master_key):
            session_id, session_info = self.session_generator()
            Server.sessions[session_id]=session_info
            Server.session_keys[session_id]=master_key
            self.logger.info(f'[ Session assignment '+'\033[32m'+'complete'+'\033[0m'+' ]'+Server.col_ip+': '+str(session_id))
            return session_id

        def login_session_creation(self, data):
            login_id, session_info = self.session_generator()
            new_login_session = {login_id: {'data':data, 'session_info':session_info}}
            Server.login_sessions.update(new_login_session)
            Server.login_session_keys[login_id]=Server.session_keys[self.session_id]
            self.logger.info(f'[ login Session assignment '+'\033[32m'+'complete'+'\033[0m'+' ]'+Server.col_ip+': '+str(login_id))
            return login_id

        def session_generator(self,length=32,session_validity=7):
            token = base64.b85encode(secrets.token_bytes(length)).decode()
            now = datetime.now()
            now_after = now + timedelta(days=session_validity)
            token_data = {'external_ip': Server.ip, 'internal_ip': self.internal_ip, 'timestamp': str(now), 'validity': str(now_after)}
            return token, token_data

        def discard_session(self, session_id):
            self.logger.info(f'[ Session '+'\033[31m'+'discarded'+'\033[0m'+'] '+Server.col_ip+': '+str(session_id))
            if Server.sessions:
                del Server.sessions[session_id]
                del Server.session_keys[session_id]

        def validate_session(self):
            pass

    class FileManagement:

        def loader(self):
            if (Server.login_sessions=={} and Server.login_session_keys=={} and Server.database =={}):
                if (self._check_database() and self._check_session()):
                    self.load_session_and_database()
                    return 'load_session_and_database'
            elif (Server.login_sessions=={} and Server.login_session_keys=={}):
                if self._check_session():
                    Server.login_sessions,Server.login_session_keys=self.load_sessione()
                    return 'load_sessione'
            elif Server.database=={}:
                if self._check_database():
                    Server.database=self.load_database()
                    return 'load_database'


        def load_session_and_database(self):
            self.load_session()
            self.load_database()

        def load_session_and_database(self):
            Server.login_sessions,Server.login_session_keys=self.load_sessione()
            Server.database = self.load_database()

        def save_session(self):
            with open('Server.sessions', 'wb') as f:
                pickle.dump({'login_sessions':Server.login_sessions, 'login_session_keys': Server.login_session_keys}, f)
            logger.info('[ Session data saved '+'\033[32m'+'completed'+'\033[0m'+' ]')

        def load_sessione(self):
            with open('Server.sessions', 'rb') as f:
                session_setup = pickle.load(f)
            logger.info('[ sessione data load '+'\033[32m'+'completed'+'\033[0m'+' ]')
            return session_setup['login_sessions'], session_setup['login_session_keys']

        def save_database(self):
            with open('Server.DB', 'wb') as f:
                pickle.dump(Server.database, f)
            logger.info('[ Database data saved '+'\033[32m'+'completed'+'\033[0m'+' ]')

        def load_database(self):
            with open('Server.DB', 'rb') as f:
                database_setup = pickle.load(f)
            logger.info('[ Database data load '+'\033[32m'+'completed'+'\033[0m'+' ]')
            return database_setup

        def _check_database(self):
            self.dir=os.listdir(os.getcwd())
            if ('Server.DB' in self.dir):
                return True
            else: return False

        def _check_session(self):
            self.dir=os.listdir(os.getcwd())
            if ('Server.sessions' in self.dir):
                return True
            else: return False

#===================================================================================================================================#
#===================================================================================================================================#

    class Crypto:
        def __init__(self,master_key=None):
            self.master_key=master_key
            self.ph = PasswordHasher()
            self.logger=logger

        def Decrypt_user_data(self,Cypher_userid,Cypher_userpw):
            self.userid=self._decrypt_aes(base64.b85decode(Cypher_userid))
            self.userpw=self._decrypt_aes(base64.b85decode(Cypher_userpw))
            return self.userid,self.userpw

        def hmac_cipher(self, data: bytes):
            hmac_data = base64.b85encode(hmac.digest(self.master_key, data, sha256))
            verified_data = base64.b85encode(data) +b'.'+hmac_data
            return verified_data

        def _encrypt_aes(self, data: bytes):
            data = base64.b85encode(data)
            send_data = bytes()
            cipher_aes = AES.new(self.master_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            send_data = cipher_aes.nonce + tag + ciphertext
            return send_data

        def _decrypt_rsa(self, set_prv_key: bytes, encrypt_data: bytes):
            private_key = RSA.import_key(set_prv_key)
            cipher_rsa = PKCS1_OAEP.new(private_key)
            decrypt_data = base64.b85decode(cipher_rsa.decrypt(encrypt_data))
            return decrypt_data

        def _decrypt_aes(self, set_data):
            nonce = set_data[:16]
            tag = set_data[16:32]
            ciphertext = set_data[32:-1] + set_data[len(set_data)-1:]
            cipher_aes = AES.new(self.master_key,AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            decrypt_data = base64.b85decode(data)
            return decrypt_data

    class User:
        def __init__(self,userid:str,userpw:str):
            self.ph = PasswordHasher()
            self.UserID = userid
            self.Userpwrd = userpw
            self.logger=logger

        def verify_credentials(self):
            if not self._verify_userid():
                Server().ERROR().error_handler("Name cannot contain spaces or special characters")
            elif not self._verify_userpw():
                Server().ERROR().error_handler("Your password is too short or too easy. Password must be at least 8 characters and contain numbers, English characters and symbols. Also cannot contain whitespace characters.")
            else:
                self.verified_UserID = self.UserID
                self.verified_Userpw = self.Userpwrd
                return self.verified_UserID, self.verified_Userpw

        def _verify_userid(self):
            if (" " not in self.UserID and "\r\n" not in self.UserID and "\n" not in self.UserID and "\t" not in self.UserID and re.search('[`~!@#$%^&*(),<.>/?]+', self.UserID) is None):
                return True
            return False

        def _verify_userpw(self):
            if (len(self.Userpwrd) > 8 and re.search('[0-9]+', self.Userpwrd) is not None and re.search('[a-zA-Z]+', self.Userpwrd) is not None and re.search('[`~!@#$%^&*(),<.>/?]+', self.Userpwrd) is not None and " " not in self.Userpwrd):
                return True
            return False

        def _name_duplicate_check(self):
            if len(Server.database) != 0:
                for DB_id,DB_val in Server.database.items():
                    return DB_val['user_id']==self.verified_UserID
            else: return False

        def _permission_checker(self,external_ip):
            if (external_ip=='127.0.0.1' and self.UserID=='administrator' or self.Userpwrd=='admin'):
                return True
            else: return False

        def pwd_hashing(self,verified_Userpw):
            while True:
                temp=self.ph.hash(verified_Userpw)
                if (self.ph.verify(temp,verified_Userpw) and self.ph.check_needs_rehash(temp)!=True):
                    break
            return temp
#===================================================================================================================================#
#===================================================================================================================================#