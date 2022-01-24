function urlify( text ) {

    var urlRegex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;

    return text.replace( urlRegex, function( url ) {
        return '<a href="' + url + '">' + url + '</a>';

    })
}
