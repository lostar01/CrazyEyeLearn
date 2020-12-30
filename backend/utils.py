import time,random,hashlib,logging,os

def get_key_obj(pkeyobj,pkey_file=None,pkey_obj=None,password=None):
    if pkey_file:
        with open(pkey_file) as fo:
            try:
                pkey = pkeyobj.from_private_key(fo,password=password)
                return pkey
            except:
                pass
    else:
        try:
            pkey = pkeyobj.from_private_key(pkey_obj,password=password)
            return pkey
        except:
            pkey_obj.seek(0)

def unique():
    ctime = str(time.time())
    salt = str(random.random())
    m = hashlib.md5(bytes(salt, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


def get_loger(base_dir,file_name):
    try:
        loger = logging.getLogger()
        file_handler = logging.FileHandler(os.path.join(base_dir,file_name))
        formater = logging.Formatter("%(asctime)s %(message)s")
        file_handler.setFormatter(formater)
        loger.addHandler(file_handler)
        loger.setLevel(logging.INFO)
        return loger
    except Exception as e:
        print(e)
        return None
    



