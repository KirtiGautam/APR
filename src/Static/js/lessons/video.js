function findGetParameter() {
    urlarray = window.location.href.split('/')
    return urlarray[urlarray.length - 1]
}

const getComments = () => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/lesson-comments",
        data: {
            'id': findGetParameter()
        },
        dataType: "json",
        success: function (response) {
            $('#discussions').html(response.body);
        },
        error: function (error) {
            alert(error.responseText);
        },
    });
}
getComments();

$(function () {
    $('#comment_body').keyup(function () {
        if (!this.value) {
            $('#comment_send_btn').prop("disabled", true);
        } else {
            $('#comment_send_btn').prop("disabled", false);
        }
    });

    $('#comment_send_btn').click(function () {
        if (!$('#comment_body').val()) {
            alert('Cannot Post empty comment');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
            url: "/lesson-comments",
            data: {
                'id': findGetParameter(),
                'parent_id': null,
                'body': $('#comment_body').val(),
            },
            dataType: "json",
            success: function (response) {
                $('#discussions').html(response.body);
                $('#comment_body').val('')
            },
            error: function (error) {
                alert(error.responseText);
            },
        });
    });

    $('.like_btn').click(function () {
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
            url: "/like-lesson-comment",
            data: {
                'id': this.value,
            },
            dataType: "json",
            success: function (response) {
                console.log(response);
                getComments();
            },
            error: function (error) {
                alert(error.responseText);
            },
        });
    });

});