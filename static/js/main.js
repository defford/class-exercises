// main.js

document.addEventListener('DOMContentLoaded', function() {
    // Example: Handling form submissions for solution submission
    const solutionForm = document.getElementById('solutionForm');
    if (solutionForm) {
        solutionForm.addEventListener('submit', function(e) {
            e.preventDefault();  // Prevent default form submission
            const formData = new FormData(solutionForm);
            
            fetch('/submit_solution', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Solution submitted successfully!');
                    // Clear the form or redirect the user
                    solutionForm.reset();
                } else {
                    alert('Failed to submit solution. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error submitting solution:', error);
                alert('Error submitting solution. Please check your network connection.');
            });
        });
    }
});
