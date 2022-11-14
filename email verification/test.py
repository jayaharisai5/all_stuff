import smtplib
from email.mime.text import MIMEText

# Define to/from
sender = 'jayaharisai1212@zohomail.in'
recipient = 'nojah83793@harcity.com'

# Create message
msg = MIMEText("Hay this is test mail")
msg['Subject'] = "Sent from python"
msg['From'] = sender
msg['To'] = recipient

# Create server object with SSL option
server = smtplib.SMTP_SSL('smtp.zoho.in', 465)

# Perform operations via server
server.login('jayaharisai1212@zohomail.in', 'Jayaharisai@123')
server.sendmail(sender, [recipient], msg.as_string())
server.quit()