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
      getSubjects();
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
  });
}

function getLessons() {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-lesson",
    data: {
      id: $("#subjects").val(),
    },
    dataType: "json",
    success: function (data) {
      html = '<option value="" selected disabled>Lessons</option>';
      for (x in data.lessons) {
        html += `<option value="${data.lessons[x].id}" >${data.lessons[x].Name}</option>`;
        $("#lessons").html(html);
      }
    },
  });
}

$(document).ready(function () {
  $("#next_btn").click(function () {
    if (
      !$("#subjects").val() ||
      !$("#lessons").val() ||
      !$(".assignment-name").val() ||
      !$(".assignment-instructions").val() ||
      !$("#deadline").val()
    ) {
      alert("Please fill neccessary details");
      return;
    }
    getMedia("pdf");
    $("#assign_details").addClass("d-none");
    $("#data_div").removeClass("d-none");
    $("#upload_btn").removeClass("d-none");
  });

  $("#class").change(function () {
    getAssignments();
    if (this.value == "") {
      $(".add-assign").addClass("d-none");
    } else {
      $(".add-assign").removeClass("d-none");
    }
  });

  $("#dataType").change(function () {
    if (this.value == "pdf") {
      getMedia("pdf");
      $("#upload_btn, #data_display").removeClass("d-none");
      $("#next_next_btn, .question_div").addClass("d-none");
    } else if (this.value == "test") {
      getQuestions();
      $("#upload_btn, #data_display").addClass("d-none");
      $("#next_next_btn, .question_div").removeClass("d-none");
    } else {
      getMedia("video");
      $("#upload_btn, #data_display").removeClass("d-none");
      $("#next_next_btn, .question_div").addClass("d-none");
    }
  });

  $("#subjects").change(function () {
    getLessons();
  });

  $("#upload_btn").click(function () {
    const Sdata = getSelecteddata();
    if (Sdata.length < 1) {
      alert("Please select a atleast one data");
      return;
    }
    let data;
    if ($("#dataType").val() == "test") {
      data = {
        type: $("#dataType").val(),
        data: getSelecteddata(),
        lesson: $("#lessons").val(),
        subject: $("#subjects").val(),
        NOA: $(".assignment-name").val(),
        deadline: $("#deadline").val(),
        instruction: $(".assignment-instructions").val(),
        TN: $("#test_name").val(),
        duration: $("#test_duration").val(),
        final: $("#final_flag").is(":checked") ? 1 : 0,
      };
    } else {
      data = {
        type: $("#dataType").val(),
        data: getSelecteddata(),
        lesson: $("#lessons").val(),
        subject: $("#subjects").val(),
        NOA: $(".assignment-name").val(),
        deadline: $("#deadline").val(),
        instruction: $(".assignment-instructions").val(),
      };
    }
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
      url: "/add-new-assignment",
      data: data,
      dataType: "json",
      success: function (response) {
        alert(response.message);
      },
    });
  });

  $("#next_next_btn").click(function () {
    if (!$("#test_name").val() || !$("#test_duration").val()) {
      alert("Please fill necessary details");
      return;
    }
    $("#upload_btn, #data_display").removeClass("d-none");
    $("#next_next_btn, .question_div, #data_div").addClass("d-none");
  });
});

const getQuestions = () => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-questions",
    data: {
      lesson: $("#lessons").val(),
    },
    dataType: "json",
    success: function (response) {
      let html =
        '<table class="table"><thead class="thead-light"><tr><th>Question</th><th>Difficulty</th><th></th></tr></thead><tbody>';
      for (let x = 0; x < response.questions.length; x++) {
        const data = response.questions[x];
        html += `<tr><td id='${data.id}' class="ques-name"> ${data.Name} </td> <td class="ques-name"> ${data.Difficulty} </td><td> <span class="col-2 checkbox"><input type="checkbox" class="question_checkbox" value="${data.id}"></span></td></tr>`;
      }
      html += "</tbody></table>";
      $("#data_display").html(html);
    },
  });
};

const getMedia = (type) => {
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
          html += `<div class="col-xs-12 col-sm-12 col-md-6 col-lg-4 mb-3"><div class="cards p-2"><span class="row row-head"><span class="text-left col-10">VIDEO</span><span class="col-2 checkbox"><input type="checkbox" class="video_checkbox" value="${data.id}"></span></span><span class="row text-center"><span class="col-3"></span><img src="/static/Images/lesson/video.png" alt="" class="col-6"></span><span class="row row-foot"><span class="col-8">${data.Name} </span><span class="description">${data.Description}</span></span></div></div>`;
        }
      }
      if (type == "pdf") {
        for (let x = 0; x < response.pdf.length; x++) {
          const data = response.pdf[x];
          html += `<div class="col-xs-12 col-sm-12 col-md-6 col-lg-4 mb-3"><div class="cards p-2"><span class="row row-head"><span class="text-left col-10">PDF</span><span class="col-2 checkbox"><input type="checkbox" class="pdf_checkbox" value="${data.id}"></span></span><span class="row text-center"><span class="col-3"></span><img src="/static/Images/lesson/video.png" alt="" class="col-6"></span><span class="row row-foot"><span class="col-8">${data.Name}</span><span class="description">${data.Description}</span></span></div></div>`;
        }
      }
      $("#data_display").html(html);
    },
  });
};

const getSelecteddata = () => {
  let data = [];
  let type;
  if ($("#dataType").val() == "pdf") {
    type = "pdf_checkbox";
  } else if ($("#dataType").val() == "video") {
    type = "video_checkbox";
  } else {
    type = "question_checkbox";
  }

  $(`input.${type}:checkbox:checked`).each(function () {
    data.push($(this).val());
  });
  return data;
};
