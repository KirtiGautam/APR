$(document).ready(function () {
  getMedia();

  $(".mdl").addClass("active");
  $(".mdt").addClass("stw");
  $(".mdi").addClass("siw");

  $("#dataType").change(function () {
    if (this.value == "video") {
      $(".video_type").removeClass("d-none");
      $(".custom-file").addClass("d-none");
    }
    if (this.value == "pdf") {
      $(".link-div").addClass("d-none");
      $(".video_type").addClass("d-none");
      $(".custom-file").removeClass("d-none");
    }
  });

  $("#video_type").change(function () {
    if (this.value == "local") {
      $(".link-div").addClass("d-none");
      $(".custom-file").removeClass("d-none");
    }
    if (this.value == "other") {
      $(".link-div").removeClass("d-none");
      $(".custom-file").addClass("d-none");
    }
  });

  $("#mediaType").change(function () {
    getMedia();
  });
});

const getMedia = () => {
  const type = $("#mediaType").val();
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
      if (type == "video" || type == "" || type == null) {
        for (let x = 0; x < response.video.length; x++) {
          const data = response.video[x];
          thumbArray.push({
            id: `#thumb${data.id}`,
            link: `${data.Local ? response.prefix : ""}${data.file}`,
          });
          html += `<div class="col-xs-12 col-sm-12 col-md-6 col-lg-3 mb-3"><a href="${
            data.Local ? response.prefix : ""
          }${
            data.file
          }"><div class="cards p-2"><span class="row row-head"><span class="text-left col-10">VIDEO</span></span><span class="row text-center"><span class="col-3"></span><img src="/static/Images/lesson/video.png" id="thumb${
            data.id
          }" class="col-6"></span><span class="row row-foot"><span class="col-8">${
            data.Name
          } </span><span class="description">${
            data.Description
          }</span></span></div></a></div>`;
        }
      }
      if (type == "pdf" || type == "" || type == null) {
        for (let x = 0; x < response.pdf.length; x++) {
          const data = response.pdf[x];
          html += `<div class="col-xs-12 col-sm-12 col-md-6 col-lg-3 mb-3"><a href="${response.prefix}${data.file}"><div class="cards p-2"><span class="row row-head"><span class="text-left col-10">PDF</span></span><span class="row text-center"><span class="col-3"></span><img src="/static/Images/lesson/video.png" alt="" class="col-6"></span><span class="row row-foot"><span class="col-8">${data.Name}</span><span class="description">${data.Description}</span></span></div></a></div>`;
        }
      }
      $("#body").html(html);
      generateThumbs(thumbArray);
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
};

const resetForm = () => {
  $("#dataType").val("");
  $("#video_type").val("");
  $("#FName").val("");
  $("#description").val("");
  $("#video_link").val("");
  $("#file_input").val("");
};

const Validate = (val) => {
  if ($("#dataType").val() == "" || $("#dataType").val() == null) {
    show_alert("Please Select File Type", "warning");
    return false;
  }
  if ($("#dataType").val() == "pdf" && !val) {
    show_alert("Please Select File", "warning");
    return false;
  }
  if ($("#dataType").val() == "video") {
    if ($("#video_type").val() == "" || $("#video_type").val() == null) {
      show_alert("Please Select Video Type", "warning");
      return false;
    }
    if ($("#video_type").val() == "local" && !val) {
      show_alert("Please Select File", "warning");
      return false;
    }
    if (
      $("#video_type").val() == "other" &&
      ($("#video_link").val() == "" || $("#video_link").val() == null)
    ) {
      show_alert("Please Paste your video link", "warning");
      return false;
    }
  }
  if (
    $("#FName").val() == "" ||
    $("#FName").val() == null ||
    $("#description").val() == "" ||
    $("#description").val() == null
  ) {
    show_alert("Please provide description and name of file", "warning");
    return false;
  }
  return true;
};

const getFormData = () => {
  let data = new FormData();
  if ($("#dataType").val() == "video" && $("#video_type").val() == "local") {
    data.append("dataType", "video");
    data.append("videoType", "local");
    data.append("file", document.getElementById("file_input").files[0]);
  }
  if ($("#dataType").val() == "video" && $("#video_type").val() == "other") {
    data.append("dataType", "video");
    data.append("videoType", "youtube");
    data.append("file", $("#video_link").val());
  }
  if ($("#dataType").val() == "pdf") {
    data.append("dataType", "pdf");
    data.append("file", document.getElementById("file_input").files[0]);
  }
  data.append("Name", $("#FName").val());
  data.append("description", $("#description").val());
  return data;
};
