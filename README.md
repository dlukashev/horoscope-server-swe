# Horoscope server

## Licensing
This project is licensed under the GNU Affero General Public License version 3. See the LICENSE.txt file.

The original swisseph library is distributed under a dual licensing system: GNU Affero General Public License, or Swiss Ephemeris Professional License. For more information, see https://github.com/astrorigin/swisseph.

## Installation
```shell
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Docker
```shell
docker compose up -d
```

## Endpoints
```shell
curl -H "X-Key:123" "http://127.0.0.1/v1/natal_chart?lat=37.7749&lon=122.4194&date=1983-06-28T16:22:00"
```

```json
{
    "houses": [
        {
            "num": 1,
            "position": 239.5515780689425,
            "sign": "scorpio"
        },
        {
            "num": 2,
            "position": 270.6405958828136,
            "sign": "capricorn"
        },
        {
            "num": 3,
            "position": 306.3375400551523,
            "sign": "aquarius"
        },
        {
            "num": 4,
            "position": 342.4153760943178,
            "sign": "pisces"
        },
        {
            "num": 5,
            "position": 13.48420171581563,
            "sign": "aries"
        },
        {
            "num": 6,
            "position": 38.542375994802796,
            "sign": "taurus"
        },
        {
            "num": 7,
            "position": 59.55157806894249,
            "sign": "taurus"
        },
        {
            "num": 8,
            "position": 90.64059588281361,
            "sign": "cancer"
        },
        {
            "num": 9,
            "position": 126.33754005515232,
            "sign": "leo"
        },
        {
            "num": 10,
            "position": 162.4153760943178,
            "sign": "virgo"
        },
        {
            "num": 11,
            "position": 193.48420171581566,
            "sign": "libra"
        },
        {
            "num": 12,
            "position": 218.5423759948028,
            "sign": "scorpio"
        }
    ],
    "info": {
        "age_in_days": 15020,
        "ascedant": 239.5515780689425,
        "date": "1983-06-28T16:22:00+08:00",
        "date_utc": "1983-06-28T08:22:00+00:00",
        "descendant": 59.55157806894249,
        "gmt_shift": 8.0,
        "house_system": "P",
        "ic": 342.4153760943178,
        "jd": 2445513.8486111113,
        "lat": 37.7749,
        "lon": 122.4194,
        "midheaven": 162.4153760943178,
        "timezone": "Etc/GMT-8"
    },
    "planets": {
        "jupiter": {
            "fd": 242.4826077609076,
            "house": 2,
            "nd": 2.482607760907598,
            "retro": true,
            "sign": "sagittarius",
            "speed": -0.08773000269241504
        },
        "mars": {
            "fd": 89.36588964911164,
            "house": 8,
            "nd": 29.365889649111637,
            "retro": false,
            "sign": "gemini",
            "speed": 0.6758466558460575
        },
        "mercury": {
            "fd": 82.98353437999342,
            "house": 8,
            "nd": 22.983534379993415,
            "retro": false,
            "sign": "gemini",
            "speed": 1.968042565154133
        },
        "moon": {
            "fd": 309.026278623876,
            "house": 4,
            "nd": 9.02627862387601,
            "retro": false,
            "sign": "aquarius",
            "speed": 11.84837772777463
        },
        "neptune": {
            "fd": 267.62574886980593,
            "house": 2,
            "nd": 27.625748869805932,
            "retro": true,
            "sign": "sagittarius",
            "speed": -0.026609918256658982
        },
        "pluto": {
            "fd": 206.73418421972403,
            "house": 12,
            "nd": 26.73418421972403,
            "retro": true,
            "sign": "libra",
            "speed": -0.005096653847388664
        },
        "saturn": {
            "fd": 207.73074896230185,
            "house": 12,
            "nd": 27.730748962301845,
            "retro": true,
            "sign": "libra",
            "speed": -0.005172680312710164
        },
        "sun": {
            "fd": 96.08755014184774,
            "house": 9,
            "nd": 6.087550141847743,
            "retro": false,
            "sign": "cancer",
            "speed": 0.9532891979594188
        },
        "uranus": {
            "fd": 245.93184515693443,
            "house": 2,
            "nd": 5.931845156934429,
            "retro": true,
            "sign": "sagittarius",
            "speed": -0.03378112184063191
        },
        "venus": {
            "fd": 140.8589816353491,
            "house": 10,
            "nd": 20.858981635349096,
            "retro": false,
            "sign": "leo",
            "speed": 0.846241663128541
        }
    }
}
```

```
curl -H "X-Key:123" "http://127.0.0.1/v1/moon_metrics?date=2024-08-11"
```

```json
[
    {
        "date": "2024-07-25",
        "illumination": 83.15195208520439,
        "phase": "Waning Gibbous",
        "sign": "pisces"
    },
    {
        "date": "2024-07-26",
        "illumination": 73.49591305003374,
        "phase": "Waning Gibbous",
        "sign": "aries"
    },
    {
        "date": "2024-07-27",
        "illumination": 62.680932941876456,
        "phase": "Waning Gibbous",
        "sign": "aries"
    }
]
```