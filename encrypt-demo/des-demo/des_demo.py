#! -*-conding: UTF-8 -*-
# @公众号: 海哥python

"""
pip install pycryptodome
"""

from Crypto.Cipher import DES3
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

message = '公众号：海哥python'
key = '4706d6c8c3d8dd5a'
"""
避坑指南
js 中key为4706d6c8也能加密，但是python中会报错，因为JS加密过程，key长度不够8位时会用0补齐长度
python 中将key赋值为 4706d6c800000000 即可，
因为bytes.fromhex会将将每两个十六进制字符转换为一个字节
"""

# ECB 加密
cipher = DES.new(bytes.fromhex(key), DES.MODE_ECB)
ciphertext = cipher.encrypt(pad(message.encode(), DES.block_size))
encrypted_text = base64.b64encode(ciphertext).decode()  # AXhbn2czryua1KJZ4VePfoVzA10ClDVoj8Cg9uiIxR4=

print(encrypted_text)

# ECB 解密
cipher = DES.new(bytes.fromhex(key), DES.MODE_ECB)
decrypted_bytes = cipher.decrypt(base64.b64decode(encrypted_text))
decrypted_text = unpad(decrypted_bytes, DES.block_size).decode("utf-8")
print(decrypted_text)


# CBC 加密
key = '4706d6c8'
iv = '5eb63bbb'  # 只有8位

cipher = DES.new(key.encode(), DES.MODE_CBC, iv.encode())
ciphertext = cipher.encrypt(pad(message.encode(), DES.block_size))
encrypted_text_cbc = base64.b64encode(ciphertext).decode()  # E2MkVnjZaaOaUvLzDLlH+9SqiNZcDyvHw1oCvng1s08=
print(encrypted_text_cbc)

# CBC 解密
cipher = DES.new(key.encode(), DES.MODE_CBC, iv.encode())
decrypted_bytes_cbc = cipher.decrypt(base64.b64decode(encrypted_text_cbc))
decrypted_text_cbc = unpad(decrypted_bytes_cbc, DES.block_size).decode("utf-8")

print(decrypted_text_cbc)
