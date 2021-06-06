// preventing resubmission of form
// $(document).ready(function(){
//     window.history.replaceState('','',window.location.href)
// });
// if ( window.history.replaceState ) { 
//     window.history.replaceState( null, null, window.location.href ); 
// } 


// enabling the create account section and disabling the login section
function create_account(){
    document.getElementById('loginbox').style.display = 'none';
    document.getElementById('createaccount-box').style.display = 'block';
    document.title = ' Create Account ';
}

// enabling the forget password section
function forget_password(){
    document.getElementById('loginbox').style.display = 'none';
    document.getElementById('forget-password-box').style.display = 'block';
    document.title = ' Reset Password ';
}

// for sending a mail to reset the password
function reset_password(){
    // sending reset password link to the email id
    preventDefault();
    console.log('reset password');
}



// eventlistener on the checkbox for enabling and disbling the submit button
checkbox = document.getElementById('agree');

checkbox.addEventListener('change', e => {
    
    if(!e.target.checked){
        console.log('Hello');
        document.getElementById('submit-account-create-btn').style.display = 'none';
    }
    else{
        document.getElementById('submit-account-create-btn').style.display = 'inline-block';
    }
    
});
   

// limiting the bytes of file upload
function file_verify(){
    // size check
    let im_file = document.getElementById('photo');
    content = im_file.value;
    // console.log(content);
    // console.log(im_file.files[0].size);
    if(im_file.files[0].size > 204800){
        im_file.value = '';
        console.log(im_file.value);
        alert(' File size should be less than 200KB ');
        // console.log('error');
    }
    else{
        // im_file.value = content;
        // console.log('Hurray');
        // format check
        let type = document.getElementById('photo').value;
        console.log(type);
        let jpg = type.match('.jpg');
        let png = type.match('.png');
        if(!jpg && !png){
            im_file.value = '';
            alert(' Invalid file type ');
        }
        console.log(im_file.files);
    }

}

// confirm password verification
function password_verify(){
    let pswd = document.getElementById('password-create').value;
    let c_pswd = document.getElementById('password-create-confirm').value;
    if(!c_pswd.match(pswd)){
        c_pswd.value = '';
        alert(' Please enter correct password ');
        // console.log(pswd);
        // console.log(c_pswd);
    }
}

// date of birth verification
function validate_date(){
    let curr_date = new Date();
    let dob = document.getElementById('dob').value;
    let dob_date = new Date(dob);
    if(curr_date < dob_date){
        dob = '';
        alert(' Please select a valid date of birth ');
        console.log(dob);
    }
}

function password_verification(){
    let lowercase_letters = /[a-z]/g;
    let uppercase_letters = /[A-Z]/g;
    let num = /[0-9]/g;
    let pswd = document.getElementById('password-create').value;
    if(!pswd.match(lowercase_letters) || !pswd.match(uppercase_letters) || !pswd.match(num) || pswd.length < 8){
        alert('Password must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters ');
    }

}
