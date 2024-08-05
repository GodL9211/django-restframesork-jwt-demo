#! -*-conding: UTF-8 -*-
# @公众号: 海哥python


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


def encrypt_data(data, key):
    # 生成一个随机的初始化向量
    iv = get_random_bytes(AES.block_size)

    # 创建一个新的AES对象
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 对数据进行填充以匹配块大小
    padded_data = pad(data, AES.block_size)

    # 加密数据
    ciphertext = cipher.encrypt(padded_data)

    # 返回加密后的数据和IV
    return iv + ciphertext


def decrypt_data(ciphertext, key):
    # 分离IV和密文
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]

    # 创建一个新的AES对象
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 解密数据
    padded_data = cipher.decrypt(ciphertext)

    # 移除填充
    data = unpad(padded_data, AES.block_size)

    return data


# 生成一个随机的 16 字节密钥
key = get_random_bytes(16)

# 原始数据
data = "公众号：海哥python".encode()

# 加密数据
encrypted_data = encrypt_data(data, key)

# 解密数据
decrypted_data = decrypt_data(encrypted_data, key)

print("Original data:", data.decode())
print("Encrypted data:",
      base64.b64encode(encrypted_data).decode())  # 如： IJllCAGNnFKifprbEg/pj/2S+a4mKfM5iGjG+1vMrs89L5rd3lYClYptQwd/7s2r
print("Decrypted data:", decrypted_data.decode())
