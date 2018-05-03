$( document ).ready(function() {
    $('.sign').on('click', function () {
        var endpoint = '/api/readings/' + this.id
        $.getJSON( endpoint, function( data ) {
            $.each( data, function( key, val ) {
                $('#' + key).replaceWith(val);
            }
        )}
    )}
)}
)