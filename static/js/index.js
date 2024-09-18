document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submitButton');
    const fileInput = document.getElementById('fileInput');
    const resultsSection = document.getElementById('results');
    const resultHeading = document.getElementById('result-heading');
    const resultMessage = document.getElementById('result-message');

    fileInput.addEventListener('change', function() {
        submitButton.disabled = !fileInput.files.length;
    });

    submitButton.addEventListener('click', function() {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        fetch('/test', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Response Status:', response.status); // Log the response status
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response Data:', data); // Log the response data
            if (data.result) {
                const resultClass = data.result; // Extract the result from the response

                if (resultClass === 'Healthy') {
                    resultHeading.innerHTML = '<span class="bold">Negative!</span>'; // Apply bold class to "Negative!"
                    resultHeading.style.color = 'green'; // Set text color to green for negative result
                    resultMessage.innerHTML = 'You have been tested <span class="bold">Negative</span>. You are Healthy.'; // Apply bold class to "Negative"
                } else {
                    resultHeading.innerHTML = '<span class="bold">Positive!</span>'; // Apply bold class to "Positive!"
                    resultHeading.style.color = 'red'; // Set text color to red for positive result
                    resultMessage.innerHTML = `You have been tested <span class="bold">Positive</span> for ${resultClass}. Please consult a doctor.`; // Apply bold class to "Positive"
                }

                // Display the results section
                resultsSection.style.display = 'block';
            } else {
                throw new Error('Unexpected response format');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing your request.');
        });
    });
});
