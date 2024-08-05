#! -*-conding: UTF-8 -*-
# @公众号: 海哥python

from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import base64


def pad_to_block_size(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length]) * padding_length
    return data + padding


def unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]


def encrypt_data(data, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    padded_data = pad_to_block_size(data, 8)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext


def decrypt_data(ciphertext, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    padded_data = cipher.decrypt(ciphertext)
    data = unpad(padded_data)
    return data


# 生成一个随机的 24 字节密钥
key = get_random_bytes(24)

# 生成一个随机的 8 字节初始化向量
iv = get_random_bytes(8)

# 原始数据
data = "公众号：海哥python".encode()

# 加密数据
ciphertext = encrypt_data(data, key, iv)

# 解密数据
decrypted_data = decrypt_data(ciphertext, key, iv)

print("Original data:", data.decode())
print("Encrypted data:", base64.b64encode(ciphertext).decode())
print("Decrypted data:", decrypted_data.decode())
