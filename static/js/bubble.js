// load csv file to d3

function bubbleChart(){
  pathcsv = csvFolder + stockTickr + ".csv";
  d3.select('#chartB1').on('click', d3.select("svg").remove()); // resets svg
  console.log(pathcsv)
  d3.csv(pathcsv, function(data) {

    // for (var key in data){
    //   priceMovement.push(+Object.values(data[key])[7])
    // };
      var volumeHigh = d3.max(data, function(d){ return +d.sharesnow});
      var volumeLow = d3.min(data, function(d){ return +d.sharesnow});
      console.log(volumeHigh)
      console.log(volumeLow)
      var cDeltaHigh = d3.max(data, function(d){ return +d.change}); //lowest price difference
      var cDeltaLow = d3.min(data, function(d){ return +d.change});
      // var cDeltaLow = priceMovement.sort(function(a, b){return b-a})[priceMovement.length-1]; // highest price difference
      // console.log(cDeltaHigh)
      // console.log(cDeltaLow)
      var colrScale = d3.scaleLinear()
                        .domain([cDeltaHigh, 0, cDeltaLow]) // should be zero
                        .range(["green", "yellow", "red"]);
//----------

  var radiusScale = d3.scaleSqrt().domain([volumeLow, volumeHigh]).range([9, 25]);

  var radiusAttr = function(d){
    return radiusScale(d.sharesnow);
  }
  var moRadiusAttr = function(d){
    return radiusScale(d.sharesnow);
  }

  var width = 1000,
  height = 300;
  if (2 * Math.sqrt(11*12*data.length) > height) {
    height = 2 * Math.sqrt(15*15*data.length);
  }

  var tip = d3.tip()
            .attr('class', 'd3-tip')
            .html(function(d) {return 'CIK: ' +d.cik
            +'</br> Insitution Name: ' +d.institution
            +'</br> Current no of shares: ' + d.sharesnow
            +'</br> No of shares from last filing: ' + d.shareslast
            +'</br> Change in holding: ' + d.change;})
  // var stockTickr = prompt("Please enter the tickr: ")
  var svg = d3.select("#chart")
    .append("svg")
    .attr("height", height)
    .attr("width", width)
    .append("g")
    .call(tip);

//------------


  //simulation is a collection of forces to interact with circles
  //get circle into middle
  var simulation = d3.forceSimulation()
    // .force("x", d3.forceX(width/2).strength(0.0))
    // .force("y", d3.forceY(height/2).strength(0.0))
    .force("collide", d3.forceCollide(moRadiusAttr))
//forceCenter
  d3.queue()
    .defer(d3.csv, pathcsv)
    .await(ready)

  function ready(error, datapoints){
    var circles = svg.append("g").selectAll(".gene")
                  .data(datapoints)
                  .enter().append("circle")
                  .attr("class", "gene")
                  // .attr("r",10)
                  .attr("r", radiusAttr)
                  .attr("cursor", "pointer")
                  .attr("id", function(d){
                    return d.cik})
                  .attr("fill", function(d){return colrScale(+d.change);})
                  .attr("stroke", "grey")
                  .on('mouseover', tip.show)
                  .on('mouseout', tip.hide);
                  // .sort(d3.ascending);
                  // .sort( function(a, b) { return  -1;})
      // .attr("onmouseover","evt.target.setAttribute('fill', 'orange')")
      // .attr("onmouseout", "evt.target.setAttribute('fill','#1E90FF')")
      // .attr("onclick","getid(this)")
      // .attr("onmouseover","evt.target.setAttribute('r', 'moRadiusAttr')")
      // .attr("onmouseout", "evt.target.setAttribute('r','radiusAttr')")
      var label = svg.append("g").selectAll(".text")
                  .data(datapoints)
                  .enter().append("text")
                  .text(function(d, i){return +i+1})
                  .style("text-anchor", "middle")
                  .style("fill", "black")
                  .style("font-family", "Lato")
                  .style("font-weight", "bold")
                  .style("font-size", 8)
    simulation.nodes(datapoints)
      .on('tick', ticked)
    function ticked() {
      circles
        .attr("cx", function(d){
          return d.x
        })
        .attr("cy", function(d) {
          return d.y
        })
        .attr('transform', 'translate(' +width/2 +','+height/2+')');
        // .sort(d3.descending);
        label
          .attr("x", function(d){
            return d.x
          })
          .attr("y", function(d) {
            return d.y
          })
          .attr('transform', 'translate(' +width/2 +', '+height/2+')');
          // .sort(d3.descending);
    }
  }
})}

function bubbleChartRedAndGreen(){
  pathcsv = csvFolder + stockTickr + ".csv";
  d3.select('#chartB1').on('click', d3.select("svg").remove()); // resets svg
  console.log(pathcsv)
  d3.csv(pathcsv, function(data) {

    // for (var key in data){
    //   priceMovement.push(+Object.values(data[key])[7])
    // };

    //summary of data
    var pChange =0;
    var noChange = 0;
    var negChange = 0;


      var volumeHigh = d3.max(data, function(d){ return +d.sharesnow});
      var volumeLow = d3.min(data, function(d){ return +d.sharesnow});
      console.log(volumeHigh)
      console.log(volumeLow)
      var cDeltaHigh = d3.max(data, function(d){ return +d.change}); //lowest price difference
      var cDeltaLow = d3.min(data, function(d){ return +d.change});
      // var cDeltaLow = priceMovement.sort(function(a, b){return b-a})[priceMovement.length-1]; // highest price difference
      // console.log(cDeltaHigh)
      // console.log(cDeltaLow)
      var colrScale = d3.scaleLinear()
                        .domain([cDeltaHigh, 0, cDeltaLow]) // should be zero
                        .range(["green", "yellow", "red"]);
//----------

  var radiusScale = d3.scaleSqrt().domain([volumeLow, volumeHigh]).range([9, 25]);

  var radiusAttr = function(d){ return radiusScale(d.sharesnow);}
  var moRadiusAttr = function(d){ return radiusScale(d.sharesnow);}

  var width = 1000,
  height = 300;
  if (2 * Math.sqrt(11*12*data.length) > height) {
    height = 2 * Math.sqrt(15*15*data.length);
  }

  var tip = d3.tip()
            .attr('class', 'd3-tip')
            .html(function(d) {return 'CIK: ' +d.cik
            +'</br> Insitution Name: ' +d.institution
            +'</br> Current no of shares: ' + d.sharesnow
            +'</br> No of shares from last filing: ' + d.shareslast
            +'</br> Change in holding: ' + d.change;})
  // var stockTickr = prompt("Please enter the tickr: ")
  var svg = d3.select("#chart")
    .append("svg")
    .attr("height", height)
    .attr("width", width)
    .append("g")
    .call(tip);

//------------


  //simulation is a collection of forces to interact with circles
  //get circle into middle
  var simulation = d3.forceSimulation()
    // .force("x", d3.forceX(width/2).strength(0.0))
    // .force("y", d3.forceY(height/2).strength(0.0))
    .force("collide", d3.forceCollide(moRadiusAttr))
//forceCenter
  d3.queue()
    .defer(d3.csv, pathcsv)
    .await(ready)

  function ready(error, datapoints){
    var circles = svg.append("g").selectAll(".gene")
                  .data(datapoints)
                  .enter().append("circle")
                  .attr("class", "gene")
                  // .attr("r",10)
                  .attr("r", radiusAttr)
                  .attr("cursor", "pointer")
                  .attr("id", function(d){
                    return d.cik})
                  .attr("fill", function(d){if(+d.change > 0)
                          {
                            pChange++;
                          return "green";

                        }else if(+d.change < 0){
                          negChange++;
                          return "red";

                        }else{
                            noChange++;
                          return "yellow";

                        };})
                  .attr("stroke", "grey")
                  .on('mouseover', tip.show)
                  .on('mouseout', tip.hide);
                  // .sort(d3.ascending);
                  // .sort( function(a, b) { return  -1;})
      // .attr("onmouseover","evt.target.setAttribute('fill', 'orange')")
      // .attr("onmouseout", "evt.target.setAttribute('fill','#1E90FF')")
      // .attr("onclick","getid(this)")
      // .attr("onmouseover","evt.target.setAttribute('r', 'moRadiusAttr')")
      // .attr("onmouseout", "evt.target.setAttribute('r','radiusAttr')")
      var label = svg.append("g").selectAll(".text")
                  .data(datapoints)
                  .enter().append("text")
                  .text(function(d, i){return +i+1})
                  .style("text-anchor", "middle")
                  .style("fill", "black")
                  .style("font-family", "Lato")
                  .style("font-weight", "bold")
                  .style("font-size", 8)

      var sumLabelData = [pChange, negChange, noChange, pChange + negChange + noChange];


      var summaryLbl = svg.append("g")
                  .selectAll(".text")
                  .data(sumLabelData)
                  .enter().append("text")
                  .text(function(d, i){
                    if (i == 0){
                      return "Increased positions: "+d;
                    }else if(i == 1){
                      return "Decreased positions: "+d;
                    }else if(i == 2){
                      return "Unchanged: "+d;
                    }else{
                      return "Total: "+d;
                    }
                  })
                  .style("text-anchor", "right")
                  .style("fill", function(d, i){
                    if (i == 0){
                      return "green";
                    }else if(i == 1){
                      return "red";
                    }else if(i == 2){
                      return "yellow";
                    }else{
                      return "black";
                    }
                  })
                  .style("font-family", "Lato")
                  .style("font-weight", "bold")
                  .style("font-size", 16)
                  // .transition()
                  // .duration(0)
                  // .delay(function (d, i) {return i * 10;})
                  .attr("x", function(d, i)
                    {
                      //group n squares for column
                      return width/8;
                    })
                  .attr("y", function(d, i)
                  {

                    return height/8+(18*i);
                  })
    simulation.nodes(datapoints)
      .on('tick', ticked)
    function ticked() {
      circles
        .attr("cx", function(d){
          return d.x
        })
        .attr("cy", function(d) {
          return d.y
        })
        .attr('transform', 'translate(' +width/2 +','+height/2+')');
        // .sort(d3.descending);
        label
          .attr("x", function(d){
            return d.x
          })
          .attr("y", function(d) {
            return d.y
          })
          .attr('transform', 'translate(' +width/2 +', '+height/2+')');
          // .sort(d3.descending);
    }
  }
})}


function waffleChart(){
    pathcsv = csvFolder + stockTickr + ".csv";
  d3.select('#chartB1').on('click', d3.select("svg").remove());
  d3.csv(pathcsv, function(data) {
  var width = 900,
      height = 75,
      totalNoGenes = 0,
      widthSquares = 20,
      heightSquares = 25,
      squareWidth = 40,
      squareHeight = 25,
      squareWidthV = 40,
      squareHeightV = 6,
      squareValue = 0,
      gap = 2,
      theData =[];
// this will generate dyanamic height of SVG canvas
// if the number of rows in waffle chart is taller than 600px
  var newHeight = ((squareHeight + gap)*((data.length)/widthSquares)) + 75;
  if (height < newHeight){
    height = newHeight;
  };

// create svg canvas
// appends svg to the DIV #chart
var tip = d3.tip()
          .attr('class', 'd3-tip')
          .html(function(d) {return 'CIK: ' +d.cik
                  +'</br> Insitution Name: ' +d.institution
                  +'</br> Current no of shares: ' + d.sharesnow
                  +'</br> No of shares from last filing: ' + d.shareslast
                  +'</br> Change in holding: ' + d.change;})

  var svg = d3.select("#chart")
    .append("svg")
    .attr("height", height)
    .attr("width", width)
    .append("g")
    .call(tip);



// generate year count array by looping through Json and pushing
// orginal json data is sorted based on year
// this additional remappin of data is to find the highest d.Count
// which is required to dynamically assign the .domain value while calculating scale
var volumeHigh = d3.max(data, function(d){ return +d.sharesnow});
var volumeLow = d3.min(data, function(d){ return +d.sharesnow});
// console.log(volumeHigh)
// console.log(volumeLow)
var cDeltaHigh = d3.max(data, function(d){ return +d.change}); //lowest price difference
var cDeltaLow = d3.min(data, function(d){ return +d.change});
var highestHigh = d3.max(data, function(d){return +d.sharesnow.substring(0, 5)});
var highestLow = d3.min(data, function(d){return +d.shareslast.substring(0, 5)});
var highestHighLabel = d3.max(data, function(d){return +d.sharesnow});
var highestLowLabel = d3.min(data, function(d){return +d.shareslast});

// scale for barchart

var colrScale = d3.scaleLinear() // color scale for price
                  .domain([cDeltaHigh, 0, cDeltaLow]) // should be zero
                  .range(["green", "yellow", "red"]);
var colrScaleV = d3.scaleLinear() //color scale for volume
                  .domain([volumeHigh, 0, volumeLow]) // should be zero
                  .range(["green", "yellow", "red"]);

  //================ waffle chart ==========================================

  //total no of hits across all genes
  totalVol = d3.sum(data, function(d) {return d.sharesnow;});
  //value of a square
  squareValue = totalVol/(widthSquares*heightSquares);
  //remap json data to variables
  data.forEach(function(d, i){
        d.Count = +d.sharesnow;
        d.units = Math.floor(d.sharesnow/squareValue);
        theData = theData.concat(
                  Array(d.units+1).join(1).split('').map(function(){
                    return{
                            squareValue:squareValue,
                            units: d.units,
                            count: d.Count,
                            groupIndex: 1
                    };
                  })
        );
  });

  console.log(data.length);
  console.log(newHeight);
  var waffleP = svg.append("g")
              .attr("transform", "translate(50, 50)")
              .selectAll("div")
              .data(data)
              .enter()
              .append("rect")
              .on('mouseover', tip.show)
              .on('mouseout', tip.hide)
              .attr('fill', function(d){return colrScale(+d.change);})
              .attr("width", squareWidth)
              .attr("height", squareHeight)
              .attr("stroke", function(d){if (+d.sharesnow == highestHighLabel){return "green"}
                    else if (+d.shareslast == highestLowLabel){return "red"}})
              .attr('stroke-width', '3')
              // .transition()
              // .duration(0)
              // .delay(function (d, i) {return i * 10;})
              .attr("x", function(d, i)
                {
                  //group n squares for column
                  col = i%widthSquares;
                  return (col*squareWidth) + (col*gap);
                })
              .attr("y", function(d, i)
              {
                row = Math.floor(i/widthSquares);
                return (row*squareHeight) + (row*gap);
              });
              var wafflev = svg.append("g")
                          .attr("transform", "translate(50, 50)")
                          .selectAll("div")
                          .data(data)
                          .enter()
                          .append("rect")
                          .on('mouseover', tip.show)
                          .on('mouseout', tip.hide)
                          .attr('fill', function(d){return colrScaleV(d.volumePercentage);})
                          .attr("width", squareWidthV)
                          .attr("height", squareHeightV)
                          // .transition()
                          // .duration(0)
                          // .delay(function (d, i) {return i * 10;})
                          .attr("x", function(d, i)
                            {
                              //group n squares for column
                              col = i%widthSquares;
                              return (col*squareWidth) + (col*gap);
                            })
                          .attr("y", function(d, i)
                          {
                            row = Math.floor(i/widthSquares);
                            return (row*squareHeight) + (row*gap);
                          })
              // .each(function(d){d3.select(this).append("title")
              //         .text(function(d){return "Avg Vol Difference : "
              //         +d.volumePercentage.substring(0, 5) + "%, Open: $"+d.Open+", Date:"+d.Date;})})

//d.volumePercentage/1.0e+6 millions
  //change square color based on percentile
                    // svg.selectAll("rect[percent = '30']")
                    //     .attr("fill", "#50D050");
                    // svg.selectAll("rect[percent = '60']")
                    //     .attr("fill", "yellow");
                    // svg.selectAll("rect[percent='100']")
                    //     .attr("fill", "#FF5733");

  // square label
     var labelindex = svg.append("g")
                 .attr("transform", "translate(68, 65)")
                 .selectAll(".text")
                       .data(data)
                       .enter().append("text")
                       .text(function(d, i){return +i+1})
                       .style("text-anchor", "middle")
                       .style("fill", "black")
                       .style("font-family", "Lato")
                       .style("font-weight", "bold")
                       .style("font-size", 10)
                      //  .transition()
                      //  .duration(0)
                      //  .delay(function (d, i) {return i * 10;})
                       .attr("x", function(d, i)
                         {
                           //group n squares for column
                           col = i%widthSquares;
                           return (col*squareWidth) + (col*gap);
                         })
                       .attr("y", function(d, i)
                       {
                         row = Math.floor(i/widthSquares);
                         return (row*squareHeight) + (row*gap);
                       });
                       var labelHighLow = svg.append("g")
                                   .attr("transform", "translate(68, 65)")
                                   .selectAll(".text")
                                         .data(data)
                                         .enter().append("text")
                                         .text(function(d){if (+d.High == highestHighLabel){return "H"}
                                                            else if(+d.Low == highestLowLabel){return "L"}})
                                         .style("text-anchor", "middle")
                                         .style("fill", "black")
                                         .style("font-family", "Lato")
                                         .style("font-weight", "bold")
                                         .style("font-size", 10)
                                         .attr("vector-effect", "non-scaling-stroke")

                                         .attr("x", function(d, i)
                                           {
                                             //group n squares for column
                                             col = i%widthSquares;
                                             return (col*squareWidth) + (col*gap) - 13;
                                           })
                                         .attr("y", function(d, i)
                                         {
                                           row = Math.floor(i/widthSquares);
                                           return (row*squareHeight) + (row*gap) - 8;
                                         });

      var high= svg.append("g")
                    .attr("transform", "translate(80, 40)")
                    .append("text")
                    .text("High: $"+highestHigh+" | Low: $"+highestLow)
                    .style("text-anchor", "middle")
                    .style("fill", "black")
                    .style("font-family", "Lato")
                    .style("font-weight", "bold")
                    .style("font-size", 15)
                    .attr("x", 50)
                    .attr("y", 0)

})}

function upMove(){
    pathcsv = csvFolder + stockTickr + ".csv";
    d3.csv(pathcsv, function(data) {
  var highestHighLabel = d3.max(data, function(d){return +d.High});
  var highestLowLabel = d3.min(data, function(d){return +d.Low});
  d3.selectAll("rect")
     .attr("visibility", function(d){if (+d.priceMovement < 0){return "hidden"}});
     d3.selectAll("circle")
        .attr("visibility", function(d){if (+d.priceMovement < 0){return "hidden"}})
})}

function downMove(){
    pathcsv = csvFolder + stockTickr + ".csv";
    d3.csv(pathcsv, function(data) {
  var highestHighLabel = d3.max(data, function(d){return +d.High});
  var highestLowLabel = d3.min(data, function(d){return +d.Low});
  d3.selectAll("rect")
     .attr("visibility", function(d){if (+d.priceMovement > 0){return "hidden"}});
     d3.selectAll("circle")
        .attr("visibility", function(d){if (+d.priceMovement > 0){return "hidden"}})
})}

function lineChart(){
  pathcsv = csvFolder + stockTickr + ".csv";
  d3.select('#chartB1').on('click', d3.select("svg").remove()); // resets svg
  d3.csv(pathcsv, function(data) {
    var dates = d3.keys(data[0]).slice(4, 6)
  console.log(data)
  var svg = d3.select("#chart"),
    margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = svg.attr("width") - margin.left - margin.right,
    height = svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%Y%m%d");

var x = d3.scaleTime().range([0, width]),
    y = d3.scaleLinear().range([height, 0]),
    z = d3.scaleOrdinal(d3.schemeCategory10);

var line = d3.line()
    .curve(d3.curveBasis)
    .y(function(d) { return y(d.temperature); })
    .data(dates)
    .x(function(d) { return x(d.dates); });


  if (error) throw error;

  var cities = data.columns.slice(1).map(function(id) {
    return {
      id: id,
      values: data.map(function(d) {
        return {date: d.date, temperature: d[id]};
      })
    };
  });

  x.domain(d3.extent(data, function(d) { return d.date; }));

  y.domain([
    d3.min(cities, function(c) { return d3.min(c.values, function(d) { return d.temperature; }); }),
    d3.max(cities, function(c) { return d3.max(c.values, function(d) { return d.temperature; }); })
  ]);

  z.domain(cities.map(function(c) { return c.id; }));

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("fill", "#000")
      .text("Temperature, ºF");

  var city = g.selectAll(".city")
    .data(cities)
    .enter().append("g")
      .attr("class", "city");

  city.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return z(d.id); });

  city.append("text")
      .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temperature) + ")"; })
      .attr("x", 3)
      .attr("dy", "0.35em")
      .style("font", "10px sans-serif")
      .text(function(d) { return d.id; });
});

function type(d, _, columns) {
  d.date = parseTime(d.date);
  for (var i = 1, n = columns.length, c; i < n; ++i) d[c = columns[i]] = +d[c];
  return d;
}
}
