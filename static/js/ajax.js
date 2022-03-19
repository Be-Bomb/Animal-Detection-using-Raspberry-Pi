$(document).ready(function () {
    setInterval(function () {
        $.ajax({
            type: "get",
            url: "/data_chart",
            dataType: "json",
            success: function (result) {
                $("#dataChart").html(JSON.stringify(result, null, 4));
            },
            error: function() {
                console.log("data chart fail")
            }
        });
    }, 1000 * 0.5);
    
    $("#storage").click(function () {
        $(".modal").fadeIn();
        
        $.ajax({
            type: "get",
            url: "/get_images",
            success: function () {
                // 모달 창을 새로고침하여 데이터를 가져온다.
                $(".modal_content").load(window.location.href + " .modal_content")
            },
            error: function() {
                console.log("get images fail")
            }
        });
    });

    $(".modal").click(function () {
        $(".modal").fadeOut();
    });
});
