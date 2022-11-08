#! -*-conding=: UTF-8 -*-
# 2022/11/8 11:33
"""
 'get_issuer',                    证书发行者名称
    "CN : 通用名称  OU : 机构单元名称"
    "O  : 机构名    L  : 地理位置"
    "S  : 州/省名   C  : 国名"
 'get_notAfter',                  证书有效期终止时间
 'get_notBefore',                 证书有效期终止时间
 'get_pubkey',                    证书公钥值
 'get_serial_number',             证书序列号，对同一CA所颁发的证书，序列号唯一标识证书
 'get_signature_algorithm',       证书签名算法标识
 'get_subject',                   证书主体名称
 'get_version',					  证书版本
 'has_expired',                   证书是否已经过期
 'gmtime_adj_notAfter',
 'gmtime_adj_notBefore',
 'set_issuer',
 'set_notAfter',
 'set_notBefore',
 'set_pubkey',
 'set_serial_number',
 'set_subject',
 'set_version',
 'sign',
 'subject_name_hash',
 'to_cryptography'
"""

import ssl
import OpenSSL
from dateutil import parser

resp = ssl.get_server_certificate(('www.qq.com', 443))
x509_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, resp.encode("utf-8"))
issuer = x509_cert.get_issuer()  # 获取证书发行者名称
gen_time = parser.parse(x509_cert.get_notBefore().decode("UTF-8"))  # 获取证书发放时间

if __name__ == '__main__':
    print(issuer)
    print(gen_time)
    print("证书版本: ", x509_cert.get_version() + 1)

    print("证书序列号: ", hex(x509_cert.get_serial_number()))

    print("证书中使用的签名算法: ", x509_cert.get_signature_algorithm().decode("UTF-8"))

    print("颁发者: ", issuer.commonName)

    datetime_struct = parser.parse(x509_cert.get_notBefore().decode("UTF-8"))

    print("有效期从: ", datetime_struct.strftime('%Y-%m-%d %H:%M:%S'))

    datetime_struct = parser.parse(x509_cert.get_notAfter().decode("UTF-8"))

    print("有效期到: ", datetime_struct.strftime('%Y-%m-%d %H:%M:%S'))

    print("证书是否已经过期: ", x509_cert.has_expired())

    print("公钥长度: ", x509_cert.get_pubkey().bits())

    print("公钥:\n", OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, x509_cert.get_pubkey()).decode("utf-8"))

    print("主体信息:")

    for item in issuer.get_components():
        print(item[0].decode("utf-8"), "  ——  ", item[1].decode("utf-8"))

    print(x509_cert.get_extension_count())

