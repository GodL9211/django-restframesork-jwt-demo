### 手动生成证书

在使用客户端证书认证的场景下，你可以通过 easyrsa、openssl 或 cfssl 等工具以手工方式生成证书。
#### 公钥基础设施PKI基础概念
CA(Certification Authority)证书，指的是权威机构给我们颁发的证书。

密钥就是用来加解密用的文件或者字符串。密钥在非对称加密的领域里，指的是私钥和公钥，他们总是成对出现，其主要作用是加密和解密。常用的加密强度是2048bit。

RSA即非对称加密算法。非对称加密有两个不一样的密码，一个叫私钥，另一个叫公钥，用其中一个加密的数据只能用另一个密码解开，用自己的都解不了，也就是说用<u>公钥加密的数据只能由私钥解开</u>。

##### 证书的编码格式

- PEM(Privacy Enhanced Mail)，通常用于数字证书认证机构（Certificate Authorities，CA），**扩展名为.pem，.crt，.cer 和 .key**。内容为Base64编码的ASCII码文件，有类似"-----BEGIN CERTIFICATE-----" 和 "-----END CERTIFICATE-----"的头尾标记。服务器认证证书，中级认证证书和私钥都可以储存为PEM格式（认证证书其实就是公钥）。Apache和nginx等类似的服务器使用PEM格式证书。

- DER(Distinguished Encoding Rules)，与PEM不同之处在于其使用二进制而不是Base64编码的ASCII。扩展名为.der，但也经常使用.cer用作扩展名，所有类型的认证证书和私钥都可以存储为DER格式。Java使其典型使用平台。

##### 证书签名请求CSR

CSR(Certificate Signing Request)，它是向CA机构申请数字×××书时使用的请求文件。 在生成请求文件前，我们需要准备一对对称密钥。私钥信息自己保存，请求中会附上公钥信息以及国家，城市，域名，Email等信息，CSR中还会附上签名信息。当我们准备好CSR文件后就可以提交给CA机构，等待他们给我们签名，签好名后我们会收到crt文件，即证书。

> 注意：CSR并不是证书。而是向权威证书颁发机构获得签名证书的申请。

把CSR交给权威证书颁发机构，权威证书颁发机构对此进行签名,完成。保留好CSR，当权威证书颁发机构颁发的证书过期的时候，你还可以用同样的CSR来申请新的证书，key保持不变.

##### 数字签名

数字签名就是"非对称加密+摘要算法"，其目的不是为了加密，而是用来**防止他人篡改数据**。

其核心思想是：比如A要给B发送数据，A先用摘要算法得到数据的指纹，然后用A的私钥加密指纹，加密后的指纹就是A的签名，B收到数据和A的签名后，也用同样的摘要算法计算指纹，然后用A公开的公钥解密签名，比较两个指纹，如果相同，说明数据没有被篡改，确实是A发过来的数据。假设C想改A发给B的数据来欺骗B，因为篡改数据后指纹会变，要想跟A的签名里面的指纹一致，就得改签名，但由于没有A的私钥，所以改不了，如果C用自己的私钥生成一个新的签名，B收到数据后用A的公钥根本就解不开。

常用的摘要算法有MD5、SHA1、SHA256。

使用私钥对需要传输的文本的摘要进行加密，得到的密文即被称为该次传输过程的签名。

##### 数字证书和公钥

数字证书则是由证书认证机构（CA）对证书申请者真实身份验证之后，用CA的根证书对申请人的一些基本信息以及申请人的公钥进行签名（相当于加盖发证书机 构的公章）后形成的一个数字文件。实际上，数字证书就是经过CA认证过的公钥，除了公钥，还有其他的信息，比如Email，国家，城市，域名等。

#### cfssl
cfssl 是另一个用于生成证书的工具。
> 项目地址： https://github.com/cloudflare/cfssl
> 
> 下载地址： https://pkg.cfssl.org/
>
> 参考链接： https://blog.cloudflare.com/how-to-build-your-own-public-key-infrastructure/

cfssl是CloudFlare开源的一款PKI/TLS工具。 cfssl包含一个命令行工具 和一个用于 签名，验证并且捆绑TLS证书的 HTTP API 服务。 使用Go语言编写。

**cfssl包括**：
- 一组用于生成自定义 TLS PKI 的工具
- cfssl程序： CFSSL的命令行工具
- multirootca程序是可以使用多个签名密钥的证书颁发机构服务器
- mkbundle程序用于构建证书池
- cfssljson程序，从cfssl和multirootca程序获取JSON输出，并将证书，密钥，CSR和bundle写入磁盘

PKI借助数字证书和公钥加密技术提供可信任的网络身份。通常，证书就是一个包含如下身份信息的文件：
- 证书所有组织的信息
- 公钥
- 证书颁发组织的信息
- 证书颁发组织授予的权限，如证书有效期、适用的主机名、用途等
- 使用证书颁发组织私钥创建的数字签名
##### cfssl工具，子命令介绍：

- bundle: 创建包含客户端证书的证书包

- genkey: 生成一个key(私钥)和CSR(证书签名请求)

- scan: 扫描主机问题

- revoke: 吊销证书

- certinfo: 输出给定证书的证书信息， 跟cfssl-certinfo 工具作用一样

- gencrl: 生成新的证书吊销列表

- selfsign: 生成一个新的自签名密钥和 签名证书

- print-defaults: 打印默认配置，这个默认配置可以用作模板

- - config：生成ca配置模板文件

- - csr：生成证书请求模板文件

- serve: 启动一个HTTP API服务

- gencert: 生成新的key(密钥)和签名证书

- - initca：初始化一个新ca
- - ca：指明ca的证书
- - ca-key：指明ca的私钥文件
- - config：指明请求证书的json文件
- - profile：与-config中的profile对应，是指根据config中的profile段来生成证书的相关信息
- ocspdump
- ocspsign
- info: 获取有关远程签名者的信息
- sign: 签名一个客户端证书，通过给定的CA和CA密钥，和主机名
- ocsprefresh
- ocspserve

1. 下载、解压并准备如下所示的命令行工具。

> 注意：你可能需要根据所用的硬件体系架构和 cfssl 版本调整示例命令。
```shell
curl -L https://github.com/cloudflare/cfssl/releases/download/v1.5.0/cfssl_1.5.0_linux_amd64 -o cfssl
chmod +x cfssl
curl -L https://github.com/cloudflare/cfssl/releases/download/v1.5.0/cfssljson_1.5.0_linux_amd64 -o cfssljson
chmod +x cfssljson
curl -L https://github.com/cloudflare/cfssl/releases/download/v1.5.0/cfssl-certinfo_1.5.0_linux_amd64 -o cfssl-certinfo
chmod +x cfssl-certinfo
```
- 工具如下：
```shell
root@lianhaifeng-virtual-machine:/opt/gen_openssl# ll
总用量 35944
drwxr-xr-x  2 root root     4096 11月  7 14:10 ./
drwxrwxrwx 14 root root     4096 11月  7 14:09 ../
-rwxr-xr-x  1 root root 15108368 11月  7 14:09 cfssl*
-rwxr-xr-x  1 root root 12021008 11月  7 14:10 cfssl-certinfo*
-rwxr-xr-x  1 root root  9663504 11月  7 14:10 cfssljson*

```
2. 创建一个目录，用它**保存所生成的构件和初始化cfssl**：
```shell
mkdir cert
cd cert
../cfssl print-defaults config > config.json
../cfssl print-defaults csr > csr.json
```

3. 配置证书生成策略，让CA软件知道颁发有什么功能的证书。创建一个 JSON 配置文件来生成**CA**文件，例如：ca-config.json：
```shell
{
  "signing": {
    "default": {
      "expiry": "8760h"
    },
    "profiles": {
      "kubernetes": {
        "usages": [
          "signing",
          "key encipherment",
          "server auth",
          "client auth"
        ],
        "expiry": "8760h"
      }
    }
  }
}
```
​    这个策略，有一个default默认的配置，和一个`profiles`，profiles可以设置多个`profile`，这里的`profile`是**kubernetes**。

- default默认策略，指定了证书的默认有效期是一年(8760h)
- kubernetes：表示该配置(profile)的用途是为kubernetes生成证书及相关的校验工作
  - signing：表示该证书可用于签名其它证书；生成的 ca.pem 证书中 CA=TRUE
  - server auth：表示可以该CA 对 server 提供的证书进行验证
  - client auth：表示可以用该 CA 对 client 提供的证书进行验证
- expiry：也表示过期时间，如果不写以default中的为准

cfssl常用命令：

- `cfssl gencert -initca ca-csr.json | cfssljson -bare ca ## 初始化ca`
- `cfssl gencert -initca -ca-key key.pem ca-csr.json | cfssljson -bare ca ## 使用现有私钥, 重新生成`
- `cfssl certinfo -cert ca.pem`
- `cfssl certinfo -csr ca.csr`

4. 创建一个 JSON 配置文件，用于**CA证书签名请求（CSR）**，例如：ca-csr.json。 ``确认用你需要的值替换掉尖括号中的值``。

```shell
{
  "CN": "kubernetes",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names":[{
    "C": "<country>",  
    "ST": "<state>",   
    "L": "<city>",
    "O": "<organization>",
    "OU": "<organization unit>"
  }]
}
```
> 参数介绍:
> - CN: Common Name，浏览器使用该字段验证网站是否合法，一般写的是域名。非常重要。浏览器使用该字段验证网站是否合法
> - key：生成证书的算法
> - hosts：包含的授权范围，不在此范围的的节点或者服务使用此证书就会报证书不匹配错误。表示哪些主机名(域名)或者IP可以使用此csr申请的证书，为空或者""表示所有的都可以使用(本例中没有hosts字段)
> - names：一些其它的属性
> - C: Country， 国家
> - ST: State，州或者是省份
> - L: Locality Name，地区，城市
> - O: Organization Name，组织名称，公司名称(在k8s中常用于指定Group，进行RBAC绑定)
> - OU: Organization Unit Name，组织单位名称，公司部门
5. 生成 CA 秘钥文件（ca-key.pem）和证书文件（ca.pem）：
```shell
../cfssl gencert -initca ca-csr.json | ../cfssljson -bare ca
```
- 生成ca文件过程：
```shell
root@lianhaifeng-virtual-machine:/opt/gen_openssl/cert# ../cfssl gencert -initca ca-csr.json | ../cfssljson -bare ca                                                         
2022/11/07 14:13:44 [INFO] generating a new CA key and certificate from CSR
2022/11/07 14:13:44 [INFO] generate received request
2022/11/07 14:13:44 [INFO] received CSR
2022/11/07 14:13:44 [INFO] generating key: rsa-2048
2022/11/07 14:13:44 [INFO] encoded CSR
2022/11/07 14:13:44 [INFO] signed certificate with serial number 53344263891369602218210366475207512428884411842                                                                                     

```
> 该命令会生成运行CA所必需的文件ca-key.pem（私钥）和ca.pem（证书），还会生成ca.csr（证书签名请求），用于交叉签名或重新签名。
- 生成的ca证书：
```shell
root@lianhaifeng-virtual-machine:/opt/gen_openssl/cert# cat ca.pem
-----BEGIN CERTIFICATE-----
MIID2DCCAsCgAwIBAgIUCVgKHiH4WWKpUsiTkkum8GNuRcIwDQYJKoZIhvcNAQEL
BQAwgYMxEjAQBgNVBAYMCTxjb3VudHJ5PjEQMA4GA1UECAwHPHN0YXRlPjEPMA0G
A1UEBwwGPGNpdHk+MRcwFQYDVQQKDA48b3JnYW5pemF0aW9uPjEcMBoGA1UECwwT
PG9yZ2FuaXphdGlvbiB1bml0PjETMBEGA1UEAxMKa3ViZXJuZXRlczAeFw0yMjEx
MDcwNjA5MDBaFw0yNzExMDYwNjA5MDBaMIGDMRIwEAYDVQQGDAk8Y291bnRyeT4x
EDAOBgNVBAgMBzxzdGF0ZT4xDzANBgNVBAcMBjxjaXR5PjEXMBUGA1UECgwOPG9y
Z2FuaXphdGlvbj4xHDAaBgNVBAsMEzxvcmdhbml6YXRpb24gdW5pdD4xEzARBgNV
BAMTCmt1YmVybmV0ZXMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDH
XQlPJK20HPZtRnzs1Rzs/J6v2D0eglGJPsig+xbDjCfEte69XgL7AwOVmAC0RWIt
Bji4RC2DfzYyUBQ0ew4x6hr7XU2Ke98dkaVpw+mUJoDlgoDFZjpkFOM94yh+4b8v
fk8iOyEowPdtUlQgltHFc+TGNVZ2STliy1mLybrEC/T+hZagT1USpvX8TFcCQDfZ
AHeIiYJA0uFuStX59sR9FVxPZtFTQIlBnnibfwWLPH2rH+6KkAbfSTH4OYzSAxQe
qR5xMOLp1NpNmm6XQsxXc5awv3LrK7rh2zvatNk4ADMXceB4EciIp1YKYSOdEqix
P7ycasGtJtPc+Gns8PjNAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB
Af8EBTADAQH/MB0GA1UdDgQWBBRKUh899dWFixW07lGGNTjkODqA3zANBgkqhkiG
9w0BAQsFAAOCAQEAIqAD907ZsO+rsYblrwgj/p4zauW68IyF8RA1Z7xRavHxpnpq
J/HZbnNQT07tClpRcBZTPydejbnqA59Qj9y9fJi9yuyZep3+fATLSzNOo33mKVCi
EB/tbMZA1f17RwTORwp/SR/O3ZwmBos1/gTZaIxjXuZJVVJtO1bbv9rRr7SLsLcn
cG0INt3/Q+NzVS46+FV5V5Tf0m6v0iWLnnPqbuImp4Ag1kjZDCgpEopfO7RQNCOB
YWoxkyVSgkWjgy59Gdm3et6guVZ0TjrHKnIS6kV8Yys50kZz8qa6St9oQL8H05ar
S6u4JKIA/3NMoVU8F7mYG1uSkYJilnLK+Nmf/g==
-----END CERTIFICATE-----
```
- 生成的ca证书私钥：
```shell
root@lianhaifeng-virtual-machine:/opt/gen_openssl/cert# cat ca-key.pem
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAx10JTySttBz2bUZ87NUc7Pyer9g9HoJRiT7IoPsWw4wnxLXu
vV4C+wMDlZgAtEViLQY4uEQtg382MlAUNHsOMeoa+11NinvfHZGlacPplCaA5YKA
xWY6ZBTjPeMofuG/L35PIjshKMD3bVJUIJbRxXPkxjVWdkk5YstZi8m6xAv0/oWW
oE9VEqb1/ExXAkA32QB3iImCQNLhbkrV+fbEfRVcT2bRU0CJQZ54m38Fizx9qx/u
ipAG30kx+DmM0gMUHqkecTDi6dTaTZpul0LMV3OWsL9y6yu64ds72rTZOAAzF3Hg
eBHIiKdWCmEjnRKosT+8nGrBrSbT3Php7PD4zQIDAQABAoIBAE6WRBcolDiNui41
PQV2tKJOqpcSnHUsVcvOLfQXRk/rLboDJYsMRgyAkackdhKZzyuEalNovLA7Mzf+
DRjq8RuH9v7jNq/CSJ81TIk2qxq1WtYd7Xji5V2SRkmdA9eQUXb9SWBrApU4C9DS
RUtbaHF3T9U6LU0PbEmfczsBWFfy1IVUoCMz/JLgLDQAycq4qYsNxntly+7v4HJr
aCeyIKTCTBohJxFKIVSKQLyye2bICuWs+/Nul4rUN/9lfWc0uE/72i7PBeDOqsRM
TDwGnnXgpUsI2F5y59FRqiMZgRUQM8bEM4LPHQUEXGh1W4vw2YC23xCiF7LWqFrI
BGaLHMECgYEA3H5KNWfc8/Q+vxil9KW6sT9M1KQ2EN0ruovNbdRcWnPHzVGsuxg1
dOgvwFKiWtmkg0hciuNhYMIo2VmefrXk8mpNeT9Os4Ote6wfRjbeqbiIcHQwnqHK
OoRmSxIy85kyMCN+6qZLRgDvrahMjOROYJDiGmRVlTv0r3MSjrSCUxUCgYEA53et
vWE7lR1oo8Wxn6BWUI6mSHJni722LkEgVPOJuS8bpWv8jCDpATevZVpozgm7yz1T
nVyE7jNdjvJikEDXPpLXurs8ad3GYWVXFQe2k6mcGaeeMdvADfLbOyLOPMIW4Imu
PtyXH+4bkfrOh3LIT3vJT8cQbwEi+BCNBD1pXNkCgYEAloHCJ+hIw2FCf3DUv0Vt
RVX/HNsmaKaAFeseA81EaR3FEdqhfGiO/MkM50vAtSEBEfgP62JAcyq1dX+eF8IT
kIGNdqkHELRedB/OjUAhB1sGDzTQh0fK4dzEcpPuoac9wexI0uVGVneHI1PRRQ8G
jRX4sKkyXha59BUpYq3Gk+0CgYAw2kmJFuSEbFiReEAs+KI/Dlx6HetMyxWQXZ59
T4lZ1F95YnlC+g8zepVCRvqnwdYo5yCmrchAnga5DN9Qot7LDiMJ/kqZ7XzZQZJH
lgEq2TlhEMeKrl6ykvdCW+47VJuPeH+WNOiQjKi0/sJoRAmS/QVYGSOWyh6fTJ72
rh92wQKBgQCtS5khzqyDtgNxLLna8KsVw+078+Q4AWz0PZMr4oJy07KY+gEMXBQQ
W95MlYOvOzD8AOwctdgSYrtiMOew3/z/+h9v5NTKw7fB2mDhxGzu+RfTEdCfV4Nf
IEcXjADnl6vkrcmdFj2OZQTPUN6yIBuSftdTDPbVItNGU2YQodqgGg==
-----END RSA PRIVATE KEY-----

```
- 查看证书的详细信息
```shell
root@lianhaifeng-virtual-machine:/opt/gen_openssl/cert# ../cfssl certinfo -cert ca.pem
{
  "subject": {
    "common_name": "kubernetes",
    "country": "CN",
    "organization": "k8s",
    "organizational_unit": "System",
    "locality": "ShangHai",
    "province": "ShangHai",
    "names": [
      "CN",
      "ShangHai",
      "ShangHai",
      "k8s",
      "System",
      "kubernetes"
    ]
  },
  "issuer": {
    "common_name": "kubernetes",
    "country": "CN",
    "organization": "k8s",
    "organizational_unit": "System",
    "locality": "ShangHai",
    "province": "ShangHai",
    "names": [
      "CN",
      "ShangHai",
      "ShangHai",
      "k8s",
      "System",
      "kubernetes"
    ]
  },
  "serial_number": "531158990857971446230196021986281027598700718933",
  "not_before": "2022-11-07T06:21:00Z",
  "not_after": "2027-11-06T06:21:00Z",
  "sigalg": "SHA256WithRSA",
  "authority_key_id": "",
  "subject_key_id": "A4:CC:78:CA:A7:5B:4F:8D:FC:C1:39:1E:A3:AC:20:D3:F6:28:16:97",
  "pem": "-----BEGIN CERTIFICATE-----\nMIIDnjCCAoagAwIBAgIUXQn+LtrjU5EUfmnCIQzbi97rK1UwDQYJKoZIhvcNAQEL\nBQAwZzELMAkGA1UEBhMCQ04xETAPBgNVBAgTCFNoYW5nSGFpMREwDwYDVQQHEwhT\naGFuZ0hhaTEMMAoGA1UEChMDazhzMQ8wDQYDVQQLEwZTeXN0ZW0xEzARBgNVBAMT\nCmt1YmVybmV0ZXMwHhcNMjIxMTA3MDYyMTAwWhcNMjcxMTA2MDYyMTAwWjBnMQsw\nCQYDVQQGEwJDTjERMA8GA1UECBMIU2hhbmdIYWkxETAPBgNVBAcTCFNoYW5nSGFp\nMQwwCgYDVQQKEwNrOHMxDzANBgNVBAsTBlN5c3RlbTETMBEGA1UEAxMKa3ViZXJu\nZXRlczCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKBQGtTtx00ZaGxj\nWOFlCDmlrI0P3fKVxWP/R7cW4REX62U/vinB2KbK8k6U6h9VS4ufVa83iWaoPuPm\ntCTBwqNUNgxBUZCiyA2ohycWvo9PJvRhS7xLUQ/nmMtiDZ+WuWi1PSkYg4e2YR7B\nQEfE2EVVx0UN/QNN1WQEa9vv0pBGMiKKETMkjV4VSsnf4XgBzjtgl5vYKODCgEqP\nST4hI+iZnzb43ofsGE2hTtEk5c/hLl52XlssfPTyqXlM/kT20cbu6ei0SuBfRoz9\nQTWvKQ2wNL46zmqZoAByg7me+5377spFPEkMwxPGmjaexd92ewGebKT2L9Nw8MCO\nGcH6al0CAwEAAaNCMEAwDgYDVR0PAQH/BAQDAgEGMA8GA1UdEwEB/wQFMAMBAf8w\nHQYDVR0OBBYEFKTMeMqnW0+N/ME5HqOsINP2KBaXMA0GCSqGSIb3DQEBCwUAA4IB\nAQAW5A/BIT9WsAA8XHTk0y1ML9GanH5AkFj7M2KsY+/EUSVjtbVUOvkAO7OSBRoM\np5nMN5Ji1fGVwHMwnoRtZEOF+rn1FdPQkntbMqD5MGf35VQlJCFKMUYxh/rcU865\nf/DF7NccxLELTi4T7zGfiAEVepxR2i6wxfJb6DOnxwu6AdsKeE6PBCMKgtYVqqSD\nZEG/ctf0CkN/D/uOyuG/7XdXaCHgvSuP2j9bI9vmPVB1pgeZIsJTtNLl+0dkk6az\nMVftKXsDsTyGKUamf6gismo32plwIgd3u31iWk/dJrkMYPtxGLVjnd8/J5AeIOp9\nN/W5TdG6EDbN31VoTTdFXiQo\n-----END CERTIFICATE-----\n"
}

```
- 查看证书请求文件信息
```shell
root@lianhaifeng-virtual-machine:/opt/gen_openssl/cert# ../cfssl certinfo -csr ca.csr
{
  "Raw": "MIICrDCCAZQCAQAwZzELMAkGA1UEBhMCQ04xETAPBgNVBAgTCFNoYW5nSGFpMREwDwYDVQQHEwhTaGFuZ0hhaTEMMAoGA1UEChMDazhzMQ8wDQYDVQQLEwZTeXN0ZW0xEzARBgNVBAMTCmt1YmVybmV0ZXMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCgUBrU7cdNGWhsY1jhZQg5payND93ylcVj/0e3FuERF+tlP74pwdimyvJOlOofVUuLn1WvN4lmqD7j5rQkwcKjVDYMQVGQosgNqIcnFr6PTyb0YUu8S1EP55jLYg2flrlotT0pGIOHtmEewUBHxNhFVcdFDf0DTdVkBGvb79KQRjIiihEzJI1eFUrJ3+F4Ac47YJeb2CjgwoBKj0k+ISPomZ82+N6H7BhNoU7RJOXP4S5edl5bLHz08ql5TP5E9tHG7unotErgX0aM/UE1rykNsDS+Os5qmaAAcoO5nvud++7KRTxJDMMTxpo2nsXfdnsBnmyk9i/TcPDAjhnB+mpdAgMBAAGgADANBgkqhkiG9w0BAQsFAAOCAQEAe24EbKDObyr2xiXK1sYhqgslgPC2II6jxq1BJuOpP3vlzhw6Hkimm8k0NYm4Z8HZQWPn0flExE2P08db2cjhMlkpK7XdZuT9saI1YQU8RPWv3LHJMgiYNdfOlUlbY0tN+zCmPkf6Cj2tw/RiRENT6xnIYsig8255GJRIJ2fZqsjKt3ekmEJAOQFrD3hAeTfeMdfceugChm7XZzyy6XUF8au47rQ910UJLzFBE+Xp1kuGV9BPF2V44c9i1qyyhv0/uFieQu2UP/6IvVN8dhERlKVHvTze3JSzfdxFws/K8JVIOaP+D2FTo+YDC+MAwauqiAsykokbur5LdnCvB7EGKA==",
  "RawTBSCertificateRequest": "MIIBlAIBADBnMQswCQYDVQQGEwJDTjERMA8GA1UECBMIU2hhbmdIYWkxETAPBgNVBAcTCFNoYW5nSGFpMQwwCgYDVQQKEwNrOHMxDzANBgNVBAsTBlN5c3RlbTETMBEGA1UEAxMKa3ViZXJuZXRlczCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKBQGtTtx00ZaGxjWOFlCDmlrI0P3fKVxWP/R7cW4REX62U/vinB2KbK8k6U6h9VS4ufVa83iWaoPuPmtCTBwqNUNgxBUZCiyA2ohycWvo9PJvRhS7xLUQ/nmMtiDZ+WuWi1PSkYg4e2YR7BQEfE2EVVx0UN/QNN1WQEa9vv0pBGMiKKETMkjV4VSsnf4XgBzjtgl5vYKODCgEqPST4hI+iZnzb43ofsGE2hTtEk5c/hLl52XlssfPTyqXlM/kT20cbu6ei0SuBfRoz9QTWvKQ2wNL46zmqZoAByg7me+5377spFPEkMwxPGmjaexd92ewGebKT2L9Nw8MCOGcH6al0CAwEAAaAA",
  "RawSubjectPublicKeyInfo": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoFAa1O3HTRlobGNY4WUIOaWsjQ/d8pXFY/9HtxbhERfrZT++KcHYpsryTpTqH1VLi59VrzeJZqg+4+a0JMHCo1Q2DEFRkKLIDaiHJxa+j08m9GFLvEtRD+eYy2INn5a5aLU9KRiDh7ZhHsFAR8TYRVXHRQ39A03VZARr2+/SkEYyIooRMySNXhVKyd/heAHOO2CXm9go4MKASo9JPiEj6JmfNvjeh+wYTaFO0STlz+EuXnZeWyx89PKpeUz+RPbRxu7p6LRK4F9GjP1BNa8pDbA0vjrOapmgAHKDuZ77nfvuykU8SQzDE8aaNp7F33Z7AZ5spPYv03DwwI4ZwfpqXQIDAQAB",
  "RawSubject": "MGcxCzAJBgNVBAYTAkNOMREwDwYDVQQIEwhTaGFuZ0hhaTERMA8GA1UEBxMIU2hhbmdIYWkxDDAKBgNVBAoTA2s4czEPMA0GA1UECxMGU3lzdGVtMRMwEQYDVQQDEwprdWJlcm5ldGVz",
  "Version": 0,
  "Signature": "e24EbKDObyr2xiXK1sYhqgslgPC2II6jxq1BJuOpP3vlzhw6Hkimm8k0NYm4Z8HZQWPn0flExE2P08db2cjhMlkpK7XdZuT9saI1YQU8RPWv3LHJMgiYNdfOlUlbY0tN+zCmPkf6Cj2tw/RiRENT6xnIYsig8255GJRIJ2fZqsjKt3ekmEJAOQFrD3hAeTfeMdfceugChm7XZzyy6XUF8au47rQ910UJLzFBE+Xp1kuGV9BPF2V44c9i1qyyhv0/uFieQu2UP/6IvVN8dhERlKVHvTze3JSzfdxFws/K8JVIOaP+D2FTo+YDC+MAwauqiAsykokbur5LdnCvB7EGKA==",
  "SignatureAlgorithm": 4,
  "PublicKeyAlgorithm": 1,
  "PublicKey": {
    "N": 20237629949365974820706845049885436811040309637650365419012787611041848963614350652974834905979249169389457764808776938439173320005646031580788863280197890952558621242361654468581384593182669636806103561150894566634021154143115585463765614965029247883960606928381820595437422302736629443607105229523181377272166698035319118526941875184336365275499709996426396441572704307701597042533577043619146335637204659100636795864342483828271998854794689356067852959966910482889097564064705828589103906799603274731526939558922859870217614941427475510011572171422180770138425914173438527004794575550492813085752887061351600122461,
    "E": 65537
  },
  "Subject": {
    "Country": [
      "CN"
    ],
    "Organization": [
      "k8s"
    ],
    "OrganizationalUnit": [
      "System"
    ],
    "Locality": [
      "ShangHai"
    ],
    "Province": [
      "ShangHai"
    ],
    "StreetAddress": null,
    "PostalCode": null,
    "SerialNumber": "",
    "CommonName": "kubernetes",
    "Names": [
      {
        "Type": [
          2,
          5,
          4,
          6
        ],
        "Value": "CN"
      },
      {
        "Type": [
          2,
          5,
          4,
          8
        ],
        "Value": "ShangHai"
      },
      {
        "Type": [
          2,
          5,
          4,
          7
        ],
        "Value": "ShangHai"
      },
      {
        "Type": [
          2,
          5,
          4,
          10
        ],
        "Value": "k8s"
      },
      {
        "Type": [
          2,
          5,
          4,
          11
        ],
        "Value": "System"
      },
      {
        "Type": [
          2,
          5,
          4,
          3
        ],
        "Value": "kubernetes"
      }
    ],
    "ExtraNames": null
  },
  "Attributes": null,
  "Extensions": null,
  "ExtraExtensions": null,
  "DNSNames": null,
  "EmailAddresses": null,
  "IPAddresses": null,
  "URIs": null
}

```
6. 创建一个 JSON 配置文件，用来为 API 服务器生成秘钥和证书，例如：server-csr.json。 确认用你需要的值替换掉尖括号中的值。MASTER_CLUSTER_IP 是为 API 服务器 指定的服务集群 IP，就像前面小节描述的那样。 以下示例假定你的默认 DNS 域名为cluster.local。
```shell
{
  "CN": "kubernetes",
  "hosts": [
    "127.0.0.1",
    "<MASTER_IP>",
    "<MASTER_CLUSTER_IP>",
    "kubernetes",
    "kubernetes.default",
    "kubernetes.default.svc",
    "kubernetes.default.svc.cluster",
    "kubernetes.default.svc.cluster.local"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [{
    "C": "<country>",
    "ST": "<state>",
    "L": "<city>",
    "O": "<organization>",
    "OU": "<organization unit>"
  }]
}
```

7. 为 API 服务器生成秘钥和证书，默认会分别存储为server-key.pem 和 server.pem 两个文件。
```shell
../cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
     --config=ca-config.json -profile=kubernetes \
     server-csr.json | ../cfssljson -bare server
```
8. 获取证书序列号
> 需要注意的是，openssl 等工具习惯用 16 进制表示序列号，而 cfssl 用十进制来表示序列号。
```shell
../cfssl certinfo -cert server.pem | jq .serial_number | tr -d '"'
# 401947805951006266249214993815881710294230149586
```
#### 分发自签名的 CA 证书
客户端节点可能不认可自签名 CA 证书的有效性。 对于非生产环境，或者运行在公司防火墙后的环境，你可以分发自签名的 CA 证书到所有客户节点，并刷新本地列表以使证书生效。

在每一个客户节点，执行以下操作：
```shell
sudo cp ca.crt /usr/local/share/ca-certificates/kubernetes.crt
sudo update-ca-certificates
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d....
done.
```
#### 证书 API
你可以通过 certificates.k8s.io API 提供 x509 证书，用来做身份验证， 如管理集群中的 TLS 认证文档所述。




### 参考
> https://blog.laisky.com/p/cfssl/