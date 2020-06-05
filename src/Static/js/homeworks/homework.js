function getAssignments() {
    console.log($('#class').val());
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-homeworks',
        data: {
            'id': $('#class').val(),
        },
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $('#body').html(data.body);
        }
    });
}

$(document).ready(function () {

    $('#class').change(function () {
        getAssignments();
    });

    $('#class').val('');
});
