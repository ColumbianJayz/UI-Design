$( function() {
    $( "#draggable" ).draggable({
        revert: function(droppable){
            return !droppable;
        }
    });
    $( "#droppable" ).droppable({
      drop: function( event, ui ) {
        $( this )
          .addClass( "ui-state-highlight" )
          .find( "p" )
            .html( "Dropped!" );
      }
    });
  } );