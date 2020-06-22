const today = new Date();
$(document).ready(function () {
  const now = today.getFullYear() + '-' + (today.getMonth() + 1 < 10 ? '0' : '') + (today.getMonth() + 1) + '-' + (today.getDate() < 10 ? '0' : '') + today.getDate() + 'T' + (today.getHours() < 10 ? '0' : '') + today.getHours() + ":" + (today.getMinutes() < 10 ? '0' : '') + today.getMinutes();

  $('#deadline').attr("min", now);

  $("#class").change(function () {
    getAssignments();
    getSubjects();
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

function getAssignments() {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-assignments",
    data: {
      id: $("#class").val(),
    },
    dataType: "json",
    success: function (data) {
      if (data.body == "") {
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

function getSubjects() {
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
