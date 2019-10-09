import hashlib
import os
import sys
#-----------Importing requests, if not exists then install based upon user response----------------#
try:
    import requests
except:
    print('This program requires \'requests\' package to run')
    while True:
        res=input('Do you want to install it? Press Y/y to install or N/n to exit: ')
        if res in ('Y','y'):
            try:
                os.system("pip install requests")
                print('''
-----------------------------------------------------------------------------
--------------------------------ALRIGHT!!! READY TO RUN----------------------
-----------------------------------------------------------------------------
                      ''')
                import requests
                break
            except:
                print("requests package couldn\'t install")
                print("Exiting....")
                os._exit(0)
        elif res in ('N','n'):
            print("Exiting....")
            os._exit(0)
        else:
            print('Please enter correct response!')
            continue

#---------------------------Importing of packages completed---------------------------------------------------------#


api_url = 'https://api.pwnedpasswords.com/range/'

#Convert the password into HEX
def convert_to_hex(password):
    '''
    Converts the password into HEXADECIMAL
    '''
    #Encoding the password
    pass_encode=password.encode('utf-8')

    #converting into hash code in bytes SHA1 hash function
    pass_sha1_bytes = hashlib.sha1(pass_encode)

    #Converting into HEXADECIMAL
    pass_sha1_hex = pass_sha1_bytes.hexdigest()

    return pass_sha1_hex

#Get the response from api
def get_response(url, hash_5_digit):
    '''
    Gets the response from api

    Parameters:
    url: api url
    hash_5_digit: First 5 digit of hashed
    '''
    #Fetching the response from the api server
    response = requests.get(url + hash_5_digit)
    return response

def get_pwned_counts(hashes,check_hash):
    '''
    Get the pwned counts from get_response
    '''
    #hashes from  the server is in format ['hash1:count1','hash2:count2',......]
    # NOTE: hash length is 5 less as we already passed first 5 char while fetching list, so returns hashes trimmed first 5 characters
    hashes = hashes.text.splitlines()
    for line in hashes:
        hash,count=line.split(':')
        if hash==check_hash:
            return count
    return 0

def check_password(args):
    '''
    Checks for the password whether it's been pwned or not
    '''
    for password in args:
        hash_pass=convert_to_hex(password).upper()
        hash_pass_head=hash_pass[:5]
        hash_pass_tail=hash_pass[5:]

        try:
            response=get_response(api_url, hash_pass_head)
            if response.status_code==200:
                pwn_counts = get_pwned_counts(response,hash_pass_tail)
                if pwn_counts:
                    print(f'Password \'{password}\' has been pwned {pwn_counts} times, Better try another password.')
                else:
                    print(f'Password \'{password}\' seems a good password. Go ahead!! :)')
            else:
                print('No response from server. :(')
        except Exception as err:
            print('Some exception occured',err)


if __name__=='__main__':
    if len(sys.argv)==1:
        print('Please enter atleast password to check!')
    else:
        check_password(sys.argv[1:])
        os._exit(0)
