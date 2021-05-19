 function searchKeyword() {
    //增加等待动画
    $("#search-result").css("height","35px")
    $("#search-result-top").append("<div class='col-md-12 text-center' id='top-item'><div class='donut text-center' id='loading'></div></div>")
     //按钮上锁
     document.getElementById("search-buttom").disabled = true
     //显示家在动画
     $('#search-result').css('display','block');
        $.ajax({
            type: "POST",                  
            dataType: "json",              
            url: "/search" ,
            data: {
                keyword:JSON.stringify(document.getElementById("keyword").value)
            }, //提交的数据
            success: function (result) {
                console.log(result);       //打印服务端返回的数据(调试用)
                if (result.status_code == 200) {
                    console.log(result)
                    //删除加载动画
                    $('#loading').remove()

                     $("#top-item").append('<button type="button" class="close text-right" data-dismiss="alert" aria-hidden="true">&times;</button>')


                    //按钮解锁
                    document.getElementById("search-buttom").disabled = false

                }
                ;
            },
            error : function() {
                document.getElementById("search-buttom").disabled = false
                alert("提交失败");
            }
        });
    }
