function validate_form(thisform) {
    if (thisform.username.value == null || thisform.username.value == '') {
        stack_bar_top = {
            "dir1": "down",
            "dir2": "right",
            "push": "top",
            "spacing1": 150,
            "spacing2": 150
        };
        $(function() {
            new PNotify({
                title: 'Required Question',
                text: 'You have to input your name to process',
                delay: 5000,
                opacity: 0.9,
                addclass: "stack_bar_top", // This is one of the included default classes.
                stack: stack_bar_top,
            })
        })
        return false;
    }
    return true;
}

function windowClose(){
    var opened = window.open('about:blank', '_self');
    opened.opener = null;
    opened.close();
}