# Get API license key at www.interzoid.com/register-api-account - free trial credits
import requests

def get_key(license,fullname):
    response = requests.get('https://api.interzoid.com/getfullnamematch?license='
                            +license+'&fullname='+fullname)
    if response.status_code == 200:
        data = response.json()
        sim_key = (data["SimKey"])
        credits = (data["Credits"])
    else:
        sim_key = ""
        credits = "0"

    return sim_key, credits, response.status_code, response.reason

