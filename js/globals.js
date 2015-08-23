// consts
var PNG_ITEMS 			= [3250, 3255, 3265, 3270, 3274, 3275, 3280];
var MAX_CHAMPS_PER_TEAM = 5;

// globals
var items511 			= [];
var items514 			= [];
var jungle511 			= [];
var jungle514 			= [];
var champs 				= [];
var champsFull 			= {};
var champsA 			= [];
var champsB 			= [];

// container for full champ data
var Champion = function(key){
	this.key = key;
	this.patch511 = {};
	this.patch514 = {};
	this.defaultObj = {};
};
Champion.prototype.setUnranked = function(unrankedA, unrankedB){
	this.patch511.unranked = unrankedA;
	this.patch514.unranked = unrankedB;
	this.defaultObj = unrankedA;
}
Champion.prototype.setRanked = function(rankedA, rankedB){
	this.patch511.ranked = rankedA;
	this.patch514.ranked = rankedB;
}
Champion.prototype.getPatch = function(patch){
	if( patch == 511 ){
		return this.patch511;
	}
	if( patch == 514 ){
		return this.patch514;
	}
}
Champion.prototype.getFilteredData = function(patch, rank){
	var patchObj = this.getPatch(patch);
	var rankKey = '';
	switch(rank){
		case 'unranked':
			rankKey = null;
			break;
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
	if(rankKey == null){
		return patchObj.unranked;
	}else{
		return patchObj.ranked[rankKey];
	}
}