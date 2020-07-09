let thumbArr = [];
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(".cards").tooltip({ boundary: "window" });
$(document).ready(function () {
  $("#dataType").change(function () {
    if (!$("#lessons").val()) {
      alert("Please select lesson first");
      this.value = "";
      return;
    }
    if (this.value == "pdf") {
      getMedia("pdf");
      $("#upload_btn, #data_display").removeClass("d-none");
      $("#next_btn, .question_div").addClass("d-none");
    } else if (this.value == "test") {
      getQuestions();
      $("#upload_btn, #data_display").addClass("d-none");
      $("#next_btn, .question_div").removeClass("d-none");
    } else {
      getMedia("video");
      $("#upload_btn, #data_display").removeClass("d-none");
      $("#next_btn, .question_div").addClass("d-none");
    }
  });
  $("#next_btn").click(function () {
    if (!$("#test_name").val() || !$("#test_duration").val()) {
      alert("Please fill necessary details");
      return;
    }
    $("#upload_btn, #data_display").removeClass("d-none");
    $("#next_btn, .question_div, .other_div").addClass("d-none");
  });
  $("#upload_btn").click(function () {
    const Sdata = getSelecteddata();
    if (Sdata.length < 1) {
      alert("Please select at least one data");
      return;
    }
    let data;
    if ($("#dataType").val() == "test") {
      data = {
        Name: $("#test_name").val(),
        duration: $("#test_duration").val(),
        final: $("#final_flag").is(":checked") ? 1 : 0,
        type: $("#dataType").val(),
        data: Sdata,
        lesson: $("#lessons").val(),
        homework: $("#homeworkid").val(),
      };
    } else {
      data = {
        type: $("#dataType").val(),
        data: Sdata,
        lesson: $("#lessons").val(),
        homework: $("#homeworkid").val(),
      };
    }
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
      url: "/add-homework-resource",
      data: data,
      dataType: "json",
      success: function (response) {
        alert(response.message);
      },
      error: function (error) {
        alert(error.responseText);
      },
    });
  });

  $("#delete_btn").click(function () {
    let data = [];
    $(`input.pdf_checks:checkbox:checked`).each(function () {
      data.push(
        JSON.stringify({
          type: "pdf",
          value: $(this).val(),
        })
      );
    });
    $(`input.video_checks:checkbox:checked`).each(function () {
      data.push(
        JSON.stringify({
          type: "video",
          value: $(this).val(),
        })
      );
    });
    if (data.length < 1) {
      alert("Please select some data to delete");
      return;
    }
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
      url: "/delete-homework-media",
      data: {
        data: data,
      },
      dataType: "json",
      success: function (response) {
        alert(response.message);
        location.reload(true);
      },
      error: function (error) {
        alert(error.responseText);
      },
    });
  });

  $("#edit_btn").click(function () {
    $.ajax({
      type: "GET",
      headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
      url: "/get-homework-details",
      data: {
        id: $("#hidden_home_id").val(),
      },
      dataType: "json",
      success: function (response) {
        for (let x in response) {
          $(`#ed_${x}`).val(response[x]);
        }
        $("#edit_modal").modal("show");
      },
      error: function (error) {
        alert(error.responseText);
      },
    });
  });

  $("#update_home_details").click(function () {
    if (!$("#ed_Name").val() || !$("#ed_Instructions").val()) {
      alert("Please fill all the details");
      return;
    }
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
      url: "/update-homework-details",
      data: {
        id: $("#hidden_home_id").val(),
        Name: $("#ed_Name").val(),
        Instructions: $("#ed_Instructions").val(),
      },
      dataType: "json",
      success: function (response) {
        alert(response.message);
        location.reload(true);
      },
      error: function (error) {
        alert(error.responseText);
      },
    });
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
    error: function (error) {
      alert(error.responseText);
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
      let thumbArray = [];
      if (type == "video") {
        for (let x = 0; x < response.video.length; x++) {
          const data = response.video[x];
          thumbArray.push({
            id: `#thumbM${data.id}`,
            duration: `#duram${data.id}`,
            link: `${data.Local ? response.prefix : ""}${data.file}`,
          });
          html += `<div class="col-xs-12 col-sm-6 col-md-6 col-lg-3 mb-3"><div class="cards" data-toggle="tooltip" data-placement="top" title="${data.Description}"><span class="row"><img src="/static/Images/lesson/video.png" id="thumbM${data.id}" class="col-12 img"></span><span class="row row-head pl-3 pr-3 pt-1"><span class="text-left col-10">Video</span><input type="checkbox" class="video_checkbox form-control col-1" value="${data.id}"></span><span class="row row-foot pl-3 pr-3 pb-3"><span class="col-12 text-truncate">${data.Name} </span></span></div></div></div>`;
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

const MARP = (id, check) => {
  if ($(check).prop("checked") == false) {
    return false;
  }
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/mark-homework-pdf-read",
    data: {
      id: id,
    },
    dataType: "json",
    success: function (response) {
      if (!response.success) {
        $(check).prop("checked", false);
      }
      alert(response.message);
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
  return true;
};
