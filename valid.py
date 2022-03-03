import validators


valid = validators.url('https://www.y.com/')
if valid == True:
    print("Url is valid")
else:
    print("Invalid url")