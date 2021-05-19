from AES.aes import encrypt, decrypt


key = b'my key'
message = b'my message'

encrypt_ = lambda key_, cipher_text: encrypt(key_, cipher_text, 10000)
decrypt_ = lambda key_, cipher_text: decrypt(key_, cipher_text, 10000)

ciphertext = encrypt_(key, message)
print(ciphertext)
if decrypt_(key, ciphertext) == message:
    print("Success")
