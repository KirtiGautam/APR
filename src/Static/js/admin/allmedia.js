$(document).ready(function () {

    getMedia();

    $('.mdl').addClass('active');
    $('.mdt').addClass('stw');
    $('.mdi').addClass('siw');

    $('#dataType').change(function () {
        if (this.value == 'video') {
            $('.video_type').removeClass('d-none')
            $('.custom-file').addClass('d-none')
        }
        if (this.value == 'pdf') {
            $('.link-div').addClass('d-none')
            $('.video_type').addClass('d-none')
            $('.custom-file').removeClass('d-none')
        }
    });

    $('#video_type').change(function () {
        if (this.value == 'local') {
            $('.link-div').addClass('d-none')
            $('.custom-file').removeClass('d-none')
        }
        if (this.value == 'other') {
            $('.link-div').removeClass('d-none')
            $('.custom-file').addClass('d-none')
        }
    })

    $('#mediaType').change(function () {
        getMedia();
    })
});

const getMedia = () => {
    const type = $('#mediaType').val()
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-media',
        data: {
            'type': type,
        },
        dataType: 'json',
        success: function (response) {
            let html = '<ul>';
            if (type == 'video' || type == '' || type == null) {
                for (let x = 0; x < response.video.length; x++) {
                    const data = response.video[x];
                    html += `<li><a href="${(data.Local) ? response.prefix : ''}${data.file}">${data.Name}</a> ${data.Description} </li>`;
                }
            }
            if (type == 'pdf' || type == '' || type == null) {
                for (let x = 0; x < response.pdf.length; x++) {
                    const data = response.pdf[x];
                    html += `<li><a href="${response.prefix}${data.file}">${data.Name}</a> ${data.Description}</li>`;
                }
            }
            html += '</ul';
            $('#body').html(html);
        }
    });
}


const resetForm = () => {
    $('#dataType').val('')
    $('#video_type').val('')
    $('#FName').val('')
    $('#description').val('')
    $('#video_link').val('')
    $('#file_input').val('')
}


const Validate = val => {
    if ($('#dataType').val() == '' ||
        $('#dataType').val() == null
    ) {
        show_alert('Please Select File Type', 'warning');
        return false;
    }
    if ($('#dataType').val() == 'pdf' && !val) {
        show_alert('Please Select File', 'warning');
        return false;
    }
    if ($('#dataType').val() == 'video') {
        if ($('#video_type').val() == '' ||
            $('#video_type').val() == null) {
            show_alert('Please Select Video Type', 'warning');
            return false;
        }
        if ($('#video_type').val() == 'local' &&
            !val) {
            show_alert('Please Select File', 'warning');
            return false;
        }
        if ($('#video_type').val() == 'other' &&
            ($('#video_link').val() == '' || $('#video_link').val() == null)) {
            show_alert('Please Paste your video link', 'warning');
            return false;
        }
    }
    if ($('#FName').val() == '' ||
        $('#FName').val() == null ||
        $('#description').val() == '' ||
        $('#description').val() == null) {
        show_alert('Please provide description and name of file', 'warning');
        return false;
    }
    return true;
}

const getFormData = () => {
    let data = new FormData();
    if ($('#dataType').val() == 'video' && $('#video_type').val() == 'local') {
        data.append('dataType', 'video');
        data.append('videoType', 'local');
        data.append('file', document.getElementById("file_input").files[0]);
    }
    if ($('#dataType').val() == 'video' && $('#video_type').val() == 'other') {
        data.append('dataType', 'video');
        data.append('videoType', 'youtube');
        data.append('file', $('#video_link').val());
    }
    if ($('#dataType').val() == 'pdf') {
        data.append('dataType', 'pdf');
        data.append('file', document.getElementById("file_input").files[0]);
    }
    data.append('Name', $('#FName').val());
    data.append('description', $('#description').val());
    return data;
}