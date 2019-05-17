/** Trigger auth modal submit on pressing enter */
$(document).keypress(function(e) {
    if ($("#authModal").hasClass('show') && (e.keycode == 13 || e.which == 13)) {
        $('#auth-form').trigger('submit')
    }
});

/** Store username in localStorage on submitting */
$('#auth-form').on('submit', function() {
    localStorage.setItem('username', $('#auth-username').val());
})

/** Initialize modal before opening */
$('#authModal').on('show.bs.modal', function (event) {
    /* Retrieve arguments */
    const url = $(event.relatedTarget).attr('data-cobalt-url');
    const name = $(event.relatedTarget).attr('data-cobalt-msg');

    /* Set arguments for form */
    $('#auth-form').attr('action', url);
    $('#auth-camp-name').text(name);

    /* Set username fro localStorage */
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
});
