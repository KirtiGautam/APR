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
            if (data.body == '') {
                $('#body').html("<h5 class='m-5 text-center'>No assignments</h5>");
            } else {
                $('#body').html(data.body);
            }
            getSubjects();
        }
    });
}

function getLessons() {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-lesson',
        data: {
            'id': $('#subjects').val(),
        },
        dataType: 'json',
        success: function (data) {
            html = '<option value="" selected disabled>Lessons</option>';
            for (x in data.lessons) {
                html += `<option value="${data.lessons[x].id}" >${data.lessons[x].Name}</option>`
                $('#lessons').html(html);
            }
        }
    });
}

function getSubjects() {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-subjects',
        data: {
            'id': $('#class').val(),
        },
        dataType: 'json',
        success: function (data) {
            let html = '<option value="" selected disabled>Subjects</option>';
            for (x in data.subjects) {
                html += `<option value="${data.subjects[x].id}" >${data.subjects[x].Name}</option>`
            }
            $('#subjects').html(html);
        }
    });
}


$(document).ready(function () {

    $('#class, #date').change(function () {
        getHomeworks();
        $('#hold').val($('#date').val());
        if ($('#class').val() == '') {
            $('.add-assign').addClass('d-none')
        } else {
            $('.add-assign').removeClass('d-none')
        }
    });

    $('#date').attr(
        "max",
        today.getFullYear() + '-' + (((today.getMonth() + 1) < 10) ? '0' : '') + (today.getMonth() + 1) + '-' + ((today.getDate() < 10) ? '0' : '') + today.getDate()
    )
    $('#date, #hold').val(
        today.getFullYear() + '-' + (((today.getMonth() + 1) < 10) ? '0' : '') + (today.getMonth() + 1) + '-' + ((today.getDate() < 10) ? '0' : '') + today.getDate()
    )

    $('#subjects').change(function () {
        getLessons();
    });

});
