
// Event listener to wait until full document is ready to render
$(document).ready(function () {


  // Line chart comparing pos/neg tweets over time, broken down by candidate
  var line_chart = $("#sentiment_comparison").get(0).getContext("2d");

  //AJAX call to retrieve sentiment data by datetime - xAxis to use datetime from Moment.js
  $.get("/sentiment_data.json", function (data) {
    var myLineChart = new Chart(line_chart, {
                                  type: "line",
                                  data: data,
                                  options: {
                                    responsive: true,
                                    scales: {
                                        xAxes: [{
                                          type: "time",
                                          time: {
                                            unit: "month"
                                          }
                                        }]
                                        }
                                      }
                                    });
                                  });

  //Donut chart showing breakdown of neg/pos tweets for each candidate:
  function generate_donut(data, html_element) {
    var donutChart = new Chart(html_element, {
                              type: "doughnut",
                              data: data
    });
  }

  var trump_donut_chart = $("#trumpDonut").get(0).getContext("2d");

  $.get("/donut_chart.json/Trump", function (data) {
      generate_donut(data, trump_donut_chart)
  });

  var clinton_donut_chart = $("#clintonDonut").get(0).getContext("2d");

  $.get("/donut_chart.json/Clinton", function (data) {
      generate_donut(data, clinton_donut_chart)
  });

  var both_donut_chart = $("#bothDonut").get(0).getContext("2d");

  $.get("/donut_chart.json/Both", function (data) {
      generate_donut(data, both_donut_chart)
  })


  // Bar chart showing comparison between Trump, Clinton and Both
  var total_comparison_chart = $("#totalComparison").get(0).getContext("2d");

  $.get("/sum_comparison.json", function (data) {
    var horizontalBar = new Chart(total_comparison_chart, {
                                  type: "horizontalBar",
                                  data: data
                                    });
                                  });


    // Initialize Google Map - Grayscale for style
    var map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      scrollwheel: false,
      streetViewControl: false,
      mapTypeControl: false,
      styles: [
        {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#e9e9e9"
                },
                {
                    "lightness": 17
                }
            ]
        },
        {
            "featureType": "landscape",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#f5f5f5"
                },
                {
                    "lightness": 20
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "#ffffff"
                },
                {
                    "lightness": 17
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#ffffff"
                },
                {
                    "lightness": 29
                },
                {
                    "weight": 0.2
                }
            ]
        },
        {
            "featureType": "road.arterial",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#ffffff"
                },
                {
                    "lightness": 18
                }
            ]
        },
        {
            "featureType": "road.local",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#ffffff"
                },
                {
                    "lightness": 16
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#f5f5f5"
                },
                {
                    "lightness": 21
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#dedede"
                },
                {
                    "lightness": 21
                }
            ]
        },
        {
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "visibility": "on"
                },
                {
                    "color": "#ffffff"
                },
                {
                    "lightness": 16
                }
            ]
        },
        {
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "saturation": 36
                },
                {
                    "color": "#333333"
                },
                {
                    "lightness": 40
                }
            ]
        },
        {
            "elementType": "labels.icon",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "transit",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#f2f2f2"
                },
                {
                    "lightness": 19
                }
            ]
        },
        {
            "featureType": "administrative",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "#fefefe"
                },
                {
                    "lightness": 20
                }
            ]
        },
        {
            "featureType": "administrative",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#fefefe"
                },
                {
                    "lightness": 17
                },
                {
                    "weight": 1.2
                }
            ]
        }
      ]
    });

  // map.data.loadGeoJson("/google.json")

  // Use geocoder to center the map on the U.S.
  var geocoder = new google.maps.Geocoder();
  geocoder.geocode({'address': 'US'}, function (results, status) {
     var ne = results[0].geometry.viewport.getNorthEast();
     var sw = results[0].geometry.viewport.getSouthWest();

     map.fitBounds(results[0].geometry.viewport);               
  }); 

  var infoWindow = new google.maps.InfoWindow({
        width: 100
      });


  // Creating circles with corresponding size and color
  function getCircle(tweets, color) {
      var circle = {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: color,
        fillOpacity: .2,
        scale: tweets**(1/2),
        strokeColor: 'white',
        strokeWeight: .5
      };
      return circle;
    }

  // AJAX call for JSON to display data on map
  $.get("/map.json", function (data) {
    var locations = data["location_data"];

    for (var i = 0; i < locations.length; i++) {
      var coordinates = (locations[i]["coordinates"]);
      var num_tweets = (locations[i]["num_tweets"]);
      var color = (locations[i]["color"]);

      var marker = new google.maps.Marker({
        map: map,
        position: coordinates,
        icon: getCircle(num_tweets, color)
        });

      // infoHTML = (
      //   '<div class="window-content">' +
      //       '<p><b>Number of Tweets: </b>' + num_tweets + '</p>' +
      //   '</div>');

      // bindInfoWindow(marker, map, infoWindow, infoHTML);

      // function bindInfoWindow(marker, map, infoWindow, infoHTML) {
      //   google.maps.event.addListener(marker, 'mouseover', function(){
      //   infoWindow.close(map, this);
      //   infoWindow.setContent(infoHTML)
      //   infoWindow.open(map, this);
      // });

      // }


      // google.maps.event.addListener(marker, 'mouseout', function() {
      //   infowindow.close(map, this);
      // });
      
    };

  });










  });