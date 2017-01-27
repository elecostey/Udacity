var cats = [{
    'img_div': $('#cat1'),
    'name_div': $('#cat1_name'),
    'name': 'Rengo',
    'img': $('#cat1_img'),
    'numberOfClicks': 0,
    'clicksNumber_div': $('#cat1_clicks_number')
    },{
    'img_div': $('#cat2'),
    'name_div': $('#cat2_name'),
    'name': 'Maru',
    'img': $('#cat2_img'),
    'numberOfClicks': 0,
    'clicksNumber_div': $('#cat2_clicks_number')
    },{
    'img_div': $('#cat3'),
    'name_div': $('#cat3_name'),
    'name': 'Romeo',
    'img': $('#cat3_img'),
    'numberOfClicks': 0,
    'clicksNumber_div': $('#cat3_clicks_number')
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
            catCopy.numberOfClicks += 1;
            catCopy.clicksNumber_div.text('Number of clicks: ' + catCopy.numberOfClicks);
        };

    }(cat));
};


