#!/usr/bin/python

import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import urllib, urllib2


# details of account from which to send reports from
email_report = 'your_email@gmail.com'
password_report = 'your_password'

# list of account(s) which will receive reports
email_receipients = ['friend1@gmail.com','friend2@yahoo.com','friend3@hotmail.com']

# details for logging into Next restaurant website
email_next = 'your_next_email'
password_next = 'your_next_password'


# wrapper for sending emails
def mail(to,subject,text):
	msg=MIMEMultipart()

	msg['From']=email_report
	msg['To']=to
	msg['Subject']=subject

	msg.attach(MIMEText(text))

	mailServer=smtplib.SMTP('smtp.gmail.com',587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(email_report,password_report)
	mailServer.sendmail(email_report,to,msg.as_string())
	mailServer.close()


# log into Next restaurant website
nexturl='https://www.nextrestaurant.com/user/login'
params=urllib.urlencode(dict(email=email_next,password=password_next))
# cookies required to maintain logged-in state
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor())
urllib2.install_opener(opener)

# n is the number of times the website will be checked
# 6 * 48 ensures website is monitored for 48 hours
n = 6 * 48
for i in range(n):
	response=opener.open(nexturl,params)
	response2=urllib2.urlopen('https://www.nextrestaurant.com/slots/find')
	
	# when no tickets are available, user is redirected to no_purchasing website
	# otherwise, booking page is available
	if response2.geturl()!='https://www.nextrestaurant.com/website/no_purchasing':
		for email in email_receipients:
			mail(email,'NEXT Restaurant Script','Tickets likely to be available. Log-in to www.nextrestaurant.com/user/login to purchase tickets.' )
		break

	# send notifications that script has successfully begun	
	if i==1:	# message sent after 10 minutes
		for email in email_receipients:
			mail(email,'NEXT Restaurant Script','NEXT Restaurant script successfully activated.')

	# sleep for 600 seconds
	time.sleep(600)


# send notification that script has completed
for email in email_receipients:
	mail(email,'NEXT Restaurant Script', 'Reporting Period Over. Restart if necessary.')
