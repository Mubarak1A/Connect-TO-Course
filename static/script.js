function openNav() {
        document.getElementById("bookmark_container").style.width = "200px";
	document.getElementById("main").style.marginLeft = "200px";
}

function closeNav() {
	document.getElementById("bookmark_container").style.width = "0px";
	document.getElementById("main").style.marginLeft = "0px";
}


// Show flash message modal
document.addEventListener('DOMContentLoaded', function() {
  var modal = document.querySelector('.flash-modal');
  modal.style.display = 'block';

// Hide flash message modal after a certain duration (e.g., 3 seconds)
  setTimeout(function() {
    modal.style.display = 'none';
  }, 3000); // Adjust the duration as needed
});



$(document).ready(function() {
  // Function to show flash message modal
  function showFlashModal() {
    $('.flash-modal').fadeIn();
    setTimeout(function() {
      $('.flash-modal').fadeOut();
    }, 3000); // Adjust the duration as needed
  }

  // Event listener for login button click
  $('.logbtn').on('click', function() {
    // Call the showFlashModal function
    showFlashModal();
  });

  // Event listener for signup button click
  $('.signupbtn').on('click', function() {
    // Call the showFlashModal function
    showFlashModal();
  });

  // Event listener for logout button click
  $('.savebtn').on('click', function() {
  // Call the showFlashModal function
  showFlashModal();
  });

  // Event listener for delete click
  $('.delete').on('click', function() {
  // Call the showFlashModal function
  $('.flash-modal').fadeIn();
    setTimeout(function() {
  $('.flash-modal').fadeOut();
  }, 3000);
  });

});

