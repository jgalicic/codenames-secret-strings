var red_count = 0
var blue_count = 0
var black_count = 0

var team = 'blue' //for testing only, DELETE LATER

$(document).ready(function () {
  /***** added by Justin on 2/25 @ 9pm */
  $(".card").click(function () {
    $(this).addClass("is-flipped");

    // Counting teams' card selections
    var card_color = $(this).find(".card_back").attr("class_hidden");
    card_color = card_color.toUpperCase();
    if (card_color == 'RED'){
        ++red_count;
    }
    if (card_color == 'BLUE'){
        ++blue_count;
    }
    if (card_color == 'BLACK'){
        ++black_count;
    }

    function win(color) {
        $(".board_container").html("<h3 style='color: white;'> Team "+ color +" won!</h3>");
      }

    if (red_count == 5){
        setTimeout(function() {win("Red")}, 4000);
    }
    if (blue_count == 5){
        setTimeout(function() {win("Blue")}, 4000);
    }
    if (black_count == 1){
        if (team == "red"){
            setTimeout(function() {win("Blue")}, 4000);
        }
        if (team == "blue"){
            setTimeout(function() {win("Red")}, 4000);
        }
    }
    
  });

  /***********************************/

  /* End jQuery */
});