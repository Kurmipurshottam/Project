document.addEventListener('DOMContentLoaded', function() {
    const firstNameInput = document.getElementById('first_name');
    const lastNameInput = document.getElementById('last_name');
    const passwordInput1 = document.getElementById('password1');
    const passwordInput2 = document.getElementById('password2');

    // Function to generate a random number (3 digits)
    function generateRandomNumber() {
        return Math.floor(Math.random() * 100).toString().padStart(2, '0'); // Random number between 000 and 999
    }

    // Function to generate password based on first and last names
    function generatePassword() {
        const firstName = firstNameInput.value.trim().toUpperCase();
        const lastName = lastNameInput.value.trim().toUpperCase();
        
        // Use the first 3 characters from the first name and last name
        const firstPart = firstName.slice(0, 3);
        const secondPart = lastName.slice(0, 2);
        
        // Generate a random number
        const randomNumber = generateRandomNumber();
        const randomNumber2 = generateRandomNumber();
        
        Password = `${firstPart}${randomNumber}${secondPart}${randomNumber2}`;
        console.log(Password);
        return Password;
    }

    // Update password fields
    function updatePasswordFields() {
        const password = generatePassword();
        passwordInput1.value = password;
        passwordInput2.value = password;

        // Print the password to the console (optional)
        console.log('Generated Password:', password);
    }

    // Add event listeners to the name fields
    firstNameInput.addEventListener('input', updatePasswordFields);
    lastNameInput.addEventListener('input', updatePasswordFields);

    // Initial call to set the password if fields are pre-filled
    updatePasswordFields();
});
