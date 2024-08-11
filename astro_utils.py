import pytz
import swisseph as swe
from timezonefinder import TimezoneFinder
import math
from datetime import timedelta

ZODIAC_SIGN_ARIES = "aries"
ZODIAC_SIGN_TAURUS = "taurus"
ZODIAC_SIGN_GEMINI = "gemini"
ZODIAC_SIGN_CANCER = "cancer"
ZODIAC_SIGN_LEO = "leo"
ZODIAC_SIGN_VIRGO = "virgo"
ZODIAC_SIGN_LIBRA = "libra"
ZODIAC_SIGN_SCORPIO = "scorpio"
ZODIAC_SIGN_SAGITTARIUS = "sagittarius"
ZODIAC_SIGN_CAPRICORN = "capricorn"
ZODIAC_SIGN_AQUARIUS = "aquarius"
ZODIAC_SIGN_PISCES = "pisces"

ZODIAC_SIGNS = [
    (ZODIAC_SIGN_ARIES, 0, 30),
    (ZODIAC_SIGN_TAURUS, 30, 60),
    (ZODIAC_SIGN_GEMINI, 60, 90),
    (ZODIAC_SIGN_CANCER, 90, 120),
    (ZODIAC_SIGN_LEO, 120, 150),
    (ZODIAC_SIGN_VIRGO, 150, 180),
    (ZODIAC_SIGN_LIBRA, 180, 210),
    (ZODIAC_SIGN_SCORPIO, 210, 240),
    (ZODIAC_SIGN_SAGITTARIUS, 240, 270),
    (ZODIAC_SIGN_CAPRICORN, 270, 300),
    (ZODIAC_SIGN_AQUARIUS, 300, 330),
    (ZODIAC_SIGN_PISCES, 330, 360)
]


def calculate_jd_utc(date, latitude, longitude):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    timezone = pytz.timezone(timezone_str)
    new_date = timezone.localize(date)
    offset_seconds = new_date.utcoffset().total_seconds()
    gmt_shift = offset_seconds / 3600.0

    new_date_utc = new_date.astimezone(pytz.utc)
    hour = new_date_utc.hour + new_date_utc.minute / 60.0 + new_date_utc.second / 3600.0
    jd = swe.julday(new_date_utc.year, new_date_utc.month, new_date_utc.day, hour)

    return jd, new_date_utc, new_date, timezone, gmt_shift


def get_ecliptic_lon(planet_id, jd):
    planet_pos, _ = swe.calc_ut(jd, planet_id, swe.FLG_SWIEPH | swe.FLG_SPEED)
    return planet_pos[0], planet_pos[3]


def get_zodiac_sign(ecliptic_longitude):
    ecliptic_longitude %= 360
    for sign, start_degree, end_degree in ZODIAC_SIGNS:
        if start_degree <= ecliptic_longitude < end_degree:
            return sign


def get_house_number(houses, planet_position):
    house_number = 1
    for i in range(1, 12):
        if planet_position < houses[i]:
            break
        house_number = i + 1
    return house_number


def moon_phase_to_text(phase, waning=False):
    if phase == 0:
        return "New Moon"
    elif 0 < phase < 50:
        return "Waning Crescent" if waning else "Waxing Crescent"
    elif phase == 50:
        return "Last Quarter" if waning else "First Quarter"
    elif 50 < phase < 100:
        return "Waning Gibbous" if waning else "Waxing Gibbous"
    elif phase == 100:
        return "Full Moon"


def get_moon_illumination(date):
    jd = swe.julday(date.year, date.month, date.day, 0)
    sun, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH + swe.FLG_MOSEPH)
    moon, _ = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH + swe.FLG_MOSEPH)
    elongation = moon[0] - sun[0]
    elongation = elongation % 360
    phase_angle = 180 - elongation
    illumination = (1 + math.cos(math.radians(phase_angle))) / 2
    return illumination * 100, get_zodiac_sign(moon[0])


def get_lunar_metrics(date):
    prev_date = date + timedelta(days=-1)
    prev_illumination, _ = get_moon_illumination(prev_date)
    illumination, sign = get_moon_illumination(date)
    next_date = date + timedelta(days=1)
    next_illumination, _ = get_moon_illumination(next_date)

    phase_illumination = illumination
    if prev_illumination > illumination and illumination < next_illumination:
        phase_illumination = 0
    elif prev_illumination < illumination and illumination > next_illumination:
        phase_illumination = 100
    elif int(illumination) == 50 or (48 < illumination < 52):
        phase_illumination = 50

    moon_phase = moon_phase_to_text(phase_illumination, phase_illumination < prev_illumination)

    return {
        "illumination": illumination,
        "phase": moon_phase,
        "sign": sign
    }
