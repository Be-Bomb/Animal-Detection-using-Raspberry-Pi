$(document).ready(function () {
    setInterval(function () {
        $.ajax({
            type: "get",
            url: "/data_chart",
            dataType: "json",
            success: function (result) {
                $("#text").html(JSON.stringify(result, null, 4));
            },
        });
    }, 1000 * 0.5);

    $("#storage").click(function () {
        $(".modal").fadeIn();
    });

    $(".modal").click(function () {
        $(".modal").fadeOut();
    });
});
