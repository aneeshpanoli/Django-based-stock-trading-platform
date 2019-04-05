      function lineGraph(){
        d3.select("svg").remove();
        var csvPathSim = csvpath + csvFname

        var svg = d3.select("#lineChartD3")
                    .append("svg")
                    .attr("width", 960)
                    .attr("height", 500)
          margin = {top: 20, right: 20, bottom: 30, left: 50},
          width = +svg.attr("width") - margin.left - margin.right,
          height = +svg.attr("height") - margin.top - margin.bottom,
          g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");


      var x = d3.scaleLinear()
          .rangeRound([0, width]);

      var y = d3.scaleLinear()
          .rangeRound([height, 0]);

      var line = d3.line()
          .x(function(d, i) { return x(i); })
          .y(function(d) { return y(d.Close); });
      d3.csv(csvPathSim, function(d, i) {
        d.index = +i;
        d.Close = +d.Close;
        return d;
      }, function(error, data) {
        if (error) throw error;

        x.domain(d3.extent(data, function(d, i) { return i; }));
        y.domain(d3.extent(data, function(d) { return d.Close; }));

        g.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))
          .select(".domain")
            .remove();

        g.append("g")
            .call(d3.axisLeft(y))
          .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("Price ($)");

        g.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            // .attr("stroke-width", null)
            .attr("stroke-width", 1.5)
            .attr("d", line);
      });
}



      (function(){
        lineGraph();
        var int = setInterval("lineGraph()", 5000);
      })();
