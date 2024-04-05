function openNav() {
    document.getElementById("bookmark_container").style.width = "200px";
    document.getElementById("main").style.marginLeft = "200px";
}

function closeNav() {
    document.getElementById("bookmark_container").style.width = "0px";
    document.getElementById("main").style.marginLeft = "0px";
}

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

document.addEventListener('DOMContentLoaded', function() {
    var modal = document.querySelector('.flash-modal');
    // Event listener for login button click
    $('#login').on('click', function() {
        showFlashModal('Login successful!');
    });
});

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

                // Results title
                $('#result-head').append('<br><div class="result"><h3>Search Results</h3></div><br>');

                if (searchResults.length > 0) {
                    for (var i = 0; i < searchResults.length; i++) {
                        // Make user_id available as ajax can not render template
                        var userId = document.getElementById('user-id').value;
                        var result = searchResults[i];
                        var resultHtml =
                            '<div class="flex-item3">' + '<a href=' + result.url + ' target="_blank">' + '<img src="static/images/img2.png" style="width: 100%;"></a>' +
                            '<b>' + result.title + '</b>' +
                            '<i style="font-size: 0.7em;">By: ' + result.instructor + '</i>' +
                            '<br>' +
                            ' ' + '<button class="savebtn" data-id="' + result.id + '" data-user_id="' + userId + '"><i class="fas fa-save"></i> Save</button>' +
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
