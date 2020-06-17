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
                html += `<div class="col-6 col-sm-6 col-md-4 col-lg-4 part-2-1 m-2">
                <span class="row">
                    <span class="col-12 cn">Chapter Number</span>
                    <span class="col-2 num">${data.lessons[x].Number}</span>
                    <span class="col-10 chap-name">${data.lessons[x].Name}</span>
                </span>
            </div>`
                // html += `<li class="list-group-item">${data.lessons[x].Name}</li>`
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

    $('#search_btn').click(function () {
        if (!$('#subject').val()) {
            alert('Please select a subject first');
            return;
        }
        getLessons()
    });

    $('#save').click(function () {
        if (!$('#lesson').val() ||
            !$('#subject').val() ||
            !$('#lesson_number').val()
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
                'lesson': $('#lesson').val(),
                'number': $('#lesson_number').val(),
            },
            dataType: 'json',
            success: function (data) {
                alert(data.message);
                getLessons();
                $('#lesson').val('');
                !$('#lesson_number').val('');
            }
        });
    });

});
