'''
Считает хеш файла
'''
import hashlib

class hash_fl:    
    def __init__(self, blocksize=65536):
        self.blocksize = blocksize
    
    def get_hash(self, file):
        hasher = hashlib.sha256()
        with open(file, 'rb') as fl:
            buf = fl.read(self.blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = fl.read(self.blocksize)
        return hasher.hexdigest()


if __name__ == '__main__':
    pass
    


