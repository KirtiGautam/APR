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
        }, error: function (error) {
            alert(error.responseText);
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
                html += `<div class="col-5 col-sm-5 col-md-5 col-lg-5 part-2-1 m-2">
                <span class="row p-1">
                    <span class="col-11 cn">Chapter Number</span>
                    <input type="checkbox" class="form-control col-1 lesson_checks" value="${data.lessons[x].id}">
                    <span class="col-2 num">${data.lessons[x].Number}</span>
                    <span class="col-10 chap-name">${data.lessons[x].Name}</span>
                </span>
            </div>`
            }
            $('#lessons').html(html);
        }, error: function (error) {
            alert(error.responseText);
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
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    });

    $('#edit_btn').click(function () {
        let data = []
        $(`input.pdf_checks:checkbox:checked`).each(function () {
            data.push($(this).val());
        });
        if(data.length<1){
            alert('Please select a chapter to edit');
            return;
        }
        $.ajax({
            type: "GET",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/chapter-details',
            data: {
                'id': data[0],
            },
            dataType: 'json',
            success: function (data) {
                console.log(data)
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    })

});
