
# Separator Oracle

A separator oracle can be used to decrypt a ciphertext which was encrypted with AES in CTR mode. The separator oracle attack is an adaptive chosen ciphertext attack. An attacker sends modified ciphertexts to the oracle. A `separator` is a special character like `;` or `|`. In our case `;` is used. The separator oracle throws a `SeparatorException`, if not the right amount of separators within the ciphertext/plaintext is used.

In this example, sessions are used (encoded in Base64). A session contains the username, password and validity which is stored in a cookie, separated by `;` (`username;password;valid`). You don't have to highjack a session, you get the session id and secret key id by executing a script (see below). If the username, password or valid until date is not valid, then an `InvalidSession` error is thrown. A http request looks like this:

```
GET http://localhost:8000/

Cookie: session_id=gDamXWzpLTMopToibp/djwvGNfs=;secret_key_id=8qTQL6X4CZrvzxF1F4LiGJrYcxDQVDR6PZjRYN1rMdQ=
```

The response of the separator oracle to a highjacked session should look like this:

```
{
    "result": {
        "message": "Everything is fine."
    }
}
```

That means, that the decryption was successful and you have a valid session id. The secret key id should stay the same (the whole time, otherwise the decryption of the session id is not possible)! If you change one byte within the session id, then an error response is returned:

```
{
    "result": {
        "error": "InvalidSession",
        "message": "The session id or secret key identifier is not correct."
    }
}
```

If you change the amount of the separators, then a `SeparatorException` is thrown (it is called `ValueError` in our separator oracle):

```
{
    "result": {
        "error": "ValueError",
        "message": "Invalid number of separators."
    }
}
```

Now, you can write an exploitation script, wherein you decrypt the ciphertext by using the separator oracle. For this purpose, you have to determine how many separators are used and the positions of them in the ciphertext/plaintext. Now, you can begin with the decryption of the ciphertext. Enjoy it ;)

## Getting Started

These steps are required to install and run the project on your local machine. 

### Prerequisites

To run the project you need the following modules/tools:

*  Python3
*  Pip (package management system)
*  Pipenv (install/uninstall packages)
*  Virtualenv (isolated Python environments)

### Installing and Deployment

To install the separator oracle service, you have to follow these steps:

```
git clone https://github.com/mprechtl/separator-oracle.git
cd separator-oracle/separator_oracle
virtualenv separator_oracle/venv
source separator_oracle/venv/bin/activate
pipenv install
./manage.py migrate
./manage.py runserver
```

If you want to deactivate the virtual Python environment, you have to enter the following instruction: 

```
deactivate
```

## Active Session

You also should add an active session to the database. For this purpose, you also need an user. This is all done by the following script:

```
./manage.py runscript add_active_session --script-args _Username <username> _Password <password> _Valid <valid_until>
```

The script prints the session id and the secret key id which should be used for the separator oracle attack. The cookie header in the http request can look like this:

```
Cookie  session_id=gDamXWzpLTMopToibp/djwvGNfs=;secret_key_id=8qTQL6X4CZrvzxF1F4LiGJrYcxDQVDR6PZjRYN1rMdQ=
```
