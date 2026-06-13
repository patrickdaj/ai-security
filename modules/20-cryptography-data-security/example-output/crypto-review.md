<!-- Example output — illustrative deliverable of module 20. -->

# Crypto & Data Security Review — `vuln-app`

5 crypto misuses found; key-management design reviewed.

## Crypto misuse (with fixes)
### [high] AES in ECB mode — `app/crypto.py:14`
ECB leaks plaintext structure (identical blocks → identical ciphertext).
```diff
- cipher = AES.new(key, AES.MODE_ECB)
- ct = cipher.encrypt(pad(data, 16))
+ nonce = os.urandom(12)
+ cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
+ ct, tag = cipher.encrypt_and_digest(data)   # store nonce+tag with ct
```

### [critical] MD5 for password hashing — `app/auth.py:31`
```diff
- hashed = hashlib.md5(password.encode()).hexdigest()
+ from argon2 import PasswordHasher
+ hashed = PasswordHasher().hash(password)
```

Others: static IV (`app/crypto.py:9`), `random.random()` for a token
(`app/ids.py:9`), `verify=False` on an HTTPS call (`app/client.py:22`).

## Key management (designed + reviewed)
Envelope encryption: data keys wrapped by a KMS CMK; 90-day rotation; key policy
scoped so only the `app-runtime` role can `Decrypt`. Blast-radius note: that role
can decrypt **all** ciphertext — split per data domain.

**Outcome:** crypto-specific findings the generic SAST pass missed, each with the
correct construction, plus a reviewed key-management design.
