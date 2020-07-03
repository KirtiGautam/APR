function findGetParameter() {
    urlarray = window.location.href.split('/')
    return urlarray[urlarray.length - 1]
}

const getComments = (parent_id = null) => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/homework-comments",
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

const like_comment = el => {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/like-homework-comment",
        data: {
            'id': el.value,
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
}

const comment = (parent_id, body) => {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/homework-comments",
        data: {
            'id': findGetParameter(),
            'parent_id': parent_id,
            'body': body,
        },
        dataType: "json",
        success: function (response) {
            $('#discussions').html(response.body);
            if (parent_id) {
                $(`.reply_div${this.value}`).toggleClass('d-none');
            }
            $('#comment_body').val('')
        },
        error: function (error) {
            alert(error.responseText);
        },
    });
}

const delete_comment = id => {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/delete-homework-comment",
        data: {
            'id': id,
        },
        dataType: "json",
        success: function (response) {
            $('#discussions').html(response.body);
            if (response.parent_id) {
                $(`.reply_div${this.value}`).toggleClass('d-none');
            }
        },
        error: function (error) {
            alert(error.responseText);
        },
    });
}

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
        comment(null, $('#comment_body').val());
    });

    $(document).on('keyup', '.reply_body', function () {
        if (!this.value) {
            $(`#reply_send_btn${this.id}`).prop("disabled", true);
        } else {
            $(`#reply_send_btn${this.id}`).prop("disabled", false);
        }
    });

    $(document).on('click', '.reply_btn', function () {
        $(`.reply_div${this.value}`).toggleClass('d-none');
        $(`.replies_list${this.value}`).toggleClass('d-none');
    });

    $(document).on('click', '.reply_send_btn', function () {
        if (!$(`.reply_body#${this.value}`)) {
            alert('Cannot Post empty comment');
            return;
        }
        comment(this.value, $(`.reply_body#${this.value}`).val());
    });

});