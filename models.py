from google.appengine.ext import ndb
import hashlib

### Models used in the program ###

# CPU model

# GPU model

# RAM model

# PC config model (GPU/CPU/RAM/Resolution)
class PC_Config(ndb.Model):
    id = ndb.KeyProperty()
    CPU = ndb.StringProperty()
    GPU = ndb.StringProperty()
    RAM = ndb.StringProperty()
    res_x = ndb.IntegerProperty()
    res_y = ndb.IntegerProperty()

#    def __init__(self, *args, **kwargs):
#        super(PC_Config, self).__init__(*args, **kwargs)
    def __init__(self, _cpu, _gpu, _ram, _res):
        CPU = _cpu
        GPU = _gpu
        RAM = _ram
        res = _res.split("x")
        res_x = int(res[0])
        res_y = int(res[1])
        hash_base = CPU+GPU+RAM+_res
        hash_object = hashlib.sha1(hash_base)
        hex_dig = hash_object.hexdigest()
        print(hex_dig)


### DXDIAG regex (english)
# Processor: (.*GHz).*?\n.*?Memory: (.*?) RAM[\s\S]*?Chip type: (.*?)\n[\s\S]*?Native Mode: (\d+ x \d+).*?\n
###

# Submission model (PC hash, squad version, map, max, min std dev)

# User model

# Waiting approval submission