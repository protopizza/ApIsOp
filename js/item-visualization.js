var csvKeys = ['ITEM_ID','511-NO_RANK-WinRate','511-NO_RANK-BuyRate','511-BRONZE-WinRate','511-BRONZE-BuyRate','511-SILVER-WinRate','511-SILVER-BuyRate','511-GOLD-WinRate','511-GOLD-BuyRate','511-PLATINUM-WinRate','511-PLATINUM-BuyRate','511-DIAMOND+-WinRate','511-DIAMOND+-BuyRate','514-NO_RANK-WinRate','514-NO_RANK-BuyRate','514-BRONZE-WinRate','514-BRONZE-BuyRate','514-SILVER-WinRate','514-SILVER-BuyRate','514-GOLD-WinRate','514-GOLD-BuyRate','514-PLATINUM-WinRate','514-PLATINUM-BuyRate','514-DIAMOND+-WinRate','514-DIAMOND+-BuyRate']
// some globals to be used later.
var currentPatch = 511;
var currentRank = 'unranked';
var currentKeyWR = '511-NO_RANK-WinRate'
var currentKeyBR = '511-NO_RANK-BuyRate'

function initChart(){
  // define margins, width, height of chart container
  var margin = {top: 20, right: 250, bottom: 50, left: 50},
      width = 800 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  // define x data type
  var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);

  // define y data type
  var y = d3.scale.linear()
      .range([height, 0]);

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
  d3.csv('data/viz/items-'+currentKeyWR+'.csv', function(error, data) {
    if (error) throw error;
    
    // define color domain
    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "ITEM_ID"; }));

    data.forEach(function(d) {
      var y0 = 0;
      d.win = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
      d.win.forEach(function(d) { d.y0 /= y0; d.y1 /= y0; });
    });

    data.sort(function(a, b) { return b.win[0].y1 - a.win[0].y1; });
    console.log(data);

    x.domain(data.map(function(d) { return d['ITEM_ID']; }));

    // append axes
    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .style({ 'fill': 'rgba(0,0,0,0)'})
      .call(xAxis);

    // convert x-axis to icons
    svg.select("x.axis").selectAll("text").remove();
    var ticks = svg.select(".axis").selectAll(".tick").data(data)
                  .append("svg:image")
                  .attr("xlink:href", function (d) { return 'assets/items/514/' + d['ITEM_ID'] + '.jpg'; })
                  .attr("width", 30)
                  .attr("height", 30)
                  .attr('x', -15)
                  .attr('y', 5);
    svg.select(".axis").selectAll(".tick")
                  .append("rect")
                  .attr("width", 30)
                  .attr("height", 30)
                  .attr('x', -15)
                  .attr('y', 5)
                  .attr('rx', 2)
                  .attr('ry', 2)
                  .attr('stroke-width', '1')
                  .attr('stroke', 'rgba(0,0,0,0.65)');

    // remove x-axis tick lines
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
        .attr("transform", function(d) { return "translate(" + x(d['ITEM_ID']) + ",0)"; });

        item.selectAll("rect").data(function(d){ return d.win; })
          .enter().append("rect")
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.y1); })
            .attr("height", function(d) { return y(d.y0) - y(d.y1); })
            .style("fill", function(d) { return color(d.name); });

    // draw 50% line only after rendering percentage values
    svg.append("g")
      .attr("class", "midaxis")
      .attr("transform", "translate(0," + height/2 + ")")
      .style({ 'stroke': 'rgba(0,0,0,0.65)', 'fill': 'none', 'stroke-width': '1px'})
      .call(midAxis);

    svg.selectAll('.item').on('mouseover', mouseOver).on('mouseout', mouseOut);

    function mouseOver(d){
      // filter for selected state.
      // var st = data.filter(function(s){ console.log(s); return s.State == d[0];})[0],
          // nD = d3.keys(st.freq).map(function(s){ return {type:s, freq:st.freq[s]};});
         
      // call update functions of pie-chart and legend.    
      // pC.update(nD);
      // leg.update(nD);
    }

    function mouseOut(d){
      // reset the pie-chart and legend.    
      // pC.update(tF);
      // leg.update(tF);
    }
  });
}

// add mouse handlers to the UI section that filters data by rank and patch.
function addFilterHandlers(){
    // reset UI when filter handlers are invoked (new 5 champions selected);
    $('.patch-select > button').removeClass('positive active');
    $('.filter-buttons > img').removeClass('select-filter');
    $('#511').addClass('positive active');
    $('#unranked').addClass('select-filter');
    
    $('.patch-select > button').click(function(){
        var id = $(this).attr('id');
        $('#'+id).addClass('positive active');
        $('.patch-select > button').not('#'+id).removeClass('positive active');
        if( parseInt(id) !== currentPatch ){
          currentPatch = id;
          currentKeyWR = currentPatch + '-' + currentRank + '-WinRate';
          currentKeyBR = currentPatch + '-' + currentRank + '-BuyRate';
          console.log('clicked:', currentPatch, currentRank);
        }
    })
    $('.filter-buttons > img').click(function(){
        var id = $(this).attr('id');
        $('#'+id).addClass('select-filter');
        $('.filter-buttons > img').not('#'+id).removeClass('select-filter');
        currentRank = id;
        switch(id){
          case 'unranked':
            currentRank = 'NO_RANK';
            break;
          case 'bronze':
            currentRank = 'BRONZE';
            break;
          case 'silver':
            currentRank = 'SILVER';
            break;
          case 'gold':
            currentRank = 'GOLD';
            break;
          case 'platinum':
            currentRank = 'PLATINUM';
            break;
          case 'diamond':
            currentRank = 'DIAMOND+';
            break;
          default:
            break;
        }
        currentKeyWR = currentPatch + '-' + currentRank + '-WinRate';
        currentKeyBR = currentPatch + '-' + currentRank + '-BuyRate';
        console.log('clicked:', currentPatch, currentRank);
    })
}