  // Create the Google Map…
  var map = new google.maps.Map(d3.select("#map").node(), {
    zoom: 5.25,
    center: new google.maps.LatLng(39, -97),
    disableDefaultUI: true,
    gestureHandling: 'greedy'
  });

  // Load the station data. When the data comes back, create an overlay.
  d3.csv("airports.csv", function (error, data) {
    if (error) throw error;

    var overlay = new google.maps.OverlayView();

    // Add the container when the overlay is added to the map.
    overlay.onAdd = function () {
      var layer = d3.select("#overlay").append("div")
        .attr("class", "airports");

      // Draw each marker as a separate SVG element.
      // We could use a single SVG, but what size would it have?
      overlay.draw = function () {
        var projection = this.getProjection(),
          padding = 10;

        var marker = layer.selectAll("svg")
          .data(d3.entries(data))
          .each(transform) // update existing markers
          .enter().append("svg")
          .each(transform)
          .attr("class", "marker");

        // Add a circle.
        marker.append("circle")
          .attr("r", 4.5)
          .attr("cx", padding)
          .attr("cy", padding);

        // Add a label.
        marker.append("text")
          .attr("x", padding + 7)
          .attr("y", padding)
          .attr("dy", ".31em")
          .text(function (d) { return d.value.IATA_CODE; });

        marker.on("click", function (d) {
          d3.select("#sidebar").classed("active", true);
          d3.selectAll(".selected").classed("selected", false);
          d3.select(this).classed("selected", true);

          d3.select("#airport-iata-code").text(d.value.IATA_CODE);
          d3.select("#airport-name").text(d.value.AIRPORT);
          d3.select("#airport-city").text(d.value.CITY);
          d3.select("#airport-state").text(d.value.STATE);

          var center = new google.maps.LatLng(parseFloat(d.value.LATITUDE), parseFloat(d.value.LONGITUDE) + 2);
          map.panTo(center);
          map.setZoom(7);
        });

        d3.select("#sidebar-close").on("click", function() {
          d3.select("#sidebar").classed("active", false);
        });

        function transform(d) {
          d = new google.maps.LatLng(parseFloat(d.value.LATITUDE), parseFloat(d.value.LONGITUDE));
          d = projection.fromLatLngToDivPixel(d);

          return d3.select(this)
            .style("left", (d.x - padding) + "px")
            .style("top", (d.y - padding) + "px");
        }
      };
    };

    // Bind our overlay to the map…
    overlay.setMap(map);
  });