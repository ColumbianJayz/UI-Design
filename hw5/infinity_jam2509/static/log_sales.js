function display_sales_list(sales) {
    $(".record-area").empty();
    $.each(sales, function(i, sale) {
        var $recordRow = $("<div class='row sale-record'></div>");

        var $salespersonCol = $("<div class='col-3'><li>" + sale.salesperson + "</li></div>");
        var $clientCol = $("<div class='col-3'><li>" + sale.client + "</li></div>");
        var $reamsCol = $("<div class='col-3'><li>" + sale.reams + "</li></div>");
        var $deleteBtnCol = $("<div class='col-2'></div>");
        var $deleteBtn = $("<button class='delete-button'>Delete</button>").click(function() {
            delete_sale(sale.id);
        });
        $deleteBtnCol.append($deleteBtn);

        $recordRow.append($salespersonCol, $clientCol, $reamsCol, $deleteBtnCol);

        // Make the record row draggable
        $recordRow.draggable({
            helper: "clone",
            revert: "invalid",
            start: function(event, ui) {
                $(this).css('opacity', '.5');
            },
            stop: function(event, ui) {
                $(this).css('opacity', '1');
            }
        });

        $(".record-area").prepend($recordRow);
    });
}



//this version incorporates the functionality the submitform had before. 

function save_sale(event) {
    event.preventDefault();  // Prevent the default form submission behavior

    // Get values from form inputs
    var salesperson = "Jason Montoya";  // Assuming this is predefined or retrieved from elsewhere
    var client = $("#input-box1").val();
    var reams = $("#input-box2").val();

    // Validation
    var errorMessages = [];
    if (!client) {
        errorMessages.push("Please enter a client name.");
    }
    if (!reams) {
        errorMessages.push("Please enter the number of reams.");
    } else if (isNaN(reams) || parseInt(reams) <= 0) {
        errorMessages.push("Number of reams must be a positive integer.");
    }

    // Display error messages if validation fails
    $("#error-messages").empty();
    if (errorMessages.length > 0) {
        $.each(errorMessages, function(i, message) {
            $("#error-messages").append("<li>" + message + "</li>");
        });
        return;  // Stop execution if there are errors
    }

    // Prepare the sale object
    var new_sale = {
        salesperson: salesperson,
        client: client,
        reams: parseInt(reams)
    };

    // AJAX call to the server to save the sale
    $.ajax({
        url: '/save_sale',  // Adjust the URL to your server's endpoint
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(new_sale),
        success: function(data) {
            let sales = data["sales"]
            display_sales_list(sales)
            /* Add the new sale to the top of the list
            let $recordRow = $("<div class='row sale-record'></div>");
            let $salespersonCol = $("<div class='col-3'><li>" + new_sale.salesperson + "</li></div>");
            let $clientCol = $("<div class='col-3'><li>" + new_sale.client + "</li></div>");
            let $reamsCol = $("<div class='col-3'><li>" + new_sale.reams + "</li></div>");
            let $deleteBtnCol = $("<div class='col-2'><button class='delete-button'>Delete</button></div>"); 

            $recordRow.append($salespersonCol, $clientCol, $reamsCol, $deleteBtnCol);
            $(".record-area").prepend($recordRow);
            */

            // Update autocomplete if the client is new
            let clients = data["clients"]
            $("#input-box1").autocomplete({source: clients});
        },
        error: function(xhr, status, error) {
            console.error("Error saving sale:", error);
        }
    });

    // Clear input fields after submission
    $("#input-box1").val("");
    $("#input-box2").val("");
    $("#input-box1").focus();
}
function delete_sale(id) {
    $.ajax({
        url: '/delete_sale/' + id, 
        type: 'DELETE',
        success: function(data) {
            display_sales_list(data.sales);
        },
        error: function(xhr, status, error) {
            console.error("Error deleting sale:", error);
        }
    });
}


$(document).ready(function() {
    // Display all sales records
    display_sales_list(sales);

    // Initialize autocomplete for input-box1
    $("#input-box1").autocomplete({source: clients});

    $("#submitButton").click(function(event) {
        save_sale(event);
    });
    $("#droppable").droppable({
        over: function(event, ui) {
            $(this).css("background-color", "yellow");
        },
        out: function(event, ui) {
            $(this).css("background-color", "");
        },
        drop: function(event, ui) {
            $(this).css("background-color", "");

            // Get the client name from the dropped item
            var clientName = ui.draggable.find(".col-3:nth-child(2) li").text();

            // Remove the corresponding entry from the sales array
            for (var i = 0; i < sales.length; i++) {
                if (sales[i].client === clientName) {
                    delete_sale(sales[i].id); // Call delete_sale function to handle deletion
                    break; // Assuming each client name is unique
                }
            }

            // Remove the dropped item from the UI
            ui.draggable.remove();
        }
    });
});
