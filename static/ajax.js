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
      dataType: 'json', // Expect JSON response
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
            var result = searchResults[i];
            var resultHtml =
              '<div class="flex-item3">' + '<img src="static/images/img2.png" style="width: 100%;">' +
              '<b>' + result.title + '</b>' +
              '<p>' + result.instructor + '</p>' +
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
});

