#! -*-conding: UTF-8 -*-
# @公众号: 海哥python


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import base64


def generate_rsa_keys():
    # 生成一个新的RSA密钥对
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def encrypt_data(data, public_key):
    # 创建一个RSA对象
    rsa_public_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_public_key)

    # 加密数据
    ciphertext = cipher_rsa.encrypt(data)

    return ciphertext


def decrypt_data(ciphertext, private_key):
    # 创建一个RSA对象
    rsa_private_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_private_key)

    # 解密数据
    data = cipher_rsa.decrypt(ciphertext)

    return data


# 生成RSA密钥对
private_key, public_key = generate_rsa_keys()

# 原始数据
data = "公众号：海哥python".encode()

# 加密数据
encrypted_data = encrypt_data(data, public_key)

# 解密数据
decrypted_data = decrypt_data(encrypted_data, private_key)

print("Original data:", data.decode())
print("Encrypted data:", base64.b64encode(encrypted_data).decode())
print("Decrypted data:", decrypted_data.decode())
