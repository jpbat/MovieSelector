$('.delete-btn').on('click', function (event) {
    $.ajax({
        type: "GET",
        contentType: "application/json",
        url: "/remove/?movieId=" + movieId,
        success: function(data, textStatus, request) {
            location.reload();
        },
        error: function(request, textStatus, error) {
            alert('An error occurred!');
        }
    });
});

$('.refresh-btn').on('click', function (event) {
    location.reload();
});
