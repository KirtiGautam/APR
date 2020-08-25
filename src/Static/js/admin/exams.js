$(function () {
  $(".EXL").addClass("active");
  $(".EXT").addClass("stw");
  $(".EXI").addClass("siw");
  $(".edit-this-type").click(function () {
    $("#exam_id").val(this.id);
    $("#exam_new_name").val($(`#cell${this.id}`).text());
    $("#editClassName").modal();
  });
});

const check = () => {
  if (!$("#exam_name").val()) {
    alert("Exam name cannot be empty!");
    return false;
  }
  return true;
};
