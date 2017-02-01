
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview

    var streetStr = $('#street').val();
    var cityStr = $('#city').val();
    var address = streetStr + ', ' + cityStr;

    $greeting.text('So, you want to live at ' + address + '?');

    // Google maps AJAX request
    var streetviewUrl = 'http://maps.googleapis.com/maps/api/streetview?size=600x300&location=' + address + '';
    $body.append('<img class="bgimg" src="' + streetviewUrl + '">');

    // NYtimes AJAX request
    var nytimesUrl = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=' + cityStr + '&sort=newest&api-key=ff9d64af9d38447b8292cf15b13570b8'

    $.getJSON(nytimesUrl, function(data) {
        $nytHeaderElem.text('New York Times Articles About ' + cityStr);
        articles = data.response.docs;
        for (var i = 0; i < articles.length; i++) {
            var article = articles[i];
            $nytElem.append('<li class="article">' + '<a href="' +
                article.web_url + '">' + article.headline.main +
                '</a>' + '<p>' + article.snippet + '</p>' + '</li>');
        };
    }).error(function(e){
        $nytHeaderElem.text('Google Map could not be loaded');
    });

    // Wikipedia AJAX request
    var wikiUrl ='https://en.wikipedia.org/w/api.php?action=opensearch&search='
        + cityStr + '&format=json&callback=wikiCallback';

    var wikiRequestTimeout = setTimeout(function(){
        $wikiElem.text("failed to get wikipedia resources");
    }, 8000);

    $.ajax({
        url: wikiUrl,
        dataType: "jsonp",
        // jsonp: "callback",
        success: function(response) {
            var articleList = response[1];
            var descriptionList = response[2];
            var urlList = response[3];
            console.log(articleList);
            for (var i = 0; i < articleList.length; i++) {
                articleStr = articleList[i];
                articleDesc = descriptionList[i]
                articleUrl = urlList[i]

                $wikiElem.append('<li><a href="' + articleUrl + '">' + articleStr +
                    '</a></li>' + articleDesc + '<br>' + '<a href="' + articleUrl + '" target="_blank">' + "view on wikipedia" +
                    '</a>');
            };

            clearTimeout(wikiRequestTimeout);
        }
    });

    return false;
};

$('#form-container').submit(loadData);
