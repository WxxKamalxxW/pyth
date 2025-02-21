document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.querySelector('.login');

    loginButton.addEventListener('click', async (event) => {
        event.preventDefault();

        // Extract form data
        const email = document.querySelector('#email-input').value;
        const password = document.querySelector('#password-input').value;

        // Send data to the Flask backend
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                console.log('Server response:', data);
                if (data.status === 'success') {
                    // Redirect to the dashboard if login is successful
                    window.location.href = "/dashboard";
                } else {
                    // If login failed, show error message
                    alert(data.message);  // Display the failure message
                }
            } else {
                console.error('Login failed:', data.message);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});
