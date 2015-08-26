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
		drawChart(false);
	})
}