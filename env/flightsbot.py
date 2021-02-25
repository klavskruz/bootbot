from flask import Flask, request, make_response, jsonify
import requests

app = Flask(__name__)

airport_codes = {
    "Riga":"RIX",
    "Barcelona":"BCN",
    "London":"LGW",
    "Paris":"CDG",
    "Beijing":"BJS"

    }


@app.route('/flights')
def flights():
    data = request.json
    from_city = data['queryResult']['parameters']['city_one']
    to_city = data['queryResult']['parameters']['city_two']
    price =  get_flight_price(airport_codes[from_city],airport_codes[to_city],"2021-03-03")
    response = {'fulfillmentText':f'{price}'}
    response_json = jsonify(response)
    ## send incoming data and response to third party analytics service
    return make_response(response_json)


def get_flight_price(to_city, from_city, date):


    url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/{from_city}-sky/{to_city}-sky/{date}"

    querystring = {"inboundpartialdate":"2019-12-01"}

    headers = {
    'x-rapidapi-key': "bf7aa826admsh914e2032ba16661p12d507jsnd32e0f8f48a5",
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = response.json()
    return str(response_json['Quotes'][0]['MinPrice'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)