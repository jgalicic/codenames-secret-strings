var red_count = 0
var blue_count = 0
var black_count = 0

var team = 'blue' //for testing only, DELETE LATER

$(document).ready(function () {
  startTimer(60);
  /***** added by Justin on 2/25 @ 9pm */
  $(".card").click(function () {
    $(this).addClass("is-flipped");
    setTimeout(function () { startTimer(60); }, 10);
    // Counting teams' card selections
    var card_color = $(this).find(".card_back").attr("class_hidden");
    card_color = card_color.toUpperCase();
    if (card_color == 'RED') {
      ++red_count;
    }
    if (card_color == 'BLUE') {
      ++blue_count;
    }
    if (card_color == 'BLACK') {
      ++black_count;
    }

    function win(color) {
      $(".board_container").html("<h3 style='color: white;'> Team " + color + " won!</h3>");
    }

    if (red_count == 5) {
      setTimeout(function () { win("Red") }, 4000);
    }
    if (blue_count == 5) {
      setTimeout(function () { win("Blue") }, 4000);
    }
    if (black_count == 1) {
      if (team == "red") {
        setTimeout(function () { win("Blue") }, 4000);
      }
      if (team == "blue") {
        setTimeout(function () { win("Red") }, 4000);
      }
    }

  });

  function startTimer(count) {
    var buffer_count = count + 2;
    timer = setInterval(function () {
      if (count == 0) {
        $("#counter").html(count);
      } else if (buffer_count - count == 2) {
        buffer_count--;
        $("#counter").html("Ready");
      } else if (buffer_count - count == 1) {
        buffer_count--;
        $("#counter").html("Set!");
      } else if (buffer_count - count == 0) {
        buffer_count--;
        $("#counter").html("Go!");
      } else {
        buffer_count = 0;
        $("#counter").html(count--)
      };
      if (count == -1) clearInterval(timer);
    }, 1000);
    $(".card_to_flip").click(function () {
      clearInterval(timer);
    });
  }





  /***********************************/

  /* End jQuery */
});