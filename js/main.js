initChamps();
initItems();
initUI();

// import champion json file (includes all champions from both patches)
function initChamps(){
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
                '<div class="item" data-value="' + champs[i] + '"><img class="ui avatar image" src="assets/champs/' + champs[i] + '.png">' + champsObj[champs[i]].name + '</div>');
        }
    })
}

// import 5.11 & 5.14 items separately since same items may have different IDs.
function initItems(){
    $.getJSON('data/static/items511.json', function(data){
        items511 = data.data;
    })
    $.getJSON('data/static/items514.json', function(data){
        items514 = data.data;
    })
}

// initialize semantic's UI components.
// other semantic UI components must be initialized after DOM creation.
function initUI(){
    $('.ui.dropdown').dropdown({
        maxSelections: 5
    });
    
    $("#fight").click(function() {
        if(checkFive()){
            // initialize rest of the page only when checkFive() passes.
            addFilterHandlers();
            getPatchData(champsA, champsB);
            addChampDOM();

            $('.ui.accordion').accordion();

            $('#champion-template').hide();
            $('#result').show();
            $('html,body').animate({
                scrollTop: $("#result").offset().top
            }, 'slow');
        }
    });
}

// function to make sure both dropdowns have 5 champions each selected.
function checkFive(){
    var dropdownA = $('#champselect-A').dropdown('get value');
    var dropdownB = $('#champselect-B').dropdown('get value');
    if( dropdownA.length > 0 ){
        dropdownA = dropdownA.split(',');
    }
    if( dropdownB.length > 0 ){
        dropdownB = dropdownB.split(',');
    }
    if( dropdownA == null || dropdownB == null || dropdownA.length < 5 || dropdownB.length < 5){
        alert('Please select 5 champions for both teams.');
        return false;
    }
    champsA = dropdownA;
    champsB = dropdownB;
    return true;
}

// some globals to be used later.
var currentPatch = 511;
var currentRank = 'unranked';

// add mouse handlers to the UI section that filters data by rank and patch.
function addFilterHandlers(){
    $('.patch-select > button').click(function(){
        var id = $(this).attr('id');
        $('#'+id).addClass('positive active');
        $('.patch-select > button').not('#'+id).removeClass('positive active');
        currentPatch = id;
        fillChampDetails(null, currentPatch, currentRank);
    })
    $('.filter-buttons > img').click(function(){
        var id = $(this).attr('id');
        $('#'+id).addClass('select-filter');
        $('.filter-buttons > img').not('#'+id).removeClass('select-filter');
        currentRank = id;
        fillChampDetails(null, currentPatch, currentRank);
    })
}