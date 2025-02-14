#login method
def login():
    type = input("input session type")
    while True:
        if(type == 'standard'):
            login = input("name")
            #from here we would check the login credentials
            break
        elif(type == 'admin'):
            #from here we would enter admin mode:
            break
        else:
            print("invalid session type")
    return type