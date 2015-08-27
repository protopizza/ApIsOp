addFilterHandlers();
initAPItems();

// import static item files.
function initAPItems(){
	$.getJSON('data/static/ap_item_changes.json', function(data){
		var obj = data;
		for(var i in obj){
			var name = obj[i].name;
			var change = obj[i].change;
			var ap = new APItem(i);
				ap.setDescription(name, change);
			items[i] = ap;
			itemsAry.push(ap);
		}
	}).then(function(){
		for(var i in ITEM_KEYS){
		    (function(i) { // protects i in an immediately called function
		    	var key = ITEM_KEYS[i];
		    	$.getJSON('data/item/' + key + '.json', function(data){
		    		var obj = data['NA'];
		    		items[key].setUnranked(obj['5.11']['NORMAL_5X5']['NO_RANK'],
		    		                  obj['5.14']['NORMAL_5X5']['NO_RANK']);
		    		items[key].setRanked(obj['5.11']['RANKED_SOLO'],
		    		                obj['5.14']['RANKED_SOLO']);
			    })
		    })(i);
		}
	}).then(function(){
		console.log(items);
		drawChart(false, false);
		initAPReference();
	})
}

function initAPReference(){
	var $list = $('#list');
	var sorted = itemsAry;
	sorted.sort(function (a, b){
		if(a.name < b.name) return -1;
	    if(a.name > b.name) return 1;
	    return 0;
	})
	for( var i in sorted ){
		var $item = $('#item-template').clone().removeAttr('id');
		$item.appendTo($list)

		$item.find('img').attr('src', 'assets/items/514/'+sorted[i].key+'.jpg');
		$item.find('.item-name').text(sorted[i].name);
		$item.find('.item-detail').text(sorted[i].detail);

		$item.show();
	}
}