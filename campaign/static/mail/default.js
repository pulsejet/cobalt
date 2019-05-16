var toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

    [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme

    ['clean']
];

var options = {
    modules: {
        toolbar: toolbarOptions
    },
    placeholder: 'Write mail content here ...',
    readOnly: false,
    theme: 'snow'
};
var editor = new Quill('.editor', options);
var csventry = {};
var emailVariable = '';

function textChange() {
    var html = editor.root.innerHTML;
    for (var key in csventry) {
        if (csventry.hasOwnProperty(key)) {
            var re = new RegExp(`{{${key}}}`, 'g');
            html = html.replace(re, csventry[key]);
        }
    }
    styles = `<style> li, p { white-space: pre-wrap; margin: 0; padding: 0; }
    ol, ul { margin-top: 0; margin-bottom:0 } </style>`;

    $('#tpreview').html(styles + html);
    $('#template').val(styles + editor.root.innerHTML);
}

editor.on('text-change', function(delta, oldDelta, source) {
    textChange();
});

function addvar(variable, event) {
    event.preventDefault();
    if (!editor.getSelection()) editor.setSelection(0);
    editor.insertText(editor.getSelection().index, `{{${variable}}}`);
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function emvar(key, event) {
    event.preventDefault();
    emailVariable = key;
    $('.emvarbtn').each(function() {
        $(this).removeClass('btn-primary');
    })
    $(event.target).addClass('btn-primary');
    $('#emailvar').val(key);
}

function openFile(input) {
    var reader = new FileReader();
    reader.onload = function(){
        /* Read one entry */
        csventry = ($.csv.toObjects(reader.result))[0];

        /* Keep adding buttons here */
        let html = '';
        let emailHtml = '';
        let foundEmail = false;

        /* Iterate all keys */
        for (var key in csventry) {
            html += `<button class='btn varbtn' onclick="addvar('${key}', event)">${key}</button>\n`
            if (validateEmail(csventry[key])) {
                emailHtml += `<button class='btn varbtn emvarbtn' onclick="emvar('${key}', event)">${key}</button>\n`
                foundEmail = true;
            }
        }

        /* Set html of variable buttons */
        $('#variables').html(html);
        $('#email-variables').html(emailHtml);

        /* Trigger change in email field */
        if (foundEmail) {
            $('.emvarbtn:first').trigger('click');
        } else {
            alert('No valid emails found in first record! This will not work!');
        }
        console.log(csventry);
        textChange();
    };
    reader.readAsText(input.files[0]);
    $('#csvname').text(input.files[0].name);
};

function openCampAuth(id, name) {
    $('#authform').attr('action', `send/${id}}`);
    $('#auth-camp-name').text(name);
}

$(document).keypress(function(e) {
    if ($("#authModal").hasClass('show') && (e.keycode == 13 || e.which == 13)) {
        $('#authform').trigger('submit')
    }
});
