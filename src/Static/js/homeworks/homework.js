let today = new Date();

function getHomeworks() {
    if ($('#class').val() == '' || $('#class').val() == null) {
        alert('Please select Class');
        return;
    }
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-homeworks',
        data: {
            'id': $('#class').val(),
            'date': $('#date').val(),
        },
        dataType: 'json',
        success: function (data) {
            $('#body').html(data.body);
        }
    });
}

$(document).ready(function () {

    $('#class, #date').change(function () {
        getHomeworks();
        $('#hold').val($('#date').val());
    });

    $('#date').attr(
        "max",
        today.getFullYear() + '-' + (((today.getMonth() + 1) < 10) ? '0' : '') + (today.getMonth() + 1) + '-' + ((today.getDate() < 10) ? '0' : '') + today.getDate()
    )
    $('#date, #hold').val(
        today.getFullYear() + '-' + (((today.getMonth() + 1) < 10) ? '0' : '') + (today.getMonth() + 1) + '-' + ((today.getDate() < 10) ? '0' : '') + today.getDate()
    )
});
