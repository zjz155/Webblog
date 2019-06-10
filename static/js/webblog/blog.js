// var token;

// 请求一(某)页数据 /blog/uname/1
function page_request(page, uname) {
      $.ajax({
          url: "/blog/" + uname + "/"  + page + "/",
          type: "get",
          dataType: "json",
          success: function (data, status, XHR) {
                html = "";
                for (i=0; i< data.entries.length; i++){
                    username = data.entries[i].user;
                    headline = data.entries[i].headline;
                    abstract = data.entries[i].abstract;
                    pub_date = data.entries[i].pub_date;
                    blog = data.entries[i].blog;
                    link = data.entries[i].link;
                    page_number = data.page_number;
                    num_pages = data.num_pages;
                    has_previous = data.has_previous;
                    has_next = data.has_next;


                    console.log(data);

                    html += '<li class="list-group-item list-group-item-action rounded-0 ">';
                    html += '<div>';
                    html += '<a  href=' + link + ' ' + 'class="text-dark d-block">';
                    html += '<h5>' + headline + '</h5>';
                    html += '<p class="text-muted">' + abstract + '</p>';
                    html += '</a>';
                    html += '</div>';
                    html += '<div>';
                    html += '<span>' + username + '<span> | ';
                    html += '<span>' + pub_date + '</span> ｜';
                    html += '<span>阅读 0</span> |';
                    html += '<span>评论 0</span>';
                    html += '</div>';
                    html += '</li>';


                }
                $("#content-list").html(html);
                $("#username-siderbar").html(" " + uname);

                // 生成分页
                paginator(uname, 3, page, has_previous, has_next)

          },

          error: function (XHR, textStatus, errorThrown) {
                html = "";
                html += '<li class="list-group-item list-group-item-action rounded-0">';
                html += '<div>';
                html += '<a  href=' + "#" + ' ' + 'class="text-dark d-block">';
                html += '<h5>' + "你还没发布任何文章!" + '</h5>';
                html += '<p class="text-muted">' + "欢迎成为本站的一员, 在这里分享您的思想与技艺! 如果觉的本站点不错，别忘了向您的朋友推荐！" + '</p>';
                html += '</a>';
                html += '</div>';
                html += '<div>';
                html += '<span>' + "admin" + '<span> | ';
                html += '<span>' + '2019-5-30' + '</span> ｜';
                html += '<span>阅读 0</span> |';
                html += '<span>评论 0</span>';
                html += '</div>';
                html += '</li>';

                $("#content-list").html(html);
                $("#username-siderbar").html(" " + uname);
                $("#pagination").remove();



              console.log(textStatus);
          }
      });


}


// 实现翻页
function paginator(uname, num, page, has_previous, has_next){
     if(num_pages > num)
        i = num;
     else
        i = num_pages;

    if(!has_previous)
        html = '<li class="page-item disabled"><a class="page-link" href="#" id="up"><< </a></li>';
    else
        html = '<li class="page-item"><a class="page-link" href="#" id="up"><< </a></li>';


    start = parseInt(page/num) + 1;
    console.log("has_next:", has_next);

    // 生成页码
    for(j=start; j<=i+start && j<=num_pages; j++){
        if(parseInt(page) === j)
            html += '<li class="page-item active"><a class="page-link" href="#">' + j + '</a></li>';
        else{
            html += '<li class="page-item"><a class="page-link" href="#">' + j + '</a></li>';
        }
    }

    if(!has_next)
        html += ' <li class="page-item disabled"><a class="page-link" href="#" id="down">>></a></li>';
    else
        html += ' <li class="page-item"><a class="page-link" href="#" id="down">>></a></li>';

    $("#pagination").html(html);


    // 为页码绑定事件
    $('a', "ul#pagination").click(function () {
        <!--获取左右翻页的id-->
        p = $(this).attr("id");
        switch (p) {
            case "up":
                n = $('.active > a', "ul#pagination").html();
                console.log("n:" + n);
                page_request((parseInt(n) - 1), uname);
                break;

            case "down":
                n = $('.active > a', "ul#pagination").html();
                page_request((parseInt(n) + 1), uname);
                break;
            default:
                 page_request($(this).html(), uname);

        }

    });
 }


// 关注
function contact(username, action, be_followed){
    if (username === be_followed){
        $("#contact").hide();
        return
    }

    $.ajax({
        url: "/" + username + "/contact/" + action + "/" + be_followed +"/",
        type: "post",
        dataType: "json",
        headers:{
             "Authorization": "Bearer" + " " +  window.localStorage.getItem("access_token")
         },

        success: function (data, textStatus, XHR) {
            text = data.display;
            if(text === "已关注"){
                $("#contact").html(text).removeClass("btn-outline-danger").addClass("btn-outline-secondary").hover(
                    function () {
                        $(this).html("取消关注").removeClass("btn-outline-secondary").addClass("btn-outline-danger");

                    },
                    function () {
                        $(this).html("已关注").removeClass("btn-outline-danger").addClass("btn-outline-secondary");

                    }
                );
            }else if (text === "关注") {
                $("#contact").html(text).addClass("btn-outline-danger").removeClass("btn-outline-secondary").hover(
                    function () {
                        $(this).html("关注").removeClass("btn-outline-secondary").addClass("btn-outline-danger");

                    },
                )

            }




        }
    });



}



$(function () {
    var path = window.location.pathname;
    // console.log(path);
    path_names = window.location.pathname.split("/");
    page_request(page=1, uname=path_names[2]);
    contact(login_user, "is_contacted", path_names[2]);

    $("#contact").click(function () {
        text = $(this).html();
        if (text === "关注") {
            // var path_names = window.location.pathname.split("/");
            contact(userame=login_user, action="follow", be_followed=path_names[2]);
            // $("#contact").html("已关注")
        }
        else if (text === "取消关注")
            contact(userame=login_user, action="cancel", be_followed=path_names[2]);

    });
});

console.log("blog - token:" + access_token);

