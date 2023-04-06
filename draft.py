import time as t
import pyodbc as py
import random as rand
#connect to database which is Microsoft Access 2016
con_str=(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
         r'DBQ=C:\Users\Admin\Documents\Database\user_information.accdb;')
py.connect(con_str)
con = py.connect(con_str)
cursor=con.cursor()

def lobby():
    
    print("Which service do you want to try? Press the number 1,2,3 or 4 to choose")
    print(
    "1. Saving\n"
    "2. Transfer\n"
    "3. Import money\n"
    "4. Remains checker\n"
    "5. Exit"
    )
    try: 
        choice = int(input("Enter your choice: "))
        if choice == 1:
            lobby()

        elif choice == 2:
            decision = int(input("Choose where to transfer to (press 1 for other banks and 2 for chun bank):"))
            if decision == 1:
                other_bank = int(input("Enter the account number: "))
                expense = int(input("Enter an amount of money to transfer: "))
                cursor.execute('''SELECT Remains FROM Customer where ID = ?''', Id)
                row = cursor.fetchone()
                if row.Remains < expense:
                    print("Your remains is not enough to transfer, import more to do this")
                    lobby()
                elif row.Remains >= expense:
                    row.Remains -= expense
                    cursor.execute('''Update Customer SET Remains = ? WHERE ID = ?''', (row.Remains,Id))
                    con.commit()
                    print("Successfully transfer to", other_bank)
                    lobby()

            elif decision == 2:
                chun_bank = input("Enter the ID of the account: ")
                cursor.execute('''SELECT * FROM Customer''')
                for row in cursor.fetchall():
                    if row[0] == chun_bank:
                        expense2 = int(input("Enter an amount of money to transfer: "))
                        cursor.execute('''SELECT Remains FROM Customer where ID = ?''', Id)
                        row1=cursor.fetchone()
                        if row1.Remains < expense2:
                            print("The remaining is not enough, try to import more")
                            lobby()
                        else:                        
                            cursor.execute('''SELECT Remains FROM Customer where ID = ?''', chun_bank)
                            row2=cursor.fetchone()

                            row1.Remains -= expense2
                            cursor.execute('''Update Customer SET Remains =? WHERE ID=?''', (row1.Remains,Id))
                            con.commit()

                            row2.Remains += expense2
                            cursor.execute('''Update Customer SET Remains =? WHERE ID=?''', (row2.Remains,chun_bank))
                            con.commit()
                            print("Successfully transfer to", chun_bank)
                            lobby()
                else:
                    print("The account doesn't exist, try an available one please")
                    lobby()
    #There are quite a few difference between the syntax of INSERT TO and UPDATE ... SET (About how to call the column)
        elif choice == 3:
            amount = float(input("Enter the amount you want to add to your account(in USD): "))
            cursor.execute('''SELECT Remains FROM Customer where ID = ?''',Id)

            #Take the element from the specific row to this program and apply something to it
            row=cursor.fetchone()
            row.Remains += amount
            #Add to it
            cursor.execute('''Update Customer SET Remains =? WHERE ID=?''', (row.Remains,Id))
            con.commit()
            print("Import successfully")
            lobby()

        elif choice == 4:
            cursor.execute('''SELECT Remains FROM Customer where ID = ?''',Id)
            row=cursor.fetchone()
            print("This is your Remains: ", row.Remains)
            lobby()

        elif choice == 5:
            print("See you again")
            exit()

    #Handling erro when user press enter instead of number
    except ValueError:
        lobby()

#Define sign up function
def sign_up():
    print("Hello, let's create your account!")
    print()
    ID=rand.choice(range(999999999999))
    user_name = input("Enter your user name: ")
    #Check if the user name from here has been registered or not
    cursor.execute('''SELECT * FROM Customer''')
    for row in cursor.fetchall():
        if row[1] == user_name:
            print("The user name has been registered, try a different one please!")
            sign_up()
            
    print()
    print("Hi "+ user_name)
    ran_or_sel = ["R", "r", "S", "s"]
    ask = input("Do you want a randomized password or your self-made one? R for randomized or S for self-made: ")
    while ask not in ran_or_sel:
        print("Try S, s, r or R please")
        ask = input("Do you want a randomized password or your self-made one? R for randomized or S for self-made: ")

    #Randomize password
    characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    randomized_pass = []
    if ask == "R":
        
        the_limit = int(input("How many digit you want your password to to have (Your password must have at least 5 digits): "))
        while the_limit < 5:
            print("Your password should have at least 5 digits")
            the_limit = int(input("How many digit you want your password to to have (Your password must have at least 5 digits): "))
        count = 0
        while count < the_limit:
            count+=1
            b=rand.choice(characters)
            randomized_pass.append(b)
        entered_pass = "".join(randomized_pass) 
        print("This is your password:", entered_pass)
        print("This is your ID:", ID,"This is your user name:",user_name, "This is your password:",entered_pass)

        #Store the ID, user name and password to ACCESS
        cursor.execute('''INSERT INTO Customer ([ID], [User name], [Password]) VALUES('{}','{}', '{}')'''.format(ID,user_name,entered_pass))
        con.commit()
        print("Sign up successfully, please log in again to enter the app")

    #Self-made password
    elif ask == "S" or ask == "s":

        selfmade_pass = input("Create your own password please: ")
        print("This is your ID:",ID,"This is your user name:",user_name, "This is your password:",selfmade_pass)
        cursor.execute('''INSERT INTO Customer ([ID], [User name], [Password]) VALUES('{}','{}', '{}')'''.format(ID,user_name,selfmade_pass))
        con.commit()
        print("Sign up successfully, please log in again to enter the app")
    else:
        print("Invalid choice")
        sign_up()

#Entrance
def entrance():
    print("Welcome User!")
    welcome_user = input("Log in or sign up: ")
    possible_ans = ["Log in", "log in", "Sign up", "sign up"]
    while welcome_user not in possible_ans:
        print("Your choice is invalid, try an appropriate one!")
        welcome_user = input("Log in or sign up: ")

    if welcome_user == "Log in" or welcome_user == "log in":
        query = "SELECT * FROM Customer;"
        cursor.execute(query)
        global Id
        #globalize the Id variable

        Id=input("Enter your id: ")
        User_name=input("enter your user name: ")
        Password=input("Enter your password: ")
        #Check data in the table Customer 
        for row in cursor.fetchall():
            if row[0] == Id and row[1] == User_name and row[2] == Password:
                print("Loading...")
                t.sleep(1)

                print()
                
                print("Login successfully!")
                lobby()
                break
        else:
            print("Loading")
            t.sleep(1)
            print("ID, user name or password is invalid! Try again")
            entrance()

    elif welcome_user == "Sign up" or welcome_user == "sign up":
        sign_up()
        entrance()

entrance()