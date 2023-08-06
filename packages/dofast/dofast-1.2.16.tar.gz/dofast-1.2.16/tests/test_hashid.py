import hashlib
from hashids import Hashids
from codefast.axe import Axe

md5 = hashlib.md5('x.png'.encode()).hexdigest()
hid = Hashids(salt=md5, min_length=32)
resp = hid.encode(34)
print(resp.lower())
import arrow
print(arrow.now())