// var token;

// 请求一(某)页文章列表数据 /blog/uname/1
function page_request(page, uname, FILER) {
      $.ajax({
          url: "/blog/" + uname + "/article/"  + page,
          type: "get",
          data: FILER,
          dataType: "json",
          success: function (data, status, XHR) {
                html = "";
                for (i=0; i< data.entries.length; i++){
                    username = data.entries[i].user;
                    headline = data.entries[i].headline;
                    abstract = data.entries[i].abstract;
                    pub_date = data.entries[i].pub_date;
                    comments = data.entries[i].comments;
                    pv = data.entries[i].pv;
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
                    html += '<small>';
                    html += '<span>' + username + '<span> | ';
                    html += '<span>' + pub_date + '</span> ｜';
                    html += '<span>阅读 ' + pv + '</span> |';
                    html += '<span>评论 ' + comments + '</span> |';
                    html += '<span>喜欢 ' + 1 + '</span>';
                    html += '</small>';
                    html += '</div>';
                    html += '</li>';


                }
                $("#content-list").html(html);
                $("#username-siderbar").html(" " + uname);

                // 生成分页
                paginator(uname, 3, page, has_previous, has_next, FILER);

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
                // $("#username-siderbar").html(" " + uname);
                $("#pagination").remove();

                console.log(textStatus);
          }
      });


}

function get_siderbar(uname){
                url = "/blog/" + uname + "/blog/info/";
                $.ajax({
                    url: url,
                    type: "get",
                    dataType: "json",
                    success: function(data, textStatus, XHR) {
                        username = data.username;
                        n_contacts = data.n_contacts;
                        n_comments = data.n_comments;
                        year = data.year;
                        pv = data.pv;

                        $("#username-siderbar").html(username);
                        $("#n_comments").html(n_comments);
                        $("#join-date").html(year);
                        $("#pv").html(pv);
                        $("#n_contacts").html(n_contacts);
                        console.log("pv:"+ pv);
                        console.log("year:"+ year);
                        console.log("n_comments:"+ n_comments);

                        html = "";
                        for(i=0; i<data.categories.length; i++){
                            category = data.categories[i].category;
                            html +="<div>";
                            html +="<a href='#'>";
                            html += category;
                            html +="</a>";
                            html +="</div>";

                        }

                        $("#sider-bar-category").html(html);
                        $("a", "div#sider-bar-category").on("click", function () {
                             data = {"category": $(this).html()};
                             console.log(data);
                             // 显示文章列
                            page_request(page=1, uname=name_visited, data);

                         });
                    }

                });

}


// 实现翻页
function paginator(uname, num, page, has_previous, has_next, FILER){
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
                page_request((parseInt(n) - 1), uname, FILER);
                break;

            case "down":
                n = $('.active > a', "ul#pagination").html();
                page_request((parseInt(n) + 1), uname, FILER);
                break;
            default:
                 page_request($(this).html(), uname, FILER);

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
        url: "/blog/" + username + "/contact/" + action + "/" + be_followed +"/",
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


// 执行
$(function () {
    var path = window.location.pathname;
    // console.log(path);
    // path_names = window.location.pathname.split("/");
    var data;
    // 显示文章列
    page_request(page=1, uname=name_visited, data);

    get_siderbar(name_visited);
    //  关注
    contact(login_user, "is_contacted", name_visited);


    $("#contact").click(function () {
        text = $(this).html();
        if (text === "关注") {
            // var path_names = window.location.pathname.split("/");
            contact(userame=login_user, action="follow", be_followed=name_visited);
            // $("#contact").html("已关注")
        }
        else if (text === "取消关注")
            contact(userame=login_user, action="cancel", be_followed=name_visited);

        get_siderbar(name_visited);

    });




});

console.log("blog - token:" + access_token);

