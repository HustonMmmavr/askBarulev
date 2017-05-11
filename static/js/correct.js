 $(document).ready(function() {

    $('.correct').click(function() {
        console.log('1');
        var aid = $(this).data('aid');
        var csrftoken = Cookies.get('csrftoken');
        var checked =$(this).prop("checked");
        console.log(csrftoken);
        console.log(aid);
        $.ajax({
            type: 'POST',
            url: '/correct',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            headers: { "X-CSRFToken": csrftoken},
            data: JSON.stringify({aid: aid, checked: checked}),
        }).done(function(resp) 
        {
            if (resp.correct) 
            {
                console.log("1sd");
                $('#correct_'+resp.aid).html("Correct!");
            } else 
            {
                $('#correct_'+resp.aid).html("");
            }
        }).fail(function(err) {
            console.log(err);
        });
    });
});
