"use strict";

// TASK ARCHIVE SCRIPT
function strikeArchiveTask(results) {
    alert(results);
    $('#submitTaskArchive').hide();
    $('#archiveTask').css({'text-decoration': 'line-through'});
    $('#archiveDueDate').css({'text-decoration': 'line-through'});
}

function sendArchiveTask(e) {
    console.log(e);
    e.preventDefault();

    const formInputs = {
        'todo_id': $('#todo-id-field').val(),
    };

    $.post('/dashboard/archive-task',
        formInputs,
        strikeArchiveTask);
}  

// EDIT CONTACT AJAX SCRIPT
function showContactInfo(results) {
    $('#email').toggle();
    $('#phone-num').toggle();
    $('#company').toggle();
    $('#notes').toggle();
    $('#edit-fields').toggle();
    $('#contactEvents').toggle();
    $('#toggleEditButton').toggle();
    $('#contactEmail').html(results.email);
    $('#contactPhone').html(results.phone);
    $('#contactCompany').html(results.company);
    $('#contactNotes').html(results.notes);
}

function getContactEdits(e) {
    console.log(e);
    e.preventDefault();

    const formInputs = {
        'contact_id': $('#contact-id-field').val(),
        'email': $('#email-field').val(),
        'phone': $('#phone-field').val(),
        'company_id': $('#company-id-field').val(),
        'company_name': $('#company-name-field').val(),
        'notes': $('#contact-notes-field').val(),
    };

    $.post('/dashboard/contacts/edit',
        formInputs,
        showContactInfo);
}

// COMPANY EDITS ON/OFF SCRIPT
function toggleEditFields(e) {
    console.log(e);
    e.preventDefault();
    $('#email').toggle();
    $('#phone-num').toggle();
    $('#company').toggle();
    $('#notes').toggle();
    $('#edit-fields').toggle();
    $('#contactEvents').toggle();
    $('#toggleEditButton').toggle();
}
