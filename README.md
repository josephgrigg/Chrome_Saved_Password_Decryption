# Chrome_Saved_Password_Decryption

![](http://i.imgur.com/edG6fjk.png)

## Purpose:
To demonstrate a security flaw with Chrome's password manager.

## The Problem:
If you try to view your saved passwords through the Chrome browser, you will receive a pop-up requesting your Windows user account password as shown below.

![](http://i.imgur.com/qjdHrFL.png)

Unfortunately, this step provides a false sense of security as anyone with access to the computer and logged in under your account can decrypt all of the passwords quickly and easily.

Chrome saves passwords into a SQLite3 database located in Windows here: ```[username]\Appdata\Local\Google\Chrome\User Data\Default\Login Data```

The database itself is not encrypted; however, the stored passwords are encrypted using the Windows DPAPI function [CryptProtectData](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380261). The problem is that these are encrypted in the context of the Windows user account and no additional entropy is used during encryption. What this means is that you do not actually need to re-enter your user password in order to decrypt the passwords.

## A Solution:
Mozilla Firefox's solution to this problem is the 'master password' which it asks for at the start of each session. The master password is a user created password that is used for added entropy during the encryption process. Thus, you would have to know the master password in order to decrypt the saved passwords. Of course, this method is still vulnerable to attacks such as keyloggers, but it does add a useful layer of protection.

Unfortunately, this has been a requested feature for Chrome for years now and it does not appear that they plan to add it. However, there are third party password managers that can be used. 
