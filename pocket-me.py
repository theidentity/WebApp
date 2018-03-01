

#!/usr/bin/env python

import os,sys
from bottle import route, run, static_file, template, view
from bottle import get, post, request
import clips_terminal
from parse_output import get_dictionary

@route('/css/<filename>')
def img_static(filename):
	return static_file(filename, root='./static/css')

@route('/img/<filename>')
def img_static(filename):
	return static_file(filename, root='./static/img')

@route('/js/<filename>')
def js_static(filename):
	return static_file(filename, root='./static/js')


clips_process = clips_terminal.start()


@route("/")
@view("main")
def hello():
	global clips_process

	if request.method == "GET":
		print 'restarting clips...'
		clips_process = clips_terminal.restart(clips_process);

	while True:
		print "in the loop"
		# try:
		isQn,content = clips_terminal.getContent(clips_process)
		if isQn ==True:
			if 'Are you ready to start?' in content:
				content = 'Are you ready to start?'
			
			if '(Yes/No)' in content:
				return dict(question=content.replace('(Yes/No)','').replace('Your Choice: ',''), opt1="Yes", opt2="No Preference", opt3=None)
			elif '(1/2)' in content:
				return dict(question=content.replace('(1/2)','').replace('Your Choice: ',''), opt1="1", opt2="2", opt3=None)
			elif '(1/2/3)' in content:
				return dict(question=content.replace('(1/2/3)','').replace('Your Choice: ',''), opt1="1", opt2="2",opt3="3")
			elif 'start?' in content:
				return dict(title='Start?',user = 'Balu',question=content.replace('(1/2/3)','').replace('Your Choice: ',''), opt1="Start", opt2=None,opt3=None)
		
		elif isQn == False:
			content = content.replace('Your Choice: ','').replace('~EndOfResult!','Please restart to run the test again!!')
			clips_terminal.giveSuggestion(clips_process,content)
			clips_process.kill()
			clips_process = None
			print 'process killed'
			return show_expense(content)
				# return dict(title='We Recommend you to',question=content,opt1=None, opt2=None,opt3=None)		
		# except:
				# return dict(title='Something Went Wrong',question='Something went wrong! Please restart.',user = '',opt1=None, opt2=None,opt3=None)

@route('/',method="POST")
def recFacts():
	global clips_process
	global answer
	answer=""
	if request.forms.get("restart"):
		clips_process = clips_terminal.restart(clips_process);
	else:
		if request.forms.get("opt1"):
			answer = request.forms.get("opt1")
		elif request.forms.get("opt2"):
			answer =  request.forms.get("opt2")
		elif request.forms.get("opt3"):
			answer = request.forms.get("opt3")
		clips_terminal.giveAnswer(clips_process,answer)

	return hello()


@route("/expense")
@view("expense")
def show_expense(content):

	print(content)
	my_dict = get_dictionary(content)
	print my_dict

	my_dict = dict(
		total="1234",     
		sharing="yes",     
		house_type="condo",     
		location="Pasir Panjang",     
		monthly_housing = "456",     
		rent ="345",     
		pub="56",     
		food_type="nonn veg",     
		cooking_type = "always",     
		cooking_exp = "123",     
		mode="mrt",     
		total_travel="50",     
		fare_2_nus="20",     
		fare_2_others="30",     
		misc = "35"
	)
	my_dict['content'] = content

	print my_dict

	return my_dict

@route('/expense',method="POST")
def restart_from_expense():
	global clips_process
	global answer
	answer=""
	if request.forms.get("restart"):
		clips_process = clips_terminal.restart(clips_process);

	return hello()

# -------------------MAIN START----------------------------
if __name__ == "__main__":
	try:
		port = int(sys.argv[1])
	except:
		port = 5000
		
	port = int(os.environ.get("PORT", port))
	run(
	host='localhost',
	port=port,
	debug=True,
	reloader = True
	)
# -------------------MAIN END----------------------------