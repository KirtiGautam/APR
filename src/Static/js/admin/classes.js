$(document).ready(function () {


    $('.CSL').addClass('active');
    $('.CST').addClass('stw');
    $('.CSI').addClass('siw');

    $('#secB, #classB, #subB, #TeachB, #syllB').click(function () {
        closeTabs();
        const id = this.id.substring(0, this.id.length - 1) + 'T';
        $('#' + id).removeClass('d-none');
        $(this).addClass('menu-active');
    });

    //Class Tab
    $('#newClass').click(function () {
        if ($('#CN').val() == '' ||
            $('#CN').val() == null
        ) {
            alert('Please Enter Class Name')
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/new-class',
            data: {
                'name': $('#CN').val(),
            },
            dataType: 'json',
            success: function (data) {
                getclasses('');
                $('#CN').val('')
                alert(data.message);
            }
        });
    })


    $('#CSsearch').keyup(delay(function (e) {
        getclasses(this.value);
    }, 500));

    $('#updateClassName').click(function () {
        if ($('#NewClassName').val() == '' ||
            $('#NewClassName').val() == null
        ) {
            alert('Please enter a new Class Name');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/edit-class',
            data: {
                'id': $('#hiddenclassid').val(),
                'name': $('#NewClassName').val(),
            },
            dataType: 'json',
            success: function (data) {
                getclasses('');
                alert(data.message);
                $('#NewClassName').val('');
            }
        });
    })

    //Subject Tab
    $('#SAS').click(function () {
        let data = getSelectedClasses();
        if (data.length != 1) {
            alert('Cannot perform this operation, Please select a single class');
            return;
        }
        if ($('#SubName').val() == '' ||
            $('#SubName').val() == null
        ) {
            alert('Please enter a Subject Name');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/new-subject',
            data: {
                'Name': $('#SubName').val(),
                'id': data[0],
            },
            dataType: 'json',
            success: function (data) {
                getSubjects('');
                $('#SubName').val('');
                alert(data.message);
            }
        });
    });

    $('#SUBC').keyup(delay(function (e) {
        getSubjects(this.value)
    }, 500));

    $('#updateSubjectName').click(function () {
        if ($('#NewSubjectName').val() == '' ||
            $('#NewSubjectName').val() == null
        ) {
            alert('Please enter a new Subject Name');
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/edit-subject',
            data: {
                'id': $('#hiddensubjectid').val(),
                'name': $('#NewSubjectName').val(),
            },
            dataType: 'json',
            success: function (data) {
                getSubjects('');
                alert(data.message);
                $('#NewSubjectName').val('');
            }
        });
    })

    //Assign Teacher Tab

    $('.teacher').change(function(){
        assignTeacher('teacher', this.id, this.value)
    })

    $('.backupteacher').change(function(){
        assignTeacher('backup', this.id, this.value)
    })

});


const closeTabs = () => {
    $('#secT, #classT, #subT, #TeachT, #syllT').addClass('d-none');
    $('#secB, #classB, #subB, #TeachB, #syllB').removeClass('menu-active');
    return;
}


function delay(callback, ms) {
    var timer = 0;
    return function () {
        var context = this, args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function () {
            callback.apply(context, args);
        }, ms || 0);
    };
}


const getclasses = term => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-class',
        data: {
            'term': term
        },
        dataType: 'json',
        success: function (data) {
            let html = ''
            for (let x = 0; x < data.class.length; x++) {
                const sub = data.class[x];
                html += `<tr><td>${sub['name']}</td><td><i class="fas fa-pen actions" onclick="editClass(this);" id="${sub['id']}"></i></td><td><i class="fas fa-trash actions" onclick="deleteClass(this);" id="${sub['id']}"></i></td></tr>`
            }
            $('#CsearchTbody').html(html);
        },
        error: function (err) {
            alert(err)
        }
    })
}

const deleteClass = e => {
    if (confirm('Are you sure you want to delete this Class ?')) {
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/delete-class',
            data: {
                'id': e.id,
            },
            dataType: 'json',
            success: function (data) {
                getclasses('');
                alert(data.message);
            }
        });
    }
}

const editClass = e => {
    $('#hiddenclassid').val(e.id);
    $('#editClassName').modal('show');
}


//Subject Tab
const getSelectedClasses = () => {
    let data = [];
    $('input.SCC:checkbox:checked').each(function () {
        data.push($(this).val());
    });
    return data;
}


const getSubjects = term => {
    $.ajax({
        type: "GET",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/get-subs',
        data: {
            'term': term
        },
        dataType: 'json',
        success: function (data) {
            let html = ''
            for (let x = 0; x < data.subject.length; x++) {
                const sub = data.subject[x];
                html += `<tr><td>${sub['Name']}</td><td>${sub['Class']}</td><td><i class="fas fa-pen actions" onclick="editSubject(this);" id="${sub['id']}"></i></td><td><i class="fas fa-trash actions" onclick="deleteSubject(this);" id="${sub['id']}"></i></td></tr>`
            }
            $('#SCTbody').html(html);
        },
        error: function (err) {
            console.log(err)
        }
    })
}


const deleteSubject = e => {
    if (confirm('Are you sure you want to delete this Subject ?')) {
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
            url: '/delete-subject',
            data: {
                'id': e.id,
            },
            dataType: 'json',
            success: function (data) {
                getSubjects('');
                alert(data.message);
            }
        });
    }
}

const editSubject = e => {
    $('#hiddensubjectid').val(e.id);
    $('#editSubjectName').modal('show');
}

//Assign teacher Tab

const assignTeacher = (type, id, teacher) => {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') },
        url: '/assign-teacher',
        data: {
            'id': id,
            'type': type,
            'teacher': teacher,
        },
        dataType: 'json',
        success: function (data) {
            alert(data.message);
            window.location.reload(true); 
        }
    });
}