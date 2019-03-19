$(document).ready(function () {
  $('.group').hide();
  $('#avg_rating').show();
  $('#dropdown').change(function () {
    $('.group').hide();
    $('#'+$(this).val()).show();
  })
});
