$(document).ready(function () {
  startTimer(60);

  $(".card_to_flip").click(function () {
    $(this).addClass("is-flipped");
    setTimeout(function () { startTimer(60); }, 10);
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