/**
 * Get the preview of an email with AJAX and open the modal
 * @param {string} id Id of Mail object to open modal for
 */
function showPreview(id) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
        $('#previewModal .modal-body').html(this.responseText);
        $('#previewModal').modal('show');
    }
    xhr.open("GET", `preview/${id}`);
    xhr.responseType = "text";
    xhr.send();
}

/** Set up click listeners */
$('.cobalt-preview-mail').on('click', function() {
    showPreview($(this).attr('data-cobalt-id'));
});
