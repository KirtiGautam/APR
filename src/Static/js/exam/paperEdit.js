$(function () {
  $("#inp-fill-add").click(function () {
    let index = parseInt($("#hidden-fill-count").val());
    $("#hidden-fill-count").val(++index);
    let html = `<textarea name="fill-question${index}" id="fill-question${index}" class="form-control"></textarea>`;
    $("#fill-up-blanks").append(html);
  });
  $("#QType").change(function () {
    if (this.value == "O") {
      $("#Objective-sect").removeClass("d-none");
      $("#Fill-sect").addClass("d-none");
      $("#Short-sect").addClass("d-none");
      $("#Long-sect").addClass("d-none");
      $("#No-sect").addClass("d-none");
    } else if (this.value == "S") {
      $("#Objective-sect").addClass("d-none");
      $("#Fill-sect").addClass("d-none");
      $("#Short-sect").removeClass("d-none");
      $("#Long-sect").addClass("d-none");
      $("#No-sect").addClass("d-none");
    } else if (this.value == "L") {
      $("#Objective-sect").addClass("d-none");
      $("#Fill-sect").addClass("d-none");
      $("#Short-sect").addClass("d-none");
      $("#Long-sect").removeClass("d-none");
      $("#No-sect").addClass("d-none");
    } else if (this.value == "U") {
      $("#Objective-sect").addClass("d-none");
      $("#Fill-sect").removeClass("d-none");
      $("#Short-sect").addClass("d-none");
      $("#Long-sect").addClass("d-none");
      $("#No-sect").addClass("d-none");
    } else {
      $("#Objective-sect").addClass("d-none");
      $("#Fill-sect").addClass("d-none");
      $("#Short-sect").addClass("d-none");
      $("#Long-sect").addClass("d-none");
      $("#No-sect").removeClass("d-none");
    }
  });
});

const check = () => {
  if (!$("#QSNo").val() || !$("#QSNo").val() < 0) {
    alert("Please Enter a valid Serial Number");
    return false;
  } else if (!$("#QType").val()) {
    alert("Please select a Question Type");
    return false;
  } else if (!$("#max_marks").val()) {
    alert("Please enter Max marks for the question");
    return false;
  } else if ($("#max_marks").val() > parseInt(marks)) {
    alert("Max marks exceed the limit");
    return false;
  } else if ($("#QType").val() == "O") {
    if (!$("#Question-text").val() && !$("#Question-Image").val()) {
      alert("Please add image or Text in Question");
      return false;
    }
    for (let index = 1; index < 5; index++) {
      if (!$(`#op${index}-text`).val() && !$(`#op${index}-file`).val()) {
        alert(`Please add image or Text in option ${index}`);
        return false;
      }
    }
    if (!$("#correct-option").val()) {
      alert(`Please select a correct option`);
      return false;
    }
    if (!$("#correct-explanation").val()) {
      alert("Please type a explanation for the answer");
      return false;
    }
  } else if ($("#QType").val() == "S") {
    if (!$("#short-Question-text").val() && !$("#short-Question-file").val()) {
      alert("Please type a short Question or add Question image");
      return false;
    } else if (!$("#short-Question-answer").val()) {
      alert("Please type a answer to question");
      return false;
    }
  } else if ($("#QType").val() == "L") {
    if (!$("#long-Question-text").val() && !$("#long-Question-file").val()) {
      alert("Please type a short Question or add Question image");
      return false;
    } else if (!$("#long-Question-answer").val()) {
      alert("Please type a answer to question");
      return false;
    }
  } else if ($("#QType").val() == "U") {
    if (!$("#fill-question").val() && !$("#fill-question-file").val()) {
      alert("Please type a fill up Question or add Question image");
      return false;
    }
    for (
      let index = 1;
      index <= document.getElementById("hidden-fill-count").value;
      index++
    ) {
      if (!document.getElementById(`fill-question${index}`).value) {
        alert(`Please fill the answer blanks ${index}`);
        return false;
      }
    }
  } else {
    alert("Please select a value from question type");
    return false;
  }
  return true;
};

const handleChange = (name, file) => {
  if (file.files[0].size > 2097152) {
    alert("File too big, please select image less than 2 mb");
    $(`#${file.id}`).val("");
    return;
  }
  var reader = new FileReader();

  reader.onload = function (e) {
    $(name).attr("src", e.target.result).removeClass("d-none");
  };

  reader.readAsDataURL(file.files[0]);
};

const getQuestion = (id) => {
  $.ajax({
    type: "GET",
    url: "/edit-question-details",
    data: {
      id: id,
    },
    dataType: "json",
    success: function (data) {
      $("#edit-question-id").val(data.id);
      $("#edit-QSNo").val(data.SNo);
      $("#edit-max_marks").val(data.Max_Marks);
      if (data.Type == "O") {
        $("#edit-Objective-sect").removeClass("d-none");
        $("#edit-Fill-sect").addClass("d-none");
        $("#edit-Short-sect").addClass("d-none");
        $("#edit-Long-sect").addClass("d-none");
        $("#edit-Question-text").val(data.Text);
        if (data.Asset)
          $("#edit-obj-img-prev").attr("src", data.Asset).removeClass("d-none");
        let options =
          "<option value='' selected disabled>Select option</option>";
        data.options.forEach((element, index) => {
          $(`#edit-op${index + 1}-text`).val(element.Text);
          $(`#hidden-edit-op${index + 1}`).val(element.id);
          if (element.Asset)
            $(`#edit-obj-op${index + 1}-prev`)
              .attr("src", `/Media/${element.Asset}`)
              .removeClass("d-none");
          options += `<option value="${element.id}">${
            index == 0 ? "A" : index == 1 ? "B" : index == 2 ? "C" : "D"
          }</option>`;
        });
        $(`#edit-correct-option`).html(options).val(data.Answer.Option);
        $(`#edit-correct-explanation`).val(data.Answer.Explanation);
        $(`#hidden-edit-ob-answer`).val(data.Answer.id);
      } else if (data.Type == "S") {
        $("#edit-Objective-sect").addClass("d-none");
        $("#edit-Fill-sect").addClass("d-none");
        $("#edit-Short-sect").removeClass("d-none");
        $("#edit-Long-sect").addClass("d-none");
        $("#edit-short-Question-text").val(data.Text);
        $("#edit-short-Question-id").val(data.id);
        $("#edit-short-Answer-id").val(data.Answer.id);
        $("#edit-short-Question-answer").val(data.Answer.Explanation);
        if (data.Asset)
          $(`#edit-short-img-prev`)
            .attr("src", data.Asset)
            .removeClass("d-none");
      } else if (data.Type == "L") {
        $("#edit-Objective-sect").addClass("d-none");
        $("#edit-Fill-sect").addClass("d-none");
        $("#edit-Short-sect").addClass("d-none");
        $("#edit-Long-sect").removeClass("d-none");
        $("#edit-long-Question-text").val(data.Text);
        $("#edit-long-Question-id").val(data.id);
        $("#edit-long-Answer-id").val(data.Answer.id);
        $("#edit-long-Question-answer").val(data.Text);
        if (data.Asset)
          $(`#edit-long-img-prev`)
            .attr("src", data.Asset)
            .removeClass("d-none");
      } else {
        $("#edit-Objective-sect").addClass("d-none");
        $("#edit-Fill-sect").removeClass("d-none");
        $("#edit-Short-sect").addClass("d-none");
        $("#edit-Long-sect").addClass("d-none");
        $("#edit-fill-question").val(data.Text);
        $("#edit-fill-question-id").val(data.id);
        $("#edit-fill-answer-id").val(data.Answer.id);
        if (data.Asset)
          $(`#edit-up-img-prev`).attr("src", data.Asset).removeClass("d-none");
        $("#edit-hidden-fill-count").val(data.Answer.blanks.length);
        let blanks = "";
        data.Answer.blanks.forEach((element, index) => {
          blanks += `<textarea name="edit-fill-question${
            index + 1
          }" id="edit-fill-question${
            index + 1
          }" class="form-control" >${element}</textarea>`;
        });
        $("#edit-fill-up-blanks").append(blanks);
      }
      $("#question-edit-modal").modal();
      console.log(data);
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
};

const markAsFile = (id, btn) => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/mark-question-file",
    data: {
      id: id,
    },
    dataType: "json",
    success: (data) => (btn.innerText = data),
    error: (error) => alert(error.responseText),
  });
};

const newSectionCheck = (number) => {
  if (!$(`#start_number${number}`).val() || !$(`#end_number${number}`).val()) {
    alert("Please fill start number and end number");
    return false;
  }
  if (
    !isFinite($(`#start_number${number}`).val()) ||
    !isFinite(!$(`#end_number${number}`).val())
  ) {
    alert("Please fill a valid Question number");
    return false;
  }
  return true;
};
