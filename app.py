from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import os
import time
import webbrowser
import mydb
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Log into System")
        self.geometry("400x600")
        self.configure(bg="#27374D")
        self.frame =  tk.Frame(self,bg="#526D82")
        self.frame.pack(pady=20,padx=20, fill="both", expand=True)

        self.loginlable = tk.Label(master=self.frame,text="Login to i-Pwd",font=("Arial",22,"bold"),bg="#526D82",fg="white")
        self.loginlable.pack(pady=20)


        self.user = tk.StringVar()
        self.pwd = tk.StringVar()
        #entry boxes for username and password
        #username
        self.usernameLabel = tk.Label(master=self.frame,text="Enter User Name",font=("Comic Sans MS",10),bg="#526D82",fg="white").pack()
        self.userinput = tk.Entry(master=self.frame,textvariable=self.user,font=("Comic Sans MS",15),highlightthickness=2,highlightbackground="#30A2FF")
        self.userinput.pack(pady=10)
        #password
        self.pwdLabel = tk.Label(master=self.frame,text="Enter Password",font=("Comic Sans MS",10),bg="#526D82",fg="white").pack()
        self.pwdinput = tk.Entry(master=self.frame,textvariable=self.pwd,show="*",font=("Comic Sans MS",15),highlightthickness=2,highlightbackground="#30A2FF")
        self.pwdinput.pack(pady=10)
        #showpassword btn
        self.showpwd = tk.Button(master=self.frame,text="Show Password",command=lambda:App.showPassword(self),font=("Comic Sans MS",12),bg="#00C4FF",borderwidth="2",fg="white")
        self.showpwd.pack(pady=10)
        # login btn
        self.submit = tk.Button(master=self.frame,command=lambda: App.checkCredentials(self),text="LogIn",font=("Comic Sans MS",12),bg="#30A2FF",borderwidth="2",fg="white").pack(pady=10)
        #alerts
        self.wrongCredentialsLabel = tk.Label(master=self.frame,text="Entered Credentials are Wrong",fg="red")
        self.enterCredentialsWarning = tk.Label(master=self.frame,text="Enter all Credentials",bg="yellow")
        #new user registration
        self.newUser = tk.Label(master=self.frame,text="New User click here to register",fg="red")
        self.newUser.pack(pady=10)
        self.newUser.bind("<Button-1>", lambda e: createNewAccount())
        
    def showPassword(self):
        if self.showpwd["text"] == "Show Password":
            self.showpwd["text"]= "Hide Password"
            self.pwdinput["show"] = ""
        else:
            self.showpwd["text"] = "Show Password"
            self.pwdinput["show"] = "*"

    def checkCredentials(self):
        global user
        user = self.user.get()
        pwd = self.pwd.get()
        if(user=="" or pwd==""):
            self.enterCredentialsWarning.pack(pady=10)
        else:
            self.enterCredentialsWarning.pack_forget()
            userinfo = mydb.checkUser(user,pwd)
            if(userinfo[0]):
                    self.destroy()
                    global root
                    global key
                    key = makeKey(userinfo[1][4])
                    root = tk.Tk()
                    root.title("Welcome to i-PWD Dashboard - "+userinfo[1][1])
                    root.geometry("600x400")
                    root.configure(bg="#27374D")
                    self.dashboardFrame =  tk.Frame(root,bg="#526D82")
                    self.dashboardFrame.pack(pady=20,padx=20, fill="both", expand=True)
                    #button that does the magic
                    global folderBtn
                    folderBtn = tk.Button(master=self.dashboardFrame,text="Decrypt All",command=decryptAll,font=("Comic Sans MS",12),bg="#30A2FF",borderwidth="2",fg="white")
                    folderBtn.pack(pady=10)
                    #encrypt file Button
                    global encryptBtn
                    encryptBtn = tk.Button(master=self.dashboardFrame,text="Encrypt File",command=encryptFileOrFiles,font=("Comic Sans MS",12),bg="#30A2FF",borderwidth="2",fg="white")
                    encryptBtn.pack(pady=10)
                    #logOut Btn
                    logOutBtn = tk.Button(master=self.dashboardFrame,text="Logout Now ",command=App.logout,font=("Comic Sans MS",12),bg="red",borderwidth="2",fg="white")
                    logOutBtn.pack(pady=10)
            else:
                    self.wrongCredentialsLabel.pack(pady=20)

    def logout():
        #delete all files from decrypted folder
        if(os.path.isdir("decrypted")):
            files = os.listdir("decrypted")
            for file in files:
                os.remove(os.path.join("decrypted",file)) 
            os.rmdir("decrypted") 
        root.destroy()

def createNewAccount():
    messagebox.showinfo("showinfo", "Welcome Sir Creating a new Key for you. Please OK and Registration window will appear!")
    key = Fernet.generate_key()
    key = str(key)
    key = key[2:len(key)-1]
    webbrowser.open_new_tab(f"http://dixit.vipul.unaux.com/PythonProjects/i-pwd/registration.php?key={key}")



def decryptAll():
    files = os.listdir("data")
    if(not os.path.isdir("decrypted")):
        os.mkdir("decrypted")
    for file in files:
        try:
            decData = decContent(os.path.join("data",file))
            newFileName = retrieve_file_name(file)
            saveFileDec(os.path.join("decrypted",newFileName),decData)
            error=False
        except Exception as e:
            logFile = open("log.txt",'a')
            logFile.write(time.ctime()+f"Error while decrypting all files Function: decryptAll(), file was: {file} for user: {user}  \n")
            logFile.close()
            error=True
    if(not error):
        folderBtn.config(text="All Done!",bg="green")
        messagebox.showinfo("All Done","Opening the App directory kindly open folder name \"decrypted\"")
        os.startfile(os.getcwd())
    else:
        messagebox.showerror("Attention!!", "Error occured may be few files got decrpyted kindly mail us the log file created inside the folder as it is.\n Note: Logout Now")
        folderBtn.config(text="Error occured!",bg="red")
        
def encryptFileOrFiles():
    files = fd.askopenfilenames(title="Select file or files")
    #check does data folder available
    if(not os.path.isdir("data")):
        #make a data folder
        os.mkdir("data")
    #else continue the work
    error=False
    for file in files:
        try:
            encData = encContent(file)
            fileName = file.split("/")
            fileNameWithExt = fileName[len(fileName)-1]
            newFileName = change_file_name(fileNameWithExt)
            saveFileEnc(os.path.join("data",newFileName),encData)
        except Exception as e:
            logFile = open("log.txt",'a')
            logFile.write(time.ctime()+f" : Error while ecrypting file :=> {file} in func:=> encryptFileOrFiles() for user:=> {user}  \n")
            logFile.close()
            error=True
    if(not error and len(files)>0):
        messagebox.showinfo("Done", f"Successfully encrypted all the files")

def makeKey(userkey):
    key=bytes(userkey,'utf-8')
    return Fernet(key)
# def getKey():
#     try:
#         keyFile = open('./key.txt','rb')
#         key = keyFile.read()
#         keyFile.close()
#         return key

#     except:
#         #if the user is opening for the first time
#         #print("Generating Key file")
#         messagebox.showinfo("showinfo", "Welcome Sir Creating a new Key for you.")
#         keyFile = open('./key.txt','wb')
#         key = Fernet.generate_key()
#         keyFile.write(key)
#         keyFile.close()
#         return key

# Opening File and Encrypting the content inside it 
def encContent(fileName):
    with open(fileName,'rb') as file:
        data = file.read()
        file.close()
        encode = key.encrypt(data)
    return encode

#Saving the encrypted data
def saveFileEnc(filename,data):
    with open(filename,'wb') as file:
        file.write(data)
        file.close()

#Opening File and Decrypting the content inside it
def decContent(filename):
    with open(filename,'rb') as file:
        data = file.read()
        file.close()
        decode = key.decrypt(data)
    return decode

#Saving the encrypted data
def saveFileDec(filename,data):
    with open(filename,'wb') as file:
        file.write(data)
        file.close()

#encryping filename
def change_file_name(filename):
    filename = bytes(filename,'utf-8')
    encFileName = key.encrypt(filename)
    encFileName = str(encFileName)
    encFileName = encFileName[2:len(encFileName)-1]
    return encFileName

#decrypting filename
def retrieve_file_name(encfilename):
    filename = bytes(encfilename,'utf-8')
    decFileName = key.decrypt(filename)
    decFileName = str(decFileName)
    decFileName = decFileName[2:len(decFileName)-1]
    return decFileName


     
if __name__ == '__main__':
    # Getting started with key in offline mode
    # passkey = getKey()
    # key = Fernet(passkey)
    app = App()
    app.mainloop()

    
