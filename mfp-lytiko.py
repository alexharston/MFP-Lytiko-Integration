import requests
import myfitnesspal
import kirjava
import pytz
from datetime import datetime, date, time, timezone, timedelta
from secrets import LYTIKO_USERNAME, LYTIKO_PASSWORD, USERNAME, PASSWORD, WEIGHT_ID

today = date.today()
yesterday = datetime.today() -timedelta(days=1)
yesterday_breakfast = int(datetime(yesterday.year, yesterday.month, yesterday.day, 9, 0, 0 ).timestamp())
yesterday_lunch = int(datetime(yesterday.year, yesterday.month, yesterday.day, 13, 0, 0 ).timestamp())
yesterday_snacks = int(datetime(yesterday.year, yesterday.month, yesterday.day, 16, 0, 0 ).timestamp())
yesterday_dinner = int(datetime(yesterday.year, yesterday.month, yesterday.day, 19, 0, 0 ).timestamp())

dt = int(datetime.now().timestamp())
#connect to MyFitnessPal with credentials
client = myfitnesspal.Client(username=USERNAME, password=PASSWORD)

#get today's information
day = client.get_date(yesterday.year, yesterday.month, yesterday.day)
print('DAY', day)

#collect data from MFP API
breakfast = day.meals[0]
lunch = day.meals[1]
dinner = day.meals[2]
snacks = day.meals[3]
print('B', breakfast)
print('L', lunch)
print('D', dinner)
print('S', snacks)

#weight = list(client.get_measurements('Weight').items())[-1][1]

breakfast_mutation = """
    mutation {createMeal(
        rawCalories: """ + str(int(breakfast.totals['calories'] if breakfast else 0)) +""",
        rawCarbohydrates: """ + str(int(breakfast.totals['carbohydrates'] if breakfast else 0)) +""",
        rawFat: """ + str(int(breakfast.totals['fat'] if breakfast else 0)) +""",
        rawProtein: """ + str(int(breakfast.totals['protein'] if breakfast else 0)) +""",
        rawSugar: """ + str(int(breakfast.totals['sugar'] if breakfast else 0)) +""",
        rawSalt: """ + str(int(breakfast.totals['sodium'] if breakfast else 0)) +""",
        components: [],
        timezone: "Europe/London",
        datetime:""" + str(yesterday_breakfast) + """
    )
    { meal {id}}
    }
"""
print(breakfast_mutation)

lunch_mutation = """
    mutation {createMeal(
        rawCalories: """ + str(int(lunch.totals['calories'] if lunch else 0)) +""",
        rawCarbohydrates: """ + str(int(lunch.totals['carbohydrates'] if lunch else 0)) +""",
        rawFat: """ + str(int(lunch.totals['fat'] if lunch else 0)) +""",
        rawProtein: """ + str(int(lunch.totals['protein'] if lunch else 0)) +""",
        rawSugar: """ + str(int(lunch.totals['sugar'] if lunch else 0)) +""",
        rawSalt: """ + str(int(lunch.totals['sodium'] if lunch else 0)) +""",
        components: [],
        timezone: "Europe/London",
        datetime:""" + str(yesterday_lunch) + """
    )
    { meal {id}}
    }
"""
print(lunch_mutation)

dinner_mutation = """
    mutation {createMeal(
        rawCalories: """ + str(int(dinner.totals['calories'] if dinner else 0)) +""",
        rawCarbohydrates: """ + str(int(dinner.totals['carbohydrates'] if dinner else 0)) +""",
        rawFat: """ + str(int(dinner.totals['fat'] if dinner else 0)) +""",
        rawProtein: """ + str(int(dinner.totals['protein'] if dinner else 0)) +""",
        rawSugar: """ + str(int(dinner.totals['sugar'] if dinner else 0)) +""",
        rawSalt: """ + str(int(dinner.totals['sodium'] if dinner else 0)) +""",
        components: [],
        timezone: "Europe/London",
        datetime:""" + str(yesterday_dinner) + """
    )
    { meal {id}}
    }
"""
print(dinner_mutation)

snacks_mutation = """
    mutation {createMeal(
        rawCalories: """ + str(int(snacks.totals['calories'] if snacks else 0)) +""",
        rawCarbohydrates: """ + str(int(snacks.totals['carbohydrates'] if snacks else 0)) +""",
        rawFat: """ + str(int(snacks.totals['fat'] if snacks else 0)) +""",
        rawProtein: """ + str(int(snacks.totals['protein'] if snacks else 0)) +""",
        rawSugar: """ + str(int(snacks.totals['sugar'] if snacks else 0)) +""",
        rawSalt: """ + str(int(snacks.totals['sodium'] if snacks else 0)) +""",
        components: [],
        timezone: "Europe/London",
        datetime:""" + str(yesterday_snacks) + """
    )
    { meal {id}}
    }
"""
print(snacks_mutation)


#weight_mutation = """
#    mutation {createMeasurement(
#        quantity: """ + WEIGHT_ID + """,
#        value:""" + str(weight) + """,
#        timezone: "Europe/London",
#        datetime:"""+ str(dt) + """
#    )
#    { measurement {id}}
#    }
#"""

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
print(kirjava.execute(lytiko_url, breakfast_mutation, headers={"Authorization": f"{token}"}))
print(kirjava.execute(lytiko_url, lunch_mutation, headers={"Authorization": f"{token}"}))
print(kirjava.execute(lytiko_url, dinner_mutation, headers={"Authorization": f"{token}"}))
print(kirjava.execute(lytiko_url, snacks_mutation, headers={"Authorization": f"{token}"}))
