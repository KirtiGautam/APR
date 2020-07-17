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

const editComment = id => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/get-lesson-comment",
        data: {
            'id': id,
        },
        dataType: "json",
        success: function (response) {
            $('#edit_comment_modal').modal('show', { backdrop: 'static', keyboard: false });
            $('#hidden_edit_comment_id').val(response.id);
            $('#edit_comment_textarea').val(response.body);

        },
        error: function (error) {
            alert(error.responseText);
        },
    });
}

const like_comment = el => {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/like-lesson-comment",
        data: {
            'id': el.value,
        },
        dataType: "json",
        success: function (response) {
            getComments();
            alert(`Comment ${response.message}`);
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
        url: "/lesson-comments",
        data: {
            'id': findGetParameter(),
            'parent_id': parent_id,
            'body': body,
            'doubt': $('#doubt_marker').is(':checked'),
        },
        dataType: "json",
        success: function (response) {
            $('#discussions').html(response.body);
            if (parent_id) {
                $(`.reply_div${this.value}`).toggleClass('d-none');
                alert('Reply added');
            } else {
                alert('Comment added');
                $('#comment_body').val('')
                $("#doubt_marker").prop("checked", false);
            }
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
        url: "/delete-lesson-comment",
        data: {
            'id': id,
        },
        dataType: "json",
        success: function (response) {
            $('#discussions').html(response.body);
            if (response.parent_id) {
                $(`.reply_div${this.value}`).toggleClass('d-none');
                alert('Reply deleted');
            } else {
                alert('Comment deleted')
            }
        },
        error: function (error) {
            alert(error.responseText);
        },
    });
}

const doubt_resolved = id => {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
        url: "/update-lesson-comment",
        data: {
            'id': id,
            "resolved": true,
        },
        dataType: "json",
        success: function (response) {
            getComments()
            alert(response.message)
        },
        error: function (error) {
            alert(error.responseText);
        },
    });
}

$(function () {
    $('#edit_comment_btn').click(function () {
        if (!$('#edit_comment_textarea').val()) {
            alert('Comment cannot be empty')
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
            url: "/update-lesson-comment",
            data: {
                'id': $('#hidden_edit_comment_id').val(),
                'body': $('#edit_comment_textarea').val()
            },
            dataType: "json",
            success: function (response) {
                getComments()
                alert(response.message)
            },
            error: function (error) {
                alert(error.responseText);
            },
        });
    });

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