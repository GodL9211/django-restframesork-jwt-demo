#! -*-conding=: UTF-8 -*-
# 2022/11/7 17:17
"""
OpenSSL 解析certificate 证书
"""
import os
import sys
import traceback

import OpenSSL
import OpenSSL.crypto
from OpenSSL.crypto import X509
from dateutil import parser


cp = OpenSSL.crypto

EC = cp.TYPE_EC  # 408
RSA = cp.TYPE_RSA  # 6
DH = cp.TYPE_DH  # 28
DSA = cp.TYPE_DSA  # 116


def analytical_certificate(cert_str=None, cert_paths=None):
    try:
        if cert_str:
            cert_content: X509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_str)
        elif cert_paths:
            cert_content: X509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(cert_paths).read())
        cert_issuer = cert_content.get_issuer()
        cert_subject = cert_content.get_subject()
        extension_count = cert_content.get_extension_count()
        extension_ls = []
        for i in range(extension_count):
            extension = str(cert_content.get_extension(i))
            print(f"extension[{i}]:{extension}")
            extension_ls.append(extension)
        _cert_info = {
            "version": cert_content.get_version() + 1,
            "serial_number": hex(cert_content.get_serial_number()),
            "signature_algorithm": cert_content.get_signature_algorithm().decode("UTF-8"),
            "common_name": cert_issuer.commonName,
            "start_time": parser.parse(cert_content.get_notBefore().decode("UTF-8")).strftime('%Y%m%d%H%M%S'),
            "format_start_time": parser.parse(cert_content.get_notBefore().decode("UTF-8")).strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": parser.parse(cert_content.get_notAfter().decode("UTF-8")).strftime('%Y%m%d%H%M%S'),
            "format_end_time": parser.parse(cert_content.get_notAfter().decode("UTF-8")).strftime('%Y-%m-%d %H:%M:%S'),
            "has_expired": cert_content.has_expired(),
            "pubkey": OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert_content.get_pubkey()).decode("utf-8"),
            "pubkey_len": cert_content.get_pubkey().bits(),
            "pubkey_type": cert_content.get_pubkey().type(),
            "extension_count": cert_content.get_extension_count(),
            "issuer_info": {},
            "subject_info": {},
            "extension_info": extension_ls,
        }
        main_info_map = {"CN": "通用名称", "OU": "机构单元名称", "O": "机构名", "L": "地理位置", "ST": "州/省名", "C": "国名"}
        pubkey_type_map = {408: "EC", 6: "RSA", 28: "DH", 116: "DSA"}
        print(f"主体信息:")
        for item in cert_issuer.get_components():
            print(item)
            _cert_info["issuer_info"][str(item[0].decode("utf-8"))] = str(item[1].decode("utf-8"))
            print(f"{main_info_map[str(item[0].decode('utf-8'))]}:{str(item[1].decode('utf-8'))}")
        for item in cert_subject.get_components():
            _cert_info["subject_info"][str(item[0].decode("utf-8"))] = str(item[1].decode("utf-8"))
        print(f"证书版本:{_cert_info['version']}")
        print(f"证书序列号:{_cert_info['serial_number']}")
        print(f"证书中使用的签名算法:{_cert_info['signature_algorithm']}")
        print(f"颁发者:{_cert_info['common_name']}")
        print(f"有效期从:{_cert_info['start_time']}到{_cert_info['end_time']}")
        print(f"证书是否已经过期:{_cert_info['has_expired']}")
        print(f"公钥类型:{pubkey_type_map.get(_cert_info['pubkey_type'])}")
        print(f"公钥长度:{_cert_info['pubkey_len']}")
        print(f"公钥:\n{_cert_info['pubkey']}")
        print(f"subject:\n{_cert_info['subject_info']}")
        print(f"issuer:\n{_cert_info['issuer_info']}")
        return _cert_info
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)


if __name__ == '__main__':
    cert_paths = os.getcwd() + "/cert/ca.pem"
    print(cert_paths)
    print(analytical_certificate(cert_paths=cert_paths))
