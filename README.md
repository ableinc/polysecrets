# Polysecrets
![alt text](https://img.icons8.com/dotty/80/000000/mesh.png "Polysecrets Logo")
A completely randomized order of secrets; built with security in mind. Secrets can be automatically generated
on a time interval or manually generated. Polysecrets keeps the guessing away from the human in exchange for
a truly secret, randomized signing order. Instead of a hardcoded secret that can be stolen during a security
breach, Polysecrets, randomizes the provided string in a way that a secret produced at 8:00pm can be completely
different from a secret produced at 8:01pm, on the same server.

# Libraries - v0.1.4
NodeJS: https://www.npmjs.com/package/polysecrets
Python: https://pypi.org/project/polysecrets/

# Author
Let's connect on LinkedIn: https://www.linkedin.com/in/jaylen-douglas-292b82a6/

# Requirements
* Python 3.5+
* Windows, OSX or Linux

# Install
Locally
```bash
git clone https://github.com/ableinc/polysecrets.git
cd polysecrets

python -m pip install --upgrade .
            or 
pip install --upgrade .
```
PyPi (Pip)
```bash
python -m pip install --upgrade polysecrets
            or
pip install --upgrade polysecrets
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
        secret='rAnd0m_s3cr3t',  # or use default
        length=10,  # default
        interval=30,  # default (only if you're using automated)
        uuid='yes',  # default
        mixcase=False,  # default
        persist=False,  # default
        symbols=False
    )


automated = PolySecrets(config).automated()  # default time is set to 30 seconds
print(environ['secret'])  # confirm secret is available
automated.terminate()  # stop automation

```

Manual: 
```python
from polysecrets import PolySecrets

config = dict(
        secret='rAnd0m_s3cr3t',  # or use default
        length=10,  # default
        interval=30,  # default (only if you're using automated)
        uuid='yes',  # default
        mixcase=False,  # default
        persist=False,  # default
        symbols=False
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
# Persistence
You can you use the persistence feature to keeps record
of the secrets produced, and verifies that no secret has been duplicated. You will need to have a .env file with the MongoDB credentials inside. An example of the .env file is below:
```text
HOST=localhost
#PORT=27017
USER=root
PASS=r00tp@ssw0rD
#DB_NAME=polysecrets
#COLLECTION=secrets
#AUTH_SOURCE=admin

# Host URI Example
HOST=mongodb://user:password@example.com/?authSource=the_database&authMechanism=SCRAM-SHA-1
``` 
Notes:
* ***All variables with the '#' prefix are optional; defaults will be assigned.***
* ***Host variable can also be a full MongoDB URI. If so, it will ignore all other variables.***

# Options
You can do the following with Polysecrets:
* Manually or Automatically generate new secrets
* Change time interval for new secret generation (for Automated feature)
* Change the length of the final Polysecrets secret (refer to Notes at end of README)
* Choose whether to generate secrets with just UUIDs, Alphanumeric characters or both
* Persist generated secrets to ensure the same secret isn't used twice

The CLI (below) has full details of each option (except automated option)

# CLI
You can use Polysecrets as a command line tool. CLI does not provided automated feature. If secret is left out, it will default to a random string built into the Polysecrets. An example is below: <br />
```bash
polysecrets --length 20 go 
```
Help menu
```bash 
Usage: polysecrets [OPTIONS] GO

Options:
  -s, --secret TEXT       The secret string
  -l, --length INTEGER    Length of the secret. Secret has a minimum length of
                          10
  -i, --interval INTEGER  How frequently should a new secret be generated (in
                          seconds)
  -u, --uuid TEXT         Whether to use UUIDs or Alphanumeric characters for
                          secret generation - yes, no, both
  -m, --mixcase BOOLEAN   Decide whether or not to mix the case of
                          alphacharacters in secret string
  -p, --persist DICT      Never get the same secret twice with persistence
                          from MongoDB
  --symbols BOOLEAN       Whether or not to use special characters in secret.
                          This will only increase the probability of appending
                          a special character.
  --version               Show the version and exit.
  --help                  Show this message and exit.

```

# Benefits
* JSON Web Tokens
* Certificate Signing
* Hashing
* Various scenarios of Cryptography

# What's Next <h5>(refer to Changelog)</h5>
If you have found a bug or would like to create new features, make a PR!

# Changelog
**v0.1.4** - June 1st, 2021
* Improved CLI tool
* Fixed persistence bug
* Simplified defaults

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
