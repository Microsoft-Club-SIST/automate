# Built-In Libraries/Modules/Packages
import smtplib
import ssl

# Third Party Libraries/Modules/Packages
import pandas as pd
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def read_template(filename) -> str:
    """
    Reads a file completely and returns it as a string.
    """
    filehandle = open(filename, 'r')
    content = filehandle.read()
    filehandle.close()
    return content


def file_object(file_name):
    try:
        with open(file_name, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file_name}",
        )

        return part
    except Exception as e:
        print(f'Oh no! We didnt found the attachment!n{e}')
        exit()


sender_email = "your gmail address"
sender_name = "your Name"
password = ""

name_of_the_event = input("Name of the event: ")
mail_sub = input("Subject of the mail: ")
link_of_the_recording = input("Recording link: ")
link_of_google_form = input("Club join form link: ")

e = pd.read_csv("details.csv")
receiver_emails = e["EmailAddress"].values
receiver_names = e["Name"].values
certificate_links = e["certificates"].values

for receiver_email, receiver_name, certificate_link in zip(receiver_emails, receiver_names, certificate_links):
    print("Sending to " + receiver_name)
    msg = MIMEMultipart()
    msg['Subject'] = mail_sub + \
        receiver_name + "!!"
    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = formataddr((receiver_name, receiver_email))
    mail_content = read_template('confirmation.html')
    mail_content = mail_content.replace('{reciever_name}', receiver_name)
    mail_content = mail_content.replace('{event_name}', name_of_the_event)
    mail_content = mail_content.replace('{rec_link}', link_of_the_recording)
    mail_content = mail_content.replace('{cert_link}', certificate_link)
    mail_content = mail_content.replace('{join_link}', link_of_google_form)
    msg.attach(MIMEText(mail_content, 'html'))

    # filename = "file.pdf"
    # msg.attach(file_object(filename))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent!')
    except Exception as e:
        print(f'Oh no! Something bad happened!n{e}')
        break
    finally:
        print('Closing the server...')
        server.quit()
