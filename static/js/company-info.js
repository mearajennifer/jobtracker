"use strict";

// COMPANY EDITS ON/OFF SCRIPT
function toggleEditFields(e) {
    console.log(e);
    e.preventDefault();
    $('#address').toggle();
    $('#website').toggle();
    $('#notes').toggle();
    $('#edit-fields').toggle();
    $('#activeJobs').toggle();
    $('#archivedJobs').toggle();
    $('#companyContacts').toggle();
    $('#toggleEditButton').toggle();
}


// COMPANY INFO EDITING SCRIPTS
function showCompanyInfo(results) {
    $('#address').show();
    $('#website').show();
    $('#notes').show();
    $('#edit-fields').hide();
    $('#activeJobs').show();
    $('#archivedJobs').show();
    $('#companyContacts').show();
    $('#companyStreetAddress').html(results.street);
    $('#companyCity').html(results.city);
    $('#companyState').html(results.state);
    $('#companyZip').html(results.zipcode);
    $('#companyWebsite').html(results.website);
    $('#companyNotes').html(results.notes);
}

function getCompanyEdits(e) {
    console.log(e);
    e.preventDefault();

    const formInputs = {
        'company_id': $('#company-id-field').val(),
        'street': $('#street-field').val(),
        'city': $('#city-field').val(),
        'state': $('#state-field').val(),
        'zipcode': $('#zipcode-field').val(),
        'notes': $('#notes-field').val(),
        'website': $('#website-field').val()
    };

    $.post('/dashboard/companies/edit',
        formInputs,
        showCompanyInfo,
    );

  }
