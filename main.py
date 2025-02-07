#start to the terminal code
import os
import sys
import time
import subprocess
import platform
import getpass
import shutil
import requests
import json
import re
import login

while True:
    #ask for the action
    act = input("enter action, type help for more information:")

    #help command gives explenation of commands and program
    if(act == "help"):
        print("\n\n--------------------")
        print("<COMMANDS> \n")
        print("help: show all commands")
        print("login: start login system")
        print("exit: exit the system")
        print("--------------------")
        print("<DESCRIPTION> \n")
        print("this is a financian banking system, you can withdraw money, depisite money, and all the other things a banking app does all from the comfor of your terminal. \n\nTo log in just type 'login' to begin the login process. ")
        print("--------------------\n\n")

    #exit command exits the program
    elif(act == "exit"):
        break

    #login command starts the login system
    elif(act == "login"):
        login.login()
