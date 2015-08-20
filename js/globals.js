var MAX_CHAMPS_PER_TEAM = 5;
var champs = [];
var champsFull = {};
var champsA = [];
var champsB = [];
var selections = [];

var Champion = function(key){
	this.key = key;
	this.patchId = 511;
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
		this.patchId = 511;
		return this.patch511;
	}
	if( patch == 514 ){
		this.patchId = 514;
		return this.patch514;
	}
}
Champion.prototype.getRank = function(rank){
	return this['patch'+this.patchId].ranked.rank;
}