var champs = [];
var champsFull = {};

$('.ui.accordion').accordion();
$('.ui.dropdown').dropdown({
    maxSelections: 5
});

$.getJSON('data/static/champions.json', function(data){
    var champsObj = data.data;
    champsFull = champsObj;
    // console.log(champsObj);
    $.each(data.data, function(key, val){
        champs.push(key);
    })

    champs.sort();
    // console.log(champs);
    for( var i in champs ){
        $(".dropdown .menu").append(
            '<div class="item" data-value="' + champs[i] + '"><img class="ui avatar image" src="assets/' + champs[i] + '.png">' + champsObj[champs[i]].name + '</div>');
    }
})

$('#champselect-A').dropdown('refresh');
$('#champselect-B').dropdown('refresh');
$("#fight").click(function() {
    if(checkFive()){
        for(var i = 0; i < champsA.length; i++){
            $('.sideA:eq(' + i + ')').find('img').attr('src', 'assets/' + champsA[i] + '.png');
            $('.sideA:eq(' + i + ')').find('.content').text(champsFull[champsA[i]].name);
            $('.sideB:eq(' + i + ')').find('img').attr('src', 'assets/' + champsB[i] + '.png');
            $('.sideB:eq(' + i + ')').find('.content').text(champsFull[champsB[i]].name);
        }

        $('#result').show();
        $('html,body').animate({
            scrollTop: $("#result").offset().top
        }, 'slow');


        // grab json data here
    }
});

var champsA = [];
var champsB = [];
function checkFive(){
    var dropdownA = $('#champselect-A').dropdown('get value');
    var dropdownB = $('#champselect-B').dropdown('get value');
    if( dropdownA.length > 0 ){
        dropdownA = dropdownA.split(',');
        // console.log('dropdownA:', dropdownA);
    }
    if( dropdownB.length > 0 ){
        dropdownB = dropdownB.split(',');
        // console.log('dropdownB:', dropdownB);
    }
    if( dropdownA == null || dropdownB == null || dropdownA.length < 5 || dropdownB.length < 5){
        alert('Please select 5 champions for both teams.');
        return false;
    }
    champsA = dropdownA;
    champsB = dropdownB;
    return true;
}

function downloadItems(){
    $.getJSON('data/static/items511.json', function(data){
        var itemsObj = data.data;
        $.each(data.data, function(key, val){

        })
    })
}