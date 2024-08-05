#! -*-conding=: UTF-8 -*-
# 2022/11/7 19:45

import OpenSSL
import OpenSSL.crypto



cp = OpenSSL.crypto

EC = cp.TYPE_EC  # 408
RSA = cp.TYPE_RSA  # 6
DH = cp.TYPE_DH  # 28
DSA = cp.TYPE_DSA  # 116


def create_csr(common_name, country=None, state=None, city=None,
               organization=None, organizational_unit=None,
               email_address=None):
    """
    Args:
        common_name (str).
        country (str).
        state (str).
        city (str).
        organization (str).
        organizational_unit (str).
        email_address (str).
    Returns:
        (str, str).  Tuple containing private key and certificate
        signing request (PEM).
    """
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

    req = OpenSSL.crypto.X509Req()
    req.get_subject().CN = common_name
    if country:
        req.get_subject().C = country
    if state:
        req.get_subject().ST = state
    if city:
        req.get_subject().L = city
    if organization:
        req.get_subject().O = organization
    if organizational_unit:
        req.get_subject().OU = organizational_unit
    if email_address:
        req.get_subject().emailAddress = email_address
    req.set_pubkey(key)
    req.sign(key, 'sha256')

    _private_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key).decode("utf-8")
    _public_key = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, key).decode("utf-8")
    _csr = OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_PEM, req).decode("utf-8")

    return _public_key, _private_key, _csr


if __name__ == '__main__':
    create_csr()
