var toolbarOptions = [
  ["bold", "italic", "underline", "strike"], // toggled buttons
  ["blockquote", "code-block"],

  [{ header: 1 }, { header: 2 }], // custom button values
  [{ list: "ordered" }, { list: "bullet" }],
  [{ script: "sub" }, { script: "super" }], // superscript/subscript
  [{ indent: "-1" }, { indent: "+1" }], // outdent/indent
  [{ direction: "rtl" }], // text direction

  [{ size: ["small", false, "large", "huge"] }], // custom dropdown
  [{ header: [1, 2, 3, 4, 5, 6, false] }],

  [{ color: [] }, { background: [] }], // dropdown with defaults from theme
  [{ font: [] }],
  [{ align: [] }],
  ["link"],
  ["clean"], // remove formatting button
];

var quill = new Quill("#body", {
  modules: {
    toolbar: toolbarOptions,
  },
  theme: "snow",
});

let offset = 1;
let loaded = false;

function _(el) {
  return document.getElementById(el);
}

function progressHandler(event) {
  var percent = (event.loaded / event.total) * 100;
  $("#prog-bar")
    .attr("aria-valuenow", Math.round(percent))
    .css("width", Math.round(percent) + "%")
    .text(Math.round(percent) + "%");
}

function completeHandler(event) {
  $("#posts-box").prepend(JSON.parse(event.target.responseText));
  $("#photo").val("");
  quill.root.innerHTML = "";
  $("#message").val("Uplaod Successfull");
  $("#progress-wrap, #post-pic-prev").addClass("d-none");
  $("#prog-bar")
    .attr("aria-valuenow", 0)
    .css("width", 0 + "%")
    .text(0 + "%");
}

function errorHandler(event) {
  $("#message").val("Uplaod Failed");
  $("#progress-wrap, #post-pic-prev").addClass("d-none");
  quill.root.innerHTML = "";
  $("#photo").val("");
  $("#prog-bar")
    .attr("aria-valuenow", 0)
    .css("width", 0 + "%")
    .text(0 + "%");
}

function abortHandler(event) {
  $("#progress-wrap, #post-pic-prev").addClass("d-none");
  $("#message").val("Uplaod Abort");
  quill.root.innerHTML = "";
  $("#photo").val("");
  $("#prog-bar")
    .attr("aria-valuenow", 0)
    .css("width", 0 + "%")
    .text(0 + "%");
}

const posts = (offset) => {
  $.ajax({
    type: "GET",
    url: "/post",
    data: {
      offset: offset,
    },
    dataType: "json",
    success: (data) => {
      console.log(data);
      $("#posts-box").append(data);
      loaded = true;
      offset++;
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
};

$(function () {
  posts(0);
  $("#photo").on("change", function () {
    var reader = new FileReader();

    reader.onload = function (e) {
      $("#post-pic-prev").attr("src", e.target.result).removeClass("d-none");
    };

    reader.readAsDataURL(this.files[0]);
  });

  $("#submit-btn").on("click", function () {
    if (!$("#body").text() && !$("#photo").val()) {
      alert("Please type some text or add a picture to post");
      return;
    }
    var formdata = new FormData();
    if ($("#photo").val()) {
      var file = _("photo").files[0];
      formdata.append("photo", file);
    }
    if ($("#body").text()) formdata.append("body", quill.root.innerHTML);
    else formdata.append("body", "");
    var ajax = new XMLHttpRequest();
    ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.addEventListener("load", completeHandler, false);
    ajax.addEventListener("error", errorHandler, false);
    ajax.addEventListener("abort", abortHandler, false);
    ajax.open("POST", "/post"); // http://www.developphp.com/video/JavaScript/File-Upload-Progress-Bar-Meter-Tutorial-Ajax-PHP
    ajax.setRequestHeader(
      "X-CSRFToken",
      $('meta[name="csrf-token"]').attr("content")
    );
    ajax.send(formdata);
    $("#progress-wrap").removeClass("d-none");
  });
});
