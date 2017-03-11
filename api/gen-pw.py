from Crypto.Hash import SHA256
import random
import string

pw_len = 8
pw = ''.join(random.SystemRandom().choice(string.ascii_uppercase \
	+ string.ascii_lowercase +string.digits) for _ in range(pw_len))
print("user password = " + pw)

h = SHA256.new()
h.update(pw)
hash_pw = h.hexdigest()
print("user hash password = " + hash_pw)
