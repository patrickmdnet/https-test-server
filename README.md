`https-test-server.py` is a simple python HTTPS server that accepts incoming requests, outputs the request to stdout, and returns the request as the response. 

I found it useful for testing when messing around with different request headers and methods. 

# Setup
## 1.) Configure cert.cnf with desired certificate information. 
Example cert.cnf:

```cnf
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C = Country
ST = State
L = Locality
O = Company
OU = unit
CN = site.common.name.com

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = site.alt.name.biz
DNS.2 = site.alt.name.io
DNS.3 = site.alt.name.net
```
## 2.) Generate server certificate and key with openssl.
```bash
openssl req -new -nodes -newkey rsa:2048 -keyout server-key.pem -out server-csr.pem -config cert.cnf
openssl x509 -req -days 365 -in server-csr.pem -signkey server-key.pem -out server-cert.pem -extensions v3_req -extfile cert.cnf
```

## 3.) Run https-test-server.py (with example output)
```bash
└─$ python3 https-test-server.py 4443
Server started at https://localhost:4443
[01/Dec/2023 16:26:05] - 127.0.0.1 - https://127.0.0.1:4443/
GET / HTTP/1.1
Host: 127.0.0.1:4443
User-Agent: curl/7.68.0
Accept: */*

[01/Dec/2023 16:26:44] - 127.0.0.1 - https://virtual.host.test/
POST / HTTP/1.1
Host: virtual.host.test
User-Agent: curl/7.68.0
Accept: */*
```

