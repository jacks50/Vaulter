import pyotp

"""
class TFA():
    def __new__(cls) -> Self:
        if not hasattr(cls, 'instance'):
            instance = super(TFA, cls).__new__(cls)

        return cls.instance
"""

def generate_secret_key() -> str:
    return pyotp.random_base32()


def generate_otpauth_url(secret_key: str, username: str) -> str:
    return pyotp.totp.TOTP(secret_key).provisioning_uri(name=username, issuer_name='Vaulter')


def tfa_valid(secret_key: str, code: str) -> bool:
    return pyotp.TOTP(secret_key).verify(code)


"""
Create a new account :
----------------------

1. Select an username and password on VaultuReact
-> React side
-> Create a new file with "username".vault and encrypt it using password
-> In memory while process is not done (?)

2. Send file to Vaulter
*-> Checks that username is not already taken
-> Vaulter generates a secret key
-> Creates a folder with "username_vault_tmp" name
-> Creates file with [secret_key].key
-> Creates file with username.vault (received)
-> Creates an otpauth URL to display a QR code

3. Confirm account creation
-> React receives URL otpauth
-> Displays the QR code and asks for OTP code
-> User adds it to authenticator
-> User enters current OTP code
-> Sends back to Vaulter

4. Vaulter receives OTP code
-> Checks username and checks if "username_vault_tmp" exists
-> Checks if .key is present
-> Checks code received
-> If OK - renames folder to "username_vault" and confirms
-> If not OK - returns error and ask for code

5. Cleanup files
-> Every X days
-> Checks every "*_vault_tmp" folder and deletes it

Login to account :
------------------
-> User has to enter username.vault, OTP code and password
-> Sends username and OTP code to Vaulter
-> Vaulter checks if folder with key exists and is not tmp
-> If not OK, returns an error
-> If OK, sends file back to React
-> React then uses password to decrypt file

Save password file :
-> A pop-up shows to ask if user wants to download file or send back to Vaulter
-> If download - downloads the file
-> If sending back - asks for OTP code
-> Vaulter receives username.vault file and OTP code
-> Check if folder exists and .key exists
-> Checks code
"""