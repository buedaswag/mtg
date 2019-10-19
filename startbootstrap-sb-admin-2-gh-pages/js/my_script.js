//import '../fusioncharts-suite-xt/js/fusioncharts.js'


document.getElementsByClassName("sidebar-brand-text mx-3")[0].innerHTML = 'MTG Data';
document.title = 'MTG Data';


/*
Assuming you have installed fusioncharts using npm
Following code snippet can be used to render chart.
*/
var FusionCharts = require("fusioncharts");
var TimeSeries = require("fusioncharts/fusioncharts.timeseries");
var $ = require("jquery");
var jQueryFusionCharts = require("jquery-fusioncharts");

TimeSeries(FusionCharts); // Resolve Charts as dependency for FusionCharts.
jQueryFusionCharts(FusionCharts); // Resolve FusionCharts as dependency for jqueryFusionCharts.

var jsonify = res => res.json();
var dataFetch = fetch(
  "https://s3.eu-central-1.amazonaws.com/fusion.store/ft/data/plotting-multiple-series-on-time-axis-data.json"
).then(jsonify);
var schemaFetch = fetch(
  "https://s3.eu-central-1.amazonaws.com/fusion.store/ft/schema/plotting-multiple-series-on-time-axis-schema.json"
).then(jsonify);

Promise.all([dataFetch, schemaFetch]).then(res => {
  const data = res[0];
  const schema = res[1];
  // First we are creating a DataStore
  const fusionDataStore = new FusionCharts.DataStore();
  // After that we are creating a DataTable by passing our data and schema as arguments
  const fusionTable = fusionDataStore.createDataTable(data, schema);

  $("document").ready(function() {
    $("#chart-container").insertFusionCharts({
      type: "timeseries",
      width: "600",
      height: "400",
      dataFormat: "json",
      dataSource: {
        data: fusionTable,
        chart: {},
        caption: {
          text: "Sales Analysis"
        },
        subcaption: {
          text: "Grocery & Footwear"
        },
        series: "Type",
        yaxis: [
          {
            plot: "Sales Value",
            title: "Sale Value",
            format: {
              prefix: "$"
            }
          }
        ]
      }
    });
  });
});

/* NOTE:
 * In case you downloaded fusioncharts in zipped format
 * var FusionCharts = require('/path/to/fusioncharts/fusioncharts.js');
 * var TimeSeries = require('/path/to/fusioncharts/fusioncharts.timeseries.js');
 */
