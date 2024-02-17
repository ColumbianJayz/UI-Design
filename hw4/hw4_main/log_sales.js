let clients = [
    "Shake Shack",
    "Toast",
    "Computer Science Department",
    "Teacher's College",
    "Starbucks",
    "Subsconsious",
    "Flat Top",
    "Joe's Coffee",
    "Max Caffe",
    "Nussbaum & Wu",
    "Taco Bell",
];
let sales = [
    {
        "salesperson": "James D. Halpert",
        "client": "Shake Shack",
        "reams": 100
    },
    {
        "salesperson": "Stanley Hudson",
        "client": "Toast",
        "reams": 400
    },
    {
        "salesperson": "Michael G. Scott",
        "client": "Computer Science Department",
        "reams": 1000
    },
];

$(document).ready(function() {
    $("#input-box1").autocomplete({
        source: function(request, response) {
            var term = request.term;
            var matches = $.grep(clients, function(client) {
                return client.toLowerCase().indexOf(term.toLowerCase()) !== -1;
            });
            if (matches.length === 0 && term !== '') {
                clients.push(term);
                matches.push(term);
            }
            response(matches);
        },
        messages: {
            noResults: '',
            results: function() {}
        }
    });

    populatingExistingInfo();

    $("#submitButton").click(function(event) {
        submitForm(event);
    });

    $("#input-box1, #input-box2").keydown(function(event) {
        if (event.keyCode === 13) {
            submitForm(event); // Ensure the event is passed to handle form submission
        }
    });

    $(".record-area").on("click", ".delete-button", function() {
        $(this).closest(".sale-record").remove();
    });

    function populatingExistingInfo() {
        $.each(sales, function(index, record) {
            addSaleRecord(record.salesperson, record.client, record.reams);
        });
    }

    function submitForm(event) {
        event.preventDefault();
        var client = $("#input-box1").val();
        var ream = $("#input-box2").val();
        var errorMessages = [];

        if (!client) {
            errorMessages.push("Please enter a client name.");
        }
        if (!ream) {
            errorMessages.push("Please enter the number of reams.");
        } else if (isNaN(ream) || parseInt(ream) <= 0) {
            errorMessages.push("Number of reams must be a positive integer.");
        }

        $("#error-messages").empty();
        if (errorMessages.length > 0) {
            $.each(errorMessages, function(i, message) {
                $("#error-messages").append("<li>" + message + "</li>");
            });
            return;
        }

        addSaleRecord("Jason Montoya", client, ream);

        $("#input-box1").val("");
        $("#input-box2").val("");
        $("#input-box1").focus();
    }

    function addSaleRecord(salesperson, client, reams) {
        var $recordRow = $("<div class='row sale-record'></div>");

        var $salespersonCol = $("<div class='col-3'><li>" + salesperson + "</li></div>");
        var $clientCol = $("<div class='col-3'><li>" + client + "</li></div>");
        var $reamsCol = $("<div class='col-3'><li>" + reams + "</li></div>");
        var $deleteBtnCol = $("<div class='col-2'><button class='delete-button'>Delete</button></div>");

        $recordRow.append($salespersonCol, $clientCol, $reamsCol, $deleteBtnCol);

        $(".record-area").prepend($recordRow);

        // Since we're using a row for each sale record now, draggable should be applied to the whole row.
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
                        sales.splice(i, 1);
                        break; // Assuming each client name is unique
                    }
                }
        
                // Remove the dropped item from the UI
                ui.draggable.remove();
        
                // Re-populate the view based on the updated sales array
                regenerateView();
            }
        });
        
        function regenerateView() {
            $(".record-area").empty(); // Clear the current view
            $.each(sales, function(index, record) { // Add each sale record back to the view
                addSaleRecord(record.salesperson, record.client, record.reams);
            });
        }
        
    }
});