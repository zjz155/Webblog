var token=window.localStorage.getItem("token");

function is_login(){
    $.ajax({
         url: "/is_login/",
         type: "get",
         dataType: "json",
         headers:{
             "Authorization": "Bearer" + " " +  window.localStorage.getItem("token")
         },

         success: function (data, status, XHR) {

             $("#login").html("退出").click(function () {
                 if (token){
                    window.localStorage.clear();
                    $("#login").html("登录").click(function () {
                        $(window).attr("location", "/login/")
                    });
                    $("#register").html("注册").click(function () {
                         $(window).attr("location", "/register/")
                    });
                    // window.location.reload();
                }
                else
                    $(window).attr("location", "/login/")


             });


             $("#register").html(data.username).click(function () {
                 $(window).attr("location", "/blog/" + data.username + "/" + "list")
             });


         },
         error: function (XHR, textStatus, errorThrown) {

             window.localStorage.clear();

             $("#login").click(function(){
                if (token){
                    window.localStorage.clear();
                    $("#login").html("登录");
                    $("#register").html("注册");
                    <!--刷新当前页-->
                    window.location.reload();
                }
                else
                    $(window).attr("location", "/login/")

             });

             $("#register").click(function(){
                 if ($("#register").html() ==="注册"){
                      $(location).attr("href", "/register/")

                 }


             });

         },


    });


    $("#markdown").click(function(){
        if (token)
          $(window).attr("location", "/compile_blog/");
        else
          alert("请先登录")

    });
}

$(is_login());



