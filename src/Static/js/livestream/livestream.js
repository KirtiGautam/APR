let today = new Date();

$(document).ready(function () {
    $('#Class').change(function () {
        getLivestreams();
    })

    const now = today.getFullYear() + '-' + (today.getMonth() + 1 < 10 ? '0' : '') + (today.getMonth() + 1) + '-' + today.getDate() + 'T' + today.getHours() + ":" + today.getMinutes();

    $('#Time').attr("min", now);

    $('#newLS').click(function () {
        if (!$('#teacher').val() ||
            !$('#Name').val() ||
            !$('#Stream_link').val() ||
            !$('#Time').val() ||
            !$('#Duration').val()) {
            alert('Please fill all the values');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/new-livestream',
            data: {
                class: $('#Class').val(),
                teacher: $('#teacher').val(),
                Name: $('#Name').val(),
                Stream_link: $('#Stream_link').val(),
                Time: $('#Time').val(),
                Duration: $('#Duration').val()
            },
            dataType: 'json',
            success: function (data) {
                getLivestreams()
                alert(data.message);
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    })


    $('#edit_btn').click(function () {
        const Sdata = getSelectedLS();
        if (Sdata.length != 1) {
            alert('Please select a single stream for edit');
            return;
        }
        $.ajax({
            type: "GET",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/get-stream',
            data: {
                'id': Sdata[0]
            },
            dataType: 'json',
            success: function (data) {
                for (let x in data) {
                    $(`#${x}`).val(data[x])
                }
                $("#Time").val(data['Time'].substring(0, data['Time'].length - 4))
                $('#hidden_ls_id').val(Sdata[0])
                $('#add').modal('show')
                $('#updateLS').removeClass('d-none');
                $('#newLS').addClass('d-none');
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    })

    $('#updateLS').click(function () {
        if (!$('#teacher').val() ||
            !$('#Name').val() ||
            !$('#Stream_link').val() ||
            !$('#Time').val() ||
            !$('#Duration').val()) {
            alert('Please fill all the values');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/update-stream',
            data: {
                id: $('#hidden_ls_id').val(),
                teacher: $('#teacher').val(),
                Name: $('#Name').val(),
                Stream_link: $('#Stream_link').val(),
                Time: $('#Time').val(),
                Duration: $('#Duration').val()
            },
            dataType: 'json',
            success: function (data) {
                getLivestreams()
                alert(data.message);
            }, error: function (error) {
                alert(error.responseText);
            }
        });
    })


    $('#delete_btn').click(function () {
        const Sdata = getSelectedLS();
        if (Sdata.length != 1) {
            alert("Please select a livestream to delete");
            return;
        }
        if (confirm('Are you sure you want to delete the selection ?')) {
            $.ajax({
                type: "POST",
                headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
                url: '/delete-stream',
                data: {
                    'data': Sdata
                },
                dataType: 'json',
                success: function (data) {
                    getLivestreams();
                    alert(data.message);
                }, error: function (error) {
                    alert(error.responseText);
                }
            });
        }
    })
})

const getTeachers = () => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-staff',
        data: {
            'term': '',
            'type': 'teacher',
        },
        dataType: 'json',
        success: function (data) {
            html = '<option value="">Please select Teacher</option>';
            for (let x = 0; x < data.staff.length; x++) {
                const teach = data.staff[x];
                html += `<option value="${teach.id}">${teach.Name}${teach.Email}</option>`
            }
            $('#teacher').html(html);
        }, error: function (error) {
            alert(error.responseText);
        }
    });
}


const getLivestreams = () => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/get-livestream",
        data: {
            class: $("#Class").val(),
        },
        dataType: "json",
        success: function (response) {
            $("#body").html(response.body);
        }, error: function (error) {
            alert(error.responseText);
        }
    });
}


const getSelectedLS = () => {
    let data = [];
    $('input.live_checks:checkbox:checked').each(function () {
        data.push($(this).val());
    });
    return data;
}

const prenew = () => {
    $('#updateLS').addClass('d-none');
    $('#newLS').removeClass('d-none');
    $('#teacher').val('')
    $('#Name').val('')
    $('#Stream_link').val('')
    $('#Time').val('')
    $('#Duration').val('')
    $('#add').modal('show');
}