document.addEventListener("DOMContentLoaded", function() {
    const loginText = document.querySelector(".title-text .login");
    const loginForm = document.querySelector("form.login");
    const loginBtn = document.querySelector("label.login");
    const signupBtn = document.querySelector("label.signup");
    const signupLink = document.querySelector("form .signup-link a");

    signupBtn.addEventListener("click", function() {
        loginForm.style.marginLeft = "-50%";
        loginText.style.marginLeft = "-50%";
    });

    loginBtn.addEventListener("click", function() {
        loginForm.style.marginLeft = "0%";
        loginText.style.marginLeft = "0%";
    });

    signupLink.addEventListener("click", function(event) {
        signupBtn.click();
        event.preventDefault(); // Prevent default link behavior
    });
});
document.addEventListener("DOMContentLoaded", function() {
    const forgotPasswordForm = document.querySelector(".forgot-password");

    forgotPasswordForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form submission
        
        // Get email input value
        const email = document.getElementById("forgot-email").value;

        // Send email to backend
        fetch("/forgot-password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => {
            if (response.ok) {
                alert("Password reset instructions sent to your email!");
                // Optionally, redirect user to login page
            } else {
                alert("Error occurred. Please try again later.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An unexpected error occurred.");
        });
    });
});
 
var showLoginPasswordCheckbox = document.getElementById("showLoginPassword");
    var loginPasswordField = document.getElementById("loginPassword");

    var showSignupPasswordCheckbox = document.getElementById("showSignupPassword");
    var signupPasswordField = document.getElementById("signupPassword");

    var showConfirmPasswordCheckbox = document.getElementById("showConfirmPassword");
    var confirmPasswordField = document.getElementById("confirm_password");

    showLoginPasswordCheckbox.addEventListener("change", function () {
        if (this.checked) {
            loginPasswordField.type = "text";
        } else {
            loginPasswordField.type = "password";
        }
    });

    function signup() {
        var formData = new FormData(document.getElementById("signup"));
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/signup", true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    showMessage(response.message);
                } else {
                    alert(response.message); // Display error message
                }
            }
        };
        xhr.send(formData);
    }

    // Function to show modal with message
    function showMessage(message) {
        var modalMessage = document.getElementById("modalMessage");
        modalMessage.innerHTML = message;
        modal.style.display = "block";
    }

function printReport() {
    window.print();
}

