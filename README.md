# i-PWD
Encrypts the file with a unique key and stores it in you pc which can decrypted by your username and password.

![i-pwd](https://github.com/vipul-dixit-2004/i-PWD/assets/72184734/a1f5f59e-76f0-4164-99b8-34f6478269ff)

# Functionality 
UserCredentials are stored in online mysql server along with the unique key generated at the time of registration. Uses cryptography module to encrypt and decrypt file. At the time of user verification the key is extracted for further use. 
Currently can only enc/dec files only to one folder (created at that time).
~ Donot delete any folder once created by application. Offers three buttons at daskboard -> Decrypt all, Encrypt File and Logout
# Decrypt All
When clicked extracts file from data folder and initiates decrypting the files to decrypted folder.
# Encrypt File
Opens a file browser window select file or files you want to ecrypt (deleting the seleted files is not supported yet so delete the original file after encryption is complete). And stores the encrypted file in folder named data.
# LogOut 
Once clicked deletes all the encrypted file thus no traces left and closes the application immediately.

# How the use 
Just run the .exe file and you are ready. If you want to do other things get remote or local mysql server and update the details in mydb.py file. Structure for database is provided check repo file named "user_credentials.sql" . Also create a php file and updates its url in app.py 
