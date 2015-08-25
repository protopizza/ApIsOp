function initChart(){
	// define margins, width, height of chart container
	var margin = {top: 20, right: 100, bottom: 30, left: 50},
	    width = 840 - margin.left - margin.right,
	    height = 300 - margin.top - margin.bottom;

	// define x data type
	var x = d3.scale.ordinal()
	    .rangeRoundBands([0, width], .1);

	// define y data type
	var y = d3.scale.linear()
	    .rangeRound([height, 0]);

    // define colors to be used per item
	var color = d3.scale.ordinal()
	    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

    // define x-axis settings
	var xAxis = d3.svg.axis()
	    .scale(x)
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

    // define domain values for x-axis
	x.domain(itemsAry.map(function(d) { console.log(d.name); return d.name; }));

    // append axes
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .style({ 'stroke': 'rgba(0,0,0,0.65)', 'fill': 'none', 'stroke-width': '1px'})
      .call(xAxis);

    svg.append("g")
      .attr("class", "midaxis")
      .attr("transform", "translate(0," + height/2 + ")")
      .style({ 'stroke': 'rgba(0,0,0,0.65)', 'fill': 'none', 'stroke-width': '1px'})
      .call(midAxis);

    svg.append("g")
      .attr("class", "y axis")
      .style({ 'fill': 'rgba(0,0,0,0.65)'})
      .call(yAxis);

    // define and append percentage values for win rate per item
    var item = svg.selectAll(".item").data(itemsAry)
      .enter().append("g")
        .attr("class", "item")
        .attr("transform", function(d) { return "translate(" + x(d.name) + ",0)"; });

    item.selectAll("rect").data(function(d) { console.log(d.patch511.unranked.winRate); return d.patch511.unranked.winRate; })
      .enter().append("rect")
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.y1); })
        .attr("height", function(d) { return y(d.y0) - y(d.y1); })
        .style("fill", function(d) { return color(d.name); });
}