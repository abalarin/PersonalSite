setTimeout(animate_in_out, 3000);

function animate_in_out() {

  $(".icon").removeClass("animate-in");
  $(".icon").addClass("animate-out");
  $('.icon').bind('animationend webkitAnimationEnd oAnimationEnd MSAnimationEnd', function(e) {
    $(this).remove();
  });

}
