// main js file

function sorting() {
    $( "#sortable-1" ).sortable();
}

function voting() {
    $('#voting-btn').click(function(event) {
        var url = '/tournament/' + $(this).attr("value") + '/voting/';
        var pks = [];
        $('.contestants-list').each(function(i, obj) {
            pks[i] = $(this).attr("value");
        });

        $.ajax({
            'type': 'POST',
            'url': url,
            'dataType': 'json',
            'traditional': true,
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'pks': pks
            },
            'success': function(data, status, xhr) {
                var cabinet_url = ' <a href="/users/cabinet/">Back to cabinet</a>';
                $('#voting-list').html('<p class="lead">' + data['status'] + cabinet_url + '</p>');

            },
            'beforeSend': function(xhr,setting) {
                $('#voting-btn').empty();
            },
            'error': function(){
//                alert("error");
            }
        });
    });
}

$(document).ready(function() {
    sorting();
    voting();
});