"use strict";


// function callback
function replaceGreeting(results) {
    const randomGreeting = results;
    $('#greeting').html(randomGreeting);
}

// function to do stuff
function getGreeting() {
    $.get('/greeting', replaceGreeting);
}

// call function to do stuff
getGreeting();