# imap-fetcher

Identify storage used by email senders on Google drive, in order for instance to delete emails to recover storage, or identify large senders to blacklist (the script itself is read only and does not delete anything). This Python script connects to an email inbox using IMAP, retrieves metadata about each email, and stores relevant information in a SQLite database for cache purposes. It then summarizes the email data by sender and writes it to a pivot CSV file. The script also includes a dynamic progress bar to track the extraction process. Designed initially for Gmail, it should work with other IMAP servers (although not tested).

*Note: First execution might take a while, but after this any subsequent run should be much faster due to the built-in SQLite cache.*

## Features
- **Fetch Emails**: Connects to your email inbox and retrieves sender and size information for each email.
- **Database Storage**: Saves email metadata to a SQLite database to avoid redundant retrievals.
- **Sender Summary**: Aggregates the number and total size of emails per sender.
- **CSV Output**: Exports the summarized sender data to a CSV file.
- **Progress Tracking**: Displays a real-time progress bar with estimated time remaining.

## Prerequisites

- Python 3.6+
- Application-specific password (see https://myaccount.google.com/apppasswords and create an App password if you do not have one)
- Required libraries: `imaplib`, `email`, `sqlite3`, `csv`, `time`, `sys`

## Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/simonjoliet/imap-fetcher.git
    cd imap-fetcher
    ```

2. Install dependencies if needed (most are built-in Python libraries).

3. Edit the script to set up your email credentials:
    ```python
    EMAIL_ADDRESS = "your-email@example.com"
    PASSWORD = "your-password"
    IMAP_SERVER = "imap.your-email-provider.com"
    ```

## Usage

Run the script from the command line:
```bash
python imap_fetcher.py
```

The script will:

1. Connect to your inbox and fetch email metadata.
2. Store each email’s unique ID, sender, and size in a SQLite database (`email_data.db`).
3. Update a dictionary with the count and total size of emails per sender.
4. Write the sender summary to a CSV file (`senders.csv`) with columns:
- Sender
- Email Count
- Total Size (MB)

## Output
- Database File: `email_data.db` - Stores email metadata to avoid redundant data fetching.
- CSV File: `senders.csv` - Summarized report of email senders, email count, and total email size in MB.

## Progress Bar
The script provides a dynamic progress bar in the terminal, displaying:

- Current progress percentage.
- Number of emails processed out of the total.
- Estimated time remaining.

```bash
> python imap_fetcher.py
█████████████████████████████████████░░░ 94.6% [48043/50786] 00:01:52 remaining
```

## Example
An example of a summarized `senders.csv` output:

| Sender	            | Email Count	| Total Size (MB) |
|---------------------|-------------|-----------------|
| sender1@example.com |          15 |           12.34 |
| sender2@example.com |           8 |            8.56 |
| ...	                |         ... |             ... |

### Disclaimer
Please be cautious when storing your email password in plain text. Consider using environment variables or a secure credential manager for added security.

Make sure to replace placeholder values (e.g., `your-username`, `your-email@example.com`, etc.) with actual values relevant to the project.
