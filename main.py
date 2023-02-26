from flask import Flask
from flask import jsonify
from flask import request

from PrayTimes.praytimes import PrayTimes

from datetime import date, datetime, timedelta
import json

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
prayTimes = PrayTimes()


# Fungsi: Mengambil jadwal dari tanggal, latitude, dan longtitude dari user
def ambil_jadwal(method, targetDate, latitude, longtitude):
    prayTimes.setMethod(method)

    # Offset (menambahkan +2 menit sebagai pengaman)
    # TODO: Cek apakah benar jadwal harus diberi offset
    prayTimes.tune({
        "fajr": 2,
        "dhuhr": 2,
        "asr": 2,
        "maghrib": 2,
        "isha": 2,
    })

    # Kalkulasi jadwal
    times = prayTimes.getTimes(targetDate, (latitude, longtitude), 7)

    # Susun jadwal
    parsedTimes = {
        "shubuh": times["fajr"],
        "dhuhur": times["dhuhr"],
        "ashar": times["asr"],
        "maghrib": times["maghrib"],
        "isya'": times["isha"],
    }
    result = {
        "date": targetDate.strftime("%d-%m-%Y"),
        "latitude": latitude,
        "longtitude": longtitude,
        "jadwal": parsedTimes
    }

    return result


# Route: Home (/)
@app.route("/")
def home():
    return jsonify(msg="Hello, World!")

# Route: Ambil jadwal Shalat (/shalat)
@app.route("/shalat")
def shalat_brother():
    targetDate = request.args.get("tanggal", None)
    if targetDate:
        targetDate = datetime.strptime(targetDate, "%d-%m-%Y").date()
    else:
        targetDate = date.today()

    method = request.args.get("metode", None)
    if not method:
        method = "Kemenag" # Metode: Kemenag

    latitude = request.args.get("lat", None)
    if latitude:
        latitude = float(latitude)
    else:
        latitude = -8.0667

    longtitude = request.args.get("long", None)
    if longtitude:
        longtitude = float(longtitude)
    else:
        longtitude = 111.9

    result = ambil_jadwal(method, targetDate, latitude, longtitude)
    result["metode"] = prayTimes.getMethod()
    return jsonify(result)

# Route: Ambil range jadwal Shalat (/range_shalat)
@app.route("/range_shalat")
def range_shalat():
    startDate = request.args.get("start", None)
    if startDate:
        startDate = datetime.strptime(startDate, "%d-%m-%Y").date()
    else:
        startDate = date.today()
    endDate = request.args.get("end", None)
    if endDate:
        endDate = datetime.strptime(endDate, "%d-%m-%Y").date()
    else:
        endDate = date.today()

    method = request.args.get("metode", None)
    if not method:
        method = "Kemenag" # Metode: Kemenag

    # Hitung selisih
    selisih = endDate - startDate
    if selisih.days < 0:
        rangeTanggal = [startDate + timedelta(days=x) for x in range(selisih.days, 1)]
        rangeTanggal.reverse()
    else:
        rangeTanggal = [startDate + timedelta(days=x) for x in range(selisih.days + 1)]

    latitude = request.args.get("lat", None)
    if latitude:
        latitude = float(latitude)
    else:
        latitude = -8.168254

    longtitude = request.args.get("long", None)
    if longtitude:
        longtitude = float(longtitude)
    else:
        longtitude = 111.804787

    jadwal = []
    for tanggal in rangeTanggal:
        j = ambil_jadwal(method, tanggal, latitude, longtitude)
        jadwal.append(j)

    result = {
        "metode": prayTimes.getMethod(),
        "start_tanggal": startDate.strftime("%d-%m-%Y"),
        "end_tanggal": endDate.strftime("%d-%m-%Y"),
        "jadwal": jadwal,
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)