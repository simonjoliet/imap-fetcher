import imaplib
import email
import csv
import io
import sys
import time

# Set the login credentials
email_address = "your_email@gmail.com"
password = "Google one time password"

# Connect to the Gmail IMAP server
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(email_address, password)
imap.select("inbox")

# Search for all emails and retrieve their IDs, sender, date and size
status, email_ids = imap.search(None, "ALL")
email_ids = email_ids[0].split()

senders = {}
total_size = 0

# Set up the progress bar
num_emails = len(email_ids)
bar_width = 40

# Initialize the remaining time and start time
remaining_time = None
start_time = time.time()

# Fetch the email data for each ID and extract the sender, and size
for i, email_id in enumerate(email_ids):
    status, msg = imap.fetch(email_id, "(RFC822)")
    msg = email.message_from_bytes(msg[0][1])
    sender = str(msg["From"])
    size = len(msg.as_bytes())

    # Update the sender's email count and total email size
    if sender in senders:
        senders[sender]["count"] += 1
        senders[sender]["size"] += size
    else:
        senders[sender] = {"count": 1, "size": size}
    
    total_size += size

    # Update the progress bar and remaining time
    progress = (i + 1) / num_emails
    filled = int(bar_width * progress)
    bar = "[" + "\u2588" * filled + " " * (bar_width - filled) + "]"
    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        remaining_time = (elapsed_time / progress) - elapsed_time
    (hours, remainder) = divmod(int(remaining_time), 3600)
    (minutes, seconds) = divmod(remainder, 60)
    remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}" if remaining_time else "--:--:--"
    sys.stdout.write(f"\rProcessing emails: {bar} {progress:.1%} [{i+1} / {num_emails}] (remaining time: {remaining_time_str})")
    sys.stdout.flush()

# Close the connection to the IMAP server
imap.close()
imap.logout()

# Sort the senders by size
senders = sorted(senders.items(), key=lambda x: x[1]["size"], reverse=True)

# Write the email data to a CSV file
csv_file = io.StringIO()
writer = csv.writer(csv_file)
writer.writerow(["Sender", "Email Count", "Total Size (MB)"])

# Write the sender's email count and total email size to the CSV file
for sender, data in senders:
    email_count = data["count"]
    total_size_mb = round(data["size"] / (1024 * 1024), 2)
    writer.writerow([sender, email_count, total_size_mb])

# Save the CSV file to disk
with open("senders.csv", "w", newline="") as file:
    file.write(csv_file.getvalue())
    
print()
