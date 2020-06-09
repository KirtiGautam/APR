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


function Validate() {
    let lesson = $('#lessons').val();
    let chapter = $('#FName').val();
    let dataType = $('#dataType').val();
    let subject = $('#subjects').val();
    let Name = $('.assignment-name').val();
    let instructions = $('.assignment-instructions').val();
    let deadline = $('#deadline').val();
    let today = new Date();
    if (subject == '' || Name == '' || instructions == '' || deadline == '' || lesson == '') {
        show_alert("Please fill all details", "warning");
        return false;
    }

    if (Date.parse(today) > Date.parse(deadline)) {
        show_alert("Cannot set deadline in past", "warning");
        return false;
    }

    if (chapter == '' || dataType == '' || chapter == null || dataType == null) {
        show_alert("Please select Data Type and Name of File", "warning");
        return false;
    }

    if (!isVideo(input.files[0].name) && dataType == 'video') {
        show_alert("Please select valid video file", "warning");
        return false;
    }

    if (!isxls(input.files[0].name) && dataType == 'csv') {
        show_alert("Please select valid csv File", "warning");
        return false;
    }

    if (!ispdf(input.files[0].name) && dataType == 'pdf') {
        show_alert("Please select valid pdf File", "warning");
        return false;
    }
    return true;

}

function resetForm() {
    $('#lessons').val('');
    $('#FName').val('');
    $('#dataType').val('');
    $('#subjects').val();
    $('.assignment-name').val('');
    $('.assignment-instructions').val();
    $('#deadline').val('');
}

function getFormData() {
    let data = new FormData();
    data.append('subject', $('#subjects').val());
    data.append('Name', $('.assignment-name').val());
    data.append('instructions', $('.assignment-instructions').val());
    data.append('deadline', $('#deadline').val());
    data.append("name", $('#FName').val());
    data.append("type", $('#dataType').val());
    data.append("lesson", $('#lessons').val());
    return data;
}

$(document).ready(function () {

    $('#class').change(function () {
        getAssignments();
        if (this.value == '') {
            $('.add-assign').addClass('d-none')
        } else {
            $('.add-assign').removeClass('d-none')
        }
    });

    $('#dataType').change(function () {
        if (this.value == 'csv') {
            $('.csv').removeClass('d-none');
        } else {
            $('.csv').addClass('d-none');
        }
    });

    $('#subjects').change(function () {
        getLessons();
    });

});
