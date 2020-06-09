function getExtension(filename) {
    var parts = filename.split('.');
    return parts[parts.length - 1];
}

function ispdf(filename) {
    var ext = getExtension(filename);
    switch (ext.toLowerCase()) {
        case 'pdf':
            return true;
    }
    return false;
}

function isxls(filename) {
    var ext = getExtension(filename);
    switch (ext.toLowerCase()) {
        case 'xls':
        case 'xlsx':
            return true;
    }
    return false;
}

function isVideo(filename) {
    var ext = getExtension(filename);
    switch (ext.toLowerCase()) {
        case 'm4v':
        case 'avi':
        case 'mpg':
        case 'mp4':
            return true;
    }
    return false;
}


var progress = document.getElementById("progress");
var progress_wrapper = document.getElementById("progress_wrapper");
var progress_status = document.getElementById("progress_status");

// Get a reference to the 3 buttons
var upload_btn = document.getElementById("upload_btn");
var loading_btn = document.getElementById("loading_btn");
var cancel_btn = document.getElementById("cancel_btn");

// Get a reference to the alert wrapper
var alert_wrapper = document.getElementById("alert_wrapper");

// Get a reference to the file input element & input label
var input = document.getElementById("file_input");
var file_input_label = document.getElementById("file_input_label");

// Function to show alerts
function show_alert(message, alert) {

    alert_wrapper.innerHTML = `
<div id="alert" class="alert alert-${alert} alert-dismissible fade show" role="alert">
    <span>${message}</span>
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
</div>
`

}

// Function to upload file
function upload(url) {

    // Reject if the file input is empty & throw alert
    if (!input.value) {

        show_alert("No file selected", "warning")

        return;

    }

    if (!Validate()) {
        return;
    }

    // Create a new FormData instance
    var data = getFormData();

    // Create a XMLHTTPRequest instance
    var request = new XMLHttpRequest();

    // Set the response type
    request.responseType = "json";

    // Clear any existing alerts
    alert_wrapper.innerHTML = "";

    // Disable the input during upload
    input.disabled = true;

    // Hide the upload button
    upload_btn.classList.add("d-none");

    // Show the loading button
    loading_btn.classList.remove("d-none");

    // Show the cancel button
    cancel_btn.classList.remove("d-none");

    // Show the progress bar
    progress_wrapper.classList.remove("d-none");

    // Get a reference to the file
    var file = input.files[0];

    // Get a reference to the filename
    var filename = file.name;

    // Get a reference to the filesize & set a cookie
    var filesize = file.size;
    document.cookie = `filesize=${filesize}`;

    // request progress handler
    request.upload.addEventListener("progress", function (e) {

        // Get the loaded amount and total filesize (bytes)
        var loaded = e.loaded;
        var total = e.total

        // Calculate percent uploaded
        var percent_complete = (loaded / total) * 100;

        // Update the progress text and progress bar
        progress.setAttribute("style", `width: ${Math.floor(percent_complete)}%`);
        progress_status.innerText = `${Math.floor(percent_complete)}% uploaded`;

    })

    // request load handler (transfer complete)
    request.addEventListener("load", function (e) {

        if (request.status == 200) {

            show_alert(`${request.response.message}`, "success");

        }
        else {

            show_alert(`Error uploading file`, "danger");

        }

        reset();

    });

    // request error handler
    request.addEventListener("error", function (e) {

        reset();

        show_alert(`Error uploading file`, "warning");

    });

    // request abort handler
    request.addEventListener("abort", function (e) {

        reset();

        show_alert(`Upload cancelled`, "primary");

    });

    // Append the file to the FormData instance
    if ($('#dataType').val() == 'csv') {
        var selectedFile = file;
        var reader = new FileReader();
        reader.onload = (function (file) {
            return function (event) {
                var dat = event.target.result;
                var workbook = XLSX.read(dat, {
                    type: 'binary'
                });
                let json_data = [];
                workbook.SheetNames.forEach(function (sheetName) {

                    var XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
                    var json_object = JSON.stringify(XL_row_object);
                    console.log(json_object);
                    json_data.push(json_object);
                })
                data.append("file", json_data);
                // Open and send the request
                request.open("post", url);

                //Add csrf
                request.setRequestHeader("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));

                request.send(data);
            };
        })(file);

        reader.onerror = function (event) {
            console.error("File could not be read! Code " + event.target.error.code);
        };

        reader.readAsBinaryString(selectedFile);

    } else {
        data.append("file", file);
        // Open and send the request
        request.open("post", url);

        //Add csrf
        request.setRequestHeader("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));

        request.send(data);
    }




    cancel_btn.addEventListener("click", function () {

        request.abort();

    })

}

// Function to update the input placeholder
function input_filename() {

    file_input_label.innerText = input.files[0].name;

}

// Function to reset the page
function reset() {

    // Clear the input
    input.value = null;

    // Hide the cancel button
    cancel_btn.classList.add("d-none");

    // Reset the input element
    input.disabled = false;

    // Show the upload button
    upload_btn.classList.remove("d-none");

    // Hide the loading button
    loading_btn.classList.add("d-none");

    // Hide the progress bar
    progress_wrapper.classList.add("d-none");

    // Reset the progress bar state
    progress.setAttribute("style", `width: 0%`);

    // Reset the input placeholder
    file_input_label.innerText = "Select file";

    resetForm();

}
