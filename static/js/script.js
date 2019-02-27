var red_count = 0
var blue_count = 0
var black_count = 0

var team_blue = true //for testing only, DELETE LATER

$(document).ready(function () {

    var all_cards = $(".card_to_flip" ).toArray();
    var flipped_cards = [];
    var available_cards = [];

  startTimer(60);
  /***** added by Justin on 2/25 @ 9pm */
  $(".card_to_flip").click(function () {

    $(this).addClass("is-flipped");
    flipped_cards = $(".is-flipped" ).toArray();

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
      if (team_blue == false) {
        setTimeout(function () { win("Blue") }, 4000);
      }
      if (team_blue == true) {
        setTimeout(function () { win("Red") }, 4000);
      }
    }

  });



  function startTimer(count) {
    team_blue = !team_blue

    var buffer_count = count + 2;
    timer = setInterval(function () {
      if (count == 0) {
        $("#counter").html(count);

        for (card in all_cards){
            if(!(flipped_cards.includes(all_cards[card]))){
                available_cards.push(all_cards[card]);
            }
        }
        random_card = available_cards[Math.floor(Math.random()*available_cards.length)];

        $(random_card).click();
        available_cards = [];


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

    if(team_blue){
        $("#team").html("<h3 style='color: white;'> Team: BLUE</h3>");
      }
    else{
        $("#team").html("<h3 style='color: white;'> Team: RED</h3>");
      }
  }





  /***********************************/

  /* End jQuery */
});