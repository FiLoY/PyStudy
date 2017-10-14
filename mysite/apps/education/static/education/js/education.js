function callAjax(url) {
    $.ajax({
        type: "POST",
        url: url,
        data: $('input').serialize(),
        success: function(data) {
            console.log(data);
            $("#test-process").html(data.code);
            console.log($("#test-index").text());
            if (data.done) {
                console.log('done');
                $("#test-process").html(data.done);
                $('#myModal').modal('show');
            }
        }
    });
}

function test_done() {
    window.location.href = ''
}