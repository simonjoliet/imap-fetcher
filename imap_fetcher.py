#!/usr/bin/env python3

import imaplib
import email, email.header
import csv
import sys
import time
import sqlite3

# Set the login credentials
EMAIL_ADDRESS = "john.doe@gmail.com"
PASSWORD = "Google one time password"
IMAP_SERVER = "imap.gmail.com"
DB_FILE = 'email_data.db'
CSV_FILE = "senders.csv"
BAR_WIDTH = 40

def connect_imap(server, email, password):
    imap = imaplib.IMAP4_SSL(server)
    imap.login(email, password)
    imap.select("inbox")
    return imap

def init_db(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS emails
                 (uid TEXT PRIMARY KEY, sender TEXT, size INTEGER)''')
    conn.commit()
    return conn, c

def fetch_email_data(imap, uid):
    result, data = imap.uid('fetch', uid, '(RFC822)')
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    sender = str(msg["From"])
    size = len(raw_email)
    return sender, size

def store_email_data(c, uid, sender, size):
    c.execute('INSERT OR IGNORE INTO emails (uid, sender, size) VALUES (?, ?, ?)',
              (uid, sender, size))

def get_email_data(c, uid):
    c.execute('SELECT sender, size FROM emails WHERE uid=?', (uid,))
    return c.fetchone()

def update_senders(senders, sender, size):
    if sender in senders:
        senders[sender]["count"] += 1
        senders[sender]["size"] += size
    else:
        senders[sender] = {"count": 1, "size": size}
    return senders

def decode_sender(sender):
    parts = sender.split(' ')
    if len(parts) > 1 and parts[0].startswith("=?") and parts[0].endswith("?="):
        encoded_subject = ' '.join(parts[:-1])
        decoded_subject = email.header.make_header(email.header.decode_header(encoded_subject))
        email_address = parts[-1]
        return f"{decoded_subject} {email_address}"
    return sender

def write_to_csv(senders, csv_file):
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Sender", "Email Count", "Total Size (MB)"])
        for sender, data in sorted(senders.items(), key=lambda x: x[1]["size"], reverse=True):
            email_count = data["count"]
            total_size_mb = round(data["size"] / (1024 * 1024), 2)
            sender = decode_sender(sender)
            writer.writerow([sender, email_count, total_size_mb])

def print_progress_bar(iteration, total, start_time):
    progress = (iteration + 1) / total
    filled = int(BAR_WIDTH * progress)
    bar = "█" * filled + "░" * (BAR_WIDTH - filled)
    elapsed_time = time.time() - start_time
    remaining_time = (elapsed_time / progress) - elapsed_time if elapsed_time > 0 else 0
    remaining_time_str = f"{int(remaining_time // 3600):02}:{int((remaining_time % 3600) // 60):02}:{int(remaining_time % 60):02}"
    print(f"\r{bar} {progress:.1%} [{iteration+1}/{total}] {remaining_time_str} remaining", end="")
    sys.stdout.flush()

def main():
    imap = connect_imap(IMAP_SERVER, EMAIL_ADDRESS, PASSWORD)
    conn, c = init_db(DB_FILE)

    status, email_data = imap.uid('search', None, 'ALL')
    email_uids = email_data[0].split()
    num_emails = len(email_uids)
    senders = {}
    total_size = 0
    start_time = time.time()

    for i, email_uid in enumerate(email_uids):
        row = get_email_data(c, email_uid)
        if row:
            sender, size = row
        else:
            sender, size = fetch_email_data(imap, email_uid)
            store_email_data(c, email_uid, sender, size)
            conn.commit()

        senders = update_senders(senders, sender, size)
        total_size += size
        print_progress_bar(i, num_emails, start_time)

    imap.close()
    imap.logout()
    conn.close()

    write_to_csv(senders, CSV_FILE)
    print()

if __name__ == "__main__":
    main()
