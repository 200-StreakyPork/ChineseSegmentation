

emails = []


def set_email(title, addresser, addressee, copy, doc, split):
    email = {
        "title": title,
        "from": addresser,
        "to": addressee,
        "cc": copy,
        "doc": doc,
        "split": split
    }
    return email


def set_emails(email_list):
    emails.clear()
    for new_email in email_list:
        emails.append(new_email)
    return emails


def add_emails(email_list):
    for new_email in email_list:
        emails.append(new_email)
    return emails
