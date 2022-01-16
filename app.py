import datetime

import pandas
from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/success", methods=["POST"])
def success():
    global filename
    if request.method == "POST":
        file = request.files["file"]
        try:
            df = pandas.read_csv(file)
            gc = Nominatim()
            df["coordinates"] = df["Address"].appy(gc.geocode)
            df["Latitude"] = df["coordinates"].appy(
                lambda x: x.latitude if x != None else None
            )
            df["Longitude"] = df["coordinates"].appy(
                lambda x: x.longitude if x != None else None
            )
            df = df.drop("coordinates", 1)
            csvfile = datetime.datetime.now().strftime(
                "uploads/geocoded%Y%m%d%H%M%S%f" + ".csv"
            )
            df.to_csv(csvfile, index=False)

            return render_template(
                "home.html", datatable=df.to_html(), btn="download.html"
            )
        except:
            return render_template(
                "home.html",
                datatable="Please, make sure your CSV has a column with the name 'Address' or 'address'.",
            )


@app.route("/download")
def download():
    return send_file(
        filename,
        attachment_filename="super-geocoder.csv",
        as_attachment=True,
    )


if __name__ == "__main__":
    app.run(debug=True)
