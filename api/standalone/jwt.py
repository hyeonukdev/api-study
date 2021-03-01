import jwt
data_to_encode = {'some':'payload'}
encryption_secret = 'secrete'
algorithm = 'HS256'
encoded = jwt.encode(data_to_encode,encryption_secret,algorithm=algorithm)
print(encoded)

decode = jwt.decode(encoded,encryption_secret,algorithm=[algorithm])
print(decode)