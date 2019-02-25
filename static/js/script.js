$(document).ready(function(){

  $(".card").click(function(){
    
        // $(this).slideUp("slow", function(){
        //     new_class = $(this).attr('class_hidden');
        //     new_class = "card " + new_class;
        //     $(this).attr('class', new_class);
        // })

        // $(this).slideDown("slow");

        $(".card").flip(true);

  });

  $(".card").flip(true, {
    trigger: 'click'
  });
});