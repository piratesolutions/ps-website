from settings import *
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flaskext.csrf import csrf
import re, os

""" 
	piratesolutions.org static website
	(C) 2011 piratesolutions
	
	@requires Flask
	@requires flask-csrf
	==================================
"""

# configuration: see settings.py

# application
app = Flask(__name__)
app.config.from_object(__name__)
csrf(app)

# sendmail implementation
def sendmail(e_from, e_to, subject, body):
	print "Hi!"
	p = os.popen("%s -t" % SENDMAIL, "w")
	p.write("From: %s\n" % e_from)
	p.write("To: %s\n" % e_to)
	p.write("Subject: %s\n" % subject)
	p.write("Content-Transfer-Encoding: 8bit\n")
	p.write("\n") # blank line separating headers from body
	p.write("Query from %s\n\n%s" % (request.remote_addr, body.encode("utf-8")))
	status = p.close()
	if status != 0:
		return True
	return False

# default route
@app.route('/')
def default():
	return render_template('default.html', p_current = PORTFOLIO_CURRENT, p_past = PORTFOLIO_PAST)
	
# contact form route
@app.route('/contact/', methods=['POST'])
def contact():
	email = request.form['email']
	text = request.form['text']
	
	print email
	
	if not re.match('^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', email) or unicode(email) == u'your@email.com' or unicode(text) == 'You are so cool!' or len(text) < 10:
		return render_template('error.html', message='The data you submitted is not valid. Please check your email address and your message!')
	else:
		try:
			sendmail(email, CONTACT_EMAIL, u'Kontaktanfrage', '%s' % unicode(text))
		except:
			raise
			return render_template('error.html', message='Unfortunately, the mail server does not want to accept your message. Sorry for that. Please try sending your query to info@piratesolutions.org. Thank you very much!')
	
	return render_template('thanks.html')

if __name__ == '__main__':
	app.run()
