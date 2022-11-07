#! -*-conding=: UTF-8 -*-
# 2022/11/7 19:10
"""
OpenSSL校验公私钥是否匹配
"""

import OpenSSL
import OpenSSL.crypto


def check_associate_cert_with_private_key(cert, private_key):
    """
    :type cert: str
    :type private_key: str
    :rtype: bool
    """
    try:
        private_key_obj = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, private_key)
    except OpenSSL.crypto.Error:
        raise Exception('private key is not correct: %s' % private_key)

    try:
        cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert.encode("utf-8"))
    except OpenSSL.crypto.Error:
        raise Exception('certificate is not correct: %s' % cert)

    context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
    context.use_privatekey(private_key_obj)
    context.use_certificate(cert_obj)
    try:
        context.check_privatekey()
        return True
    except OpenSSL.SSL.Error:
        return False


if __name__ == '__main__':
    with open("./cert/ca.pem", "r") as f:
        ca_cert = f.read()

    with open("./cert/ca-key.pem", "r") as f:
        ca_private_key = f.read()
    print(check_associate_cert_with_private_key(cert=ca_cert, private_key=ca_private_key))
