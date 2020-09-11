$(function () {
  let dh = timeLeft.split("T");
  timeLeft = dh[0] + "T" + (dh[1].length == 8 ? dh[1] : "0" + dh[1]);
  var countdown = setInterval(function () {
    var over = new Date(timeLeft).getTime();
    var now = new Date().getTime();
    var timeleft = over - now;
    var hours = Math.floor(
      (timeleft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    var minutes = Math.floor((timeleft % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((timeleft % (1000 * 60)) / 1000);
    if (timeleft < 0) {
      clearInterval(countdown);
      $("#left-time").text(`Time UP!`);
    } else $("#left-time").text(`Time left ${hours}:${minutes}:${seconds}`);
  }, 1000);
  $("#file-submission").change(function () {
    console.log(this.files[0]);
    const name = this.value;
    // Allowing file type
    var allowedExtensions = /(\.pdf)$/i;

    if (!allowedExtensions.exec(name)) {
      alert("Invalid file type");
      this.value = "";
      return false;
    }
    $("#file-submission-label").text(this.files[0].name);
  });
  $("#file-submission-btn").click(function () {
    if (!$("#file-submission").val()) {
      alert("Please select a file");
      return false;
    }
    var file = _("file-submission").files[0];
    // alert(file.name+" | "+file.size+" | "+file.type);
    var formdata = new FormData();
    formdata.append("file-submission", file);
    var ajax = new XMLHttpRequest();
    ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.addEventListener("load", completeHandler, false);
    ajax.addEventListener("error", errorHandler, false);
    ajax.addEventListener("abort", abortHandler, false);
    ajax.open("POST", window.location.href); // http://www.developphp.com/video/JavaScript/File-Upload-Progress-Bar-Meter-Tutorial-Ajax-PHP
    ajax.setRequestHeader(
      "X-CSRFToken",
      $('meta[name="csrf-token"]').attr("content")
    );
    ajax.send(formdata);
    $("#progress-wrap").removeClass("d-none");
  });
  $("#finish-exam-btn").click(function () {
    completeEx();
  });
});

const completeEx = () => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: window.location.href,
    data: {
      finissh: true,
    },
    dataType: "json",
    success: (data) => (location = "/paper-finished"),
    error: (error) => alert(error.responseText),
  });
};

function _(el) {
  return document.getElementById(el);
}

function progressHandler(event) {
  _("loaded_n_total").innerHTML =
    "Uploaded " + event.loaded + " bytes of " + event.total;
  var percent = (event.loaded / event.total) * 100;
  _("progressBar").value = Math.round(percent);
  _("status").innerHTML = Math.round(percent) + "% uploaded... please wait";
}

function completeHandler(event) {
  showpdf(JSON.parse(event.target.responseText));
  _("progressBar").value = 0; //wil clear progress bar after successful upload
  $("#file-submission").val("");
}

function errorHandler(event) {
  _("status").innerHTML = "Upload Failed";
  $("#file-submission").val("");
}

function abortHandler(event) {
  $("#file-submission").val("");
}

const showpdf = (url) => {
  // Loaded via <script> tag, create shortcut to access PDF.js exports.
  var pdfjsLib = window["pdfjs-dist/build/pdf"];

  // The workerSrc property shall be specified.
  pdfjsLib.GlobalWorkerOptions.workerSrc =
    "//mozilla.github.io/pdf.js/build/pdf.worker.js";

  // Asynchronous download of PDF
  var loadingTask = pdfjsLib.getDocument(url);
  loadingTask.promise.then(
    function (pdf) {
      console.log("PDF loaded");

      // Fetch the first page
      var pageNumber = 1;
      pdf.getPage(pageNumber).then(function (page) {
        console.log("Page loaded");

        var scale = 1.5;
        var viewport = page.getViewport({ scale: scale });

        // Prepare canvas using PDF page dimensions
        var canvas = document.getElementById("the-canvas");
        var context = canvas.getContext("2d");
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        // Render PDF page into canvas context
        var renderContext = {
          canvasContext: context,
          viewport: viewport,
        };
        var renderTask = page.render(renderContext);
        renderTask.promise.then(function () {
          console.log("Page rendered");
        });
      });
    },
    function (reason) {
      // PDF loading error
      console.error(reason);
    }
  );
};
