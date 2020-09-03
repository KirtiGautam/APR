let rows = 1;

$(function () {
  $("#exam-next-btn").click(function () {
    $("#body").modal("hide");
    $("#body2").modal();
  });
  $("#mode").change(function () {
    for (let index = 1; index <= rows; index++) {
      let loc = document.getElementById(`location${index}`);
      if ($("#mode").val() === "O") loc.setAttribute("readonly", true);
      else loc.removeAttribute("readonly", false);
      loc.value = "ONLINE";
    }
  });
  $("#add-row-btn").click(function () {
    $("#t-body").append(
      `<tr id="Drow${++rows}">
      <td><button class="btn button-5" onclick="removeRow(${rows});" ><i class="far fa-times-circle"></i></button></td>
    <td>${rows}</td>
    <td>
        <select id="class${rows}" name="class${rows}" class="custom-select" onchange="getSubjects(this.value, ${rows})">
            ${$("#class1").html()}
        </select>
    </td>
    <td>
        <select id="subject${rows}" name="subject${rows}" class="custom-select">
          <option value="" disabled selected>Select Class first</option>
        </select>
    </td>
    <td><input type="text" name="location${rows}" id="location${rows}" class="form-control" ${
        $("#mode").val() === "O" ? "readonly" : ""
      } value='${$("#mode").val() === "O" ? "ONLINE" : ""}'></td>
    <td><input type="datetime-local" name="dNt${rows}" id="dNt${rows}" class="form-control"></td>
    <td>
        <input type="number" name="max-marks${rows}" id="max-marks${rows}" class="form-control">
    </td>
    <td>
        <input type="number" name="pass-marks${rows}" id="pass-marks${rows}" class="form-control">
    </td>
    <td>
        <input type="number" name="duration${rows}" id="duration${rows}" class="form-control">
    </td>
</tr>`
    );
  });
});

const getSubjects = (Class, row) => {
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr("content") },
    url: "/get-subjects",
    data: {
      id: Class,
    },
    dataType: "json",
    success: function (data) {
      let html = '<option value="" selected disabled>Subjects</option>';
      for (x in data.subjects) {
        html += `<option value="${data.subjects[x].id}" >${data.subjects[x].Name}</option>`;
      }
      document.getElementById(`subject${row}`).innerHTML = html;
    },
    error: function (error) {
      alert(error.responseText);
    },
  });
};

const check = () => {
  $("#hidden_sn_count").val(rows);
  if (!$("#exam_name").val() || !$("#mode").val() || !$("#exam_type").val()) {
    console.log($("#exam_name").val(), $("#mode").val(), $("#exam_type").val());
    alert("Please fill all the values");
    return false;
  }
  for (let index = 1; index <= rows; index++) {
    let subject = document.getElementById(`subject${index}`).value;
    let location = document.getElementById(`location${index}`).value;
    let dNt = document.getElementById(`dNt${index}`).value;
    let maxMarks = document.getElementById(`max-marks${index}`).value;
    let passMarks = document.getElementById(`pass-marks${index}`).value;
    let duration = document.getElementById(`duration${index}`).value;
    if (!subject || !location || !dNt || !maxMarks || !passMarks || !duration) {
      alert("Please fill all the values");
      return false;
    }
    if (parseInt(maxMarks) < parseInt(passMarks)) {
      alert(`Max marks cannot be less than pass marks in S.No. ${index}`);
      return false;
    }
    if (new Date(dNt) < new Date()) {
      alert(`Cannot schedule Exam in past at S.No. ${index}`);
      return false;
    }
  }
  return true;
};

const removeRow = (id) => {
  document.getElementById(`Drow${id}`).remove();
  --rows;
};
