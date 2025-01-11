# APIfinder
APIfinder主要用于在网站js文件中寻找API路径，这个需要把站点的js代码拷贝到同一级目录下的**API文件夹**下

  只是一个半成品

  分别由三个单独py组成

-单文件.py   //用于在当文件下发现API路径

-文件夹.py     //在API文件夹中的文件寻找路径

-文件夹(带文件名).py     //也是在文件夹中寻找，在后面附得有路径所在文件

#批量js获取方法
关于怎么获取站点全部的js文件，一个一个下？太麻烦了
###1、使用爬虫，获取：
不过有时候会下载不全
###3.使用packer-Fuzzer
但是还有存在下载不全的问题，所以更推荐下面这种方法
###2、直接在浏览器中
####直接使用浏览器的控制台，通过脚本获取，使用下面就行了
'''
(async () => {
    // 初始化存储所有 JS 文件的链接
    const jsFiles = new Set();

    // 方法 1: 提取页面上静态 script[src] 标签的链接
    document.querySelectorAll('script[src]').forEach(script => {
        if (script.src) jsFiles.add(script.src);
    });

    // 方法 2: 提取页面加载的所有资源
    performance.getEntriesByType('resource').forEach(entry => {
        if (entry.initiatorType === 'script' && entry.name.endsWith('.js')) {
            jsFiles.add(entry.name);
        }
    });

    // 打印结果 (调试用)
    console.log([...jsFiles]);

    // 方法 3: 自动下载所有文件
    for (const url of jsFiles) {
        await downloadFile(url);
    }

    // 下载函数
    async function downloadFile(url) {
        const a = document.createElement('a');
        a.href = url;
        a.download = url.split('/').pop(); // 使用文件名作为下载名称
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        await new Promise(resolve => setTimeout(resolve, 100)); // 防止请求过多导致的阻塞
    }
})();
'''
下载方式如下：
![image](https://github.com/user-attachments/assets/55bc2acc-ebc7-474b-a759-ff54fc3626e4)
这不就手到擒来
![image](https://github.com/user-attachments/assets/bcbcd728-2dfd-4ed8-88bf-e1555f8fd062)

不过最好在不经常用的浏览器下载，主要是我的浏览器肯定是用了不少插件的
![image](https://github.com/user-attachments/assets/5721b0bd-6f64-4066-9586-b9584c50b47f)
这会导致下载一些不属于网站的js
'''
