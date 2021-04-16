document.addEventListener("DOMContentLoaded", function () {

        
    // hide / unhide div based on the user interactions : ...
    document.querySelector('#div_create_field').style.display='none';
    document.getElementById("form_create_field").reset();

    // ...: when he clicks on add a field
    document.querySelector('#button_add_field').onclick = function () {
        document.querySelector('#div_create_field').style.display='block';
        document.querySelector('#address').style.display='none';
        document.querySelector('#address_question').style.display='block';
        document.querySelector('#field_list').style.display='none';
        document.getElementById("form_create_field").reset();
    }

    // ...: when he cancel the creation of a field
    document.querySelector('#button_cancel_field').onclick = function () {
        document.querySelector('#div_create_field').style.display='none';
        document.querySelector('#field_list').style.display='block';
        document.querySelector('#address').style.display='none';
        document.querySelector('#address_question').style.display='none';
        document.getElementById("form_create_field").reset();
    }

    // ...: when he the field he wants to create does not have the same address as the club's address
    document.querySelector('#same_address').onclick = function () {
        document.querySelector('#address').style.display='block';
        document.querySelector('#address_question').style.display='none';

    }


});

