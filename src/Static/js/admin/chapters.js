const getSubjects = () => {
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
            $('#subject').html(html);
        }
    });
}

const getLessons = () => {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-lesson',
        data: {
            'id': $('#subject').val(),
        },
        dataType: 'json',
        success: function (data) {
            html = '';
            for (x in data.lessons) {
                html += `<li class="list-group-item">${data.lessons[x].Name}</li>`
            }
            $('#lessons').html(html);
        }
    });
}



$(document).ready(function () {


    $('.CHL').addClass('active');
    $('.CHT').addClass('stw');
    $('.CHI').addClass('siw');

    $('#class').change(function () {
        getSubjects()
    });

    $('#subject').change(function () {
        getLessons()
    });

    $('#save').click(function () {
        if ($('#lesson').val() == '' ||
            $('#lesson').val() == null ||
            $('#subject').val() == '' ||
            $('#subject').val() == null
        ) {
            alert('Please select Subject and Lesson Name');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/new-lesson',
            data: {
                'id': $('#subject').val(),
                'lesson': $('#lesson').val()
            },
            dataType: 'json',
            success: function (data) {
                alert(data.message);
                getLessons();
                $('#lesson').val('');
            }
        });
    });

});
