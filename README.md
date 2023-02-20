# imap_fetcher

This Python script connects to a Gmail IMAP server and retrieves email data, including the sender, date, and size. It then processes this data to calculate the total number of emails and size sent by each sender and saves it as a CSV file.

**Requirements**

* Python 3.x
* imaplib and email modules
* A Gmail account and an application-specific password


**How to Use**
* Clone or download the repository to your computer.
* Open the script in a text editor and modify the email_address and password variables with your Gmail credentials.
* Run the script in your terminal or IDE.
* The script will output a progress bar showing the percentage of emails processed and the estimated remaining time.
* Once the script has finished processing all the emails, it will save the data as a CSV file named "senders.csv" in the same directory as the script.
