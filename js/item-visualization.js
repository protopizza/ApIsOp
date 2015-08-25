function initChart(){
  // define margins, width, height of chart container
  var margin = {top: 20, right: 100, bottom: 50, left: 50},
      width = 800 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  // define x data type
  var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);

  // define y data type
  var y = d3.scale.linear()
      .rangeRound([height, 0]);

  // define colors to be used per item
  var color = d3.scale.ordinal()
      .range(["#28B8C8", "#CB5C5C"]);

  // define x-axis settings
  var xAxis = d3.svg.axis()
      .scale(x)
      .ticks(0)
      .orient("bottom");

  // define y-axis settings
  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickFormat(d3.format(".0%"));

  var midAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  // append main chart container
	var svg = d3.select("#winrate").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  // open csv file:
  d3.csv("data/viz/items.csv", function(error, data) {
    if (error) throw error;

    color.domain(d3.keys(data[0]).filter(function(key) { return key == "511-NO_RANK-WinRate" || key == "511-NO_RANK-BuyRate"; }));

    data.forEach(function(d) {
      var y0 = 0;
      d.winRate = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
      d.winRate.forEach(function(d) { d.y0 /= y0; d.y1 /= y0; });
    });

    data.sort(function(a, b) { return b.winRate[0].y1 - a.winRate[0].y1; });

    // define domain values for x-axis
  	x.domain(data.map(function(d) {
      var key = d['ITEM_ID'];
      return items[key].name; 
    }));

    // append axes
    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .style({ 'fill': 'rgba(0,0,0,0)'})
      .call(xAxis);

    svg.select("x.axis").selectAll("text").remove();
    var ticks = svg.select(".axis").selectAll(".tick").data(data)
                  .append("svg:image")
                  .attr("xlink:href", function (d) { return 'assets/items/514/' + d['ITEM_ID'] + '.jpg'; })
                  .attr("width", 38)
                  .attr("height", 38)
                  .attr('x', -19)
                  .attr('y', 5);

    svg.select(".axis").selectAll(".tick")
                  .append("rect")
                  .attr("width", 38)
                  .attr("height", 38)
                  .attr('x', -19)
                  .attr('y', 5)
                  .attr('rx', 2)
                  .attr('ry', 2)
                  .attr('stroke-width', '1')
                  .attr('stroke', 'rgba(0,0,0,0.65)');

    svg.selectAll('.tick line')
     .attr({'y2': 0});

    svg.append("g")
      .attr("class", "y axis")
      .style({ 'fill': 'rgba(0,0,0,0.65)'})
      .call(yAxis);

    // define and append percentage values for win rate per item
    var item = svg.selectAll(".item").data(data)
      .enter().append("g")
        .attr("class", "item")
        .attr("transform", function(d) { return "translate(" + x(items[d['ITEM_ID']].name) + ",0)"; });

    item.selectAll("rect")
          .data(function(d) { return d.winRate; })
        .enter().append("rect")
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.y1); })
          .attr("height", function(d) { return y(d.y0) - y(d.y1); })
          .style("fill", function(d) { return color(d.name); });

    svg.append("g")
      .attr("class", "midaxis")
      .attr("transform", "translate(0," + height/2 + ")")
      .style({ 'stroke': 'rgba(0,0,0,0.65)', 'fill': 'none', 'stroke-width': '1px'})
      .call(midAxis);
  });
}