# Get API license key at www.interzoid.com/register-api-account - free trial credits
import requests

def get_score(license,fullname1,fullname2):
    response = requests.get('https://api.interzoid.com/getfullnamematchscore?license='
                            +license+'&fullname1='+fullname1+'&fullname2='+fullname2)
    if response.status_code == 200:
        data = response.json()
        score = (data["Score"])
        credits = (data["Credits"])
    else:
        score = "0"
        credits = "0"

    return score, credits, response.status_code, response.reason