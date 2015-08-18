var champs = [];

$('.ui.dropdown').dropdown({
    maxSelections: 5
});

$.getJSON('data/static/champions.json', function(data){
    var champsObj = data.data;
    console.log(champsObj);
    $.each(data.data, function(key, val){
        champs.push(key);
    })

    champs.sort();
    console.log(champs);
    for( var i in champs ){
        $(".dropdown .menu").append(
            '<div class="item" data-value="' + champs[i] + '"><img class="ui avatar image" src="assets/' + champs[i] + '.png">' + champsObj[champs[i]].name + '</div>');
    }
})

$('#champselect-A').dropdown('refresh');
$('#champselect-B').dropdown('refresh');