#coding=utf-8
__author__ = 'yujingrong'

import json, base64, rsa, os, pyDes, binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcsl_v1_5
from base64 import b64encode
from gmssl import sm4, sm2
from Crypto.Cipher import AES

# rsa加密算法，pk为公钥，msg为待加密字符串
def rsaEncrypt(msg, pk):
    msg = json.dumps(msg)
    a = bytes(msg.encode('utf-8'))
    rsakey = RSA.importKey(pk)
    cipher = Cipher_pkcsl_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(a))
    return cipher_text.decode('utf-8')

def rsaEncrypt2(msg, pk):
    st=""
    for i in range(int(len(pk) / 64) + 1):
        st += pk[i * 63:i * 63 + 63] + "\n"
    final="-----BEGIN PUBLIC KEY-----\n"+st+"-----END PUBLIC KEY-----"
    with open('public_key.pem', mode='wb') as f:
        f.write(final.encode())
    with open("public_key.pem", mode='rb') as f:
        pub = f.read()
    public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub)       #   创建 PublicKey 对象
    cryto_msg = rsa.encrypt(msg.encode(' utf-8'), public_key_obj)        #  生成加密文本
    cipher_base64 = base64.b64encode(cryto_msg)      # 将加密文本转化为 base64 编码
    os.remove("public_key.pem")
    return cipher_base64.decode()

# des加密，key为秘钥，长度为8的倍数
def desBase64Encrypt(key, reqdata):
    key = key.encode('utf-8')
    reqdata = reqdata.encode('utf-8')
    des = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
    encrypt_data = des.encrypt(reqdata)
    return str(base64.b64encode(encrypt_data), "UTF-8")

def pad(length, text):
    """
    #填充函数，使被加密数据的字节码长度是block_size的整数倍
    """
    count = len(text.encode('utf-8'))
    add = length - (count % length)
    entext = text + (chr(add) * add)
    return entext

# aes加密（ECB+pkcs5+base64）
def aesEncryptBase64(key, encrData):  # 加密函数
    key = key.encode("utf-8")  # 初始化**
    length = AES.block_size  # 初始化数据块大小
    aes = AES.new(key, AES.MODE_ECB)  # 初始化AES,ECB模式的实例
    res = aes.encrypt(pad(length, encrData).encode("utf8"))
    msg = str(base64.b64encode(res), encoding="utf8")
    return msg

# aes加密（ECB+pkcs5+hex）
def aesEncryptHex(key, encrData):
    key = key.encode("utf-8")  # 初始化**
    length = AES.block_size  # 初始化数据块大小
    aes = AES.new(key, AES.MODE_ECB)  # 初始化AES,ECB模式的实例
    res = aes.encrypt(pad(length, encrData).encode("utf8"))
    msg = res.hex().upper()
    return msg

# 国密SM4加密
def encryptSM4(encrypt_key, value):
    """
    国密sm4加密
    :param encrypt_key: sm4加密key
    :param value: 待加密的字符串
    :return: sm4加密后的十六进制值
    """
    crypt_sm4 = sm4.CryptSM4()
    crypt_sm4.set_key(encrypt_key.encode(), sm4.SM4_ENCRYPT)  # 设置密钥
    date_str = json.dumps(value)
    encrypt_value = crypt_sm4.crypt_ecb(date_str.encode())  # 开始加密。bytes类型
    # return encrypt_value.hex()  # 返回十六进制值
    encrypt_value = b64encode(encrypt_value)
    encrypt_value = str(encrypt_value, encoding='utf-8')
    return encrypt_value

# 国密SM2加密
def encryptSM2(privateKey, publicKey, info):
    sm2_crypt = sm2.CryptSM2(public_key=publicKey, private_key=privateKey)
    encode_info = sm2_crypt.encrypt(info.encode(encoding="utf-8"))
    encode_info = b64encode(encode_info).decode()  # 将二进制bytes通过base64编码
    return encode_info

def str_to_hexStr(hex_str):
    """
    字符串转hex
    :param hex_str: 字符串
    :return: hex
    """
    hex_data = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hex_data)
    return str_bin.decode('utf-8')

