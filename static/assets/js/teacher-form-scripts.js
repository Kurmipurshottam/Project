document.addEventListener('DOMContentLoaded', function () {
    const firstNameInput = document.getElementById('first_name');
    const lastNameInput = document.getElementById('last_name');
    const loginIdInput = document.getElementById('login_id');

    function updateLoginId() {
        const firstName = firstNameInput.value.trim().toUpperCase();
        const lastName = lastNameInput.value.trim().toUpperCase();

       // Extract first 2 characters from first name and last name
        const firstTwoFirstName = firstName.slice(0, 2);
        const firstTwoLastName = lastName.slice(0, 2);

       // Generate random number between 0 and 999
       const randomNumber = Math.floor(Math.random() * 1000).toString().padStart(3, '0');

       // Construct login ID
        let loginId = `TE${firstTwoFirstName}${firstTwoLastName}${randomNumber}`;

       // Ensure the login ID is exactly 8 characters long
        if (loginId.length > 8) {
            loginId = loginId.slice(0, 8);
        }

        loginIdInput.value = loginId;   
        }

    firstNameInput.addEventListener('input', updateLoginId);
    lastNameInput.addEventListener('input', updateLoginId);

    // Initial call to set the Login ID if fields are pre-filled
    updateLoginId();
    });