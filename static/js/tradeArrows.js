function candlestickChart(){ // css is an important part of this code, always include css
  d3.select("svg").remove();
var csvPathSim = csvpath + csvFname;
var csvPath = csvpath + csvFnameD3;

var margin = {top: 20, right: 20, bottom: 30, left: 50},
            width = 960 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

    var dateFormat = d3.timeFormat("%d-%b-%y"),
        parseDate = d3.timeParse("%d-%b-%y"),
        valueFormat = d3.format(',.2f');

    var x = techan.scale.financetime()
            .range([0, width]);

    var y = d3.scaleLinear()
            .range([height, 0]);

    var candlestick = techan.plot.candlestick()
            .xScale(x)
            .yScale(y);

    var tradearrow = techan.plot.tradearrow()
            .xScale(x)
            .yScale(y)
            .orient(function(d) { return d.type.startsWith("buy") ? "up" : "down"; })
            .on("mouseenter", enter)
            .on("mouseout", out);

    var xAxis = d3.axisBottom(x);

    var yAxis = d3.axisLeft(y);

    var svg = d3.select("#candle").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var valueText = svg.append('text')
            .style("text-anchor", "end")
            .attr("class", "coords")
            .attr("x", width - 5)
            .attr("y", 15);

    d3.csv(csvPath, function(error, data) {
        var accessor = candlestick.accessor();
        if (data.length < 200){ // slice the data to show only the recent 200
          var dataSlice = -data.length;
        }else{var dataSlice = -200;}
        data = data.slice(dataSlice, -1).map(function(d, i) {
            return {
                date: i, // since no date replaced it with index
                open: +d.Open,
                high: +d.High,
                low: +d.Low,
                close: +d.Close,
                type: d.Type,
            };
        }).sort(function(a, b) { return d3.ascending(accessor.d(a), accessor.d(b)); });
        console.log(data[data.length -1].type)

        //create trade array from data array
        var trades = [];
        for(i=0; i < data.length; i++){
          if (data[i].type === "buy"){
            trades.push({ date: data[i].date, type: data[i].type , price:data[i].low, quantity: 1000 })
          }else if(data[i].type === "sell"){
            trades.push({ date: data[i].date, type: data[i].type , price:data[i].high, quantity: 1000 })
          }
        }
        // var trades = JSON.stringify(trades)
        // console.log(trades[0])
        // console.log(trades[1])
        // console.log(data.length)

        // var trades = [
        //     { date: data[26].date, type: "buy", price: data[26].low, quantity: 1000 },
        //     { date: data[60].date, type: "sell", price: data[60].high, quantity: 200 },
        //     { date: data[15].date, type: "buy", price: data[15].open, quantity: 500 },
        //     { date: data[46].date, type: "sell", price: data[46].close, quantity: 300 },
        //     { date: data[57].date, type: "buy-pending", price: data[57].low, quantity: 300 }
        // ];

        svg.append("g")
                .attr("class", "candlestick");

        svg.append("g")
                .attr("class", "tradearrow");

        svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")");

        svg.append("g")
                .attr("class", "y axis")
                .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", ".71em")
                .style("text-anchor", "end")
                .text("Price ($)");

        // Data to display initially
        draw(data, trades); // initiate drawing
        // Only want this button to be active if the data has loaded
        d3.select("button").on("click", function() { draw(data, trades); }).style("display", "inline");
    });

    function draw(data, trades) {
        x.domain(data.map(candlestick.accessor().d));
        y.domain(techan.scale.plot.ohlc(data, candlestick.accessor()).domain());

        svg.selectAll("g.candlestick").datum(data).call(candlestick);
        svg.selectAll("g.tradearrow").datum(trades).call(tradearrow);

        svg.selectAll("g.x.axis").call(xAxis);
        svg.selectAll("g.y.axis").call(yAxis);
    }

    function enter(d) {
        valueText.style("display", "inline");
        refreshText(d);
    }

    function out() {
        valueText.style("display", "none");
    }

    function refreshText(d) {
        valueText.text("Trade: " + dateFormat(d.date) + ", " + d.type + ", " + valueFormat(d.price));
    }}

    (function(){
    candlestickChart();
    var int = setInterval("candlestickChart()", 12000); // doesnt need to refresh too often as long as the table is refreshed
    })();
