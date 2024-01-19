const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

function validateForm() {
    var name = document.getElementById("name").value;
    var phone = document.getElementById("phone").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    // Basic validation
    if (name === '' || phone === '' || email === '' || password === '') {
        document.getElementById('getit').innerHTML="Please Enter all Values";
        return false;
    }

    // Validate phone number format
    if (!/^\d{10}$/.test(phone)) {
		document.getElementById('getit').innerHTML="Please enter a valid 10-digit phone number";
        return false;
    }

    // Validate email format
    if (!/\S+@\S+\.\S+/.test(email)) {
		document.getElementById('getit').innerHTML="Please enter a valid email address";
        return false;
    }

    // You can add more complex password validation logic here if needed

    return true; // Submit the form if all validations pass
}