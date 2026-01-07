// Like button functionality for blog posts

document.addEventListener('DOMContentLoaded', function() {
    const likeButton = document.getElementById('like-button');
    
    if (likeButton) {
        likeButton.addEventListener('click', function() {
            const slug = this.dataset.postSlug;
            
            // Save original button state
            const originalContent = this.innerHTML;
            const originalClasses = this.className;
            
            // Add loading state
            this.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                </span>
            `;
            this.disabled = true;
            
            // Send AJAX request
            fetch(`/post/${slug}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Update button based on response
                if (data.liked) {
                    // User just liked the post
                    this.className = 'btn btn-like btn-danger';
                    this.innerHTML = `<i class="bi bi-heart-fill"></i> <span id="like-count">${data.like_count}</span>`;
                    this.dataset.liked = 'true';
                } else {
                    // User just unliked the post
                    this.className = 'btn btn-like btn-outline-danger';
                    this.innerHTML = `<i class="bi bi-heart"></i> <span id="like-count">${data.like_count}</span>`;
                    this.dataset.liked = 'false';
                }
                
                // Re-enable the button
                this.disabled = false;
                
                // Update the like text
                const likeText = document.getElementById('like-text');
                if (data.like_count === 0) {
                    likeText.textContent = 'Be the first to like this!';
                } else if (data.like_count === 1) {
                    likeText.textContent = '1 person likes this';
                } else {
                    likeText.textContent = `${data.like_count} people like this`;
                }
                
                // Show success toast
                showToast(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
                
                // Restore original button state on error
                this.className = originalClasses;
                this.innerHTML = originalContent;
                this.disabled = false;
                
                // Show error message
                showErrorToast('An error occurred. Please try again.');
            });
        });
    }
    
    // Function to show success toast
    function showToast(message) {
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        // Create toast element
        const toastId = 'toast-' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header">
                    <i class="bi bi-heart-fill text-danger me-2"></i>
                    <strong class="me-auto">Like Updated</strong>
                    <small class="text-muted">just now</small>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        
        // Initialize and show the toast
        const toastEl = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 3000
        });
        toast.show();
        
        // Remove toast from DOM after it's hidden
        toastEl.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    }
    
    // Function to show error toast
    function showErrorToast(message) {
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        // Create toast element
        const toastId = 'error-toast-' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header bg-danger text-white">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    <strong class="me-auto">Error</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        
        // Initialize and show the toast
        const toastEl = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000
        });
        toast.show();
        
        // Remove toast from DOM after it's hidden
        toastEl.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    }
});

// Function to get CSRF token (to be used globally)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}