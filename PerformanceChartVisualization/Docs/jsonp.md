

## jsonp 跨域访问问题

* Ajax通过jsonp实现跨域访问,访问成功但走error不走success

* 原因: 用jsonp跨域访问, 会注册callback, 生产一个随机的callback，正确的jsonp格式应该是 callback({"id" : "1","name" : "小王"}); 
       所以我们需要定义callback，前台指定回调函数jsonpCallback：successCallback，后台指定返回的json格式：String jj = "successCallback("+aapJson+")";


原生ajax请求&JSONP
直接撸代码

封装方法：

复制代码
            function ajax(options) {
                options = options || {};
                options.type = (options.type || "GET").toUpperCase();
                options.dataType = options.dataType || "json";
                var params = formatParams(options.data);

                //创建 - 非IE6 - 第一步
                if (window.XMLHttpRequest) {
                    var xhr = new XMLHttpRequest();
                } else { //IE6及其以下版本浏览器
                    var xhr = new ActiveXObject('Microsoft.XMLHTTP');
                }

                //连接 和 发送 - 第二步
                if (options.type == "GET") {
                    xhr.open("GET", options.url + "?" + params, true);
                    xhr.send(null);
                } else if (options.type == "POST") {
                    xhr.open("POST", options.url, true);
                    //设置表单提交时的内容类型
                    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    xhr.send(params);
                }

                //接收 - 第三步
                xhr.onreadystatechange = function () {
                    if (xhr.readyState == 4) {
                        if (xhr.status >= 200 && xhr.status < 300) {
                            options.success && options.success(xhr.responseText, xhr.responseXML);
                        } else {
                            options.error && options.error(xhr.status);
                        }
                    }
                }
            }
            //格式化参数
            function formatParams(data) {
                var arr = [];
                for (var name in data) {
                    arr.push(encodeURIComponent(name) + "=" + encodeURIComponent(data[name]));
                }
                arr.push(("v=" + Math.random()).replace(".", ""));
                console.log(arr);
                return arr.join("&");
            }
复制代码
 

请求实例：

复制代码
                ajax({
                    url: "http://www.xxx.com/app/index",              //请求地址
                    type: "get",                       //请求方式
                    data: { page: "page" },        //请求参数
                    dataType: "json",
                    success: function (response, xml) {
                        // 此处放成功后执行的代码
                        console.log(JSON.parse(response))
                    },
                    error: function (status) {
                        // 此处放失败后执行的代码
                    }
                });
复制代码
 JSONP

JSONP的核心是动态添加script标签来调用服务器提供的js脚本

复制代码
    function jsonp(options) {
        options = options || {};
        if (!options.url || !options.callback) {
            throw new Error("参数不合法");
        }

        //创建 script 标签并加入到页面中
        var callbackName = ('jsonp_' + Math.random()).replace(".", "");
        var oHead = document.getElementsByTagName('head')[0];
        options.data[options.callback] = callbackName;
        var params = formatParams(options.data);
        var oS = document.createElement('script');
        oHead.appendChild(oS);

        //创建jsonp回调函数
        window[callbackName] = function (json) {
            oHead.removeChild(oS);
            clearTimeout(oS.timer);
            window[callbackName] = null;
            options.success && options.success(json);
        };

        //发送请求
        oS.src = options.url + '?' + params;

        //超时处理
        if (options.time) {
            oS.timer = setTimeout(function () {
                window[callbackName] = null;
                oHead.removeChild(oS);
                options.fail && options.fail({ message: "超时" });
            }, time);
        }
    };

    //格式化参数
    function formatParams(data) {
        var arr = [];
        for (var name in data) {
            arr.push(encodeURIComponent(name) + '=' + encodeURIComponent(data[i]));
        }
        return arr.join('&');
    }
复制代码
 ajax与jsonp本质上不是一个东西，ajax的核心是通过XMLHttpRequest对象来获取非本页的内容，而jsonp则是通过动态创建script标签来获取服务器端的js脚本。

ajax与jsonp的本质区别不在于是否跨域，ajax通过服务器端代理（浏览器请求同源服务器，再由后者请求外部服务）也一样可以实现跨域，jsonp本身也可以获取同源的数据。

 

同源策略

javascript只能访问与包含他的文档在同一页面下的内容。

即主机名、协议、端口相同。

复制代码
//下表给出了相对http://store.company.com/dir/page.html同源检测的示例:
//URL    结果    原因
http://store.company.com/dir2/other.html           成功     
http://store.company.com/dir/inner/another.html    成功     
https://store.company.com/secure.html              失败    协议不同
http://store.company.com:81/dir/etc.html           失败    端口不同
http://news.company.com/dir/other.html             失败    主机名不同
