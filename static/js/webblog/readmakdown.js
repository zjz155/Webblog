var access_token = window.localStorage.getItem("access_token");
path = window.location.pathname;
path_name = path.split("/");
article_id = path_name[4];
comment_url = "/" +  login_user  + "/" + "comment" + "/" + article_id + "/";


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
    // re_path(r"comment/(?P<article_id>\w+)/(?P<blog_id>\w+)/$", CommentView.as_view()),
    $("#comment-form").attr("href",comment_url )

}



// 请求评论列表
function comment_list(article_id, page) {
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
                html += '<li class="list-group-item">';
                html +='<span style="margin-right: 10px; ">' + '<img alt="头像" src="https://static.runoob.com/images/mix/cinqueterre.jpg" class="rounded-circle" style="width: 40px;height: 40px">' + '</span>';
                html +='<span id="username-comment" style="margin-right: 10px; ">' +  comment_username + ":" +  '</span>';
                html += '<span id="content-comment" style="margin-right: 10px; ">' +  comment_content + '</span>';
                html += '<span id="content-comment" style="margin-right: 10px; ">' + "(" +  comment_date + ")" + '</span>';
                html += '<span id="reply_comment" style="margin-right: 10px; ">' + '<a href=#comment' + comment_id + ' data-toggle="collapse">' + "查看回复" + '</a>' + "(" + replys + ")" +'</span>';
                html += '<span id="reply_comment" style="margin-right: 10px; ">' + '<a href=#reply' + comment_id + ' data-toggle="collapse">' + "回复" + '</a>' +'</span>';
                html +='</span>';
                html +='</li>';
                html +='</ul>';
                html +='</div><br>';
                html +="\n";

            }


            $("#comment_list").html(html);

            reply_list("/reply/jz_zhou/2/1/")

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
     $("#comment-form").attr("action",comment_url )
    comment_list(article_id,1);

});