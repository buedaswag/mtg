from flask import Flask, render_template

app = Flask(__name__)

columnChart = {
        "chart": {
            "caption": "Countries With Most Oil Reserves [2017-18]",
            "subCaption": "In MMbbl = One Million barrels",
            "xAxisName": "Country",
            "yAxisName": "Reserves (MMbbl)",
            "numberSuffix": "K",
            "theme": "fusion",
        },
        "data": [{
            "label": "Venezuela",
            "value": "290"
        }, {
            "label": "Saudi",
            "value": "260"
        }, {
            "label": "Canada",
            "value": "180"
        }, {
            "label": "Iran",
            "value": "140"
        }, {
            "label": "Russia",
            "value": "115"
        }, {
            "label": "UAE",
            "value": "100"
        }, {
            "label": "US",
            "value": "30"
        }, {
            "label": "China",
            "value": "30"
        }]
    }

lineChart = {
    "chart": {
        "caption": "Store footfall vs Online visitors ",
        "subCaption": "Last Year",
        "xAxisName": "Quarter",
        "yAxisName": "USD",
        "base": "10",
        "numberprefix": "$",
        "theme": "fusion"
    },
    "categories": [
        {
            "category": [
                {
                    "label": "Q1"
                },
                {
                    "label": "Q2"
                },
                {
                    "label": "Q3"
                },
                {
                    "label": "Q4"
                }
            ]
        }
    ],
    "dataset": [
        {
            "seriesname": "Total footfalls",
            "data": [
                {
                    "value": "126734"
                },
                {
                    "value": "159851"
                },
                {
                    "value": "197393"
                },
                {
                    "value": "168560"
                },
                {
                    "value": "199428"
                }
            ]
        },
        {
            "seriesname": "Online Visits",
            "data": [
                {
                    "value": "1126059"
                },
                {
                    "value": "1292145"
                },
                {
                    "value": "1496849"
                },
                {
                    "value": "1460249"
                },
                {
                    "value": "1083962"
                }
            ]
        }
    ]
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/column")
def column_page():
    return render_template("column.html", chart=columnChart)

@app.route("/line")
def line_page():
    return render_template("line.html", chart=lineChart)
    
if __name__ == "__main__":
    app.run(debug=True)