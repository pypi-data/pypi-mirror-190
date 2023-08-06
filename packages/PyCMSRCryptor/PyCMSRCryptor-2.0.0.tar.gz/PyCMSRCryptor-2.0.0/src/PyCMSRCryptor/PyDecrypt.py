#coding=utf-8
__author__ = 'yujingrong'

import base64, pyDes
from base64 import b64decode
from gmssl import sm4, sm2
from Crypto.Cipher import AES


# 国密SM4解密
def decryptSM4(decrypt_key, encrypt_value):
    """
    国密sm4解密
    :param decrypt_key:sm4加密key
    :param encrypt_value: 待解密的十六进制值
    :return: 原字符串
    """
    encrypt_value = b64decode(encrypt_value.encode()).hex()
    crypt_sm4 = sm4.CryptSM4()
    crypt_sm4.set_key(decrypt_key.encode(), sm4.SM4_DECRYPT)  # 设置密钥
    decrypt_value = crypt_sm4.crypt_ecb(bytes.fromhex(encrypt_value))  # 开始解密。十六进制类型
    return decrypt_value.decode()
    # return self.str_to_hexStr(decrypt_value.hex())

# 国密SM2解密
def decryptSM2(privateKey, publicKey, info):
    sm2_crypt = sm2.CryptSM2(public_key=publicKey, private_key=privateKey)
    info = b64decode(info.encode())  # 通过base64解码成二进制bytes
    decode_info = sm2_crypt.decrypt(info).decode(encoding="utf-8")
    return decode_info

# aes解密（ECB+pkcs5+base64）
def aesDecryptBase64(key, decrData):
    key = key.encode("utf-8")  # 初始化**
    aes = AES.new(key, AES.MODE_ECB)  # 初始化AES,ECB模式的实例
    unpad = lambda date: date[0:-ord(date[-1])]
    res = base64.decodebytes(decrData.encode("utf8"))
    msg = aes.decrypt(res).decode("utf8")
    return unpad(msg)

# aes解密（ECB+pkcs5+hex）
def aesDecryptHex(key, decrData):
    key = key.encode("utf-8")
    aes = AES.new(key, AES.MODE_ECB)
    unpad = lambda date: date[0:-ord(date[-1])]
    bytes_out = bytes.fromhex(decrData)
    str_out = base64.b64encode(bytes_out)
    res = base64.decodebytes(str_out)
    msg = aes.decrypt(res).decode("utf8")
    return unpad(msg)

# des解密，key为秘钥，长度为8的倍数
def desBase64Decrypt(key, reqdata):
    key = key.encode('utf-8')
    reqdata = reqdata.encode('utf-8')
    data = base64.b64decode(reqdata.decode('utf-8'))
    k = pyDes.des(key, pyDes.ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    return str(k.decrypt(data, pad=None, padmode=pyDes.PAD_PKCS5), "UTF-8")