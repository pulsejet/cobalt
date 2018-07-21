import smtplib
from email.mime.text import MIMEText

"""
# ===========================================================================

TEMPLATE_FILE = 'datelaunch.html'
DATA_FILE = 'cldata.csv'
SLEEP_TIME = 2
FROM_ADDRESS = 'Himank Jain <himank@moodi.org>'
SIGN_FILE = 'sign.html'
SUBJECT = 'Dates for Mood Indigo 2018 are out!'

# ===========================================================================

def blast_merge():
        reader = csv.DictReader(open(DATA_FILE))

        with open(TEMPLATE_FILE, 'r') as file:
                template = file.read()

        with open(SIGN_FILE, 'r') as file:
                sign = file.read()

        template = template.replace('{{sign}}', sign)

        rows = [row for row in reader]

        for row in tqdm(rows):
                body = str(template)

                tqdm.write('Sending e-mail to' + ' ' + row['name'] + ' ' + row['email'])

                for col in row:
                        body = body.replace('{{' + col + '}}', row[col])

                time.sleep(SLEEP_TIME)

                sendmail(body, FROM_ADDRESS, row['email'], SUBJECT)
"""

def sendmail(body, addr_from, addr_to, subject):
    msg = MIMEText(body, 'html')

    msg['Subject'] = subject
    msg['From'] = addr_from
    msg['To'] = addr_to

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(addr_from, [addr_to], msg.as_string())
    s.quit()
