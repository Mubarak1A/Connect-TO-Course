function openNav() {
        document.getElementById("bookmark_container").style.width = "200px";
	document.getElementById("main").style.marginLeft = "200px";
}

function closeNav() {
	document.getElementById("bookmark_container").style.width = "0px";
	document.getElementById("main").style.marginLeft = "0px";
}


document.addEventListener('DOMContentLoaded', function() {
  var modal = document.querySelector('.flash-modal');

  // Function to show flash message modal
  function showFlashModal() {
    modal.style.display = 'block';
    setTimeout(function() {
      modal.style.display = 'none';
    }, 3000); // Adjust the duration as needed
  }
})
  // Event listener for login button click
  $('#login').on('click', function() {
    showFlashModal();
  });

/*  // Event listener for logout button click
  $('#signup').on('click', function() {
    showFlashModal();
  });

  // Event listener for signup button click
  $('#logout').on('click', function() {
    showFlashModal();
  });

  // Event listener for logout button click
  $('.savebtn').on('click', function() {
    showFlashModal();
  });

  // Event listener for delete click
  $('.delete').on('click', function() {
    showFlashModal();
  });
})*/

$(document).ready(function() {
  // Function to show flash message modal
  function showFlashModal(message) {
    var modal = $('.flash-modal');
    var flashMessage = $('.flash-message');
    flashMessage.text(message);
    modal.fadeIn();
    setTimeout(function() {
      modal.fadeOut();
    }, 3000); // Adjust the duration as needed
  }

  // Event listener for signup button click
  $('#login').on('click', function(event) {
    //event.preventDefault();
    showFlashModal('Login successful!');
    // You can also trigger the signup route here if needed
     $('.signupbtn').submit();
  });

  // Event listener for login button click
  $('.savebtn').on('click', function(event) {
    //event.preventDefault();
    showFlashModal('Save successful!');
    // You can also trigger the login route here if needed
    $('.savebtn').submit();
  });

  // Event listener for logout button click
  $('.delete').on('click', function(event) {
    //event.preventDefault();
    showFlashModal('Delete successful!');
    // You can also trigger the logout route here if needed
    $('.delete').submit();
  });
});

