$(document).ready(function () {

        // 为Ajax设置csrf_token
        $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", gLocals.csrf);
            }
        }
    });


//后台表格js
    (function () {
        $('.btn.btn-w-m').prop('disabled', true);
        var a = $('#userListCheck'),
            b = $('tr.gradeX input[type="checkbox"]'),
            c = $('tr.gradeX input[type="checkbox"],#userListCheck'),
            d = $('.btn.btn-w-m'),
            e = function () {
                var a = 0;
                $.each(b, function () {
                    if ($(this).prop('checked')) a++;
                });
                if (a > 0) {
                    $('.btn.btn-w-m').prop('disabled', false);
                } else {
                    $('.btn.btn-w-m').prop('disabled', true);
                }
            };
        a.click(function () {
            if ($(this).prop('checked')) {
                b.prop('checked', true);
            } else {
                b.prop('checked', false);
            }
        });
        c.click(function () {
            e();
        });

        $('.btn.btn-white').click(function () {
            if ($(this).data("type") != 'review') {
                $('tr.gradeX input[type="checkbox"]').each(function (k, v) {
                    if ($(v).prop('checked')) {
                        $(v)[0].parentNode.parentNode.outerHTML = '';
                    }
                });
            }

            $('.btn.btn-w-m').prop('disabled', true);

        });
        /*$('.btn.btn-primary').click(function () {
         $('tr.gradeX input[type="checkbox"]').each(function(k,v){
         $(v).prop('checked',false);
         });
         });*/

    })();

});


//btn1删除按钮  msgClss弹窗的p标签  msg1弹窗前缀内容 函数返回选中的所有id
function _alert(btn1, msgClss, msg1) {
    var j = {};
    $(btn1).click(function () {
        var n = new Array(), msg = '';
        $('tr.gradeX input[type="checkbox"]').each(function (k, v) {
            if ($(v).prop('checked')) {
                n.push($(v).parent().parent().children('.userListId').text());
            }
        });
        for (var i in n) {
            j[i] = n[i];
            msg += n[i] + ',';
        }
        JSON.stringify(j);
        if (msg != '') {
            $(msgClss).html(msg1 + '<span style="color:red;font-weight: bold">' + msg + '</span>');
        } else {
            $(btn1).prop('disabled', true);
        }
    });
    return j;
}

function listNubmer() {
    var n = new Array(), j = {};
    $('tr.gradeX input[type="checkbox"]').each(function (k, v) {
        if ($(v).prop('checked')) {
            n.push($(v).parent().parent().children('.userListId').text());
        }
    });
    for (var i in n) {
        j[i] = n[i];
    }
    JSON.stringify(j);
    return j;
}

