$(document).ready(function(){
    $('.like_question').click(function() {
        var qid = $(this).data('qid');
            console.log('1');
        var type =  'que';
        var type_like=$(this).data('typ');
        var csrftoken = Cookies.get('csrftoken');
        $.ajax({
            type: 'POST',
            url: '/like',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            headers: { "X-CSRFToken": csrftoken},
            data: JSON.stringify({qid: qid, type: type, type_like: type_like})
        }).done(function(resp) {
            var add_value = $('#down_q'+resp.qid).hasClass('disabled_link') == $('#up_q'+resp.qid).hasClass('disabled_link') ? 1 : 2;
            if (resp.like == 1) 
            {
                $('#like_q'+resp.qid).html(parseInt($('#like_q'+resp.qid).text())+add_value);
                $('#up_q'+resp.qid).addClass('disabled_link');
                $('#down_q'+resp.qid).removeClass('disabled_link');
            } else {
                $('#like_q'+resp.qid).html(parseInt($('#like_q'+resp.qid).text())-add_value);
                $('#down_q'+resp.qid).addClass('disabled_link');
                $('#up_q'+resp.qid).removeClass('disabled_link');
            }
        }).fail(function(err) {
            console.log(err);
        });
    });

    $('.like_answer').click(function() {
        var aid = $(this).data('aid');
        var type =  'ans';
        var type_like=$(this).data('typ');
        var csrftoken = Cookies.get('csrftoken');
        $.ajax({
            type: 'POST',
            url: '/like',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            headers: { "X-CSRFToken": csrftoken},
            data: JSON.stringify({aid: aid, type: type, type_like: type_like})
        }).done(function(resp) {
            var add_value = $('#down_a'+resp.aid).hasClass('disabled_link') == $('#up_a'+resp.aid).hasClass('disabled_link') ? 1 : 2;
            console.log(resp.like);
            if (resp.like == 1) 
            {
                $('#like_a'+resp.aid).html(parseInt($('#like_a'+resp.aid).text())+add_value);
                $('#up_a'+resp.aid).addClass('disabled_link');
                $('#down_a'+resp.aid).removeClass('disabled_link');
            } else {
                $('#like_a'+resp.aid).html(parseInt($('#like_a'+resp.aid).text())-add_value);
                $('#down_a'+resp.aid).addClass('disabled_link');
                $('#up_a'+resp.aid).removeClass('disabled_link');
            }
        }).fail(function(err) {
            console.log(err);
        });
    });

});