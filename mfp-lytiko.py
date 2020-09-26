import requests
import myfitnesspal
import kirjava
import pytz
from datetime import datetime, date, time, timezone
from secrets import LYTIKO_USERNAME, LYTIKO_PASSWORD, USERNAME, PASSWORD, CALORIES_ID, SUGAR_ID, WEIGHT_ID, CARBOHYDRATES_ID, FAT_ID, PROTEIN_ID, SODIUM_ID



DATE = int(datetime.now().timestamp())
today = date.today()
dt = int(datetime.now().timestamp())
print('dt: ', dt)
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
print(totals)
nutrients_mutation = """
    mutation {createMeal(
        rawCalories: """ + str(int(totals['calories'])) +""",
        rawCarbohydrates: """ + str(int(totals['carbohydrates'])) +""",
        rawFat: """ + str(int(totals['fat'])) +""",
        rawProtein: """ + str(int(totals['protein'])) +""",
        rawSugar: """ + str(int(totals['sugar'])) +""",
        rawSalt: """ + str(int(totals['sodium'])) +""",
        components: [],
        timezone: "Europe/London",
        datetime:"""+ str(dt) + """
    )
    { meal {id}}
    }
"""
print(nutrients_mutation)

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

login_mutation = """
    mutation {login(
            email: """ + '"' + LYTIKO_USERNAME + '"' + """, 
            password: """ + '"' + LYTIKO_PASSWORD + '"' + """
        ) 
        { token } 
        }
"""
lytiko_url = "https://api.lytiko.com/graphql"
token = (kirjava.execute(lytiko_url, login_mutation))
token = token['data']['login']['token']
print(kirjava.execute(lytiko_url, nutrients_mutation, headers={"Authorization": f"{token}"}))
