import json
import requests


def lambda_handler(event, context):
    
    postcode = ''.join(event['rawQueryString'].split('=')[1])
    
    # Using the postcodes.io API to get the parliamentary constituency data for any postcode parsed
    
    url = 'https://api.postcodes.io/postcodes/{}/'.format(postcode)
    
    res = requests.get(url)
    con_data = json.loads(res.content)
    
    # if con_data["status"] != 200:
    #     return con_data.json()

    constituency = con_data['result']['parliamentary_constituency']
    longitude = con_data['result']['longitude']
    latitude = con_data['result']['latitude']

    # Using the postcodes.io API and parsing the longitude and latitude to gather a list of nearby postcodes
    
    npc_url = "https://api.postcodes.io/postcodes?lon={}&lat={}/".format(longitude, latitude)

    res1 = requests.get(npc_url)
    npc_data = json.loads(res1.content)
    nearby_pc = []

    for results in npc_data['result']:
        nearby_pc.append(results['postcode'])

    # Latest planning permission records within a 2 mile radius of the search postcode
    
    try:
        plan_perm_url = 'https://www.planit.org.uk/api/applics/json?lat={}&lng={}&krad=5.0&recent=30&pg_sz=5&sort=-start_date&compress=on/'.format(
            longitude, latitude)

        res2 = requests.get(plan_perm_url)
        plan_perm_data = json.loads(res2.content)

        latest_plan_perm = plan_perm_data['result']['records']

    except KeyError:
        latest_plan_perm = None

    # Using the data police API to get lastest 10 crimes based on the longitude and latitude
    
    # crimes_url = 'https://data.police.uk/api/crimes-street/all-crime?lat={}&lng={}&limit=10'.format(latitude, longitude)

    # crime_stats = []

    # res3 = requests.get(crimes_url).json()
                
    # for crime in res3:
    #     category = crime['category']
    #     area = crime['location']['street']['name']
    #     outcome = None
    #     if crime['outcome_status']:
    #         outcome = crime['outcome_status']['category']

    #     crime_stats.append((category, area, outcome, postcode))
    
    crimes_url = 'https://data.police.uk/api/crimes-street/all-crime?lat={}&lng={}&limit=10'.format(latitude, longitude)
    res3 = requests.get(crimes_url)
    crime_data = json.loads(res3.content)

    crime_stats = []
    
    if crime_data:
        for index, item in enumerate(crime_data):
            if index < 10:
                category = item['category']
                area = item['location']['street']['name']
                outcome = None
                if item['outcome_status']:
                    outcome = item['outcome_status']['category']
            crime_stats.append((category, area, outcome))
                    
    
    body = {
        'parliamentary_constituency': constituency,
        'nearby_postcodes': nearby_pc,
        'crime_stats': crime_stats,
        'plan_perm': latest_plan_perm
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

