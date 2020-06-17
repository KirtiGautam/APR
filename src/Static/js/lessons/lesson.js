function getlessons(id = "") {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-lessons",
    data: {
      id: $("#class").val(),
      subject: id,
    },
    dataType: "json",
    success: function (data) {
      if (data.body == "") {
        $("#body").html(
          '<h5 class="m-5 text-center"> No lessons available for this subject.</h5>'
        );
      } else {
        $("#body").html(data.body);
      }
      let html = "";
      let subjects = data.subjects;
      for (let i = 0; i < subjects.length; i++) {
        html +=
          "<span onclick='getlessons(" +
          subjects[i].id +
          ")' class='subject col-1 p-2 m-1";
        html +=
          id == subjects[i].id || (id == "" && i == 0) ? " active'>" : "'>";
        html += subjects[i].Name + "</span>  ";
      }
      $("#SB").html(html);
    },
  });
}

function setChapName(id) {
  getMedia($("#dataType").val());
  $("#ChapName").val(id);
}

$(document).ready(function () {
  $("#class").change(function () {
    getlessons();
  });
  $("#dataType").change(function () {
    if (this.value == "pdf") {
      getMedia("pdf");
    } else if (this.value == "test") {
      getQuestions();
    } else {
      getMedia("video");
    }
  });
});

const getQuestions = () => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-questions",
    data: {
      lesson: $("#ChapName").val(),
    },
    dataType: "json",
    success: function (response) {
      let html = "<ol>";
      for (let x = 0; x < response.questions.length; x++) {
        const data = response.questions[x];
        html += `<li id='${data.id}'> ${data.Name} ${data.Difficulty} <span class="col-2 checkbox"><input type="checkbox" id="" disabled></span></li>`;
      }
      html += "</ol>";
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
          html += `<div class="col-xs-12 col-sm-12 col-md-6 col-lg-4 mb-3"><div class="cards p-2"><span class="row row-head"><span class="text-left col-10">VIDEO</span><span class="col-2 checkbox"><input type="checkbox" id="" disabled></span></span><span class="row text-center"><span class="col-3"></span><img src="/static/Images/lesson/video.png" alt="" class="col-6"></span><span class="row row-foot"><span class="col-8">${
            data.Name
          } </span><span class="description">${
            data.Description
          }</span></span></div></div>`;
        }
      }
      if (type == "pdf") {
        for (let x = 0; x < response.pdf.length; x++) {
          const data = response.pdf[x];
          html += `<div class="col-xs-12 col-sm-12 col-md-6 col-lg-4 mb-3"><div class="cards p-2"><span class="row row-head"><span class="text-left col-10">PDF</span><span class="col-2 checkbox"><input type="checkbox" id="" disabled></span></span><span class="row text-center"><span class="col-3"></span><img src="/static/Images/lesson/video.png" alt="" class="col-6"></span><span class="row row-foot"><span class="col-8">${data.Name}</span><span class="description">${data.Description}</span></span></div></div>`;
        }
      }
      $("#data_display").html(html);
    },
  });
};
