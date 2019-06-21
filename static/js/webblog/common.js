var access_token=window.localStorage.getItem("access_token");
var login_user = window.localStorage.getItem("username");
path = window.location.pathname;
path_name = path.split("/");
name_visited = path_name[2];
console.log("common.js--path_name:" + path_name);

console.log("blog_list_path:" + name_visited);
if (!login_user)
    login_user = "jz_zhou";

// function user_info(login_user){
//     $.ajax({
//         url: "/userinfo/" + name_visited,
//         type: "get",
//         dataType: "json",
//         success: function (data, textSatust, XHR) {
//             username = data.username;
//             n_comments = data.n_comments;
//             year = data.year;
//             pv = data.pv;
//
//            $("#username-siderbar").html(username);
//            $("#n_comments").html(n_comments);
//            $("#join-date").html(year);
//            $("#pv").html(pv);
//             console.log("pv:"+ pv);
//             console.log("year:"+ year);
//             console.log("n_comments:"+ n_comments);
//
//         }
//
//     });
//
// }


function nav_login_btn(){
    $("#login").html("登录").attr("href", "/login/");


    $("#register").html("注册").attr("href", "/register/")
}


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


             $("#login").html("退出").attr("href", "#").click(function () {
                window.localStorage.clear();
                $(this).html("登录");
                $("#register").html("注册");
                window.location.reload();




             });



            var url = "/blog/" + data.username + "/article/" + "list" + "/";
            $("#register").html(data.username).attr("href", url);


         },
         error: function (XHR, textStatus, errorThrown) {
            window.localStorage.clear();
            nav_login_btn();

         },
        complete: function (XHR, textStatus) {
            $("#markdown").click(function() {
            if (access_token)
                $(window).attr("location", "/compile_blog/" + login_user );
            else
                alert("请先登录")
            });
        }


    });


}

function search() {
    $("#search_btn").click(function () {
        text = $("#search").val();
        $("#reset-btn").trigger("click");
        console.log(text);
        page_request(page=1, uname=name_visited,{"title": text});

    });



}




$(function (){
    is_login();
    search();
});
