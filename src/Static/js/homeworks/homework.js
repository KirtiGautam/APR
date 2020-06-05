let today = new Date();

function getAssignments() {
    console.log($('#class').val())
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
        getAssignments();
    });

    $('#date').attr(
        "max",
        today.getFullYear() + '-' + (((today.getMonth() + 1) < 10) ? '0' : '') + (today.getMonth() + 1) + '-' + ((today.getDate() < 10) ? '0' : '') + today.getDate()
    )
    $('#date').val(
        today.getFullYear() + '-' + (((today.getMonth() + 1) < 10) ? '0' : '') + (today.getMonth() + 1) + '-' + ((today.getDate() < 10) ? '0' : '') + today.getDate()
    )

    $('#class').val('');
});
