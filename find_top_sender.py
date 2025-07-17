import mailbox
from collections import Counter
from email.header import decode_header
from email.utils import parseaddr

def decode_sender(header):
    if not header:
        return "Unknown"
    decoded_parts = decode_header(header)
    decoded_str = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                decoded_str += part.decode(encoding or 'utf-8', errors='replace')
            except Exception:
                decoded_str += part.decode('utf-8', errors='replace')
        else:
            decoded_str += part
    return parseaddr(decoded_str)[1]  # extract just the email

# Load MBOX
mbox = mailbox.mbox('CategoryUpdates.mbox')

senders = Counter()

for message in mbox:
    try:
        raw_sender = message['from']
        sender = decode_sender(raw_sender)
        senders[sender] += 1
    except Exception as e:
        print(f"Error processing message: {e}")

# Print top 10 senders
for sender, count in senders.most_common(10):
    print(f"{sender}: {count}")
