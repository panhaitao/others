跨域解决方案大全
什么是跨域
注：本文完整示例地址 
先来说一个概念就是同源，同源指的是协议，端口，域名全部相同。

同源策略（Same origin policy）是一种约定，它是浏览器最核心也最基本的安全功能，如果缺少了同源策略，则浏览器的正常功能可能都会受到影响。可以说Web是构建在同源策略基础之上的，浏览器只是针对同源策略的一种实现。

同源策略是处于对用户安全的考虑，如果非同源就会受到以下限制：

cookie不能读取
dom无法获得
ajax请求不能发送
但是事实是经常需要借助非同源来提供数据，所以就需要进行跨域请求。

JSONP
JSONP是指JSON Padding，JSONP是一种非官方跨域数据交换协议，由于script的src属性可以跨域请求，所以JSONP利用的就是浏览器的这个“漏洞”，需要通信时，动态的插入一个script标签。请求的地址一般带有一个callback参数，假设需要请求的地址为http://localhost:666?callback=show，服务端返回的代码一般是show(数据)的JSON数据，而show函数恰恰是前台需要用这个数据的函数。JSONP非常的简单易用，自动补全API利用的就是JSONP，下面来看一个例子：

// 前端请求代码
function jsonp (callback) {
    var script = document.createElement("script"),
        url = `http://localhost:666?callback=${callback}`;
    script.setAttribute("src", url);
    document.querySelector("head").appendChild(script);
}
function show (data) {
    console.log(`学生姓名为：${data.name}，年龄为：${data.age}，性别为${data.sex}`);
}
jsonp("show");
// 后端响应代码
const student = {
    name: "zp1996",
    age: 20,
    sex: "male"
};
var callback = url.parse(req.url, true).query.callback;
res.writeHead(200, {
    "Content-Type": "application/json;charset=utf-8"
});
res.end(`${callback}(${JSON.stringify(student)})`);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
JSONP虽说简单易用，但是有一个很大问题，那就是JSONP只能进行get请求

CORS
CORS(跨域资源共享)是由W3C制定的跨站资源分享标准，可以让AJAX实现跨域访问。想要了解跨域的话，首先需要了解下简单请求：

请求方式为GET或者POST
假若请求是POST的话，Content-Type必须为下列之一： 
application/x-www-form-urlencoded
multipart/form-data
text/plain
不含有自定义头（类似于segmentfault自定义的头X-Hit）
对于简单请求的跨域只需要进行一次http请求：

function ajaxPost (url, obj, header) {
    return new Promise((resolve, reject) => {
        var xhr = new XMLHttpRequest(),
        str = '',
        keys = Object.keys(obj);
      for (var i = 0, len = keys.length; i < len; i++) {
        str += `${keys[i]}=${obj[keys[i]]}&`;
      }
      str = str.substring(0, str.length - 1);
      xhr.open('post', url);
      xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
      if (header instanceof Object) {
        for (var k in header) 
            xhr.setRequestHeader(k, header[k]);
      }
      xhr.send(str);
      xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
          if (xhr.status >= 200 && xhr.status < 300 || xhr.status == 304) {
            resolve(xhr.responseText);
          } else {
            reject();
          }
        }
      }
    });
}
ajaxPost("http://localhost:666?page=cors", {
    name: "zp1996",
    age: 20,
    sex: "male"
})
.then((text) => { console.log(text); }, 
            () => { console.log("请求失败"); });

// 后端处理
var postData = "";
// 注释下，下面示例后台代码补充在此处
req.on("data", (data) => {
    postData += data;
});
req.on("end", () => {
    postData = querystring.parse(postData);
    res.writeHead(200, {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json;charset=utf-8"
    });
    if (postData.name === student.name &&
        Number(postData.age) === student.age &&
        postData.sex === student.sex
         ) {
        res.end(`yeah！${postData.name} is a good boy~`);
    } else {
        res.end("No！a bad boy~");
    }
});
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
打开控制台观察可以发现，Network只是发出了一次请求，但是对于非简单请求来说，需要两次http请求，在真正的请求之前需要进行一次预请求，下图是进行一次预请求的请求/响应：

clipboard.png

观察响应头，可以发现需要多出了两个响应头： 
- Access-Control-Allow-Headers，用来指明在实际的请求中，可以使用那些自定义的http请求头。 
- Access-Control-Max-Age，用来指定此次预请求的结果的有效期，在有效期内则不会发出预请求，有点像缓存的感觉。

当然还有诸如好多这样的响应头，请大家自行搜索了解，这里就不再过多介绍，下面来看下对于非简单请求跨域的代码处理：

// 前端请求代码
ajaxPost("http://localhost:666?page=cors", {
    name: "zp1996",
    age: 20,
    sex: "male"
}, { "X-author": "zp1996" })
.then((text) => { console.log(text); }, 
            () => { console.log("请求失败"); });

// 后端处理，补充在简单请求代码注释处
if (req.method === "OPTIONS") {
    res.writeHead(200, {
        "Access-Control-Max-Age": 3000,
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "X-author",
        "Content-Type": "application/json;charset=utf-8"
    }); 
    res.end();
    return void 0;      
} 
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
CSS Text Transformation
既然可以利用script的“漏洞”来进行JSONP跨域，那么是不是也可以利用css样式写可以进行跨域请求来进行跨域呢？答案肯定是yes，利用css还有一个好处那就是，当被注入攻击脚本时，css尽管被注入，也不会引起什么大的安全问题，顶多也就是把页面的样式给改变，而js被注入的话，cookie就有可能被盗取等一系列安全问题出现。大牛已经将其做的非常完善，大家可以去star王集鹄（zswang）CSST，这里我就把我所理解给大家简单的分享下：

// 前端代码
const id = "csst",
    ele = document.querySelector(`#${id}`),
    head = document.querySelector("head");
function getStyle (ele, prop) {
    return getComputedStyle(ele, "").getPropertyValue(prop);
}
function loadCss (url) {
    return new Promise((resolve) => {
        const link = document.createElement("link");
         link.setAttribute("rel", "stylesheet");
        link.setAttribute("type", "text/css");
        link.setAttribute("href", url);
        ele.addEventListener("webkitAnimationStart", function () {
            resolve(getStyle(ele, "content"));
        });
        head.appendChild(link);
    });
}
loadCss(`http://localhost:666?page=data.css&id=${id}`).then((data) => {
    console.log(data);
});

// 后端代码
function cssData (id) {
    return `
        @keyframes a{
            from{

            }
            to{
                color: red;
            }
        }
        #${id} {
            content: "这种是很好，但是只能传输文本啊";
            animation: a 2s;
        }
    `;
}
res.writeHead(200, {
    "Content-Type": "text/css"
});
res.end(cssData(query.id));
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
通过代码可以看出这种实现方式是靠元素的content来拿接收到的数据，所以传输的只能是文本。至于为什么要返回动画？是因为不利用动画，无法来对css脚本加载进行监测，也就无法进行回调（由于谷歌/火狐不支持link的onload和onreadychange，所以利用animationstart事件）。

window.postMessage
window.postMessage 是一个安全的跨源通信的方法。一般情况下，当且仅当执行脚本的页面使用相同的协议（通常都是 http）、相同的端口（http默认使用80端口）和相同的 host（两个页面的 document.domain 的值相同）时，才允许不同页面上的脚本互相访问。 window.postMessage 提供了一个可控的机制来安全地绕过这一限制，当其在正确使用的情况下。 
window.postMessage解决的不是浏览器与服务器之间的交互，解决的是浏览器不同的窗口之间的通信问题，可以做的就是同步两个网页，当然这两个网页应该是属于同一个基础域名。

// 发送端代码
var domain = "http://localhost",
    index = 1,
    target = window.open(`${domain}/postmessage-target.html`);
function send () {
    setInterval(() => {
        target.postMessage(`第${index++}次数据发送`, domain);
    }, 1000);
}
send();
// 接受端代码
<div id="test">没有数据过来啊<div>
<script type="text/javascript">
    var test = document.querySelector("#test");
    window.addEventListener("message", e => {
        if (e.origin !== "http://localhost") {
            return void 0;
        }
        test.innerText = e.data;
    });
</script>
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
上述代码实现了向一个页面向另一个发送数据，但是这么写往往有着一些“危险”，需要知道的是，postMessage是向document对象中，网络连接有时会很慢，可能会出现些问题，所以最好的方式是接受页面已经开始加载了，这时发送一个消息给发送端，发送端在开始向接收端发送数据。改进下：

// 发送端添加代码
window.addEventListener("message", (e) => {
    if (e.data === "ok")
        send();
    else 
        console.log(e.data);
});

// 接受端的head里面加上script标签
<script type="text/javascript">
    opener.postMessage("ok", opener.domain);
</script>
1
2
3
4
5
6
7
8
9
10
11
12
window.name
window.name 的美妙之处：name 值在不同的页面（甚至不同域名）加载后依旧存在，并且可以支持非常长的 name 值（2MB）

这个方式我基本上没有用过，所以没有过多的发言权，大家想了解这个技术的话，可以通过怿飞（圆心）：使用 window.name 解决跨域问题，圆心大神解释的非常透彻。

document.domain
将子域和主域的document.domain设为同一个主域 
前提条件：

这两个域名必须属于同一个基础域名
而且所用的协议，端口都要一致，否则无法利用document.domain进行跨域


