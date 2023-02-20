# imap_fetcher

This Python script connects to a Gmail IMAP server and retrieves the sender and size data for all emails. It then processes this data to calculate the total number of emails and size sent by each sender and saves it as a CSV file. This could be used to identify senders to blacklist or to recover some Google storage space by deleting emails (the script is read only and does not delete anything). It should work with other IMAP servers (although not tested).

**Requirements**

* Python 3.x
* imaplib and email modules
* A Gmail account and an application-specific password (see https://myaccount.google.com/security and create an App password if you do not have one)


**How to Use**
* Clone or download the repository to your computer.
* Open the script in a text editor and modify the email_address and password variables with your Gmail credentials.
* Run the script in your terminal or IDE.
* The script will output a progress bar showing the percentage of emails processed and the estimated remaining time.
* Once the script has finished processing all the emails, it will save the data as a CSV file named "senders.csv" in the same directory as the script.
