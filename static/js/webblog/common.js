var access_token=window.localStorage.getItem("access_token");
var login_user = window.localStorage.getItem("username");

function is_login(){
    $.ajax({
         url: "/is_login/",
         type: "get",
         dataType: "json",
         headers:{
             "Authorization": "Bearer" + " " +  access_token
         },

         success: function (data, textstatus, XHR) {
             new_access_token = data.new_access_token;
             if (new_access_token)
                 window.localStorage.setItem("access_token", new_access_token);

             $("#login").html("退出").click(function () {
                 if (access_token){
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

             $("#login").click(function(){
                if (access_token){
                    window.localStorage.clear();
                    $("#login").html("登录");
                    $("#register").html("注册");
                    <!--刷新当前页-->
                    window.location.reload();
                }
                else
                    $(window).attr("location", "/login/")

             });

             window.localStorage.clear();

             $("#register").click(function(){
                 if ($("#register").html() ==="注册"){
                      $(location).attr("href", "/register/")

                 }


             });

         },


    });

    $("#markdown").click(function() {
        if (access_token)
            $(window).attr("location", "/compile_blog/");
        else
            alert("请先登录")
    });

}


$(function (){
    is_login();
});
