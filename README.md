# imap_fetcher

This Python script uses the IMAP protocol to connect to a Gmail account, retrieve data about all emails in the inbox, and save the data to a CSV file. The script requires the imaplib, email, csv, io, and sys libraries.

Setup
Before running the script, replace the email_address and password variables with the email address and one-time password for the Gmail account you want to access.

Running the script
The script will connect to the Gmail IMAP server and search for all emails in the inbox. It will then fetch the email data for each email and write the sender, date, and size to a CSV file called emails.csv.

As the script processes the emails, it will display a progress bar showing the percentage of emails processed and the number of emails completed.

Once all the emails have been processed, the script will close the connection to the IMAP server and save the CSV file to disk.

Note that the script only retrieves data about emails in the inbox. If you want to retrieve data about emails in another mailbox or with specific labels, you will need to modify the search criteria in the imap.search() method.

Purpose
Using the output csv data might be useful for analytics purposes. For instance, pivoting the data will give you some insight to delete email threads and unsubscribe mailing lists that are using significant storage space on your Gmail account.
