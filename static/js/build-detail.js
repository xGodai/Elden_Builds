document.addEventListener('DOMContentLoaded', function() {
  // Get CSRF token
  function getCSRFToken() {
    // Try meta tag first
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken) {
      return metaToken.getAttribute('content');
    }
    
    // Try form token
    const formToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (formToken) {
      return formToken.value;
    }
    
    // Try cookie (fallback)
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'csrftoken') {
        return value;
      }
    }
    
    return null;
  }

  // Grace button functionality
  const graceBtn = document.querySelector('.grace-btn');
  if (graceBtn) {
    const buildId = graceBtn.getAttribute('data-build-id');
    const likeUrl = graceBtn.getAttribute('data-like-url');
    
    graceBtn.addEventListener('click', function(e) {
      e.preventDefault();
      
      const button = e.target.closest('.grace-btn');
      const isLiked = button.getAttribute('data-liked') === 'true';
      
      console.log('Grace button clicked:', { buildId, isLiked });
      
      // Disable button during request
      button.disabled = true;
      
      // Get CSRF token from the page
      const csrfToken = getCSRFToken();
      console.log('CSRF token:', csrfToken);
      
      if (!csrfToken) {
        console.error('CSRF token not found');
        alert('Security token not found. Please refresh the page.');
        button.disabled = false;
        return;
      }
      
      // Create form data
      const formData = new FormData();
      formData.append('csrfmiddlewaretoken', csrfToken);
      
      console.log('Like URL:', likeUrl);
      
      fetch(likeUrl, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
      })
      .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Response data:', data);
        if (data.success) {
          // Update button appearance and text
          const graceText = button.querySelector('.grace-text');
          if (data.is_liked) {
            button.className = 'btn grace-btn btn-warning';
            button.setAttribute('data-liked', 'true');
            graceText.textContent = '⚡ Remove Grace';
          } else {
            button.className = 'btn grace-btn btn-outline-warning';
            button.setAttribute('data-liked', 'false');
            graceText.textContent = '⚡ Grace Build';
          }
          
          // Update Grace count
          const graceCountElement = document.querySelector('[data-grace-count]');
          if (graceCountElement) {
            graceCountElement.textContent = data.total_likes;
          }
          
          console.log('Grace updated successfully');
        } else {
          console.error('Server returned success=false:', data);
          alert('Failed to update Grace. Server error.');
        }
      })
      .catch(error => {
        console.error('Error toggling grace:', error);
        alert(`Failed to update Grace: ${error.message}. Please try again.`);
      })
      .finally(() => {
        // Re-enable button
        button.disabled = false;
      });
    });
  }

  // Voting functionality
  const voteForms = document.querySelectorAll('.vote-form');
  
  voteForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const commentId = this.dataset.commentId;
      const voteType = this.dataset.voteType;
      const formData = new FormData(this);
      
      fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Update vote counts
          const comment = document.querySelector(`[data-comment-id="${commentId}"]`).closest('.comment');
          const upvoteCount = comment.querySelector('.upvote-count');
          const downvoteCount = comment.querySelector('.downvote-count');
          const scoreValue = comment.querySelector('.score-value');
          const upvoteBtn = comment.querySelector('.upvote-btn');
          const downvoteBtn = comment.querySelector('.downvote-btn');
          
          upvoteCount.textContent = data.upvotes;
          downvoteCount.textContent = data.downvotes;
          scoreValue.textContent = data.score;
          
          // Update button styles based on user vote
          upvoteBtn.className = 'btn btn-sm upvote-btn ' + 
            (data.user_vote === 'upvote' ? 'btn-success' : 'btn-outline-success');
          downvoteBtn.className = 'btn btn-sm downvote-btn ' + 
            (data.user_vote === 'downvote' ? 'btn-danger' : 'btn-outline-danger');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  });

  // Comment sorting functionality
  const sortSelect = document.getElementById('comment-sort-select');
  if (sortSelect) {
    sortSelect.addEventListener('change', function() {
      const currentUrl = new URL(window.location);
      currentUrl.searchParams.set('comment_sort', this.value);
      window.location.href = currentUrl.toString();
    });
  }
});
