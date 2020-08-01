from passlib.context import CryptContext
import tkinter
import time
import threading
import yagmail
import os
import random

randomNumber = random.randint(100000, 999999)

context = CryptContext("sha256_crypt")


def labels():
    tkinter.Label(root, text="Email", justify=tkinter.LEFT).grid(sticky=tkinter.W, row=1, column=3)
    tkinter.Label(root, text="Password", justify=tkinter.LEFT).grid(sticky=tkinter.W, row=2, column=3)
    tkinter.Label(root, text="Confirm Password", justify=tkinter.LEFT).grid(sticky=tkinter.W, row=3, column=3)


def entriesAndButtons():
    mailvalue = tkinter.StringVar()
    pwdvalue = tkinter.StringVar()
    confirmvalue = tkinter.StringVar()

    mailenter = tkinter.Entry(root, show=None, textvariable=mailvalue, width=44)
    pwdenter = tkinter.Entry(root, show='*', textvariable=pwdvalue, width=44)
    confirmenter = tkinter.Entry(root, show='*', textvariable=confirmvalue, width=44)

    mailenter.grid(row=1, column=4)
    pwdenter.grid(row=2, column=4)
    confirmenter.grid(row=3, column=4)

    def verify():
        if pwdvalue.get() == confirmvalue.get() and not os.path.exists(f"database/{mailvalue.get()}.sha"):
            t2 = threading.Thread(target=sendMail)
            t2.daemon = True
            t2.start()

            otpvalue = tkinter.StringVar()
            tkinter.Label(root, text="OTP", justify=tkinter.LEFT).grid(sticky=tkinter.W, row=6, column=3)
            tkinter.Entry(root, show='*', textvariable=otpvalue, width=44).grid(row=6, column=4)
            otplabel = tkinter.Label(root, text="The OTP has been sent to your E-Mail", justify=tkinter.LEFT)
            otplabel.grid(sticky=tkinter.W, row=5, column=4)

            def otpverify():
                print(f"{otpvalue.get()}", str(randomNumber))
                if f"{otpvalue.get()}" == str(randomNumber):
                    f = open(f"database/{mailvalue.get()}.sha", "w+")
                    f.write(context.hash(f"{pwdvalue.get()}"))
                    f.close()
                    tkinter.Label(root, text="Successfully Registered", justify=tkinter.LEFT).grid(sticky=tkinter.W,
                                                                                                   row=8, column=4)
                else:
                    t3 = threading.Thread(target=wrongotplol)
                    t3.daemon = True
                    t3.start()

            def wrongotplol():
                wrongotplabel = tkinter.Label(root, text="Wrong OTP", justify=tkinter.LEFT)
                wrongotplabel.grid(sticky=tkinter.W, row=8, column=4)
                time.sleep(3)
                wrongotplabel.destroy()

            tkinter.Button(root, text="Verify", command=otpverify).grid(row=7, column=3)

        else:
            t1 = threading.Thread(target=labelpasscancel)
            t1.daemon = True
            t1.start()

    def sendMail():
        # Enter your Email and password here. Also disable some security features in your google account coz google
        # doesn't allow 3rd party sources by default
        server = yagmail.SMTP("example@gmail.com", "password")
        server.send(f"{mailvalue.get()}", "Verify your Email", f"Your Registration OTP is {randomNumber}")

    def labelpasscancel():
        wrong = tkinter.Label(root, text="Passwords don't match up or Email already exists", justify=tkinter.LEFT)
        wrong.grid(sticky=tkinter.W, row=5, column=4)
        time.sleep(3)
        wrong.destroy()

    tkinter.Button(root, text="Register", command=verify, justify=tkinter.LEFT).grid(sticky=tkinter.W, row=4, column=4)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("380x200")
    root.title("Register")

    labels()
    entriesAndButtons()

    root.mainloop()
