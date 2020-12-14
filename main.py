import socket             # get ip address sent using sms for 2FA
from requests import get
from tkinter import *     # always be explicit rather than implicit - pep8
from functools import partial
from tkinter import messagebox as m_box
from twilio.rest import Client # Twilio api
from datetime import datetime
import secrets            # https://docs.python.org/3/library/secrets.html
                          # Generates a ten-character alphanumeric salt with at least
                          # one lowercase character, at least one uppercase character, and at least three digits


import requests
joke_ = requests.get(
    "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw&format=txt")  # JOKE API
ipaddr = get('https://api.ipify.org').text
hostname = socket.gethostname()
local_ipaddr = socket.gethostbyname(hostname)


def generateOTP():
    global otp_
    otp_ = secrets.token_hex(4)
    return otp_


def validateLogin(username, password):
    if username.get() == "admin" and password.get() == "s4401":
        m_box.showinfo("paradoXe-Password Manager",
                       "OTP has been sent to your resgistered mobile number")
        # Your Account Sid and Auth Token from twilio.com/console
        account_sid = 'xxxx'
        auth_token = 'xxxx'
        client = Client(account_sid, auth_token)
        client.messages \
            .create(
                body="Hey, You made a successful login attempt at {}. \nHostname: {}\nPublic IP: {}\nLocal IP:{}\nYour OTP is: {}".format(
                    datetime.now(), hostname, ipaddr, local_ipaddr, generateOTP()),
                from_='xxxx',
                to='xxxx'
            )

    else:
        m_box.showwarning("paradoXe-Password Manager", "Enter Valid Credentials")
        # Error Attemp made
        account_sid = 'xxxx'
        auth_token = 'xxxx'
        client = Client(account_sid, auth_token)
        client.messages \
            .create(
                body="Hey, You made an unsuccessful login attempt at {}. \nHostname: {}\nPublic IP: {}\nLocal IP: {}".format(
                    datetime.now(), hostname, ipaddr, local_ipaddr),
                from_='xxxx',
                to='xxxx'
            )


# window
tkWindow = Tk()
# tkWindow.geometry('400x150')
tkWindow.title('paradoXe - Password Manager')

# username label and text entry box
usernameLabel = Label(tkWindow, text="User Name", anchor=W, justify=LEFT).grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)

# password label and password entry box
passwordLabel = Label(tkWindow, text="Password", anchor=W, justify=LEFT).grid(row=1, column=0)
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)

# OTP label and OTP entry box
OTPLabel = Label(tkWindow, text="OTP *case sensitive", anchor=W, justify=LEFT).grid(row=5, column=0)
OTP = StringVar()
OTPEntry = Entry(tkWindow, textvariable=OTP, show='*').grid(row=5, column=1)


validateLogin = partial(validateLogin, username, password)

# login button
OTPButton = Button(tkWindow, text="Generate OTP", command=validateLogin).grid(row=2, column=1)


def validateOTP():
    if OTP == otp_:
        m_box.showinfo("paradoXe-Password Manager", "OTP verification Successful")
        tkWindow.destroy
    else:
        tkWindow.destroy


# verify OTP button
verifyButton = Button(tkWindow, text="Verify OTP", command=validateOTP).grid(row=6, column=1)


# JOKE API label
jokeLabel = Label(tkWindow, text="\nHere to make your day: \n" + joke_.text,
                  font=("Helvetica", 8), anchor=W, justify=LEFT).grid(row=8, column=1)
tkWindow.mainloop()
