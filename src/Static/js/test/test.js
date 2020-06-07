//calculate the seconds 
var secs;
var mins;

//countdown function is evoked when page is loaded 
function countdown(duration) {
    arr = duration.split(':');
    mins = Number(arr[0]);
    secs = (mins * 60) + Number(arr[1]);
    setTimeout('Decrement()', 60);
}

//Decrement function decrement the value. 
function Decrement() {
    if (document.getElementById) {
        minutes = document.getElementById("timer");

        //if less than a minute remaining 
        //Display only seconds value. 
        if (secs < 59) {
            minutes.innerHTML = 'Time left: 00:' + secs + ' Mins';
        }

        //Display both minutes and seconds 
        //getminutes and getseconds is used to 
        //get minutes and seconds 
        else {
            minutes.innerHTML = 'Time left: ' + getminutes() + ':' + getseconds() + ' Mins';
        }
        //when less than a minute remaining 
        //colour of the minutes and seconds 
        //changes to red 
        if (mins < 1) {
            minutes.style.color = "red";
        }
        //if seconds becomes zero, 
        //then page alert time up 
        if (secs < 0) {
            alert('Time up');            
            minutes.innerHTML = 'Time Left: 00:00 Mins';
            $('#myform').submit();
        }
        //if seconds > 0 then seconds is decremented 
        else {
            secs--;
            setTimeout('Decrement()', 1000);
        }
    }
}

function getminutes() {
    //minutes is seconds divided by 60, rounded down 
    mins = Math.floor(secs / 60);
    return mins;
}

function getseconds() {
    //take minutes remaining (as seconds) away  
    //from total seconds remaining 
    return secs - Math.round(mins * 60);
}

function SubmitFunction() {
    submitted.innerHTML = "Time is up!";
    document.getElementById('myform').submit();

}


function set(QID, option, g) {
    $('#' + QID + 'A').css('background-color', '#FFFFFF');
    $('#' + QID + 'B').css('background-color', '#FFFFFF');
    $('#' + QID + 'C').css('background-color', '#FFFFFF');
    $('#' + QID + 'D').css('background-color', '#FFFFFF');
    $('#' + QID + 'A').css('color', '#292b2c');
    $('#' + QID + 'B').css('color', '#292b2c');
    $('#' + QID + 'C').css('color', '#292b2c');
    $('#' + QID + 'D').css('color', '#292b2c');
    $('#' + g).css('background-color', '#0275d8');
    $('#' + g).css('color', '#FFFFFF');
    $('#' + QID).val(option);
    console.log($('#' + QID).val());
}

$(document).ready(function () {
    $("a#dashboard").css("color", " #FFF700");

    $('#logout').click(function () {
        return confirm('Your test wil be saved');
    });

});

$(window).bind('beforeunload', function () {

    return 'Your test will be saved';

});

window.onbeforeunload = function (evt) {
    var message = 'Your test will be saved';
    if (typeof evt == 'undefined') {
        evt = window.event;
    }
    if (evt) {
        evt.returnValue = message;
    }

    return message;
}