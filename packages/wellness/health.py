from packages.internal.postbacks import mental_health_resources
import sys
sys.path.append("../interal")

  
def health_concern_msg(result):
  return mental_health_resources

def health_resources(payload):
	general_message = "Life at Columbia can be pretty rough at times. Here are some resources that can help.\n"
	if payload == 'stress':
		msg = "For stress and anxiety related issues, visit https://barnard.edu/counseling/resources/anxiety"
	elif payload == 'alcohol':
		msg = "For alcohol and drug related issues, visit https://barnard.edu/counseling/resources/alcohol"
	elif payload == 'wellness':
		msg = "For resources on health and wellness, visit http://universitylife.columbia.edu/student-life/health-wellness"
	elif payload == 'depression':
		msg = "For issues involving depression, visit https://barnard.edu/counseling/resources/depression"
	elif payload == 'LGBT':
		msg = "For help finding LGBT-specific resources, visit https://barnard.edu/counseling/resources/lgbt"
	elif payload == 'eating-disorders':
		msg = "For resources on dealing with eating disorders, visit https://barnard.edu/counseling/resources/eating-disorders"
	elif payload == 'suicide':
		msg = "For issues dealing with suicide, please visit https://barnard.edu/counseling/resources/suicide."
	elif payload == 'sleep':
		msg = "For sleep related issues, visit https://barnard.edu/counseling/resources/sleep"
	elif payload == 'sexual-assault':
		msg = "For issues involving sexual assault, please visit https://barnard.edu/counseling/resources/trauma or http://noredtapecu.org/immediate-hotlines"
	
	else:
		note = "Please remember that there is always help available. Check out these resources.\n"
		cps = "Columbia Psychological Services and After-Hours Emergency Help: (212) 854-2878"
		nightline = "Nightline Peer Listening: (212) 854-7777 from 10PM - 3AM"
		furman = "Rosemary Furman Counseling Center at Barnard (212) 854-2092"
		barnard_after_hours = "Barnard After-Hours Psychological Hotline (855) 622-1903"
		svr = "Columbia University Sexual Violence Response (212) 854-HELP"
		msg = note + cps + nightline + furman + barnard_after_hours + svr
	
	msg = general_message + msg
	return msg