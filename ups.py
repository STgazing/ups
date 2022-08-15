import os
import random
import hashlib
import platform
import sqlite3
import time
from time import sleep
from rich.console import Console
from rich.traceback import install
from rich.progress import Progress , track

console = Console()

#this func set a password for program
def set_password():
    login_banner()
    print('')
    passwd = console.input(' Please Set Your [bold red]Password[/] : ').encode('utf-8')
    passwd2 = console.input(' Please Enter the [bold red]Password Again[/] : ').encode('utf-8')
    print('')
    hashed_password = hashlib.md5(passwd).hexdigest()
    for i in track(range(5), description="[bold #05e8d5] Generating... "):
        time.sleep(1) 
    clear_screen()
    if passwd == passwd2:
        with open('.passwd.txt', 'w') as f:
            f.write(hashed_password)
    else:
        console.rule('[i] The Passwords Does Not Match![/] [bold red]Try Again[/]')
        set_password()

#this func check login password 
def login():
    login_banner()
    passwd = console.input('''
 [italic]Enter Your [bold green]Login[/] Password[/] :    
 [bold #e87a05][F][/] Forgot Password : 
 [bold red][Q][/] Quit : 
 [#05e8d5]--̶>̶ [/] ''')
    hashed_password = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    file = open('.passwd.txt')
    if passwd.upper() == 'Q':
        print('')
        console.print('[#05e8d5]See You Later :)[/]')
        quit()
    elif passwd.upper() == 'F':
        try:
            file.close()
            reset_password()
            quit()
        except FileNotFoundError:
            file.close()
            console.print(' [bold green]Done!')
            console.input(' Press [italic green]Enter[/] To Continue: ')
            runner()            
    elif file.read() != hashed_password:    
        print('')
        console.print(' [bold red]Wrong Password!')
        choose = console.input(' Please Enter the Password Currectly, Try Again? [#05e8d5](Y/n)[/] : ')
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
    clear_screen()
    usernme = console.input('Enter [bold red]Username[/]: ')
    passwd = console.input('Enter [bold #e87a05]Password[/]: ') 
    print('')
    tasks = [f"task {n}" for n in range(1, 4)]
    with console.status("[bold green]Working on tasks...") as status:
        while tasks:
            task = tasks.pop(0)
            sleep(1)
            console.log(f"{task} complete!")
    print('')
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
        print('')
        print(*c.fetchall() , sep='\n')
    else:
        console.print('[bold red]Database is Empty! ')    

#this func change current password
def password_changer():
    oldpasswd = console.input('[italic red]Enter the Old Password: ').encode('utf-8')
    hashed_password = hashlib.md5(oldpasswd).hexdigest()
    file = open('.passwd.txt')
    if file.read() == hashed_password:
        newpasswd = console.input('Enter [bold green]New Password[/] : ')
        newpasswd2 = console.input('Enter [bold green]New Password Again[/] : ')
        new_hashed_password = hashlib.md5(newpasswd.encode('utf-8')).hexdigest()
        if newpasswd == newpasswd2:
            with open('.passwd.txt', 'w') as f:
                f.write(new_hashed_password)
    else:
        print('Wrong Password!')
        password_changer()            

#this func reset password and database
def reset_password():
    question = console.input('''This Method [bold red]Deletes[/] the Entire Database, Are You Sure? [#05e8d5](Y/n)[/] :  ''')
    if question.upper() == 'Y':
        os.remove('.passwd.txt')
        os.remove('.database.db')
    elif question.upper() == 'N':
        console.print('[green]Password and Database Reset Successfully')
        runner()    

#this func show menue
def menue():
    clear_screen()
    menue_banner()
    console.print('[bold #05e8d5][1][/] Write a Data in the Database')
    console.print('[bold #05a4e8][2][/] Read Datas in the Database')
    console.print('[bold #d105e8][3][/] Clear Database')
    console.print('[bold #4f0241][4][/] Change Password')
    console.print('[bold yellow][5][/] Reset Password')
    console.print('[bold #e87a05][6][/] Generate a Random Password')
    console.print('[bold red][7][/] Exit')
    console.print('')
    choose = console.input('[#05e8d5]--̶>̶ [/] ')
    if choose == '1':
        database_writer()
        print('')
        console.input('Press Enter to Back to the [italic green]Menue[/] : ')
        menue()
    elif choose == '2':
        database_reader()
        print('')
        console.input('Press Enter to Back to the [italic green]Menue[/] : ')
        menue()
    elif choose == '3':
        warn = console.input('This Method [bold red]Clear[/] Database, Are You Sure? [bold blue](Y/n)[/] : ')
        if warn.upper() == 'Y':
            os.remove('.database.db')
        else:
            menue()
        print('')
        console.input('Press Enter to Back to the [italic green]Menue[/] : ')
        menue()    
    elif choose == '4':                    
        password_changer()
        print('')
        console.input('Press Enter to Back to the [italic green]Menue[/] : ')
        menue()
    elif choose == '5':
        reset_password()
        runner()
        print('')
        console.input('Press Enter to Back to the [italic green]Menue[/] : ')
        menue()
    elif choose == '6':
        password_generator()
        print('')
        console.input('Press Enter to Back to the [italic green]Menue[/] : ')
        menue()   
    elif choose == '7':
        print('')
        console.print('[#05e8d5]See You Later :)[/]')
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
    console.print('''[bold #05e8d5]  ____    _____                         _                 
 / ___|  |_   _|   __ _    __ _   ____ (_)  _ __     __ _ 
 \___ \    | |    / _` |  / _` | |_  / | | | '_ \   / _` |
  ___) |   | |   | (_| | | (_| |  / /  | | | | | | | (_| |
 |____/    |_|    \__, |  \__,_| /___| |_| |_| |_|  \__, |
                  |___/                             |___/  T̶M̶
                  ''')
    console.print('[bold #acfaf3] Follow us : Mhyar-nsi & Mobin79')

#this func displays the banner on the menue
def menue_banner():
    console.print('''[#05e8d5]
█░█ █▀█   █▀ ▄▀█ █░█ █▀▀ █▀█
█▄█ █▀▀   ▄█ █▀█ ▀▄▀ ██▄ █▀▄''')
    print('')

#this func generate a random password
def password_generator():
    charnums = int(console.input('Please enter the number of [bold green]digits[/] : '))
    passchars = list('''0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/''')
    random.shuffle(passchars)
    print('')
    console.print('[bold yellow]Your password : ')
    for i in passchars[:charnums]:
        print(i,end='')
    print('')


#this func run the main program
def runner():
    clear_screen()
    check_password_set()
    menue()

runner()
