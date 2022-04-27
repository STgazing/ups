import os
import hashlib
import platform
import sqlite3

#this class change texts color
class color:
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Grey = '\033[90m'
    Black = '\033[90m'

#this func set a password for program
def set_password():
    login_banner()
    print('')
    passwd = input('Please Set Your Password: ').encode('utf-8')
    passwd2 = input('Please Enter the Password Again: ').encode('utf-8')
    hashed_password = hashlib.md5(passwd).hexdigest()
    if passwd == passwd2:
        with open('.passwd.txt', 'w') as f:
            f.write(hashed_password)
    else:
        print('The Passwords Does Not Match! Try Again')
        set_password()

#this func check login password 
def login():
    login_banner()
    passwd = input('''
Enter Your Login Password:    
F: Forgot Password
Q: Quit

--̶>̶ ''')
    hashed_password = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    file = open('.passwd.txt')
    if passwd.upper() == 'Q':
        print('')
        print('See You Later :)')
        quit()
    elif passwd.upper() == 'F':
        try:
            file.close()
            reset_password()
            quit()
        except FileNotFoundError:
            file.close()
            print('Done!')
            input('Press Enter To Continue: ')
            runner()            
    elif file.read() != hashed_password:    
        print('Wrong Password!')
        choose = input('Please Enter the Password Currectly, Try Again? Y/n  ')
        if choose.upper() == 'Y':
            clear_screen()
            login()    
        else:
            quit() 
    if passwd == 'F':
        reset_password()                   
        
#this func call password setter func for the first time and next times call login func
def check_password_set():
    if os.path.exists('.passwd.txt') == False:
        set_password()
    else:
        login()

#this func write datas in database
def database_writer():
    usernme = input('Enter Username: ')
    passwd = input('Enter Password: ') 
    conn = sqlite3.connect('.database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS datas (username text, password text)')
    c.execute('INSERT INTO datas VALUES("{}","{}")'.format(usernme , passwd))
    conn.commit()
    conn.close()

#this func show saved datas
def database_reader():
    if os.path.exists('.database.db'):
        conn = sqlite3.connect('.database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM datas')
        print(*c.fetchall() , sep='\n')
    else:
        print('Database is Empty! ')    

#this func change current password
def password_changer():
    oldpasswd = input('Enter the Old Password: ').encode('utf-8')
    hashed_password = hashlib.md5(oldpasswd).hexdigest()
    file = open('.passwd.txt')
    if file.read() == hashed_password:
        newpasswd = input('Enter New Password: ')
        newpasswd2 = input('Enter New Password Again: ')
        new_hashed_password = hashlib.md5(newpasswd.encode('utf-8')).hexdigest()
        if newpasswd == newpasswd2:
            with open('.passwd.txt', 'w') as f:
                f.write(new_hashed_password)
    else:
        print('Wrong Password!')
        password_changer()            

#this func reset password and database
def reset_password():
    question = input('''This Method Deletes the Entire Database, Are You Sure? Y/n:  ''')
    if question.upper() == 'Y':
        os.remove('.passwd.txt')
        os.remove('.database.db')
    elif question.upper() == 'N':
        print('Password and Database Reset Successfully')
        runner()    

#this func show menue
def menue():
    clear_screen()
    menue_banner()
    print('[1] Write a Data in the Database')
    print('[2] Read Datas in the Database')
    print('[3] Clear Database')
    print('[4] Change Password')
    print('[5] Reset Password')
    print('[6] Exit')
    print('')
    choose = input('--̶>̶ ')
    if choose == '1':
        database_writer()
        input('Press Enter to Back to the Menue: ')
        menue()
    elif choose == '2':
        database_reader()
        input('Press Enter to Back to the Menue: ')
        menue()
    elif choose == '3':
        warn = input('This Method Clear Database, Are You Sure? Y/n: ')
        if warn.upper() == 'Y':
            os.remove('.database.db')
        else:
            menue()
        input('Press Enter to Back to the Menue: ')
        menue()    
    elif choose == '4':                    
        password_changer()
        input('Press Enter to Back to the Menue: ')
        menue()
    elif choose == '5':
        reset_password()
        runner()
        input('Press Enter to Back to the Menue: ')
        menue()
    elif choose == '6':
        print('')
        print('See You Later :)')
        quit()   
    else:
        menue()         

#this func clear screen
def clear_screen():
    OS = platform.system()
    if OS == 'Windows':
        os.system('cls')
    elif OS == 'Linux' or OS == 'Darwin':
        os.system('clear')       

#this func displays the banner on the login page
def login_banner():
    print('''  ____    _____                         _                 
 / ___|  |_   _|   __ _    __ _   ____ (_)  _ __     __ _ 
 \___ \    | |    / _` |  / _` | |_  / | | | '_ \   / _` |
  ___) |   | |   | (_| | | (_| |  / /  | | | | | | | (_| |
 |____/    |_|    \__, |  \__,_| /___| |_| |_| |_|  \__, |
                  |___/                             |___/  T̶M̶''')

#this func displays the banner on the menue
def menue_banner():
    print('''
█░█ █▀█   █▀ ▄▀█ █░█ █▀▀ █▀█
█▄█ █▀▀   ▄█ █▀█ ▀▄▀ ██▄ █▀▄''')
    print('')

#this func run the main program
def runner():
    clear_screen()
    check_password_set()
    menue()

runner()