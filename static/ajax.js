//To retrieve course search results from the server
$(document).ready(function() {
  // Function to handle the search form submission
  $('.search-container').submit(function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the search query from the input field
    var query = $('#search-input').val();

    // Make an Ajax request to the server
    $.ajax({
      url: '/search', // The server-side endpoint to handle the search
      method: 'GET',
      data: { query: query }, // Pass the query as a parameter
      success: function(response) {
        // Handle the successful response
        var searchResults = response.results;

        // Clear previous search results
	$('#result-head').empty();
	$('#search-results').empty();
	
	//Results title
	$('#result-head').append('<br><div class="result"><h3>Search Results</h3></div><br>');

        if (searchResults.length > 0) {
          for (var i = 0; i < searchResults.length; i++) {
            //make user_id available as ajax can not render template
	    var userId = document.getElementById('user-id').value;
	    var result = searchResults[i];
            var resultHtml =
              '<div class="flex-item3">' + '<a href='  + result.url + ' target="_blank">' + '<img src="static/images/img2.png" style="width: 100%;"></a>' +
              '<b>' + result.title + '</b>' +
              '<i style="font-size: 0.7em;">By: ' + result.instructor + '</i>' +
	      '<br>' +
	      ' ' + '<button class="savebtn" data-id="' + result.id  + '" data-user_id="' + userId + '"><i class="fas fa-save"></i> Save</button>'  + 
              '</div>';

            $('#search-results').append(resultHtml);
          }
        } else {
          $('#search-results').append('<p>No results found.</p>');
        }
      },
      error: function(xhr) {
        // Handle the error
        alert('Error: ' + xhr.statusText);
      }
    });
  });



//For save/bookmark

// Check the current page and apply different behaviors
if (window.location.pathname === "/") {
  // Behavior for index.html page random courses
  $(".savebtn").on("click", function() {
    // Trigger the click event of signup button
    $("#f2").show();
  });
  // For searched courses
 $('#search-results').on('click', '.savebtn', function() {
  $("#f2").show();
});
} else if (window.location.pathname === "/user") {
  // Behavior for User_page.html
  $(".savebtn").on("click", function() {
    // Send a request, url and username as data, to the server
    var id = $(this).attr("data-id");
    var user_id = $(this).attr("data-user_id");
    $.ajax({
      url: "/save",
      method: "POST",
      data: JSON.stringify({id: id, user_id: user_id}),
      success: function(response) {
        // Handle the response from the Flask server
        console.log("Request sent to Flask server");
      },
      error: function(xhr, status, error) {
        // Handle the error
        console.error("Error sending request to Flask server");
      }
    });
  });
  //For searched courses
  $('#search-results').on('click', '.savebtn', function() {
    //send request to server
    var id = $(this).attr("data-id");
    var user_id = $(this).attr("data-user_id");
    $.ajax({
      url: "/save",
      method: "POST",
      data: JSON.stringify({id: id, user_id: user_id}),
      success: function(response) {
      // Handle the response from the Flask server
      console.log("Request sent to Flask server");
      },
      error: function(xhr, status, error) {
	// Handle the error
	console.error("Error sending request to Flask server");
	}
	});
      });

  // Delete bookmark
$('.delete').on('click', function() {
    var courseId = $(this).data('id');
    var userId = $(this).data('user_id');
    
    $.ajax({
        type: 'POST',
        url: '/delete',
        contentType: 'application/json',
        data: JSON.stringify({ id: courseId, user_id: userId }),
        success: function(response) {
            // Update the UI with the updated list of bookmarked courses
            $('#bookmark_container').empty();
            response.saved_courses.forEach(function(course) {
                $('#bookmark_container').append(
                    '<div class="bookmark">' +
                        '<a href="' + course.url + '" target="_blank"><img src="static/images/img2.png" style="width: 100%;"></a>' +
                        '<b style="color: white; font-size: 0.6em;">' + course.title + '</b>' +
                        '<i style="font-size: 0.4em; color: white"> By: ' + course.instructor + '</i>' +
                        '<span class="delete" data-id="' + course.id + '" data-user_id="' + userId + '"> <i class="far fa-trash-alt"></i></span>' +
                    '</div>'
                );
            });
        },
        error: function(error) {
            console.log('Error deleting bookmark:', error);
        }
    });
});
	    
});

/*
 $(".delete").on("click", function() {
  var id = $(this).attr("data-id");
  var user_id = $(this).attr("data-user_id");
  $.ajax({
	  url: "/delete",
	  method: "POST",
	  data: JSON.stringify({id: id, user_id: user_id}),
	  contentType: "application/json",
	  success: function(response) {
	  Handle the response from the Flask server
		  console.log("Request sent to Flask server");
	  },
	  error: function(xhr, status, error) {
		  //Handle the error
		  console.error("Error sending request to Flask server");
	  }
  });
 });
 */
