import datetime
import swisseph
import calendar
from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv

from astro_utils import calculate_jd_utc, get_ecliptic_lon, get_zodiac_sign, get_lunar_metrics

load_dotenv()

app = Flask(__name__)

PLANET_IDS = [swisseph.SUN, swisseph.MOON, swisseph.MERCURY, swisseph.VENUS, swisseph.MARS, swisseph.JUPITER,
              swisseph.SATURN, swisseph.URANUS, swisseph.NEPTUNE, swisseph.PLUTO]

PLANET_NAME_SUN = 'sun'
PLANET_NAME_MOON = 'moon'
PLANET_NAME_MERCURY = 'mercury'
PLANET_NAME_VENUS = 'venus'
PLANET_NAME_MARS = 'mars'
PLANET_NAME_JUPITER = 'jupiter'
PLANET_NAME_SATURN = 'saturn'
PLANET_NAME_URANUS = 'uranus'
PLANET_NAME_NEPTUNE = 'neptune'
PLANET_NAME_PLUTO = 'pluto'

PLANET_NAMES = {
    swisseph.SUN: PLANET_NAME_SUN,
    swisseph.MOON: PLANET_NAME_MOON,
    swisseph.MERCURY: PLANET_NAME_MERCURY,
    swisseph.VENUS: PLANET_NAME_VENUS,
    swisseph.MARS: PLANET_NAME_MARS,
    swisseph.JUPITER: PLANET_NAME_JUPITER,
    swisseph.SATURN: PLANET_NAME_SATURN,
    swisseph.URANUS: PLANET_NAME_URANUS,
    swisseph.NEPTUNE: PLANET_NAME_NEPTUNE,
    swisseph.PLUTO: PLANET_NAME_PLUTO
}


def decimal_degrees_to_degrees_minutes(decimal_degrees):
    # Extract the integer part for degrees
    degrees = int(decimal_degrees)

    # Extract the fractional part and convert it to minutes
    full_minutes = (decimal_degrees - degrees) * 60
    minutes = int(full_minutes)

    # Extract the fractional part of the minutes to convert it to seconds
    seconds = int((full_minutes - minutes) * 60)

    return {'d': degrees, 'm': minutes, 's': seconds}


def get_house_number(cusps, longitude):
    house_num = 1  # Start from the first house
    for i in range(0, 12):
        if i < 11:
            if cusps[i - 1] <= longitude < cusps[i]:
                break
        else:
            return 12
        house_num += 1
    return house_num


def get_info(house_cusps, sign, degrees, longitude):
    return {'sign': sign, 'position': decimal_degrees_to_degrees_minutes(degrees),
            'house': get_house_number(house_cusps, longitude)}


@app.route("/v1/moon_metrics")
def get_moon_metrics():
    iso_date = request.args.get('date')
    date = datetime.datetime.fromisoformat(iso_date)
    _, num_days = calendar.monthrange(date.year, date.month)
    result = []
    date = datetime.date(date.year, date.month, 1)
    date = date - datetime.timedelta(days=7)
    # return full month plus previous and next week
    for day in range(0, num_days + 14):
        metrics = get_lunar_metrics(date)
        metrics['date'] = date.isoformat()
        result.append(metrics)
        date = date + datetime.timedelta(days=1)
    return jsonify(result)


@app.route("/v1/natal_chart")
def get_natal_chart():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    iso_date = request.args.get('date')

    date = datetime.datetime.fromisoformat(iso_date)
    lat = float(latitude)
    lon = float(longitude)

    today_date = datetime.datetime.today()

    jd, date_utc, new_date, timezone, gmt_shift = calculate_jd_utc(date, lat, lon)
    age_in_days = (today_date - date).days
    new_date_tz = new_date.astimezone(timezone)

    house_system = 'P'
    try:
        houses, ascmc = swisseph.houses(jd, lat, lon, house_system.encode('utf-8'))
    except:
        house_system = 'W'
        houses, ascmc = swisseph.houses(jd, lat, lon, house_system.encode('utf-8'))

    info = {
        'date': new_date_tz.isoformat(),
        'date_utc': date_utc.isoformat(),
        'jd': jd,
        'timezone': str(timezone),
        'gmt_shift': gmt_shift,
        'lat': lat,
        'lon': lon,
        'age_in_days': age_in_days,
        'house_system': house_system,
        'ascedant': ascmc[0],
        'midheaven': ascmc[1],
        'descendant': (ascmc[0] + 180) % 360,
        'ic': (ascmc[1] + 180) % 360
    }

    planets = {}
    for planet_id in PLANET_IDS:
        full_degree, speed = get_ecliptic_lon(planet_id, jd)
        normal_degree = full_degree % 30
        sign = get_zodiac_sign(full_degree)
        planets[PLANET_NAMES[planet_id]] = {
            'fd': full_degree,
            'nd': normal_degree,
            'speed': speed,
            'sign': sign,
            'house': get_house_number(houses, full_degree),
            'retro': speed < 0
        }

    houses_result = []
    num = 1
    for house in houses:
        sign = get_zodiac_sign(house)
        houses_result.append({
            'num': num,
            'sign': sign,
            'position': house
        })
        num += 1

    result = {'info': info,
              'planets': planets,
              'houses': houses_result}
    return jsonify(result)


@app.before_request
def check_signature():
    if not request.path.startswith('/v1/'):
        return
    if 'X-Key' not in request.headers or request.headers['X-Key'] != os.getenv('XKEY'):
        return jsonify({'error': 'Unauthorized'}), 401


@app.route("/")
def root():
    return jsonify({'message': 'Horoscope API v.1.0.0'})


if __name__ == "__main__":
    debug = os.getenv('ENV', 'production') != 'production'
    port = os.getenv('PORT', 8080)
    app.run(host="127.0.0.1", port=port, debug=debug)
