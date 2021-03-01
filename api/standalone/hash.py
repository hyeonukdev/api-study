import hashlib 
m = hashlib.sha256()
m.update(b"test password")
a = m.hexdigest()
print(a)
print(m)
