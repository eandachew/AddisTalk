// Add Bootstrap classes to form fields
document.addEventListener('DOMContentLoaded', function() {
    // Get all form inputs
    const inputs = document.querySelectorAll('#contactForm input, #contactForm textarea, #contactForm select');
    
    inputs.forEach(input => {
        // Add Bootstrap form-control class
        if (input.type !== 'checkbox' && input.type !== 'radio') {
            input.classList.add('form-control');
        }
        
        // Add Bootstrap form-control-lg for larger inputs
        if (input.id === 'id_name' || input.id === 'id_email' || input.id === 'id_subject') {
            input.classList.add('form-control-lg');
        }
        
        // Set placeholders if not already set
        if (!input.placeholder) {
            switch(input.id) {
                case 'id_name':
                    input.placeholder = 'Enter your name';
                    break;
                case 'id_email':
                    input.placeholder = 'Enter your email';
                    break;
                case 'id_subject':
                    input.placeholder = 'Subject (optional)';
                    break;
            }
        }
    });
    
    // Style textarea specifically
    const textarea = document.getElementById('id_message');
    if (textarea) {
        textarea.classList.add('form-control');
        textarea.rows = 6;
        if (!textarea.placeholder) {
            textarea.placeholder = 'Write your message here...';
        }
    }
});
</script>