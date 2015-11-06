function getSummonerIngameInfo(summonerName) {
    var apiUrl = 'http://127.0.0.1:5000/get/ingameInfo/by-name/' + summonerName;
    $('#summoner_title').text(summonerName);
    console.log(summonerName);
    $.get(apiUrl, function(data) {
        console.log(data);

        $('#result').text(JSON.stringify(data));
        return data;
    });
}

(function($) {

    $.sanitize = function(input) {
        if (typeof input === 'string' || input instanceof String) {
            var output = input.replace(/<script[^>]*?>.*?<\/script>/gi, '').
            replace(/<[\/\!]*?[^<>]*?>/gi, '').
            replace(/<style[^>]*?>.*?<\/style>/gi, '').
            replace(/<![\s\S]*?--[ \t\n\r]*>/gi, '');
            return output;
        } else {
            return "Error: not a string";
        }
    };

})(jQuery);

$(function() {
    $('#summonerName').keypress(function(e) {
        var key = e.which;
        if (key == 13) {
            $('#btnSearch').click();
        }
    });

    $('#btnSearch').click(function(e) {
        var summonerName = $.sanitize($('input[type="text"]').val());
        var info = getSummonerIngameInfo(summonerName);
    });
});
