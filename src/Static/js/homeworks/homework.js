let today = new Date();

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(".cards").tooltip({ boundary: "window" });

function getHomeworks() {
  if (!$("#class").val()) {
    alert("Please select Class");
    return;
  }
  if (!$("#date").val()) {
    alert("Invalid date");
    return;
  }
  $.ajax({
    type: "GET",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-homeworks",
    data: {
      id: $("#class").val(),
      date: $("#date").val(),
    },
    dataType: "json",
    success: function (data) {
      if (data.body == "") {
        $("#body").html("<h5 class='m-5 text-center'>No homework</h5>");
      } else {
        $("#body").html(data.body);
      }
      getSubjects();
    },
    error: function (error) {
      alert(error.responseText);
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
      }
      $("#lessons").html(html);
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

$(document).ready(function () {
  $("#next_btn").click(function () {
    if (
      !$("#subjects").val() ||
      !$("#lessons").val() ||
      !$(".homework-name").val() ||
      !$(".homework-instructions").val()
    ) {
      alert("Please fill neccessary details");
      return;
    }
    getMedia("pdf");
    $("#homework_details").addClass("d-none");
    $(".test-d-none, #data_div").removeClass("d-none");
  });

  $("#dataType").change(function () {
    if (this.value == "pdf") {
      getMedia("pdf");
      $(".test-d-none, #data_display, #media_search_term").removeClass(
        "d-none"
      );
      $("#next_next_btn, .question_div").addClass("d-none");
    } else if (this.value == "test") {
      getQuestions();
      $(".test-d-none, #data_display, #media_search_term").addClass("d-none");
      $("#next_next_btn, .question_div").removeClass("d-none");
    } else if (this.value == "video") {
      getMedia("video");
      $(".test-d-none, #data_display, #media_search_term").removeClass(
        "d-none"
      );
      $("#next_next_btn, .question_div").addClass("d-none");
    } else {
      $(
        "#data_display, #media_search_term, .question_div, #next_next_btn"
      ).addClass("d-none");
      $("#upload_btn").removeClass("d-none");
    }
  });

  $("#media_search_term").keyup(
    delay(function (e) {
      getMedia($("#dataType").val());
    }, 500)
  );

  $("#upload_btn").click(function () {
    if ($("#dataType").val() != "skip") {
      const Sdata = getSelecteddata();
      if (Sdata.length < 1) {
        alert("Please select a atleast one data");
        return;
      }
    }
    let data;
    if ($("#dataType").val() == "skip") {
      data = {
        type: $("#dataType").val(),
        subject: $("#subjects").val(),
        NOH: $(".homework-name").val(),
        instruction: $(".homework-instructions").val(),
      };
    } else if ($("#dataType").val() == "test") {
      data = {
        type: $("#dataType").val(),
        data: getSelecteddata(),
        lesson: $("#lessons").val(),
        subject: $("#subjects").val(),
        NOH: $(".homework-name").val(),
        instruction: $(".homework-instructions").val(),
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
        NOH: $(".homework-name").val(),
        instruction: $(".homework-instructions").val(),
      };
    }
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
      url: "/add-new-homework",
      data: data,
      dataType: "json",
      success: function (response) {
        location.reload();
        alert(response.message);
      },
      error: function (error) {
        alert(error.responseText);
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

  $("#class, #date").change(function () {
    getHomeworks();
    $("#hold").val($("#date").val());
    if ($("#class").val() == "") {
      $(".add-home").addClass("d-none");
    } else {
      $(".add-home").removeClass("d-none");
    }
  });

  $("#date").attr(
    "max",
    today.getFullYear() +
      "-" +
      (today.getMonth() + 1 < 10 ? "0" : "") +
      (today.getMonth() + 1) +
      "-" +
      (today.getDate() < 10 ? "0" : "") +
      today.getDate()
  );
  $("#date, #hold").val(
    today.getFullYear() +
      "-" +
      (today.getMonth() + 1 < 10 ? "0" : "") +
      (today.getMonth() + 1) +
      "-" +
      (today.getDate() < 10 ? "0" : "") +
      today.getDate()
  );

  $("#subjects").change(function () {
    getLessons();
  });
});

const delay = (callback, ms) => {
  var timer = 0;
  return function () {
    var context = this,
      args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      callback.apply(context, args);
    }, ms || 0);
  };
};

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
    error: function (error) {
      alert(error.responseText);
    },
  });
};

const getMedia = (type) => {
  $.ajax({
    type: "GET",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-media",
    data: {
      type: type,
      term: $("#media_search_term").val(),
    },
    dataType: "json",
    success: function (response) {
      let html = "";
      let thumbArray = [];
      if (type == "video") {
        for (let x = 0; x < response.video.length; x++) {
          const data = response.video[x];
          thumbArray.push({
            id: `#thumbM${data.id}`,
            duration: `#duram${data.id}`,
            link: `${data.Local ? response.prefix : ""}${data.file}`,
          });
          html += `<div class="col-xs-12 col-sm-6 col-md-6 col-lg-3 mb-3"><div class="cards" data-toggle="tooltip" data-placement="top" title="${data.Description}"><span class="row"><img src="/static/Images/lesson/video.png" id="thumbM${data.id}" class="col-12 img"></span><span class="row row-head pl-3 pr-3 pt-1"><span class="text-left col-10">Video</span><input type="checkbox" class="video_checkbox form-control col-1" value="${data.id}"></span><span class="row row-foot pl-3 pr-3 pb-3"><span class="col-12 text-truncate">${data.Name} </span></span></div></div>`;
        }
      }
      if (type == "pdf") {
        for (let x = 0; x < response.pdf.length; x++) {
          const data = response.pdf[x];
          html += `<div class="col-xs-12 col-sm-6 col-md-6 col-lg-3 mb-3"><div class="cards" data-toggle="tooltip" data-placement="top" title="${data.Description}"><span class="row"><img src="/static/Images/lesson/video.png" alt="" class="col-12 img"></span><span class="row row-head pl-3 pr-3 pt-1"><span class="text-left col-10">PDF</span><input type="checkbox" class="pdf_checkbox form-control col-1" value="${data.id}"></span><span class="row row-foot pl-3 pr-3 pb-3"><span class="col-12 text-truncate">${data.Name}</span></span></div></div>`;
        }
      }
      $("#data_display").html(html);
      generateThumbs(thumbArray);
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
};

const delhomework = (id) => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/delete-homework",
    data: {
      id: id,
    },
    dataType: "json",
    success: function (data) {
      getHomeworks();
      alert(data.message);
    },
    error: function (error) {
      console.log(error.responseText);
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
