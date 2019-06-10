var access_token = window.localStorage.getItem("access_token");
path = window.location.pathname;
path_name = path.split("/");
article_id = path_name[4];
comment_url = "/" +  login_user + "/comment/" + "/" + article_id + "/";

// 显示markdown
$(function() {
    url = window.location.pathname;
    var testEditormdView, testEditormdView2;
    $.get(url + "data/", function(markdown) {
        console.log(markdown);
        headline = markdown["headline"];
        testEditormdView = editormd.markdownToHTML("test-editormd-view", {
            markdown        : "## " + markdown["headline"] + "\r\n" + markdown["content"],//+ "\r\n" + $("#append-test").text(),
            //htmlDecode      : true,       // 开启 HTML 标签解析，为了安全性，默认不开启
            htmlDecode      : "style,script,iframe",  // you can filter tags decode
            //toc             : false,
            tocm            : true,    // Using [TOCM]
            //tocContainer    : "#custom-toc-container", // 自定义 ToC 容器层
            //gfm             : false,
            //tocDropdown     : true,
            // markdownSourceCode : true, // 是否保留 Markdown 源码，即是否删除保存源码的 Textarea 标签
            emoji           : true,
            taskList        : true,
            tex             : true,  // 默认不解析
            flowChart       : true,  // 默认不解析
            sequenceDiagram : true,  // 默认不解析
        });
        $("#title").html(headline)
        //console.log("返回一个 jQuery 实例 =>", testEditormdView);
        // 获取Markdown源码
        //console.log(testEditormdView.getMarkdown());
        //alert(testEditormdView.getMarkdown());
    });
    testEditormdView2 = editormd.markdownToHTML("test-editormd-view2", {
        htmlDecode      : "style,script,iframe",  // you can filter tags decode
        emoji           : true,
        taskList        : true,
        tex             : true,  // 默认不解析
        flowChart       : true,  // 默认不解析
        sequenceDiagram : true,  // 默认不解析
    });

});

// 发表评论
function comment() {
    $("#comment-btn").click(function () {

        $.ajax({
            url: comment_url,
            type: "post",
            dataType: "json",
            headers: {
                "Authorization": "Bearer" + " " + window.localStorage.getItem("access_token")
            },
            data: $("#comment-form").serialize(),

            success: function (data, textStatus, XHR) {
               // $("input[type=reset]").trigger("click");
               comment_list(article_id, 1);
                alert("评论成功！")

            },

            error: function (XHR, textStatus, errorThrown) {
                alert("发布失败, 请重试");
                nav_login_btn();

            }

        });
    });


    // function reply() {
    //
    //
    // }
}

// 回复评论
function reply(reply_btn,reply_url, form_id) {
    $(reply_btn).click(function (reply_url, form_id) {

        $.ajax({
            url: reply_url,
            type: "post",
            dataType: "json",
            headers: {
                "Authorization": "Bearer" + " " + window.localStorage.getItem("access_token")
            },
            data: $(form_id).serialize(),

            success: function (data, textStatus, XHR) {

                alert("回复成功！")

            },

            error: function (XHR, textStatus, errorThrown) {
                alert("发布失败, 请重试");
                nav_login_btn();

            }

        });
    });


    // function reply() {
    //
    //
    // }
}


// 请求评论列表
function comment_list(article_id, page) {
     // 显示评论列表
    $("#comment_list").empty();
    $.ajax({
        url: "/comment/list/" + article_id  + "/" + page,
        type: "get",
        dataType: "json",
        success: function (data, textStatus, XHR) {
            console.log(data.comment_page);
            n = data.comment_page.length;
            html = '';
            for(i=0; i< n; i++){
                comment_id = data.comment_page[i].comment_info.comment_id;
                comment_content = data.comment_page[i].comment_info.comment_content;
                comment_username = data.comment_page[i].comment_info.comment_username;
                comment_date = data.comment_page[i].comment_info.comment_date;

                entry_entry_author = data.comment_page[i].entry_info.entry_author;
                entry_headline = data.comment_page[i].entry_info.entry_headline;

                replys = data.comment_page[i].n_replys;




                html +='<div id=' + comment_id + '>';
                html +='<ul class="list-group">';
                html += '<li class="list-group-item" id=list-group-item' + comment_id + '>';
                html += '<p>';
                html +='<span style="margin-right: 10px; ">' + '<img alt="头像" src="https://static.runoob.com/images/mix/cinqueterre.jpg" class="rounded-circle" style="width: 40px;height: 40px">' + '</span>';
                html +='<span id="username-comment" style="margin-right: 10px; ">' +  comment_username + ":" +  '</span>';
                html += '<span id="content-comment" style="margin-right: 10px; ">' +  comment_content + '</span>';
                html += '<span id="content-comment" style="margin-right: 10px; ">' + "(" +  comment_date + ")" + '</span>';
                html += '<span style="margin-right: 10px; ">' + '<a id=com' + comment_id  + ' href=#comment' + comment_id + ' data-toggle="collapse" class=' + comment_id + '>' + "查看回复" + '</a>' + "(" + replys + ")" +'</span>';
                html += '<span style="margin-right: 10px; ">' + '<a id=rep' + comment_id + ' href=#reply' + comment_id + ' data-toggle="collapse" class='+ comment_id + '>' + "回复" + '</a>' +'</span>';
                html +='</span>';
                html += '</p>';
                html +='</li>';
                html +='</ul>';
                html +='</div><br>';
                html +="\n";

                // 还一添评论
                $("#comment_list").append(html);


                // 回复
                html="";
                html += '<p>';
                html += '<form id=' + 'reply' + comment_id + ' class=collapse' + '>';
                html += '<p>';
                html += '<textarea class="form-control" placeholder="写下你的回复..." name="reply-content"></textarea>';
                html += '</p>';
                html += '<p>';
                html += '<input type="button" class="btn btn-primary" value="提交"' + ' id=reply-btn' + comment_id +'>';
                html += '<input type="reset" style="display:none;" />';
                html += '</p>';
                html += ' </form>';
                html += '</p>';

                $("#list-group-item" + comment_id).append(html);
                html = "";

                reply_btn = '#reply-btn' + comment_id ;
                form_id = "#reply" + comment_id;
                var login_user = window.localStorage.getItem("login_user");
                reply_url = "/" + login_user + "/reply/" + comment_id + "/";
                reply(reply_btn, reply_url, form_id);


            //     <form id="replys" class="collapse">
            //     <p>
            //         <textarea class="form-control" placeholder="写下你的回复..." name="reply-content"></textarea>
            //     </p>
            //     <p>
            //         <input type="button" class="btn btn-primary" value="提交" id="reply-btn" />
            //         <input type="reset" style="display:none;" />
            //     </p>
            //
            //
            // </form>


                // $("#rep" + comment_id).on("click", function(){
                //     $("#comment-form").focus();
                // });

                // 获取每一条评论的评论
                url = "/reply_list/" + comment_id + "/1/";
                reply_list(url);

            }



        },
        complete: function (XHR, textStatus) {

            $("a").on("click", function(){
                cls = $(this).attr("class");
                text = $(this).html();

                if (text === "回复"){

                    console.log("cls:" + cls);
                }
                else if (text === "查看回复"){

                    console.log("cls:"+ cls);

                    $(this).html("收起回复")

                }

                 $("#comment" + cls).on("hidden.bs.collapse", function () {
                      $("#com" + cls).html("查看回复");
                 })


            });









        }
    });

}


// 请求评论对应的回复内容
function reply_list(url) {
    $.ajax({
        url: url,
        type: "get",
        datatype: "json",
        success: function (data, textStatus, XHR) {
            n = data.reply.length;
            reply_from = data.reply[0].reply_from;
            reply_to = data.reply[0].reply_to;
            reply_content= data.reply[0].reply_content;
            reply_time = data.reply[0].reply_time;
            comment_id = data.reply[0].comment_id;
            replys = data.reply[0].n_replys;

            html = '<div id=comment' + comment_id + ' class=collapse>';
            for(i=0; i < n; i++){
                html += '<li class="list-group-item">';
                html +='<span style="margin-right: 10px; ">' + '<img alt="头像" src="https://static.runoob.com/images/mix/cinqueterre.jpg" class="rounded-circle" style="width: 40px;height: 40px">' + '</span>';
                html +='<span id="username-comment" style="margin-right: 10px; ">' +  reply_from +  '<span>' + "回复：" + reply_to + '</span>' + ':' +  '</span>';
                html += '<span id="content-comment"style="margin-right: 10px; ">' +  reply_content + '</span>';
                html += '<span id="content-comment" style="margin-right: 10px; ">' + "(" +  reply_time + ")" + '</span>';
                html += '<span id="reply_comment" style="margin-right: 10px; ">' + "查看回复" + "(" + replys + ")" +'</span>';
                html +='</span>';
                html +='</li>';

            }
            html +="</div>";


            $('#' +  comment_id ).append(html);



        }



    });
}

$(function () {
     // $("#comment-form").attr("action",comment_url );

    comment_list(article_id,1);

    comment()

});