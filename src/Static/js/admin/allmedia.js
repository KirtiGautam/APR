$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(".cards").tooltip({ boundary: "window" });

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
    if (this.value == "local" || this.value == 'vimeo') {
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

  $("#edit_btn").click(function () {
    const Sdata = getSelectedData();
    if (Sdata.length != 1) {
      alert("Cannot perform this operation, Please select single data");
      return;
    }
    let da = JSON.parse(Sdata[0]);
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
      url: "/get-media-details",
      data: da,
      dataType: "json",
      success: function (response) {
        $("#edit_media_details").modal("show");
        $("#media_type_hidden").val(da.type);
        $("#media_id_hidden").val(da.value);
        for (x in response) {
          $(`#${x}`).val(response[x]);
        }
        console.log(response);
      },
      error: function (error) {
        console.log(error);
        alert("Some error occurred");
      },
    });
  });

  $("#delete_btn").click(function () {
    const Sdata = getSelectedData();
    if (Sdata.length < 1) {
      alert("Please select some items to delete");
      return;
    }
    if (confirm("Are you sure you want to delete the selected items?")) {
      $.ajax({
        type: "POST",
        headers: {
          "X-CSRFToken": $('meta[name="csrf-token"]').attr("content"),
        },
        url: "/delete-media",
        data: {
          data: Sdata,
        },
        success: function (response) {
          getMedia();
          alert(response.message);
        },
        error: function (error) {
          alert(error.responseText);
        },
      });
    }
  });

  $("#update_details_btn").click(function () {
    const Name = $("#Name").val();
    const Description = $("#Description").val();
    if (!Name || !Description) {
      alert("Details cannot be empty");
      return;
    }
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
      url: "/update-media",
      data: {
        id: $("#media_id_hidden").val(),
        Name: Name,
        Description: Description,
        type: $("#media_type_hidden").val(),
      },
      success: function (response) {
        getMedia();
        alert(response.message);
      },
      error: function (error) {
        alert(error.responseText);
      },
    });
  });

  $('#search_btn').click(function () {
    getMedia();
  });

});

const getMedia = () => {
  const type = $("#mediaType").val();
  $.ajax({
    type: "GET",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-media",
    data: {
      type: type,
      term: $('#term').val()
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
          html += `<div class="col-xs-12 col-sm-6 col-md-6 col-lg-3 mb-3">
          <a href="${data.Local ? response.prefix : ""}${
            data.file
            }"><div class="cards" data-toggle="tooltip" data-placement="top" title="${
            data.Description
            }"><span class="row"><img src="/static/Images/lesson/video.png" id="thumb${
            data.id
            }" class="col-12 img"></span><span class="row row-head pl-3 pr-3 pt-1"><span class="text-left col-10 pt-1">Video</span><input type="checkbox" class="form-control video_checks col-1" value="${
            data.id
            }" ></span><span class="row row-foot pl-3 pr-3 pb-3"><span class="col-12 text-truncate">${
            data.Name
            } </span></span></div></a></div>`;
        }
      }
      if (type == "pdf" || type == "" || type == null) {
        for (let x = 0; x < response.pdf.length; x++) {
          const data = response.pdf[x];
          html += `<div class="col-xs-12 col-sm-6 col-md-6 col-lg-3 mb-3"><a href="${response.prefix}${data.file}"><div class="cards" data-toggle="tooltip" data-placement="top" title="${
            data.Description
            }><span class="row"><img src="/static/Images/lesson/video.png" alt="" class="col-12 img"></span><span class="row row-head pl-3 pr-3 pt-1"><span class="text-left col-10 pt-1">PDF</span><input type="checkbox" class="form-control pdf_checks col-1" value="${data.id}" ></span><span class="row row-foot pl-3 pr-3 pb-3"><span class="col-12 text-truncate">${data.Name}</span></span></div></a></div>`;
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

const getSelectedData = () => {
  let data = [];
  const type = $("#mediaType").val();
  if (type == "pdf" || !type) {
    $("input.pdf_checks:checkbox:checked").each(function () {
      data.push(
        JSON.stringify({
          type: "pdf",
          value: $(this).val(),
        })
      );
    });
  }
  if (type == "video" || !type) {
    $("input.video_checks:checkbox:checked").each(function () {
      data.push(
        JSON.stringify({
          type: "video",
          value: $(this).val(),
        })
      );
    });
  }

  return data;
};


const commit_video_to_db = (name, description, link) => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/upload-allmedia",
    data: {
      Name: name,
      description: description,
      dataType: "video",
      videoType: "youtube",
      file: link,
    },
    success: function (response) {
      show_alert('<strong>Upload Successful!</strong>', 'success')
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
}

const checkStatus = video_id => {
  $.ajax({
    type: 'GET',
    headers: { 'Authorization': 'Bearer 6c21103f46f31555ecd9a9a69ac77f7b' },
    url: `https://api.vimeo.com/videos/${video_id}`,
    success: function (result) {
      if (result.transcode.status == 'complete') {
        var url = 'https://player.vimeo.com/video/' + video_id;
        commit_video_to_db(result.name, result.description, url);
        // showMessage('<strong>Upload Successful</strong>: check uploaded video @ <a href="' + url + '">' + url + '</a>. Open the Console for the response details.')
      } else if (result.transcode.status == 'error') {
        show_alert('Error in processing the video', 'danger')
      } else {
        show_alert('Please Wait, Your video is being processed <div class="spinner-border text-info" role="status"><span class= "sr-only"> Loading...</span> ', 'warning')
        setTimeout(function () {
          checkStatus(video_id)
        }, 6000)
      }
    }
  });
}


const upload_to_vimeo = () => {
  if (!$('#file_input').val()) {
    alert('Please select a video to be uploaded');
    return;
  }
  if (!$('#FName').val()) {
    alert('Please enter Video Name');
    return;
  }
  if (!$('#description').val()) {
    alert('Please enter Video Description');
    return;
  }

  alert_wrapper.innerHTML = "";

  // Disable the input during upload
  input.disabled = true;

  // Hide the upload button
  upload_btn.classList.add("d-none");

  // Show the loading button
  loading_btn.classList.remove("d-none");

  // Show the cancel button
  cancel_btn.classList.remove("d-none");

  let uploader = new VimeoUpload({
    name: $('#FName').val(),
    description: $('#description').val(),
    private: false,
    file: document.getElementById("file_input").files[0],
    token: '6c21103f46f31555ecd9a9a69ac77f7b',
    upgrade_to_1080: false,
    onError: function (data) {
      show_alert(JSON.parse(data).error, danger)
      reset();
      // showMessage('<strong>Error</strong>: ' + JSON.parse(data).error, 'danger')
    },
    onProgress: function (data) {

      // Show the progress bar
      progress_wrapper.classList.remove("d-none");
      progress.setAttribute("style", `width: ${Math.floor((data.loaded / data.total) * 100)}%`);
      progress_status.innerText = `${Math.floor((data.loaded / data.total) * 100)}% uploaded`;
      // updateProgress(data.loaded / data.total)
    },
    onComplete: function (videoId, index) {
      var url = 'https://vimeo.com/' + videoId
      console.log(url);

      if (index > -1) {
        /* The metadata contains all of the uploaded video(s) details see: https://developer.vimeo.com/api/endpoints/videos#/{video_id} */
        url = this.metadata[index].link //

        /* add stringify the json object for displaying in a text area */
        var pretty = JSON.stringify(this.metadata[index], null, 2)

        console.log(pretty) /* echo server data */
      }
      checkStatus(videoId);

      reset();
      // showMessage('<strong>Upload Successful</strong>: check uploaded video @ <a href="' + url + '">' + url + '</a>. Open the Console for the response details.')
    }
  });
  uploader.upload()
}