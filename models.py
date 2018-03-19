from google.appengine.ext import ndb
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

### Models used in the program ###

# CPU model

# GPU model

# RAM model

# PC config model (GPU/CPU/RAM/Resolution)
class PC_Config(ndb.model.Model):
    CPU = ndb.StringProperty()
    GPU = ndb.StringProperty()
    RAM = ndb.StringProperty()
    res_x = ndb.IntegerProperty()
    res_y = ndb.IntegerProperty()

#    def __init__(self, *args, **kwargs):
#        super(PC_Config, self).__init__(*args, **kwargs)
    @classmethod
    def create(cls, _cpu, _gpu, _ram, _res):
        item = cls()
        cls.CPU = _cpu
        cls.GPU = _gpu
        cls.RAM = _ram
        res = _res.split("x")
        cls.res_x = int(res[0])
        cls.res_y = int(res[1])
        hash_base = cls.CPU+cls.GPU+cls.RAM+_res
        hash_object = hashlib.sha1(hash_base)
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
        cls.id = hex_dig
        return cls

### DXDIAG regex (english)
# Processor: (.*GHz).*?\n.*?Memory: (.*?) RAM[\s\S]*?Chip type: (.*?)\n[\s\S]*?Native Mode: (\d+ x \d+).*?\n
###

# Submission model (PC hash, squad version, map, max, min std dev)

# User model
class User(ndb.model.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
    activated = ndb.BooleanProperty()
    last_login = ndb.DateTimeProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    num_submissions = ndb.IntegerProperty()

    @classmethod
    def get_by_id(cls, user_id):
        user_key = ndb.Key('User', str(user_id).lower())
        return user_key.get()

    def get_activation_hash(self):
        return hashlib.sha1(username)

    @classmethod
    def hash_password(self, pass_to_hash):
        return generate_password_hash(pass_to_hash)

    def check_password(self, pass_to_check):
        return check_password_hash(self.password, pass_to_check)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True#self.activated

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username.lower()

# Waiting approval submission
