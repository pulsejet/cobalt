/**
 * Open the authentication modal for a campaign
 * @param {string} id Id of campaign
 * @param {string} name Name of the campaign
 */
function openCampAuth(id, name) {
    $('#authform').attr('action', `send/${id}}`);
    $('#auth-camp-name').text(name);
}

/** Trigger auth modal submit on pressing enter */
$(document).keypress(function(e) {
    if ($("#authModal").hasClass('show') && (e.keycode == 13 || e.which == 13)) {
        $('#authform').trigger('submit')
    }
});

/** Store username in localStorage on submitting */
$('#authform').on('submit', function() {
    localStorage.setItem('username', $('#auth-username').val());
})

/** Get username from localStorage before opening */
$('#authModal').on('show.bs.modal', function () {
    if (localStorage.getItem('username') !== null) {
        $('#auth-username').val(localStorage.getItem('username'));
    }
});

/** Set focus to the correct input on open */
$('#authModal').on('shown.bs.modal', function () {
    if ($('#auth-username').val() == '') {
        $('#auth-username').focus();
    } else {
        $('#auth-password').focus();
    }
})
