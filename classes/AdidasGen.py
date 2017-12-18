import time, random, string, os, sys, threading
from bs4 import BeautifulSoup
from colorama import *
init()
from GmailDotGen import GmailDotEmailGenerator
from random import getrandbits


class AccountGEN:
	active_threads = 0
	captchas_sent = 0
	def __init__(self, s, config, proxies):
		self.s = s
		self.config = config
		self.proxies = proxies

	def log(self, msg, Color = ""):
		currenttime = time.strftime("%H:%M:%S")
		sys.stdout.write("[%s]%s %s\n" % (currenttime,Color, str(msg) + Style.RESET_ALL))
		sys.stdout.flush()

	def AccountCheck(self, response):
		try:
			return True if (BeautifulSoup(response.text, "html.parser").find('input', {'name': 'username'})['value'] != "") else False
		except:
			return False

	def POST(self, s, URL, payload = ""):
		proxy = random.choice(self.proxies)
		resp   = s.post(URL,data=payload,proxies={'http:': 'http://' + proxy})

		if self.AccountCheck(resp):
			return True

		elif not self.AccountCheck(resp):
			return False


	def beginHarvest(self, s, data, region, NumberofAccounts):
		Email = data['INFO']['Email']
		createTotal = 0;
		createMode = data['createMode']
		if createMode == "gmail":
			for email in (GmailDotEmailGenerator(Email).generate())[:NumberofAccounts]:
				t = threading.Thread(target=self.get_token_from_2captcha, args=(s,data,region,email))
				t.daemon = True
				t.start()
				time.sleep(0.1)
				createTotal+=1
			print('Requested ' + str(createTotal) + ' captcha(s).')

		if createMode == "catchall":
			domain = data['domain']
			base_email = data['base_email']
			for x in range(NumberofAccounts):
				email = (base_email + "{}" + domain).format(getrandbits(40))
				t = threading.Thread(target=self.get_token_from_2captcha, args=(s,data,region,email))
				t.daemon = True
				t.start()
				time.sleep(0.1)
				createTotal+=1
			print('Requested ' + str(createTotal) + ' captcha(s).')

		while not self.active_threads == 0:
			print('-------------------------')
			print('Active Threads          -', self.active_threads)
			print('Captchas Collected  -', self.captchas_sent)
			time.sleep(5)

	def createAccount(self, s, data, region, token, email):
		if region == "US":
			self.US(s,data,token,email)
		#TODO move along

	def US(self, s, data, token, email):
		RandPass    = False
		error       = Fore.RED
		success     = Fore.GREEN
		info        = Fore.BLUE
		FirstName   = data['INFO']['First_Name']
		LastName    = data['INFO']['Last_Name']
		Month       = data['INFO']['Month']
		Day         = data['INFO']['Day']
		Year        = data['INFO']['Year']
		Email       = email
		Password    = data['INFO']['Password']


		if Password  == "":
			RandPass = True


		self.log("-------------------------------",info)
		self.log('ADIDAS US | Generator',success)
		self.log("First Name: %s" % (FirstName))
		self.log("Last Name: %s"  % (LastName))
		self.log("Date Of Birth: {Month: %s} {Day: %s} {Year: %s} " % (Month,Day,Year))
		self.log("Using Email: %s" % (Email.split("@")[0]))
		self.log('Password Usage: %s' % (Password if Password != '' else "Random Passwords"))
		self.log("-------------------------------",info)

		headers = {
						  'User-Agent'               : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
						  'Accept-Encoding'          : 'gzip, deflate, sdch, br',
						  'Accept-Language'          : 'en-US,en;q=0.8',
						  'Upgrade-Insecure-Requests': '1'
				}

		s.headers.update(headers)
		try:
			GETCSRF      = s.get('https://cp.adidas.com/web/eCom/en_US/loadcreateaccount')
			CSRF         = BeautifulSoup(GETCSRF.text, "html.parser").find('input', {'name': 'CSRFToken'})['value']
		except:
			self.log("Could not grab Token! Possible you're Banned!")
		s.headers.update({
						  'Origin' : 'https://cp.adidas.com',
						  'Referer': 'https://cp.adidas.com/web/eCom/en_US/loadcreateaccount'})
		if RandPass:
			length      = 13
			chars       = string.ascii_letters + string.digits + '$&@?!#%'
			random.seed = (os.urandom(1024))
			Password    = ''.join(random.choice(chars) for i in range(length))

		POSTDATA     =   {
			'firstName'                                     : FirstName,
			'lastName'                                      : LastName,
			'minAgeCheck'                                   : 'true',
			'_minAgeCheck'                                  : 'on',
			'email'                                         : email,
			'password'                                      : Password,
			'confirmPassword'                               : Password,
			'amf'                                           : 'on',
			'_amf'                                          : 'on',
			'terms'                                         : 'true',
			'_terms'                                        : 'on',
			'g-recaptcha-response'                          : token,
			'metaAttrs[pageLoadedEarlier]'                  : 'true',
			'app'                                           : 'eCom',
			'locale'                                        : 'en_US',
			'domain'                                        : '',
			'consentData1'                                  : 'Sign me up for adidas emails, featuring exclusive offers, featuring latest product info, news about upcoming events, and more. See our <a target="_blank" href="https://www.adidas.com/us/help-topics-privacy_policy.html">Policy Policy</a> for details.',
			'consentData2'                                  : '',
			'consentData3'                                  : '',
			'CSRFToken'                                     : CSRF
		}

		URL           = 'https://cp.adidas.com/web/eCom/en_US/accountcreate'
		AccountStatus = self.POST(s, URL, payload=POSTDATA)

		if AccountStatus:
			self.log("Account Created Successfully! Email: %s. Password: %s" % (email,Password),success)
			self.active_threads -= 1
			self.captchas_sent += 1
			with open('accounts' + '.txt', 'a') as f:
				f.write('%s:%s \n' % (email,Password))
				f.close()
			Sleep = (random.randint(2, 10))
			self.log("Sleeping for %d seconds" % (Sleep),info)
			time.sleep(Sleep)


		if not AccountStatus:
			self.log("Account could not be created! Email: %s. Password: %s" % (email,Password),error)
			self.active_threads -= 1
			self.captchas_sent += 1

		s.cookies.clear()


	def get_token_from_2captcha(self, session, create_data, region, email):
		"""
		All credit here to https://twitter.com/solemartyr, just stole this from his script
		"""


		self.active_threads += 1

		apikey = create_data["APIKEY_2CAP"]
		sitekey = create_data["sitekey"]
		session.verify = False
		session.cookies.clear()
		pageurl = "https://cp.adidas.com/"

		while True:
			data = {
				'key': apikey,
				'action': 'getbalance',
				'json': 1,
			}
			response = session.get(url='http://2captcha.com/res.php', params=data)
			if "ERROR_WRONG_USER_KEY" in response.text or "ERROR_KEY_DOES_NOT_EXIST" in response.text:
				print('Incorrect APIKEY, exiting.')
				exit()

			captchaid = None
			proceed = False
			while not proceed:
				data = {
					'key': apikey,
					'method': 'userrecaptcha',
					'googlekey': sitekey,
					'proxy': 'localhost',
					'proxytype': 'HTTP',
					'pageurl': pageurl,
					'json': 1
				}

				# if not len(proxies) == 0:
				#     # We will just pick randomly from the list because it doesn't matter if we use one more than others.
				#     data['proxy'] = random.choice(proxies)

				response = session.post(url='http://2captcha.com/in.php', data=data)
				try:
					json = response.json()
				except:
					time.sleep(3)
					continue

				if json['status'] == 1:
					captchaid = json['request']
					proceed = True
				else:
					time.sleep(3)
			time.sleep(3)

			token = None
			proceed = False
			while not proceed:
				data = {
					'key': apikey,
					'action': 'get',
					'json': 1,
					'id': captchaid,
				}
				response = session.get(url='http://2captcha.com/res.php', params=data)
				json = response.json()
				if json['status'] == 1:
					token = json['request']
					proceed = True
				else:
					time.sleep(3)

			if token is not None:
				self.createAccount(session, create_data, region, token, email)
				return



if __name__ == '__main__':
	print 'DO NOT RUN THIS FILE!!!!!'
	#exit()
