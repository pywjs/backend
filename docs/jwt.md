# JWT - JSON Web Token

JSON Web Token, or JWT ("jot") for short, is a standard for _safely_ passing _claims_ in space constrained environments.

It comprises three parts:
- Header
- Payload
- Signature

## Header
The header typically consists of two parts: the type of the token, which is JWT, and the signing algorithm being used, such as HMAC SHA256 or RSA.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
## Payload
The payload contains the claims. Claims are statements about an entity (typically, the user) and additional data. There are three types of claims: registered, public, and private claims.
- **Registered claims**: These are a set of predefined claims that are not mandatory but recommended, to provide a set of useful, interoperable claims. Some of the registered claims are:
  - `iss` (issuer): Issuer of the JWT
  - `sub` (subject): Subject of the JWT (the user)
  - `aud` (audience): Recipient for which the JWT is intended
  - `exp` (expiration time): Expiration time on or after which the JWT must not be accepted for processing
  - `nbf` (not before): Time before which the JWT must not be accepted for processing
  - `iat` (issued at): Time at which the JWT was issued; can be used to determine age of the JWT
  - `jti` (JWT ID): Unique identifier for the JWT; can be used to prevent the JWT from being replayed (allows a nonce)
- **Public claims**: These are claims that can be defined at will by those using JWTs. To avoid collisions, these claims should be defined in the IANA JSON Web Token Registry or as a URI that contains a collision-resistant namespace.
- **Private claims**: These are the custom claims created to share information between parties that agree on using them. These claims are neither registered nor public claims, and they are not defined in the IANA JSON Web Token Registry. Private claims can be used to share information between parties that agree on using them.

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```

## Signature
To create the signature part, you have to take the encoded header, the encoded payload, a secret, and the algorithm specified in the header and sign that.
For example if you want to use the HMAC SHA256 algorithm, the signature will be created in the following way:

```plaintext
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```
The signature is used to verify that the sender of the JWT is who it says it is and to ensure that the message wasn't changed along the way.
