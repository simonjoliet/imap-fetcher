import imaplib
import email
import csv
import io
import sys

# Set the login credentials
email_address = "your_email@gmail.com"
password = "Google one time password"

# Connect to the Gmail IMAP server
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(email_address, password)
imap.select("inbox")

# Search for all emails and retrieve their IDs
status, email_ids = imap.search(None, "ALL")
email_ids = email_ids[0].split()

# Set up the progress bar
num_emails = len(email_ids)
bar_width = 40

# Write the email data to a CSV file
csv_file = io.StringIO()
writer = csv.writer(csv_file)
writer.writerow(["Sender", "Date", "Size"])

# Fetch the email data for each ID and write it to the CSV file
num_emails = len(email_ids)
for i, email_id in enumerate(email_ids):
    status, msg = imap.fetch(email_id, "(RFC822)")
    msg = email.message_from_bytes(msg[0][1])
    sender = msg["From"]
    date = msg["Date"]
    size = len(msg.as_bytes())
    writer.writerow([sender, date, size])

    # Update the progress bar
    progress = (i + 1) / num_emails
    filled = int(bar_width * progress)
    bar = "[" + "=" * filled + " " * (bar_width - filled) + "]"
    sys.stdout.write(f"\rProcessing emails: {bar} {progress:.1%} [{i+1} / {num_emails}]")
    sys.stdout.flush()

# Close the connection to the IMAP server
imap.close()
imap.logout()

# Save the CSV file to disk
with open("emails.csv", "w", newline="") as file:
    file.write(csv_file.getvalue())
