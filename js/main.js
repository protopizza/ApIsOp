var champs = [];

$('.ui.dropdown').dropdown({
    maxSelections: 5
});

$.getJSON('data/static/champions.json', function(data){
    $.each(data.data, function(key, val){
        champs.push(val.name);
    })
    champs.sort();

    for( var i in champs ){
        $(".dropdown .menu").append('<div class="item">' + champs[i] + '</div>');
    }
})

$('#champselect-A').dropdown('refresh');
$('#champselect-B').dropdown('refresh');