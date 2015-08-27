var ITEM_KEYS 	= [1026,1058,3003,3027,3040,3089,3115,3116,3135,3136,3151,3152,3157,3165,3174,3285];
var items 	 	= {};
var itemsAry 	= [];

var APItem = function(key){
	this.key = key;
	this.name = '';
	this.detail = '';
	this.patch511 = {};
	this.patch514 = {};
};
APItem.prototype.setUnranked = function(unrankedA, unrankedB){
	this.patch511.unranked = unrankedA;
	this.patch514.unranked = unrankedB;
}
APItem.prototype.setRanked = function(rankedA, rankedB){
	this.patch511.ranked = rankedA;
	this.patch514.ranked = rankedB;
}
APItem.prototype.setDescription = function(name, change){
	this.name = name;
	this.detail = change;
}
APItem.prototype.getPatch = function(patch){
	if( patch == 511 ){
		return this.patch511;
	}
	if( patch == 514 ){
		return this.patch514;
	}
}
APItem.prototype.getFilteredData = function(patch, rank){
	var patchObj = this.getPatch(patch);
	if(rank == 'NO_RANK'){
		return patchObj.unranked;
	}else{
		return patchObj.ranked[rank];
	}
}