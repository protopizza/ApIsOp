initChamps();
initItems();
initUI();

// import champion json file (includes all champions from both patches)
function initChamps(){
    $.getJSON('data/static/champions.json', function(data){
        var champsObj = data.data;
        champsFull = champsObj;
        // console.log(champsObj);
        //
        temp_champs = [];
        $.each(data.data, function(key, val){
            temp_champs.push(val["name"]);
        })
        temp_champs.sort();

        $.each(temp_champs, function(i, val){
            $.each(data.data, function(key, ob){
                if(val == ob["name"]) {
                    champs.push(key);
                    return false;
                }
            })
        })


        // console.log(champs);
        for( var i in champs ){
            $(".dropdown .menu").append(
                '<div class="item" data-value="' + champs[i] + '"><img class="ui avatar image" src="assets/champs/' + champs[i] + '.png">' + champsObj[champs[i]].name + '</div>');
        }
    })
}

// import static item files.
function initItems(){
    $.getJSON('data/static/items511.json', function(data){
        items511 = data.data;
    });
    $.getJSON('data/static/items514.json', function(data){
        items514 = data.data;
    });
    $.getJSON('data/static/jungle_enchantments.json', function(data){
        jungle511 = data['5.11'];
        jungle514 = data['5.14'];
    });
}

var checkFiveA = false;
var checkFiveB = false;
// initialize semantic's UI components.
// other semantic UI components must be initialized after DOM creation.
function initUI(){
    $('#fight-error').show();

    $('#champselect-A').dropdown({
        maxSelections: 5,
        onChange: function(val, text, $sel){
            if(val.split(',').length == 5){
                checkFiveA = true;
            }else{
                checkFiveA = false;
            }
            if(checkFiveA && checkFiveB){
                $('#fight').removeClass('disabled');
                $('#fight-error').hide();
                $('#fight, #randomize').css('margin-top', '15px');
            }else{
                $('#fight').addClass('disabled');
                $('#fight-error').show();
                $('#fight, #randomize').css('margin-top', '0');
            }
        }
    })
    $('#champselect-B').dropdown({
        maxSelections: 5,
        onChange: function(val, text, $sel){
            if(val.split(',').length == 5){
                checkFiveB = true;
            }else{
                checkFiveB = false;
            }
            if(checkFiveA && checkFiveB){
                $('#fight').removeClass('disabled');
                $('#fight-error').hide();
                $('#fight, #randomize').css('margin-top', '15px');
            }else{
                $('#fight').addClass('disabled');
                $('#fight-error').show();
                $('#fight, #randomize').css('margin-top', '0');
            }
        }
    })

    $("#fight").click(function() {
        // initialize rest of the page only when checkFive() passes.
        var dropdownA = $('#champselect-A').dropdown('get value');
        var dropdownB = $('#champselect-B').dropdown('get value');
        champsA = dropdownA.split(',');
        champsB = dropdownB.split(',');

        addFilterHandlers();
        getPatchData(champsA, champsB);
        addChampDOM();

        $('#champion-template').hide();
        $('#result').show();
        $('html,body').animate({
            scrollTop: $("#result").offset().top
        }, 'slow');
    });

    $("#randomize").click(function() {
        addRandomChampions()
        if(checkFive()){
            // initialize rest of the page only when checkFive() passes.
            addFilterHandlers();
            getPatchData(champsA, champsB);
            addChampDOM();

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
    console.log('dropdown A: ', dropdownA);
    console.log('dropdown B: ', dropdownB);
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
    // reset UI when filter handlers are invoked (new 5 champions selected);
    $('.patch-select > button').removeClass('positive active');
    $('.filter-buttons > img').removeClass('select-filter');
    $('#511').addClass('positive active');
    $('#unranked').addClass('select-filter');

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

        if(selections.length < 10 && id !== 'unranked'){
            $('#duplicate-warning').show();
        } else {
            $('#duplicate-warning').hide();
        }
    })
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
}

function addRandomChampions(){
    var dropdownACurrent = $('#champselect-A').dropdown('get value');
    var dropdownBCurrent = $('#champselect-B').dropdown('get value');

    if( dropdownACurrent.length > 0 ){
        dropdownACurrent = dropdownACurrent.split(',');
    }
    if( dropdownBCurrent.length > 0 ){
        dropdownBCurrent = dropdownBCurrent.split(',');
    }

    if( dropdownACurrent.length == 5 && dropdownBCurrent.length == 5){
        $('#champselect-A').dropdown('clear');
        $('#champselect-B').dropdown('clear');
        dropdownACurrent = $('#champselect-A').dropdown('get value');
        dropdownBCurrent = $('#champselect-B').dropdown('get value');

        if( dropdownACurrent.length > 0 ){
            dropdownACurrent = dropdownACurrent.split(',');
        }
        if( dropdownBCurrent.length > 0 ){
            dropdownBCurrent = dropdownBCurrent.split(',');
        }
    }


    var dropdownANeeded = 5 - dropdownACurrent.length;
    var dropdownBNeeded = 5 - dropdownBCurrent.length;

    var teamARandom = [];
    var teamBRandom = [];

    // console.log(dropdownANeeded);
    // console.log(dropdownBNeeded);
    for(var i = 0; i < dropdownANeeded; ) {
        var rand = champs[Math.floor(Math.random()*champs.length)];
        // console.log(rand);
        if($.inArray(rand, dropdownACurrent) == -1) {
            if($.inArray(rand, teamARandom) == -1) {
                teamARandom.push(rand)
                i++;
            }
        }
    }

    for(var i = 0; i < dropdownBNeeded; ) {
        var rand = champs[Math.floor(Math.random()*champs.length)];
        // console.log(rand);
        if($.inArray(rand, dropdownACurrent) == -1) {
            if($.inArray(rand, teamARandom) == -1) {
                if($.inArray(rand, dropdownBCurrent) == -1) {
                    if($.inArray(rand, teamBRandom) == -1) {
                        teamBRandom.push(rand)
                        i++;
                    }
                }
            }
        }
    }

    for(var i in teamARandom){
        $('#champselect-A').dropdown('set selected', teamARandom[i]);
    }
    for(var i in teamBRandom){
        $('#champselect-B').dropdown('set selected', teamBRandom[i]);
    }
}