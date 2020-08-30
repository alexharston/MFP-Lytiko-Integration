import requests
import myfitnesspal
import kirjava
import pytz
from datetime import datetime, date, time, timezone
from secrets import LYTIKO_TOKEN, USERNAME, PASSWORD, CALORIES_ID, SUGAR_ID, WEIGHT_ID
# CALORIES_ID, CARBOHYDRATES_ID, FAT_ID, PROTEIN_ID, SODIUM_ID, SUGAR_ID, 


DATE = int(datetime.now().timestamp())
today = date.today()
dt = int(datetime(today.year, today.month, today.day, tzinfo=pytz.utc).timestamp())

#connect to MyFitnessPal with credentials
client = myfitnesspal.Client(username=USERNAME, password=PASSWORD)

#get today's information
day = client.get_date(today.year, today.month, today.day)

#collect data from MFP API
breakfast = day.meals[0]
lunch = day.meals[1]
dinner = day.meals[2]
snacks = day.meals[3]

totals = day.totals
weight = list(client.get_measurements('Weight').items())[-1][1]

calories_mutation = """
    mutation {createMeasurement(
        quantity: """ + CALORIES_ID + """,
        value:""" + str(int(totals['calories'])) + """,
        timezone: "Europe/London",
        datetime:"""+ str(dt) + """
    )
    { measurement {id}}
    }
"""

sugar_mutation = """
    mutation {createMeasurement(
        quantity: """ + SUGAR_ID + """,
        value:""" + str(int(totals['sugar'])) + """,
        timezone: "Europe/London",
        datetime:"""+ str(dt) + """
    )
    { measurement {id}}
    }
"""
weight_mutation = """
    mutation {createMeasurement(
        quantity: """ + WEIGHT_ID + """,
        value:""" + str(weight) + """,
        timezone: "Europe/London",
        datetime:"""+ str(DATE) + """
    )
    { measurement {id}}
    }
"""
lytiko_url = "https://api.lytiko.com/graphql"
print(kirjava.execute(lytiko_url, calories_mutation, headers={"Authorization": f"{LYTIKO_TOKEN}"}))
print(kirjava.execute(lytiko_url, sugar_mutation, headers={"Authorization": f"{LYTIKO_TOKEN}"}))
print(kirjava.execute(lytiko_url, weight_mutation, headers={"Authorization": f"{LYTIKO_TOKEN}"}))
# print(kirjava.execute(lytiko_url, carbohydrates_mutation, headers={"Authorization": f"{LYTIKO_TOKEN}"}))
# print(kirjava.execute(lytiko_url, fat_mutation, headers={"Authorization": f"{LYTIKO_TOKEN}"}))
# print(kirjava.execute(lytiko_url, protein_mutation, headers={"Authorization": f"{LYTIKO_TOKEN}"}))
# print(kirjava.execute(lytiko_url, sodium_mutation, headers={"Authorization": f"{LYTIKO_TOKEN}"}))
