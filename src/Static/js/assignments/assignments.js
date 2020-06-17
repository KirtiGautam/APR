function getAssignments() {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-assignments',
        data: {
            'id': $('#class').val(),
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



$(document).ready(function () {


    $('#next_btn').click(function () {
        if (!$('#subjects').val() ||
            !$('#lessons').val() ||
            !$('.assignment-name').val() ||
            !$('.assignment-instructions').val() ||
            !$('#deadline').val()
        ) {
            alert('Please fill neccessary details')
            return;
        }
        getMedia('pdf');
        $('#assign_details').addClass('d-none');
        $('#data_div').removeClass('d-none');
    })

    $('#class').change(function () {
        getAssignments();
        if (this.value == '') {
            $('.add-assign').addClass('d-none')
        } else {
            $('.add-assign').removeClass('d-none')
        }
    });

    $('#dataType').change(function () {
        if (this.value == 'pdf') {
            getMedia('pdf')
        } else if (this.value == 'test') {
            getQuestions()
        } else {
            getMedia('video')
        }
    });

    $('#subjects').change(function () {
        getLessons();
    });

});

const getQuestions = () => {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/get-questions",
        data: {
            'lesson': $('#lessons').val(),
        },
        dataType: "json",
        success: function (response) {
            let html = '<ol>';
            for (let x = 0; x < response.questions.length; x++) {
                const data = response.questions[x];
                html += `<li id='${data.id}'> ${data.Name} ${data.Difficulty} </li>`
            }
            html += '</ol>'
            $("#data_display").html(html);
        },
    });
}

const getMedia = type => {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/get-media",
        data: {
            type: type,
        },
        dataType: "json",
        success: function (response) {
            let html = "";
            if (type == "video") {
                for (let x = 0; x < response.video.length; x++) {
                    const data = response.video[x];
                    html += `<div class="col-xs-12 col-sm-12 col-md-6 col-lg-4 mb-3"><a href="${
                        data.Local ? response.prefix : ""
                        }${
                        data.file
                        }"><div class="cards p-2"><span class="row row-head"><span class="text-left col-10">VIDEO</span></span><span class="row text-center"><span class="col-3"></span><img src="/static/Images/lesson/video.png" alt="" class="col-6"></span><span class="row row-foot"><span class="col-8">${
                        data.Name
                        } </span><span class="description">${data.Description}</span></span></div></a></div>`;
                }
            }
            if (type == "pdf") {
                for (let x = 0; x < response.pdf.length; x++) {
                    const data = response.pdf[x];
                    html += `<div class="col-xs-12 col-sm-12 col-md-6 col-lg-4 mb-3"><a href="${response.prefix}${data.file}"><div class="cards p-2"><span class="row row-head"><span class="text-left col-10">PDF</span></span><span class="row text-center"><span class="col-3"></span><img src="/static/Images/lesson/video.png" alt="" class="col-6"></span><span class="row row-foot"><span class="col-8">${data.Name}</span><span class="description">${data.Description}</span></span></div></a></div>`;
                }
            }
            $("#data_display").html(html);
        },
    });
}