/** Setup form submit buttons */
$('*[data-form-submit]').on('click', function() {
    $($(this).attr('data-form-submit')).trigger('submit');
});
