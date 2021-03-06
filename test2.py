# TEST DATA INFORMATION #
cost = float(0.1)

# GLOBAL VARIABLES #
account = []
charity = []
product = []
userid  = 0 # WARNING! SHOULD NOT CHANGE ONCE SET IN CHECKUSER() BLOCK
prodid  = 0 # WARNING! SHOULD NOT CHANGE ONCE SET IN CHECKPROD() BLOCK
barcode = 0 # WARNING! SHOULD NOT CHANGE ONCE SET IN SCANBARCODE() BLOCK
toscan  = 1
numbot  = 0 # Number of bottles for the current session.
session = []

# INDEX VALUES #
i_user = 0  # UserDB : col 0
i_snme = 1  # UserDB : col 1, surname
i_fnme = 2  # UserDB : col 2, first name
i_tusr = 3  # UserDB : col 3, total bottles collected by the user
i_ucrd = 4  # UserDB : col 4, user credit
i_favc = 5  # UserDB : col 5, favourite charity
i_char = 0  # CharDB : col 0, charity id
i_tchr = 1  # CharDB : col 1, total bottles donated to the charity
i_cnme = 2  # CharDB : col 2, charity name
i_desc = 3  # CharDB : col 3, charity description
i_code = 0  # ProdDB : col 0, barcode
i_petB = 1  # ProdDB : col 1, pet or not (Boolean value: 0,1)
i_manu = 2  # ProdDB : col 2, manufacturer
i_orig = 3  # ProdDB : col 3, country of origin

############################
## LOAD ALL THE DATABASES ##
############################

# USER DATABASE #
def loadUSERDB():
    import csv
    with open('userDB.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            account.append(row)

# CHARITY DATABASE #
def loadCHARDB():
    import csv
    with open('charDB.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            charity.append(row)

# PRODUCT DATABASE #
def loadPRODDB():
    import csv
    with open('prodDB.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            product.append(row)

######################
## HELPER FUNCTIONS ##
######################

def getCREDIT():
    credit = '%.2f'%( float(account[userid][i_tusr]) * cost )
    return credit

def checkPET():
    if int(product[prodid][i_petB]):
        return 1
    return 0

def scanBARCODE():
    prompt = input('Scan product? (y/n) ')
    global toscan
    
    if prompt is "y":
        toscan = 1
        prompt = input('\nScan product barcode: ')
        global barcode
        barcode = int(prompt)
        checkPRODUCT()
    else:
        toscan = 0

def scanLOOP():
    scanBARCODE()
    global numbot
    while int(toscan) != 0:
        if checkPRODUCT() == 1:
            print("Product exists in the database.")
            if checkPET() == 1:
                print("Product is PET!")
                numbot += 1
                repeatSCAN()
                session.append(barcode)
                print("Total bottles for this session:", numbot)
            else:
                print("Product is NOT PET!")
        else:
            print("Product does not exist in the database.")
        scanBARCODE()

def repeatSCAN():
    global session
    global numbot
    if barcode in session:
        print("Bottle already scanned.")
        numbot -= 1

def selectCHAR():
    global numbot
    print("Who would you like to donate to?")
    incr = 0
    while incr < len(charity):
        print(incr, ":", charity[incr][i_cnme], sep=' ')
        incr += 1

    loop = 0
    while numbot > 0:
        select = input('Please select charity: ')
        value = input('How many bottles? ')
        ivalue = int(value)

        # Need to ensure user does not enter more bottles than scanned. #
        if ivalue > numbot:
            print("Invalid number. Please try again.")
        else:
            charity[int(select)][4] = ivalue
            numbot = numbot - ivalue
            print("Bottles left: ", numbot)
        loop += 1
        
    print("Thank you for donating your PET bottles!")

##########################################################################
## STAGE ONE : ASK FOR QR CODE AND CHECK IF USER EXISTS IN THE DATABASE ##
##########################################################################

def checkUSER():
    """
    Check user log in options.
    
    INPUT  : None.
    OUTPUT :
        0 >> Exit
        1 >> Default user, continue.
        2 >> Existing user, continue.
        3 >> Not existing user, create account and continue.
    """
    welcome = input('Please select:\nA) Default user\nB) Existing user\nC) Exit\n')

    if welcome is "A":
        return 1
    
    if welcome is "B":
        user = input('Enter userID: ')  # FUTURE : Please scan QR code.
        
        incr = 0
        while incr < len(account):
            hold_user = account[incr][i_user]
            if int(hold_user) == int(user):
                global userid
                userid = incr
                return 2
            incr += 1
            
        notfound = input('User not found.\nPlease select:\nA) Default user\nB) Create new account\nC) Exit\n')
        if notfound is "A":
            return 1
        if notfound is "B":
            return 3
        else:
            return 0
    else:
        return 0

#############################################################################
## STAGE TWO : ASK FOR BARCODE AND CHECK IF PRODUCT EXISTS IN THE DATABASE ##
#############################################################################

def checkPRODUCT():
    """
    Check if product exists in the database.

    INPUT  : None.
    OUTPUT :
        0 >> Product not in the database, exit.
        1 >> Product in the database, continue.
        2 >> Enter product in the database.
    """
    incr = 0
    while incr < len(product):
        hold_code = product[incr][i_code]

        # PRODUCT EXISTS IN THE DATABASE #
        if int(hold_code) == int(barcode):
            global prodid
            prodid = incr
            return 1
        incr += 1
    return 0

################
## MAIN BLOCK ##
################

loadUSERDB()
loadPRODDB()
loadCHARDB()

usertype = int(checkUSER())

if usertype == 1:
    print("Welcome!")
    scanLOOP()
if usertype == 2:
    print("Welcome,", account[userid][i_fnme], account[userid][i_snme], sep=' ', end="!\n")
    scanLOOP()
    print("Total bottles for this session: ", numbot)
    selectCHAR()
if usertype == 3:
    #Create a new account#
    print("Please wait while we set up an account for you...")
else:
    print("END.")


