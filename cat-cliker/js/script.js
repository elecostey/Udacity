
var $body = $('body');
var $catImage = $('#cat_img');
var $clicksNumber = $('#clicks_number');
var numberOfClicks = 0;
$clicksNumber.append(numberOfClicks);

$('#cat_img').click(function() {
    //the element has been clicked... do stuff here
    console.log('clicked');
    numberOfClicks += 1;
    $clicksNumber.text('Number of clicks: ' + numberOfClicks);
});

