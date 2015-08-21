var selections = [];

function getPatchData(a, b){
    // merge two arrays of selected champions, as we don't need to save data twice.
    var c = a.concat(b.filter(function (item) {
        return a.indexOf(item) < 0;
    }));

    // get json files for each champ in team
    for(var i in c){
        (function(i) { // protects i in an immediately called function
            var key = c[i];
            $.getJSON('data/champion/' + key + '.json', function(data){
                var obj = data['NA'];
                var champ = new Champion(key);
                champ.setUnranked(obj['5.11']['NORMAL_5X5']['NO_RANK'],
                                  obj['5.14']['NORMAL_5X5']['NO_RANK']);
                champ.setRanked(obj['5.11']['RANKED_SOLO'],
                                obj['5.14']['RANKED_SOLO']);
                selections.push(champ);
            }).then(function(data){
                if( i == (c.length-1) ){
                    setTimeout(function(){
                        fillChampDetails(selections, 511, 'unranked');
                    },300);
                }
            })
        })(i);
    }
}

function fillChampDetails(sel, patch, rank){
    for(var i = 0; i < selections.length; i++){
        var dat = selections[i].defaultObj;
        var currItems = null;
        console.log(selections[i]);
        if(patch == 511){
            if( rank == 'unranked' ){
                dat = selections[i].patch511.unranked;
            }else{
                var rankKey = '';
                switch(rank){
                    case 'bronze':
                        rankKey = 'BRONZE';
                        break;
                    case 'silver':
                        rankKey = 'SILVER';
                        break;
                    case 'gold':
                        rankKey = 'GOLD';
                        break;
                    case 'platinum':
                        rankKey = 'PLATINUM';
                        break;
                    case 'diamond':
                        rankKey = 'DIAMOND+';
                        break;
                    default:
                        break;
                }
                dat = selections[i].patch511.ranked[rankKey];
            }
            currItems = items511;
        }
        if(patch == 514){
            if( rank == 'unranked' ){
                dat = selections[i].patch514.unranked;
            }else{
                var rankKey = '';
                switch(rank){
                    case 'bronze':
                        rankKey = 'BRONZE';
                        break;
                    case 'silver':
                        rankKey = 'SILVER';
                        break;
                    case 'gold':
                        rankKey = 'GOLD';
                        break;
                    case 'platinum':
                        rankKey = 'PLATINUM';
                        break;
                    case 'diamond':
                        rankKey = 'DIAMOND+';
                        break;
                    default:
                        break;
                }
                dat = selections[i].patch514.ranked[rankKey];
            }
            currItems = items514;
        }

        // win rate, kda, avg gold/min, total dmg to champs
        var champKey = selections[i].key;
        var winRate = dat.winRate;
        var kda = dat.averageKda;
            kda = parseFloat(kda).toFixed(2);
        var goldAvg = dat.averageGoldPerMin;
            goldAvg = parseFloat(goldAvg).toFixed(2);
        var dmg = dat.averageTotalDamageDealtToChampions;
            dmg = parseInt(dmg);
            dmg = addCommas(dmg);
        var commonItems = dat.mostCommonItems;
        var $dom = null;
        if($('.sideA').find('.'+champKey).length){
            $dom = $('.sideA').find('.'+champKey).find('.summary-stats');
            $dom.find('.win-rate').find('.value').text(winRate);
            $dom.find('.kda').find('.value').text(kda);
            $dom.find('.gold-min').find('.value').text(goldAvg);
            $dom.find('.tot-dmg').find('.value').text(dmg);
            var count = 0;
            for(var key in commonItems){
                var id = key;
                var time = commonItems[key].averageTimeBought;
                    time = 'approx. ' + parseInt(moment.duration(time, "milliseconds").as('minutes')) + ' minutes';
                var $items = $('.sideA').find('.'+champKey).find('.top-items');
                    var item = currItems[id];
                    var ext = '.jpg';
                    if( $.inArray(item.id, pngItems) !== -1 ){
                        ext = '.png';
                    }
                    $items.find('.item:eq('+count+')').find('img').attr('src', 'assets/items/'+ patch + '/' + item.id + ext);
                    $items.find('.item:eq('+count+')').find('.item-name').text(item.name);
                    $items.find('.item:eq('+count+')').find('.item-time').text(time);
                count++;
            }
        }
        if($('.sideB').find('.'+champKey).length){
            $dom = $('.sideB').find('.'+champKey).find('.summary-stats');
            $dom.find('.win-rate').find('.value').text(winRate);
            $dom.find('.kda').find('.value').text(kda);
            $dom.find('.gold-min').find('.value').text(goldAvg);
            $dom.find('.tot-dmg').find('.value').text(dmg);
            var count = 0;
            for(var key in commonItems){
                var id = key;
                var time = commonItems[key].averageTimeBought;
                    time = 'approx. ' + parseInt(moment.duration(time, "milliseconds").as('minutes')) + ' minutes';
                var $items = $('.sideB').find('.'+champKey).find('.top-items');
                    var item = currItems[id];
                    var ext = '.jpg';
                    if( $.inArray(item.id, pngItems) !== -1 ){
                        ext = '.png';
                    }
                    $items.find('.item:eq('+count+')').find('img').attr('src', 'assets/items/'+ patch + '/' + item.id + ext);
                    $items.find('.item:eq('+count+')').find('.item-name').text(item.name);
                    $items.find('.item:eq('+count+')').find('.item-time').text(time);
                count++;
            }
        }
    }
}

function addChampDOM(){
    for(var i = 0; i < MAX_CHAMPS_PER_TEAM; i++){
        var champDOM_a = $('#champion-template').clone();
            champDOM_a.appendTo('.sideA').removeAttr('id').addClass(champsA[i]);
            champDOM_a.find('.champ-name').text(champsFull[champsA[i]].name);
            champDOM_a.find('.champ-img').attr('src', 'assets/champs/' + champsA[i] + '.png');
            champDOM_a.show();

        var champDOM_b = $('#champion-template').clone();
            champDOM_b.appendTo('.sideB').removeAttr('id').addClass(champsB[i]);
            champDOM_b.find('.champ-name').text(champsFull[champsB[i]].name);
            champDOM_b.find('.champ-img').attr('src', 'assets/champs/' + champsB[i] + '.png');
            champDOM_b.show();

        if( i == 0 ){
            champDOM_a.find('.champ-tab').addClass('active');
            champDOM_b.find('.champ-tab').addClass('active');
        }
    }
}

function addCommas(nStr){
    nStr += '';
    var x = nStr.split('.');
    var x1 = x[0];
    var x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
        x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }
    return x1 + x2;
}

/*  
    TODO: merge this with fillChampDetails
*/
function refreshDetail(type, id){
    if(type == 'patch'){

    }
    if(type == 'rank'){

    }
}