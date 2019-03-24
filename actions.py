from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet, UserUtteranceReverted
import zomatopy
import json
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.agent import Agent
import pandas as pd

class ActionSendEmail(Action):
    def name(self):
        return 'action_send_email'

    def run(self, dispatcher, tracker, domain):
            send_email='yes'
            if ( (tracker.get_slot('email_needed') is not None) and (tracker.get_slot('email_needed').strip() is not '')):
                send_email = tracker.get_slot('email_needed').strip()
            if (send_email == 'yes'):
                print("In here!!")
                receiver_address = tracker.get_slot('email')
                mail_content = tracker.get_slot('email_content')
                dispatcher.utter_message('Sending email to '+ receiver_address)
                sender_address = 'dummy.upgrad@gmail.com'
                sender_pass = '!Qaz2wsx'
                # add in the message body
                msg = MIMEMultipart()
                msg['From'] = sender_address
                msg['To'] = receiver_address
                msg['Subject'] = "Chat Bot Message with list of resturants"
                #The body and the attachments for the mail
                msg.attach(MIMEText(mail_content, 'plain'))
                try:
                    #Create SMTP session for sending the mail
                    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
                    session.starttls() #enable security
                    session.login(sender_address, sender_pass) #login with mail_id and password
                    text = msg.as_string()
                    session.sendmail(sender_address, receiver_address, text)
                    print('Mail Sent')
                except Exception as e:
                    # Print any error messages to stdout
                    print(e)
                finally:
                    session.quit()
                    dispatcher.utter_message("-----" + 'Email sent')



class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'

	def run(self, dispatcher, tracker, domain):
		config={ "user_key":"6ce88a5ec1419e335afa1c7f92f4b739"}
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget = tracker.get_slot('budget')
		resturant_result = pd.DataFrame(columns=['id','name', 'address', 'rating', 'avg_price'])
		print("{} {} {}".format(loc,cuisine,budget))
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={'bakery':5,'chinese':25,'cafe':30,'italian':55,'biryani':7,'north indian':50,'south indian':85}
		if(budget == "business"):
			sort_order="desc"
		elif(budget == "luxury"):
			sort_order = "desc"
		else:
			sort_order = "asc"
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 1000, sort_order)

		d = json.loads(results)
		response=""
		if d['results_found'] == 0:
			response= "no results"
		else:
			for restaurant in d['restaurants']:
				#response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+"\n"
				resturant_result.loc[len(resturant_result)] = [restaurant['restaurant']['id'], restaurant['restaurant']['name'], restaurant['restaurant']['location']['address'], restaurant['restaurant']['user_rating']['aggregate_rating'], restaurant['restaurant']['average_cost_for_two']]

		sort_by_rating = resturant_result.sort_values('rating', ascending=False)
		if (budget == "business"):
			sort_by_rating = sort_by_rating[sort_by_rating["avg_price"] > 700]
		elif (budget == "luxury"):
			sort_by_rating = sort_by_rating[(sort_by_rating["avg_price"] > 300) & (sort_by_rating["avg_price"] < 700)]
		elif(budget == "economy"):
			sort_by_rating = sort_by_rating[sort_by_rating["avg_price"] < 300]

		sort_by_rating = sort_by_rating.head()
		for index, row in sort_by_rating.iterrows():
			print("{} in {} has been rated {}".format(row['name'], row['address'], row['rating']))

		email_response = "List of top rated restaurants: \n"
		chat_response = "Showing you top rated restaurants: \n"

		for i in sort_by_rating.index:
			email_response = email_response + "Restaurant " + sort_by_rating.loc[i,'name'] + " in "+ sort_by_rating.loc[i,'address'] + "And the average price for two people here is: " + str(sort_by_rating.loc[i,'avg_price']) + " Rs. And has been rating is: " + sort_by_rating.loc[i,'rating'] + "\n"
			if i < 5:
				chat_response = chat_response + "Restaurant " + sort_by_rating.loc[i,'name'] + " in "+ sort_by_rating.loc[i,'address'] + "And the average price for two people here is: " + str(sort_by_rating.loc[i,'avg_price']) + " Rs. And has been rating is: " + sort_by_rating.loc[i,'rating'] + "\n"

		dispatcher.utter_message("-----"+response)
		return [SlotSet('location',loc),SlotSet('email_content', email_response)]
