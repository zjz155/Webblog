var access_token = window.localStorage.getItem("access_token");
$(function() {
     $("#login").click(function(){
         if (access_token){
            window.localStorage.clear();
            $("#login").html("登录");
            $("#register").html("注册");
         }
         else
             $(window).attr("location", "/login/")
     });
    $("#register").click(function(){
         if ($("#register").html() ==="注册"){
              $(location).attr("href", "/register/")
         }
    });

    $("#markdown").click(function(){
    if (access_token)
        $(window).attr("location", "/compile_blog/");
    else
        alert("请先登录")

    });

});

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