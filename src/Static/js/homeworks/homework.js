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
                $('#body').html("<h5 class='m-5 text-center'>No homework</h5>");
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


function Validate() {
    let lesson = $('#lessons').val();
    let chapter = $('#FName').val();
    let dataType = $('#dataType').val();
    let subject = $('#subjects').val();
    let Name = $('.homework-name').val();
    let instructions = $('.homework-instructions').val();
    if (subject == '' || Name == '' || instructions == '' || lesson == '') {
        show_alert("Please fill all details", "warning");
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
    $('.homework-name').val('');
    $('.homework-instructions').val();
}

function getFormData() {
    let data = new FormData();
    data.append('subject', $('#subjects').val());
    data.append('Name', $('.homework-name').val());
    data.append('instructions', $('.homework-instructions').val());
    data.append("name", $('#FName').val());
    data.append("type", $('#dataType').val());
    data.append("lesson", $('#lessons').val());
    return data;
}


$(document).ready(function () {

    $('#dataType').change(function () {
        if (this.value == 'csv') {
            $('.csv').removeClass('d-none');
        } else {
            $('.csv').addClass('d-none');
        }
    });

    $('#class, #date').change(function () {
        getHomeworks();
        $('#hold').val($('#date').val());
        if ($('#class').val() == '') {
            $('.add-home').addClass('d-none')
        } else {
            $('.add-home').removeClass('d-none')
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
