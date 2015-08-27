var MISSINGNO  = ['Caitlyn', 'Jayce', 'TahmKench'];
var selections = [];

// get individual champ data for all selected champions from the two dropdowns,
// wait for data to load, and then call function to update UI (fillChampDetails)
function getPatchData(a, b){
    selections = [];
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

// update UI with appropriate champ data.
var updatedMissing = [];
var aggregateSummaryA = [];
var aggregateSummaryB = [];
function fillChampDetails(sel, patch, rank, type){
    var summaryAry = [];
    var summaryAryA = [];
    var summaryAryB = [];
    var totalMatchCount = 0;
    for(var i = 0; i < selections.length; i++){
        var champObj = selections[i].getFilteredData(patch, rank);

        // win rate, kda, avg gold/min, total dmg to champs
        var champKey = selections[i].key;
        var winRate = champObj.winRate;
        var kda = champObj.averageKda;
            kda = parseFloat(kda).toFixed(2);
        var goldAvg = champObj.averageGoldPerMin;
            goldAvg = parseFloat(goldAvg).toFixed(2);
        var dmg = champObj.averageTotalDamageDealtToChampions;
            dmg = parseFloat(dmg/1000).toFixed(2) + 'k';
        var commonItems = champObj.mostCommonItems;
        var matchesCounted = champObj.matchesCounted;
        totalMatchCount += matchesCounted;

        summaryAry.push({
            key: champKey,
            winRate: +winRate,
            kda: +kda,
            gold: +goldAvg,
            dmg: champObj.averageTotalDamageDealtToChampions,
            matchesCounted
        })

        // sort common items
        var sortedCommonItems = [];
        for(var key in commonItems){
            sortedCommonItems.push([key, commonItems[key]]);
        }
        sortedCommonItems.sort(function(a,b){ return b[1].buyPercentage - a[1].buyPercentage; });

        var $dom = null;
        if($('.ui.segments').find('.'+champKey).length){
            // modify inner content if there's actually no data (do this only after DOM creation)
            if(MISSINGNO.indexOf(champKey) > -1 && patch == 511 && updatedMissing.indexOf(champKey) == -1){
                $dom = $('.ui.segments').find('.'+champKey);
                $dom.find('.content.champ-tab').removeClass('active').hide();
                $dom.find('i.fa').hide();
                $dom.find('.title').removeClass('active').unwrap();
                $dom.find('.title').find('.sub.header').text('This champion has no data for 5.11.');
                $dom.find('.blue.statistic').find('.value').text('???');
                updatedMissing.push(champKey);
            }else{
                // check if user switches between ranks within 5.11
                if(updatedMissing.indexOf(champKey) > -1 && patch == 511){
                    continue;
                }
                // check if user switched to 5.14 when one of MISSINGNO champs were selected.
                // undo UI modification from above.
                if(updatedMissing.indexOf(champKey) > -1 && patch !== 511){
                    $dom = $('.ui.segments').find('.'+champKey);
                    $dom.wrapInner('<div class="ui accordion"></div>');
                    $dom.find('.content.champ-tab').show();
                    $dom.find('i.fa').show();
                    updatedMissing.splice(updatedMissing.indexOf(champKey), 1);
                    $('.ui.accordion').accordion('refresh');
                }
               // handle normal champ data.
                $dom = $('.ui.segments').find('.'+champKey);
                $dom.find('.title').find('.sub.header').text(matchesCounted + ' matches played');
                $dom.find('.title').find('.win-rate').find('.value').text(winRate);
                $dom.find('.kda').find('.value').text(kda);
                $dom.find('.gold-min').find('.value').text(goldAvg);
                $dom.find('.tot-dmg').find('.value').text(dmg);

                addItemDetails(sortedCommonItems, champKey, patch);
            }
        }
    }

    // add each match count
    // value * (match count of champion / total match count)
    console.log(champsA);
    console.log(champsB);
    console.log(summaryAry);
    // console.log('total matches:', totalMatchCount);
    summaryAry.forEach(function(o){
        var weightedKDA = o.kda * o.matchesCounted / totalMatchCount;
        var weightedGold = o.gold * o.matchesCounted / totalMatchCount;
        var weightedDmg = o.dmg * o.matchesCounted / totalMatchCount;
        var weightedWin = o.winRate * o.matchesCounted / totalMatchCount;
        weightedKDA = parseFloat(weightedKDA).toFixed(2);
        weightedGold = parseFloat(weightedGold).toFixed(2);
        weightedDmg = parseFloat(weightedDmg/1000).toFixed(2);
        weightedWin = parseFloat(weightedWin).toFixed(2);

        if(champsA.indexOf(o.key) > -1){
            summaryAryA.push({
                key: o.key,
                kda: +weightedKDA,
                gold: +weightedGold,
                dmg: +weightedDmg,
                win: +weightedWin
            })
        }else if(champsB.indexOf(o.key) > -1){
            summaryAryB.push({
                key: o.key,
                kda: +weightedKDA,
                gold: +weightedGold,
                dmg: +weightedDmg,
                win: +weightedWin
            })
        }
    });

    summaryAryA.forEach(function(i){
        var o = summaryAryA[i];
    })
    console.log(summaryAryA)
    summaryAryB.forEach(function(i){
        var o = summaryAryB[i];
    })
    console.log(summaryAryB)
}

function addItemDetails(commonItems, champKey, patch){
    var currItems   = null;
    var currJungle  = null;
    var MAX_LENGTH  = commonItems.length;
    $('.ui.segments').find('.'+champKey).find('.top-items').find('.item').not('#item-template').remove();
    if(patch == 511){
        currItems   = items511;
        currJungle  = jungle511;
    }else if(patch == 514){
        currItems   = items514;
        currJungle  = jungle514;
    }
    if(commonItems.length > 8){
        MAX_LENGTH = 8;
    }
    for(var i = 0; i < MAX_LENGTH; i++){
        var id = commonItems[i][0];
        var itemObj = currItems[id];
        var buyPercentage = parseFloat(commonItems[i][1].buyPercentage).toFixed(2);
        var time = commonItems[i][1].averageTimeBought;
            time = 'approx. ' + parseInt(moment.duration(time, "milliseconds").as('minutes')) + ' minutes';

        // double-check for duplicate champions, so that items don't propagate on both sides.
        $('.ui.segments').find('.'+champKey).each(function(i){
            var $items = $(this).find('.top-items');
            var $item = $items.find('#item-template').clone().attr('id', 'item'+patch+'-'+itemObj.id);
                $item.appendTo($items).css('display', 'inline-block');
                // $item.find('img').attr('src', 'assets/items/'+ patch + '/' + itemObj.id + '.jpg');

                // hover handler:
                // check jungle item
                if(currJungle.hasOwnProperty(id)){
                    itemObj.name = currJungle[id].full_name;
                }
                $item.find('.item-name').html('<b>' + itemObj.name + '</b>');
                $item.find('.item-time').text('Average purchase time: ' + time);
                $item.find('.item-percent').text(buyPercentage + '% bought');
                $item.find('.filler').popup({
                    inline: true
                });

            $('#item-template').hide();
        });
    }
}

// splits selected champions into two columns and adds DOMs
function addChampDOM(){
    $('.sideA').html('');
    $('.sideB').html('');
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

// helper function to add commas to every 3 digits.
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