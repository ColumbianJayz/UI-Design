function display_songs(data) {
    $(".record-area").empty();
    $.each(data, function(i, item) {
        console.log("Item index: " + i + ", Image: " + item.image); // Log the image address for each item

        var $recordRow = $("<div class='row song-row'></div>");
        var artists = item.artist.join(', ');
        var $song = $(
            "<div class='col-3 btn'>" +
                "<img class='song-img' src='" + item.image + "' alt='Song Image'><br>" +
                item.title + "<br>" +
                artists +
            "</div>"
        );
        $recordRow.click(function() {
            window.location.href = `view/${item.id}`;
        });
        $recordRow.append($song);
        $(".record-area").append($recordRow);
    });
}

function searchSongs() {
    var searchTerm = $('input[name="query"]').val().trim();
    if (searchTerm) {  // Check if searchTerm is not empty after trimming whitespace
        $.ajax({
            url: '/search',
            type: 'GET',
            data: { 'query': searchTerm },
            success: function(response) {
                display_songs(response.data);
                $('#searchResults').html(`Showing Results for "${searchTerm}"`);
            },
            error: function(error) {
                console.log(error);
            }
        });
    } else {
        // If searchTerm is empty or just whitespace, do nothing
        $('input[name="query"]').val('').focus();  // Clear input and focus
    }
}

// Trigger search when enter is pressed
$('#searchInput').on('keypress', function(e) {
    if (e.which == 13) {
        searchSongs();
    }
});

// Event delegation for search result clicks
$('.search-results').on('click', '.search-result', function() {
    var searchTerm = $('input[name="query"]').val().trim();
    if (!searchTerm) {
        return false;  // Prevent further action if search term is empty after trimming whitespace
    }

    var itemId = $(this).data("id");
    handleSearchResultClick(itemId);
});

$(document).ready(function() {
    // Assuming 'data' is defined elsewhere in your script as it's referenced here
    display_songs(data);
});
