// Main Template transition

window.addEventListener('DOMContentLoaded', function() {
  document.querySelector('.page-transition').classList.add('active');
});

// Add this code to trigger fade-out when clicking on links
document.addEventListener('click', function(event) {
  var link = event.target.closest('a'); // Get the closest link element
  if (link) {
    event.preventDefault(); // Prevent default link behavior
    var targetUrl = link.href; // Get the target URL

    // Check if the target URL is the same as the current page URL
    if (targetUrl !== window.location.href) {
      var pageTransition = document.querySelector('.page-transition');
      pageTransition.classList.remove('active'); // Remove 'active' class to trigger fade-out
      setTimeout(function() {
        window.location.href = targetUrl; // Navigate to the target URL after fade-out
      }, 250); // Fade out for 0.25 seconds (250 milliseconds)
    } else {
      // If the target URL is the same as the current page URL, directly navigate to the target URL
      window.location.href = targetUrl;
    }
  }
});


// Messages

// Wait 0.5 seconds before showing the message
setTimeout(() => {
  document.querySelector('#message').classList.add('show');
}, 500);

// Close message when close button is clicked
document.querySelector('#message button').addEventListener('click', function() {
  document.querySelector('#message').remove();
});

// Hide message after 3 seconds
setTimeout(function() {
  document.querySelector('#message').remove();
}, 3000);


// for allauth notifications

// Wait 0.5 seconds before showing the message
setTimeout(() => {
document.querySelectorAll('.notification').forEach(msg => {
  msg.classList.add('show');
});
}, 500);

// Close message when close button is clicked
document.querySelectorAll('.notification button').forEach(btn => {
btn.addEventListener('click', function() {
  this.closest('.notification').remove();
});
});

// Hide message after 3 seconds
setTimeout(function() {
document.querySelectorAll('.notification').forEach(msg => {
  msg.remove();
});
}, 3000);