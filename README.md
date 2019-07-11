# Polysecrets
![alt text](https://img.icons8.com/dotty/80/000000/mesh.png "Polysecrets Logo")
A completely randomized order of secrets; built with security in mind. Secrets can be automatically generated
on a time interval or manually generated. Polysecrets keeps the guessing away from the human in exchange for
a truly secret, randomized signing order. Instead of a hardcoded secret that can be stolen during a security
breach, Polysecrets, randomizes the provided string in a way that a secret produced at 8:00pm can be completely
different from a secret produced at 8:01pm, on the same server.

# Versions
Node: https://github.com/ableinc/polysecrets-js

# Requirements
* Python 3.5+
* Windows, OSX or Linux

# Install
Locally
```bash
git clone https://github.com/ableinc/polysecrets.git
cd polysecrets

python3.6 -m pip install --upgrade .
            or 
pip3.6 install --upgrade .
```
PyPi (Pip)
```bash
python3.6 -m pip install --upgrade polysecrets
            or
pip3.6 install --upgrade polysecrets
```
# How To Use
Polysecrets can be used manually or automated. Automated use can be provided a time (in seconds) for
how often a new secret should be generated, the default time is set to 30 seconds. You do not have
to provide a secret to Polysecrets class, but you can if you'd like
certain characters in your secret. Reminder, the secret is a collection of
randomly ordered characters so the secret you provide will not be used entirely.<br />

** Look through examples folder ** <br />

Automated (this will add the secret to your environment)
```python
from os import environ
from polysecrets import PolySecrets


config = dict(
        secret='rAnd0m_s3cr3t',  # default
        length=10,  # default
        interval=30,  # default (only if you're using automated)
        uuid=True,  # default
        mixcase=False,  # default
        persist={}  # default
    )


automated = PolySecrets(config).automated()  # default time is set to 30 seconds
print(environ['secret'])  # confirm secret is available
automated.terminate()  # stop automation

```

Manual: 
```python
from polysecrets import PolySecrets

config = dict(
        secret='rAnd0m_s3cr3t',  # default
        length=10,  # default
        interval=30,  # default (only if you're using automated)
        uuid=True,  # default
        mixcase=False,  # default
        persist={}  # default
    )


secret = PolySecrets(config).manual()
print(secret)  # confirm secret is available
```

Refer to examples folder for all use cases.
Also refer to 'Notes' section at the bottom of
this README. <br />
**If you want your environment variables cleared after Polysecrets
terminates, do the following:** <br />
```python

from polysecrets import PolySecrets
from os import environ

config = {}  # use all defaults
automated = PolySecrets(config=config, clear_on_exit=True).automated()
print(environ['secret'])
automated.terminate()  # forcibly remove envs
```


# Options
You can do the following with Polysecrets:
* Manually or Automatically generate new secrets
* Change time interval for new secret generation (for Automated feature)
* Change the length of the final Polysecrets secret (refer to Notes at end of README)
* Choose whether to generate secrets with just UUIDs, Alphanumeric characters or both
* Persist generated secrets to ensure the same secret isn't used twice

The CLI (below) has full details of each option (except automated option)

# CLI
You can use Polysecrets as a command line tool. CLI does not provided automated feature. <br />
```bash
polysecrets -s -l 20 
```

```bash 
Usage: polysecrets [OPTIONS]

Options:
  -s, --secret TEXT       The secret string  [required]
  -l, --length INTEGER    Length of the secret. Secret has a minimum length of
                          10
  -u, --uuid INTEGER      Whether to use UUIDs or Alphanumeric characters for
                          secret generation
  -m, --mixcase BOOLEAN   Decide whether or not to mix the case of
                          alphacharacters in secret string
  -p, --persist           Never get the same secret twice with persistence from MongoDB
  --version               Show the version and exit.
  --help                  Show this message and exit.

```

# Benefits
* JSON Web Tokens
* Certificate Signing
* Hashing
* Various scenarios of Cryptography

# What's Next <h5>(refer to Changelog)</h5>
1. Add persistence. This will monitor the generated secrets and make sure the newly generated secret
has not be used previously. Add a time in which to clear the data and restart this check.
2. NodeJS version of Polysecrets
________
 -- Completed June 4th, 2019 -- <br />
1. Randomized upper and lower case alpha characters in secret string - Done. <br />
2. Custom secret string length - Done. <br />
3. Choice of just UUIDs, alphanumeric characters or both in secret generation - Done. <br />

# Changelog
**v0.1.3** - July 11th, 2019
* Improved code and squashed bugs

**v0.1.2** - July 1st, 2019
* Persistence added. You can now avoid duplicate secrets being generated.
* Node version is now available. Install:
```bash
npm install polysecrets
```
* Improved code and squashed bugs

**v0.1.1** - June 4th, 2019
* Custom secret string length, with a minimum of 10 characters
* You may mix the secret, in combination with the provided secret string, with UUIDs, alphanumeric characters or both.
* You can now select between upper and lower case mixing during secret generation

**v0.1.0** - June 3rd, 2019
* Manually and autogenerated secrets, with fixed secret length
* Polysecrets CLI added

# Note

- If you change the length of the secret via the 'length' parameter, you will notice that the 
secret string you provided will not contain all the characters provided. If you want the final
secret to contain all the exact same characters, then provide the exact string length to 
Polysecrets 'length' field.

- The secret provided in the config is just used as reference characters and are not
guaranteed to be a part of the final secret. If you would like to use the secret you
provide I would recommend going the traditional route; add secret to your project 
.env file and use Able's <a href="https://github.com/ableinc/pydotenvs">Py.Envs</a>
python library.

- You cannot run manual and automated in the same file. You will throw an error.
