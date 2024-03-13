function display_songs(data) {
    $(".record-area").empty();

    $.each(data, function(i, item) {
        console.log("Item index: " + i + ", Image: " + item.image); // Log the image address for each item
       
        var artists = item.artist.join(', ');
        var $song = $(
            "<div class='col-3 btn song-item' data-id='" + item.id + "'>" +
                "<img class='song-img' src='" + item.image + "' alt='Song Image'><br>" +
                item.title + "<br>" +
                artists +
            "</div>"
        );

        // Append the song to the record area
        $(".record-area").append($song);
    });

    // Set up click event for each song item after they have been added to the DOM
    $(".record-area").on('click', '.song-item', function() {
        var itemId = $(this).data('id'); // Use data attribute to fetch the unique ID
        window.location.href = `view/${itemId}`;
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
function add_song(event) {
    console.log('add_song function called'); // Confirm function call
    event.preventDefault();
    
    var errorMessages = [];

    var song = $(".song-input").val();
    var artist = $(".artist-input").val().split(', ');
    var description = $(".description-input").val();
    var genres = $(".genres-input").val().split(', ');
    var year = $(".year-input").val();
    var image = $(".img-input").val();

    if(!song | !artist| !description| !genres| !description| !image| !year){
        errorMessages.push("Can't submit anything, when there's nothing there mi queridisime amige!");
        $(".song-input").addClass('error-focus').focus();
    }
    else if (!song) {
        errorMessages.push("Please ente the song's name.");
        $(".song-input").addClass('error-focus').focus();
    }
    else if (!artist) {
        errorMessages.push("Please enter the name of the artist");
        $(".artist-input").addClass('error-focus').focus();
    }
    else if (!description) {
        errorMessages.push("Please enter the description");
        $(".description-input").addClass('error-focus').focus();
    }
    else if(!genres){
        errorMessages.push("Please enter the genres.");
        $(".genres-input").addClass('error-focus').focus();
    }
    else if(!description){
        errorMessages.push("Please enter a description.");
        $(".description-input").addClass('error-focus').focus();
    }
    else if (isNaN(year) || parseInt(year) <= 0) {
        errorMessages.push("Please enter the year of the song immediately.");
        $(".year-input").addClass('error-focus').focus();
    }
    else if(!image){
        errorMessages.push("Please enter a description.");
        $(".im-input").addClass('error-focus').focus();
    }
    
    


    $("#error-messages").empty();
    if (errorMessages.length > 0) {
        $.each(errorMessages, function(i, message) {
            $("#error-messages").append("<li>" + message + "</li>");
        });
        return;  // Stop execution if there are errors
    }

    var new_song = {
        title: song,
        artist: artist,
        summary: description,
        genres: genres,
        year: parseInt(year, 10),
        image: image
    };

    console.log('Sending data:', new_song); // Log the data being sent

    $.ajax({
        url: '/add',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(new_song),
        success: function(response) {
            alert('New item successfully created!');
            console.log('Success response:', response); // Log success response

            var newItemLink = '/view/' + response.id;
    
        $('#link-container').html('<a href="' + newItemLink + '">Click here to see the item you just added</a>');
        },
        error: function(xhr, status, error) {
            console.error('Error adding song:', error);
            alert('Error adding song. Check console for details.');
        }
    });
}
function populateEditForm() {
    var pathArray = window.location.pathname.split('/');
    var songId = pathArray[pathArray.length - 1];

    $.ajax({
        url: '/api/song/' + songId,
        type: 'GET',
        success: function(data) {
            populateForm(data);
        },
        error: function(xhr, status, error) {
            console.error("Error fetching song data:", error);
        }
    });
}
function populateForm(data) {
    $(".song-input").val(data.title);
    $(".artist-input").val(data.artist.join(', '));
    $(".description-input").val(data.summary);
    $(".genres-input").val(data.genres.join(', '));
    $(".year-input").val(data.year);
    $(".img-input").val(data.image);
}
function initializeEventListeners() {
    $('#submit-btn').click(function(event) {
        add_song(event);
    });
    $('#submit-btn2').click(function(event) {
        event.preventDefault();
        updateSong();
    });

    $('#searchInput').on('keypress', function(e) {
        if (e.which == 13) {
            searchSongs();
        }
    });
    $('#discardChangesButton').click(function(event) {
        event.preventDefault(); // Prevent default form submission
        discardChanges();
    });
    
}
function updateSong() {
    var songId = window.location.pathname.split('/').pop();

    var updatedSong = {
        title: $(".song-input").val(),
        artist: $(".artist-input").val().split(', '),
        summary: $(".description-input").val(),
        genres: $(".genres-input").val().split(', '), 
        year: parseInt($(".year-input").val(), 10), 
        image: $(".img-input").val()
    };

    $.ajax({
        url: '/update/' + songId,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(updatedSong),
        success: function(response) {
            console.log('Update response:', response);
            // Redirect the user to the view page of the updated item
            window.location.href = '/view/' + songId;
        },
        error: function(xhr, status, error) {
            console.error('Error updating song:', error);
            alert('Error updating song. Check console for details.');
        }
    });
    
}
function discardChanges() {
    var confirmation = confirm('Are you sure you want to discard changes?');
    if (confirmation) {
        var songId = window.location.pathname.split('/').pop();
        window.location.href = `/view/${songId}`;
    }
}

$(document).ready(function() {
    console.log('Document is ready');

   
    initializeEventListeners();


    if ($("#song-form").length > 0) {
        populateEditForm();
    }
    display_songs(data);
});

