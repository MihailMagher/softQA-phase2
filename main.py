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

while True:
    #ask for the action
    act = input("enter action:")
    if( act == "help"):
        print("--------------------")
        print("help: show all commands")
        print("login start login system")
        print("exit exit the system")
        print("--------------------")
