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

// SALARY PICKER AJAX SCRIPT
function showSalary(results) {
    $('#averageSalary').html(results);
    $('#averageSalaryEditField').html(results);
    $('#metroDiv').hide();
    $('#jobTitleDiv').hide();
    $('#salaryButton').hide();
}

function getSalary(e) {
    console.log(e);
    e.preventDefault();

    const formInputs = {
        'metro': $('#metro-field').val(),
        'job_title': $('#job-title-field').val(),
        'job_id': $('#job-id-field').val(),
    };

    $.post('/dashboard/jobs/salary',
        formInputs,
        showSalary);
}

// JOB INFO EDITING SCRIPT
function showJobInfo(results) {
    $('#job-posting').show();
    $('#avg-salary').show();
    $('#notes').show();
    $('#edit-fields').hide();
    $('#jobEventsTasks').show();
    $('#toggleEditButton').show();
    $('#jobPosting').html(results['link']);
    $('#jobPostingHref').attr("href", results['link']);
    $('#averageSalary').html(results.avg_salary);
    $('#jobNotes').html(results.notes);
}

function getJobEdits(e) {
    console.log(e);
    e.preventDefault();

    const formInputs = {
        'link': $('#job-link-field').val(),
        'avg_salary': $('#avg-salary-field').val(),
        'notes': $('#job-notes-field').val(),
        'job_id': $('#job-id-field').val(),
    };

    $.post('/dashboard/jobs/edit',
           formInputs,
           showJobInfo);
}

// JOB EDITS ON/OFF SCRIPT
function toggleEditFields(e) {
    console.log(e);
    e.preventDefault();
    $('#job-posting').toggle();
    $('#avg-salary').toggle();
    $('#notes').toggle();
    $('#edit-fields').toggle();
    $('#jobEventsTasks').toggle();
    $('#toggleEditButton').toggle();
}














































