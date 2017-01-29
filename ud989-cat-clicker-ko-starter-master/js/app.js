var initialCats = [
    {
        clickCount: 0,
        name: "Rengo",
        imgSrc: "img/rengo.jpg",
        imgAttribution: "Somebody",
        nickNames: ['Rengar', 'Rengui', 'Rengach']
    },
    {
        clickCount: 0,
        name: "Maru",
        imgSrc: "img/maru.jpg",
        imgAttribution: "Somebody",
        nickNames: ['Tiger', 'Hero', 'Cat']
    },
    {
        clickCount: 0,
        name: "Romeo",
        imgSrc: "img/romeo.jpg",
        imgAttribution: "Somebody",
        nickNames: ['Tiger', 'Hero', 'Cat']
    },
    {
        clickCount: 0,
        name: "Ulfie",
        imgSrc: "img/ulfie.jpg",
        imgAttribution: "Somebody",
        nickNames: ['Tiger', 'Hero', 'Cat']
    },
    {
        clickCount: 0,
        name: "Bobi",
        imgSrc: "img/bobi.jpg",
        imgAttribution: "Somebody",
        nickNames: ['Tiger', 'Hero', 'Cat']
    }
];


var ViewModel = function(){
	var self = this;//self always maps to ViewModel

	this.catList = ko.observableArray([]);

	initialCats.forEach(function(catItem){
		self.catList.push(new Cat(catItem));
	});

	this.currentCat = ko.observable(this.catList()[0]);

	this.incrementCounter = function(){
		this.clickCount(this.clickCount() + 1);
	};

	this.changeCurrentCat = function(clickedCat){
		self.currentCat(clickedCat)
	};
};


var Cat = function(data) {
    this.clickCount = ko.observable(data.clickCount);
    this.name = ko.observable(data.name);
    this.nickNames = ko.observableArray(data.nickNames);
    this.imgSrc = ko.observable(data.imgSrc);
    this.imgAttribution = ko.observable(data.imgAttribution);
    this.level = ko.computed(function(){
        if (this.clickCount() < 5){
            level = "Newborn";
            return level;
        } else if (this.clickCount() < 10){
            level = "Infant";
            return level;
        } else {
            level = "Teen";
            return level;
        }
    },this);

}


ko.applyBindings(new ViewModel());
