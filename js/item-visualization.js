var csvKeys = ['ITEM_ID','511-NO_RANK-WinRate','511-NO_RANK-BuyRate','511-BRONZE-WinRate','511-BRONZE-BuyRate','511-SILVER-WinRate','511-SILVER-BuyRate','511-GOLD-WinRate','511-GOLD-BuyRate','511-PLATINUM-WinRate','511-PLATINUM-BuyRate','511-DIAMOND+-WinRate','511-DIAMOND+-BuyRate','514-NO_RANK-WinRate','514-NO_RANK-BuyRate','514-BRONZE-WinRate','514-BRONZE-BuyRate','514-SILVER-WinRate','514-SILVER-BuyRate','514-GOLD-WinRate','514-GOLD-BuyRate','514-PLATINUM-WinRate','514-PLATINUM-BuyRate','514-DIAMOND+-WinRate','514-DIAMOND+-BuyRate']
// some globals to be used later.
var currentPatch = 511;
var currentRank = 'NO_RANK';
var currentWinBuy = 'win';
var currentKeyWR = '511-NO_RANK-WinRate';
var currentKeyBR = '511-NO_RANK-BuyRate';
var sort = false;

var margin = {top: 20, right: 250, bottom: 50, left: 45},
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
var svg = d3.select("#vis").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// open csv file:
function drawChart(update, sort){
  d3.csv('data/viz/items.csv').row(function(d){
      return{
        ITEM_ID: d.ITEM_ID,
        winRate: +d[currentKeyWR],
        notWinRate: 100 - +d[currentKeyWR],
        buyRate: +d[currentKeyBR],
        notBuyRate: 100 - +d[currentKeyBR]
      };
  })
  .get(function(error, data) {
    if (error) throw error;

    var sorted = itemsAry;
    sorted.sort(function (a, b){
      if(a.name < b.name) return -1;
        if(a.name > b.name) return 1;
        return 0;
    })

    var result = [];
    sorted.forEach(function(i){
      var found = false;
      data.filter(function(item) {
        if(!found && item['ITEM_ID'] == i.key) {
          result.push(item);
          found = true;
          return false;
        } else
          return true;
      })
    })

    data = result;

    // define color domain
    if( currentWinBuy == 'win' ){
      color.domain(d3.keys(data[0]).filter(function(key) { return key == "winRate" || key == 'notWinRate'; }));
    }
    if( currentWinBuy == 'buy' ){
      color.domain(d3.keys(data[0]).filter(function(key) { return key == "buyRate" || key == 'notBuyRate'; }));
    }

    data.forEach(function(d) {
      var y0 = 0;
      d.rate = color.domain().map(function(name) {
        return {name: name, y0: y0, y1: y0 += +d[name]};
      });
      d.rate.forEach(function(d) { d.y0 /= y0; d.y1 /= y0; });
    });

    if(sort){
      data.sort(function(a, b) { return b.rate[0].y1 - a.rate[0].y1; });
    }
    // console.log(data);

    x.domain(data.map(function(d) { return d['ITEM_ID']; }));

    // append axes
    drawTicks(data, update);
    drawBars(data, update, currentWinBuy);

    if(!update){
      // draw 50% line only after rendering percentage values
      svg.append("g")
        .attr("class", "midaxis")
        .attr("transform", "translate(0," + height/2 + ")")
        .style({ 'stroke': 'rgba(0,0,0,0.65)', 'fill': 'none', 'stroke-width': '1px'})
        .call(midAxis);
    }
  });
}

function drawTicks(data, update){
  if(!update){
    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .style({ 'fill': 'rgba(0,0,0,0)'})
      .call(xAxis);

    // convert x-axis to icons
    svg.select("x.axis").selectAll("text").remove();
  }

  var ticks = svg.selectAll("image").data(data);
      ticks.enter().append("svg:image")
           .attr("xlink:href", function (d) { return 'assets/items/514/' + d['ITEM_ID'] + '.jpg'; })
           .attr("width", 30)
           .attr("height", 30)
           .attr('transform', function (d){ return "translate(" + x(d['ITEM_ID']) + ",0)"; })
           .attr('y', function(d){ return height+2; });
      ticks.exit().remove();
      ticks.attr("xlink:href", function (d) { return 'assets/items/514/' + d['ITEM_ID'] + '.jpg'; })
      ticks.transition().duration(500)
           .attr('transform', function (d){ return "translate(" + x(d['ITEM_ID']) + ",0)"; });

      ticks.append("rect")
           .attr("width", 30)
           .attr("height", 30)
           .attr('y', function (d){ return height+2; })
           .attr('rx', 2)
           .attr('ry', 2)
           .attr('stroke-width', '1')
           .attr('stroke', 'rgba(0,0,0,0.65)');
      ticks.exit().remove();
      ticks.transition().duration(500)
           .attr('transform', function (d){ return "translate(" + x(d['ITEM_ID']) + ",0)"; })

  if(!update){
    // remove x-axis tick lines
    svg.selectAll('.tick line')
     .attr({'y2': 0});

    svg.append("g")
      .attr("class", "y axis")
      .style({ 'fill': 'rgba(0,0,0,0.65)'})
      .call(yAxis);
  }
}

function drawBars(data, update, type){
  // define and append percentage values for win rate per item
  var item = svg.selectAll(".item").data(data);
      item.enter().append("g")
        .attr("class", "item")
        .attr("transform", function(d) { return "translate(" + x(d['ITEM_ID']) + ",0)"; });

      item.exit().remove();
      item.transition().duration(500)
          .attr("transform", function(d) { return "translate(" + x(d['ITEM_ID']) + ",0)"; });

  var rect = item.selectAll("rect").data(function(d){ return d.rate; });
      rect.enter().append("rect")
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.y1); })
          .attr("height", function(d) { return y(d.y0) - y(d.y1); })
          .style("fill", function(d) { return color(d.name); });

      rect.exit().remove();
      rect.transition().duration(500)
          .attr("y", function(d) { return y(d.y1); })
          .attr("height", function(d) { return y(d.y0) - y(d.y1); })

  // append labels
  var labelTotalCounted = svg.append('text')
    .attr('x', function(d){ return 800 - margin.right - 40; })
    .attr('y', function(d){ return 12; })
    .style('opacity', 0);

  var labelNegativeRateSub = svg.append('text')
        .attr('x', function(d){ return 800 - margin.right - 40; })
        .attr('y', function(d){ return height/4 - 10; })
        .style('opacity', 0);

  var labelNegativeRate = svg.append('text')
        .attr('x', function(d){ return 800 - margin.right - 40; })
        .attr('y', function(d){ return height/4 + 10; })
        .style('font-size', '1.2em')
        .style('fill', 'rgb(203, 92, 92)')
        .style('opacity', 0);

  var labelName = svg.append('text')
    .attr('x', function(d){ return 800 - margin.right - 40; })
    .attr('y', function(d){ return height/2 + 5; })
    .style('font-size', '1.1em')
    .style('font-weight', 'bold')
    .style('opacity', 0);

  var labelPositiveRate = svg.append('text')
    .attr('x', function(d){ return 800 - margin.right - 40; })
    .attr('y', function(d){ return height/4*3 - 10; })
    .style('font-size', '1.2em')
    .style('fill', 'rgb(40, 184, 200)')
    .style('opacity', 0);

  var labelPositiveRateSub = svg.append('text')
    .attr('x', function(d){ return 800 - margin.right - 40; })
    .attr('y', function(d){ return height/4*3 + 10; })
    .style('opacity', 0);

  if(type == 'win'){
      labelPositiveRateSub.text('Win Rate');
      labelNegativeRateSub.text('Loss Rate');
  }
  if(type == 'buy'){
      labelPositiveRateSub.text('Purchase Rate');
      labelNegativeRateSub.text('Not purchased');
  }

  // add hover handlers
  item.on("mouseover", mouseOver);
  item.on("mouseout", mouseOut);

  function mouseOver(d){
    var name = items[d.ITEM_ID].name;
    var detail = items[d.ITEM_ID].detail;
    labelName.text(name).style('opacity', 1);
    if(type == 'win'){
      labelPositiveRate.text(parseFloat(d.winRate).toFixed(2) + '%').style('opacity', 1);
      labelNegativeRate.text(parseFloat(d.notWinRate).toFixed(2) + '%').style('opacity', 1);
    }
    if(type == 'buy'){
      labelPositiveRate.text(parseFloat(d.buyRate).toFixed(2) + '%').style('opacity', 1);
      labelNegativeRate.text(parseFloat(d.notBuyRate).toFixed(2) + '%').style('opacity', 1);
    }
    labelPositiveRateSub.style('opacity', 1);
    labelNegativeRateSub.style('opacity', 1);

    var additionalInfo = items[d.ITEM_ID].getFilteredData(currentPatch, currentRank);
    labelTotalCounted
      .text(additionalInfo.matchesCounted + ' matches analyzed')
      .style('opacity', 1);
  }

  function mouseOut(d){
    labelName.style('opacity', 0);
    labelPositiveRate.style('opacity', 0);
    labelNegativeRate.style('opacity', 0);
    labelPositiveRateSub.style('opacity', 0);
    labelNegativeRateSub.style('opacity', 0);
    labelTotalCounted.style('opacity', 0);
  }
}

// add mouse handlers to the UI section that filters data by rank and patch.
function addFilterHandlers(){
    // reset UI when filter handlers are invoked (new 5 champions selected);
    $('.patch-select > button').removeClass('positive active');
    $('.sort-select > button').removeClass('positive active');
    $('.type-select > button').removeClass('positive active');
    $('.filter-buttons > img').removeClass('select-filter');
    $('#511').addClass('positive active');
    $('#unranked').addClass('select-filter');
    $('#sort-name').addClass('positive active');
    $('#type-win').addClass('positive active');
    $('.ui.checkbox').checkbox();

    $('#unranked').popup({
        content  : 'Display statistics for normal matches (players can be at any tier).',
    })
    $('#bronze').popup({
        content  : 'Display statistics for ranked matches at Bronze tier.',
    })
    $('#silver').popup({
        content  : 'Display statistics for ranked matches at Silver tier.',
    })
    $('#gold').popup({
        content  : 'Display statistics for ranked matches at Gold tier.',
    })
    $('#platinum').popup({
        content  : 'Display statistics for ranked matches at Platinum tier.',
    })
    $('#diamond').popup({
        content  : 'Display statistics for ranked matches at Diamond or higher tier.',
    })
    $('#sort-name').popup({
        content  : 'Sort statistics by alphabetical order of the AP item name.',
    })
    $('#sort-rate').popup({
        content  : 'Sort statistics by win rate or buy rate of the AP item name.',
    })
    $('#type-buy').popup({
        content  : 'Sort statistics by purchase rate of the AP items.',
    })
    $('#type-win').popup({
        content  : 'Sort statistics by win rate of the AP items.',
    })

    $('.patch-select > button').click(function(){
        var id = $(this).attr('id');
        $('#'+id).addClass('positive active');
        $('.patch-select > button').not('#'+id).removeClass('positive active');
        if( parseInt(id) !== currentPatch ){
          currentPatch = id;
          currentKeyWR = currentPatch + '-' + currentRank + '-WinRate';
          currentKeyBR = currentPatch + '-' + currentRank + '-BuyRate';
          drawChart(true, sort, currentWinBuy);
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
        drawChart(true, sort, currentWinBuy);
    })
    $('.sort-select > button').click(function(){
      var id = $(this).attr('id');
      $('#'+id).addClass('positive active');
      $('.sort-select > button').not('#'+id).removeClass('positive active');
      if( id == 'sort-name' ){
        sort = false;
      }
      if( id == 'sort-rate'){
        sort = true;
      }
      drawChart(true, sort, currentWinBuy);
    })
    $('.type-select > button').click(function(){
      var id = $(this).attr('id');
      $('#'+id).addClass('positive active');
      $('.type-select > button').not('#'+id).removeClass('positive active');
      if( id == 'type-win' ){
        currentWinBuy = 'win';
      }
      if( id == 'type-buy'){
        currentWinBuy = 'buy';
      }
      drawChart(true, sort, currentWinBuy);
    })
}