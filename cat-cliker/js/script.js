var $cat1_div = $('#cat1');
var $cat1Img = $('#cat1_img');
var $cat1ClicksNumber_div = $('#cat1_clicks_number');
var $cat1Name = $('#cat1_name');

var $cat2_div = $('#cat2');
var $cat2Img = $('#cat2_img');
var $cat2ClicksNumber_div = $('#cat2_clicks_number');
var $cat2Name = $('#cat2_name');

var $cat3_div = $('#cat3');
var $cat3Img = $('#cat3_img');
var $cat3ClicksNumber_div = $('#cat3_clicks_number');
var $cat3Name = $('#cat3_name');

var cats = [{
    'img_div': $cat1_div,
    'name_div': $cat1Name,
    'name': 'Rengo',
    'img': '#cat1_img',
    'numberOfClicks': 0,
    'clicksNumber_div': $cat1ClicksNumber_div
    },{
    'img_div': $cat2_div,
    'name_div': $cat2Name,
    'name': 'Maru',
    'img': '#cat2_img',
    'numberOfClicks': 0,
    'clicksNumber_div': $cat2ClicksNumber_div
    },{
    'img_div': $cat3_div,
    'name_div': $cat3Name,
    'name': 'Romeo',
    'img': '#cat3_img',
    'numberOfClicks': 0,
    'clicksNumber_div': $cat3ClicksNumber_div
     }]


for (i = 0; i < cats.length; i++) {

    var cat = cats[i];
    cat.name_div.text(cat.name);
    cat.clicksNumber_div.append(cat.numberOfClicks);

    $(cat.name_div).click(function(catCopy) {

        return function() {
            $(".cat").hide();
            catCopy.img_div.show();
        };

    }(cat));

    $(cat.img).click(function(catCopy) {

        return function() {
            console.log(catCopy.img + ' clicked');
            catCopy.numberOfClicks += 1;
            catCopy.clicksNumber_div.text('Number of clicks: ' + catCopy.numberOfClicks);
        };

    }(cat));
};


