# Polysecrets

A completely randomized order of secrets; built with security in mind. Secrets can be automatically generated
on a time interval or manually generated. Polysecrets keeps the guessing away from the human in exchange for
a truly secret, randomized signing order. Instead of a hardcoded secret that can be stolen during a security
breach, Polysecrets, randomizes the provided string in a way that a secret produced at 8:00pm can be completely
different from a secret produced at 8:01pm, on the same server.

# Requirements
* Python 3.6+
* Windows, OSX or Linux

# Install
```bash
git clone https://github.com/ableinc/polysecrets.git
cd polysecrets

python3.6 -m pip install --upgrade .
            or 
pip3.6 install --upgrade .
```
# How To Use
Polysecrets can be used manually or automated. Automated use can be provided a time (in seconds) for
how often a new secret should be generated, the default time is set to 30 seconds. <br />

Automated: This will add the secret to your environment
```python
from os import environ
from polysecrets import PolySecrets

PolySecrets('rAnd0m_s3cr3t', 15).automated()  # default time is set to 30 seconds
print(environ['secret'])  # confirm secret is available
```

Manual: 
```python
from polysecrets import PolySecrets

secret = PolySecrets('rAnd0m_s3cr3t').manual()
print(secret)  # confirm secret is available
```

# Benefits
* JSON Web Tokens
* Certificate Signing
* Hashing
* Various scenarios of Cryptography

# What's Next
1. Randomized upper and lower case alpha characters in secret string
2. Custom secret string length
3. Choice of just UUIDs, alphanumeric characters or both in secret generation
