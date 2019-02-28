$(document).ready(function () {

  var red_count = 0;
  var blue_count = 0;
  var black_count = 0;

  var team_blue = true;
  var lock_out = true;

  if ($("#color_start").hasClass("blue_starts")) {
    team_blue = false;
  }


  var all_cards = $(".card_to_flip").toArray();
  var flipped_cards = [];
  startTimer(60);

  $(".card_to_flip").click(function () {
    // Prevent function from running if card has already been flipped
    if (!$(this).hasClass("is-flipped") && lock_out == false ) {
        // lock_out = true;

      $(this).addClass("is-flipped");
      flipped_cards = $(".is-flipped").toArray();
    //   setTimeout(function () { startTimer(60); }, 2500);

      // Counting teams' card selections
      var card_color = $(this).find(".card_back").attr("class_hidden");
      countCardColors(card_color);

      checkWin(red_count, blue_count, black_count);
    }
  });

  $("#end_turn").click(function(){
      if (lock_out == false){
        lock_out = true;
        setTimeout(function () { startTimer(60); }, 1000);
      }
  });


  function startTimer(count) {
    //Team banner toggle
    team_blue = !team_blue;

    var buffer_count = count + 2;
    timer = setInterval(function () {
      if (count == 0) {
        $("#counter").html(count);
        flipRandomCard(all_cards, flipped_cards);

      } else if (buffer_count - count == 2) {
        buffer_count--;
        $("#counter").html("Ready");
      } else if (buffer_count - count == 1) {
        buffer_count--;
        $("#counter").html("Set!");
      } else if (buffer_count - count == 0) {
        buffer_count--;
        $("#counter").html("Go!");
        lock_out = false;
      } else {
        buffer_count = 0;
        $("#counter").html(count--)
      };
      if (count == -1) {

        clearInterval(timer);
      }

      teamBannerToggle(team_blue);
    }, 1000);

    // Clear timer when a new card is clicked
    $("#end_turn").click(function () {
      // Prevent function from executing if card is already flipped
    //   if (!$(this).hasClass("is-flipped") && lock_out == false ) {
        if (lock_out == false){
            clearInterval(timer);
        }
    //   }
    });

  }

  /**********
  FUNCTIONS
  **********/
  function flipRandomCard(all_cards, flipped_cards) {
    var available_cards = [];
    for (card in all_cards) {
      if (!(flipped_cards.includes(all_cards[card]))) {
        available_cards.push(all_cards[card]);
      }
    }
    random_card = available_cards[Math.floor(Math.random() * available_cards.length)];

      $(random_card).click();
      $('#end_turn').click();
 }

  function checkWin(red_count, blue_count, black_count) {
    if (red_count == 5) {
        setTimeout(function () { win("red") }, 900);
      }
      if (blue_count == 5) {
        setTimeout(function () { win("blue") }, 900);
      }
      if (black_count == 1) {
        if (team_blue == false) {
          setTimeout(function () { win("blue") }, 500);
        }
        if (team_blue == true) {
          setTimeout(function () { win("red") }, 500);
        }
      }
    }


  function win(color) {
    // $(".board_container").html("<h3 style='color: white;'> Team " + color + " won!</h3>");
    window.location.replace('/win/' + color);
  }

  function teamBannerToggle(team_blue) {
    if (team_blue) {
      $(".top_bar1").removeClass("red");
      $(".top_bar1").addClass("blue");
    }
    else {
      $(".top_bar1").removeClass("blue");
      $(".top_bar1").addClass("red");
    }
  }

  function countCardColors(card_color) {
    card_color = card_color.toUpperCase();
      if (card_color == 'RED') {
        ++red_count;
        if(team_blue){
            $('#end_turn').click();
        }
      }
      else if (card_color == 'BLUE') {
        ++blue_count;
        if(!team_blue){
            $('#end_turn').click();
        }
      }
      else if (card_color == 'BLACK') {
        ++black_count;
      }
      else{
        $('#end_turn').click();
      }
}

  /***********************************/

  /* End jQuery */
});