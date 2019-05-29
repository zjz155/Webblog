// var token;

<!--请求一页数据-->
function page_request(page, uname) {
      $.get("/blog/" + uname + "/"  + page + "/", function (data, status) {
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
            $("#headline").html(headline);
            $("#abstract").html(abstract);



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

         <!--生成分页-->
         paginator(uname, 3, page, has_previous, has_next)

     },"json");



}


<!--实现翻页-->
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

    <!--生成页码-->
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


    <!--为页码绑定事件-->
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


path = window.location.pathname;
console.log(path);
path_names = window.location.pathname.split("/");
$(page_request(page=1, uname=path_names[2]));
console.log("blog - token:" + token);
