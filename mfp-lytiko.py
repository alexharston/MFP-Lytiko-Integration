import requests
import myfitnesspal
import kirjava
import pytz
from datetime import datetime, date, time, timezone
from secrets import LYTIKO_USERNAME, LYTIKO_PASSWORD, USERNAME, PASSWORD, CALORIES_ID, SUGAR_ID, WEIGHT_ID, CARBOHYDRATES_ID, FAT_ID, PROTEIN_ID, SODIUM_ID



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

carbohydrates_mutation = """
    mutation {createMeasurement(
        quantity: """ + CARBOHYDRATES_ID + """,
        value:""" + str(int(totals['carbohydrates'])) + """,
        timezone: "Europe/London",
        datetime:"""+ str(dt) + """
    )
    { measurement {id}}
    }
"""

fat_mutation = """
    mutation {createMeasurement(
        quantity: """ + FAT_ID + """,
        value:""" + str(int(totals['fat'])) + """,
        timezone: "Europe/London",
        datetime:"""+ str(dt) + """
    )
    { measurement {id}}
    }
"""

protein_mutation = """
    mutation {createMeasurement(
        quantity: """ + PROTEIN_ID + """,
        value:""" + str(int(totals['protein'])) + """,
        timezone: "Europe/London",
        datetime:"""+ str(dt) + """
    )
    { measurement {id}}
    }
"""

sodium_mutation = """
    mutation {createMeasurement(
        quantity: """ + SODIUM_ID + """,
        value:""" + str(int(totals['sodium'])) + """,
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
print(kirjava.execute(lytiko_url, calories_mutation, headers={"Authorization": f"{token}"}))
print(kirjava.execute(lytiko_url, sugar_mutation, headers={"Authorization": f"{token}"}))
print(kirjava.execute(lytiko_url, weight_mutation, headers={"Authorization": f"{token}"}))
print(kirjava.execute(lytiko_url, carbohydrates_mutation, headers={"Authorization": f"{token}"}))
print(kirjava.execute(lytiko_url, fat_mutation, headers={"Authorization": f"{token}"}))
print(kirjava.execute(lytiko_url, protein_mutation, headers={"Authorization": f"{token}"}))
print(kirjava.execute(lytiko_url, sodium_mutation, headers={"Authorization": f"{token}"}))
