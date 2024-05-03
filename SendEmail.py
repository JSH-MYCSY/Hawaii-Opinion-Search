import smtplib, csv, os
from email.mime.text import MIMEText
from datetime import datetime, timezone, timedelta

# setting up some variables to use in the email function below.
subject = "Humane Society Update"
body = ""
sender = "joshua.automated.emails@gmail.com"
recipients = [sender, "caseyjos@hawaii.edu"]
password = os.environ['EMAIL_PASSCODE']

# opens up the court opinions csv.
with open("CourtOpinion_Hawaii_New.csv", "r", encoding="utf-8") as file:
    read = csv.reader(file)
    for row in read:
        try: # this tries to pull out only the cases that were added in the past year.
            if(datetime.strptime(row[2],'%Y-%m-%d %H:%M:%S') > (datetime.now(tz=timezone(-timedelta(hours=10))) - timedelta(days=6))):
                titleTemp = str(row[1]).split("/")[-1]
                title = titleTemp.split(".")[0]
                with open("courtOpinionText/" + title + ".txt", "r", encoding="utf-8") as txtObj:
                    if("estate" in txtObj.read().lower()):
                        body = body + str(row[0]) + ", " + str(row[1]) +", " + str(row[3]) + ";\n"
                txtObj.close()
        except:
            continue

# the email sending function.
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Done.")

if(body): # if there is anything in the body, then it will send me an email, otherwise it won't.
    send_email(subject, body, sender, recipients, password)
else:
    print("No Updates")