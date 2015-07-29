(function(){

var app = angular.module('store', [ ]);


var gems = [

{
name: "Dodecahedron",
price: 2.95,
description: ". . .",
canPurchase: true,
images: [
			{
				full: 'Photo0001.jpg',
				thumb: 'Photo0038.jpg'
			},
			{
				full: 'Photo0038.jpg',
				thumb: 'Photo0001.jpg'
			}

		]
},

{
name: "Pentagonal Gem",
price: 5.95,
description: ". . .",
canPurchase: false,
}
];








app.controller("StoreController", function(){


this.products = [
{
name: 'Awesome Multi-touch Keyboard',
price: 250.00,
description: "...",
images: "...",
reviews: [
	{
		stars: 5,
		body: "I love this product!",
		author: "joe@thomas.com",
		terms: "-",
		color: "-"
	},

	{
	stars: 1,
	body: "This product sucks",
	author: "tim@hater.com",
	terms: "-",
	color: "-"
	}]
}
];



}
);





app.controller("ReviewController", function(){

this.review = {};

this.addReview = function(product) {
product.reviews.push(this.review);
this.review = {};
};



});







app.controller("PanelController", function(){


this.tab = 1;

this.selectTab = function(setTab) {
this.tab = setTab;
};

this.isSelected = function(checkTab){
return this.tab === checkTab;
};


});

}
)();




