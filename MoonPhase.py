# Write your code here :-)
# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# Moonphase example utilizing Farmsense API by bk
# brandonklevence@gmail.com

from adafruit_magtag.magtag import MagTag
import adafruit_requests
import secrets
import wifi
import ipaddress
import ssl
import socketpool

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)

requests = adafruit_requests.Session(pool, ssl.create_default_context())


TIME_URL = "https://io.adafruit.com/api/v2/time/seconds"

response = requests.get(TIME_URL)
unix = str(response.text)

print(unix)

# Set up where we'll be fetching data from
DATA_SOURCE = "https://api.farmsense.net/v1/moonphases/?d="
DATA_SOURCE += unix
DATA_Phase = [0, "Phase"]
DATA_Illumination = [0, "Illumination"]
DATA_Age = [0, "Age"]


def text_transform(value):
    return value

magtag = MagTag(url=DATA_SOURCE,
json_path=(DATA_Phase, DATA_Illumination, DATA_Age))

magtag.network.connect()

magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        (magtag.graphics.display.height // 2) + 22,
    ),
    text_scale=1.5,
    text_transform=text_transform,
    text_anchor_point=(0.5, 0.5),
)

magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        (magtag.graphics.display.height // 2) + 43,
    ),
    text_scale=1.5,
    text_transform=text_transform,
    text_anchor_point=(0.5, 0.5),
 #   is_data= False,
)


magtag.add_text(
    text_font="/fonts/MoonPhases-75.bdf",
    text_position=((magtag.graphics.display.width // 2) - 1, 40),
    text_anchor_point=(0.5, 0.5),
)

try:
    value = magtag.fetch()

    moonChar = [
        "0",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "1",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",

    ]

    z = value[2] / 29.56
    y = int(z * 28)

    print(moonChar[y])
    magtag.set_text(value[0], index=0)
    p = str("Illuminated: " + str(int(value[1]*100)) +"%")
    magtag.set_text(p, index=1)
    magtag.set_text(moonChar[y], index=2)
    print(value)
    print("Illumination:", value[1], "%")
except (ValueError, RuntimeError) as e:
    print("Some error occured, retrying! -", e)
magtag.exit_and_deep_sleep(60)
