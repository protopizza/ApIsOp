initChamps();
initUI();

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

function initUI(){
    $('.ui.dropdown').dropdown({
        maxSelections: 5
    });
    
    $("#fight").click(function() {
        if(checkFive()){
            getPatchData(champsA, champsB);
            addChampDOM();
            addFilterHandlers();

            $('.ui.accordion').accordion();

            $('#champion-template').remove();
            $('#result').show();
            $('html,body').animate({
                scrollTop: $("#result").offset().top
            }, 'slow');
        }
    });
}

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

function addFilterHandlers(){
    $('.patch-select > button').click(function(){
        var id = $(this).attr('id');
        $('#'+id).addClass('positive active');
        $('.patch-select > button').not('#'+id).removeClass('positive active');
        // refreshDetail('patch', id);
    })
    $('.filter-buttons > img').click(function(){
        var id = $(this).attr('id');
        $('#'+id).addClass('select-filter');
        $('.filter-buttons > img').not('#'+id).removeClass('select-filter');
        // refreshDetail('rank', id);
    })
}