from Crypto.Hash import SHA256

def hash(s):
    h = SHA256.new()
    h.update(s.encode('utf-8'))
    return h.hexdigest()
