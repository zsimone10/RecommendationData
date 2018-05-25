# RecommendationData
Get static data for initial wellness bot recommendation.
---------------------------------------------------------
active code in send_message:

resp = requests.get("https://graph.facebook.com/v2.6/{}?fields=first_name,last_name,locale,gender,last_ad_referral,profile_pic&access_token={}".format(recipient_id, ACCESS_TOKEN))
data = resp.json()
print data

setup notes for rerunning:
-start flask
-start ngrok
-copy ngrok address on the second forwarding line
-go to webhooks page for app and paste into address and enter "testtest"
  in the token field
-go back to the main settings fb page and copy token
-paste into code and save
-restart Flask
-should be good to go !
