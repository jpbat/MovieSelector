javascript:$.ajax({
  type: "GET",
  crossDomain: true,
  url: "http://jpbat.pt/movies/add/?imdb=" + window.location.href,
  success: function(data, textStatus, request) {alert('Movie added!');},
  error: function(request, textStatus, error) {alert('An error occurred!');}
});
void(0);