const today = new Date();
$(document).ready(function () {
  const now = today.getFullYear() + '-' + (today.getMonth() + 1 < 10 ? '0' : '') + (today.getMonth() + 1) + '-' + (today.getDate() < 10 ? '0' : '') + today.getDate() + 'T' + (today.getHours() < 10 ? '0' : '') + today.getHours() + ":" + (today.getMinutes() < 10 ? '0' : '') + today.getMinutes();

  $('#deadline').attr("min", now);

  $("#class").change(function () {
    getAssignments();
    $('input[name="id"]').val(this.value)
    console.log($('input[name="id"]').val());
    $("#past_btn").removeClass("d-none");
    if (this.value == "") {
      $(".add-assign").addClass("d-none");
    } else {
      $(".add-assign").removeClass("d-none");
    }
  });

  $("#upload_btn").click(function () {
    let data = {
      subject: $("#subjects").val(),
      NOA: $(".assignment-name").val(),
      deadline: $("#deadline").val(),
      instruction: $(".assignment-instructions").val(),
    };
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
      url: "/add-new-assignment",
      data: data,
      dataType: "json",
      success: function (response) {
        getAssignments();
        alert(response.message);
      },
      error: function (error) {
        alert(error.responseText);
      },
    });
  });

});

const getAssignments = () => {
  $.ajax({
    type: "GET",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-assignments",
    data: {
      id: $("#class").val(),
      time: 'present'
    },
    dataType: "json",
    success: function (data) {
      // pastAssignments();
      if (!data.body.replace(/(\r\n|\n|\r)/gm, "")) {
        $("#body").html("<h5 class='m-5 text-center'>No assignments</h5>");
      } else {
        $("#body").html(data.body);
      }
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
}

const pastAssignments = () => {
  $.ajax({
    type: "GET",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-assignments",
    data: {
      id: $("#class").val(),
      time: 'past'
    },
    dataType: "json",
    success: function (data) {
      getSubjects();
      if (!data.body.replace(/(\r\n|\n|\r)/gm, "")) {
        $("#past_assign").html("<h5 class='m-5 text-center'>No past assignments</h5>");
      } else {
        $("#past_assign").html(data.body);
      }
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
}

const getSubjects = () => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-subjects",
    data: {
      id: $("#class").val(),
    },
    dataType: "json",
    success: function (data) {
      let html = '<option value="" selected disabled>Subjects</option>';
      for (x in data.subjects) {
        html += `<option value="${data.subjects[x].id}" >${data.subjects[x].Name}</option>`;
      }
      $("#subjects").html(html);
    },
    error: function (error) {
      console.log(error.responseText);
    },
  });
}
