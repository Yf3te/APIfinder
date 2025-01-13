# APIfinder
**APIfinder**主要用于在网站js文件中寻找API路径，这个需要把站点的js代码拷贝到同一级目录下的**API文件夹**下

  只是一个半成品
匹配路径的方式有：
1. 简单的路径提取："/api"、'/api'、"api/de"、
2. 针对< base_url+ "api/v2" >，全局检索base_url，再进行简单拼接。
3. 
  分别由三个单独py组成

-**单文件.py**   //用于在当文件下发现API路径

-**文件夹.py**     //在API文件夹中的文件寻找路径

-**文件夹(带文件名).py**     //也是在文件夹中寻找，在后面附得有路径所在文件

# 批量js获取方法
关于怎么获取站点全部的js文件，一个一个下？太麻烦了
### 1、使用爬虫，获取：
不过有时候会下载不全
### 3.使用packer-Fuzzer
但是还有存在下载不全的问题，所以更推荐下面这种方法
### 2、直接在浏览器中
#### 直接使用浏览器的控制台，通过脚本获取，使用下面就行了

注意：有时候火狐浏览器下载不了，可以使用微软官方浏览器和google下载
```
(async () => {
    // 获取静态加载的 JS 文件
    const scripts = Array.from(document.querySelectorAll('script'));
    const staticJSFiles = scripts
        .map(script => script.src) // 获取 src 属性
        .filter(src => src); // 过滤没有 src 的内联脚本

    // 获取动态加载的 JS 文件
    const dynamicJSFiles = performance.getEntriesByType('resource')
        .filter(entry => entry.initiatorType === 'script') // 过滤脚本文件
        .map(entry => entry.name); // 获取脚本文件 URL

    // 合并并去重
    const allJSFiles = Array.from(new Set([...staticJSFiles, ...dynamicJSFiles]));

    console.log(`共找到 ${allJSFiles.length} 个 JS 文件:`, allJSFiles);

    // 下载函数
    const downloadFile = async (url, filename) => {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                console.warn(`无法下载文件: ${url}`);
                return;
            }
            const blob = await response.blob();
            const a = document.createElement('a');
            const objectURL = URL.createObjectURL(blob);
            a.href = objectURL;
            a.download = filename;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(objectURL);
        } catch (err) {
            console.error(`下载文件 ${url} 失败:`, err);
        }
    };

    // 下载所有文件
    for (const file of allJSFiles) {
        const filename = file.split('/').pop() || 'unknown.js';
        await downloadFile(file, filename);
    }

    console.log('所有 JS 文件下载完成！');
})();

```
下载方式如下：
![image](https://github.com/user-attachments/assets/55bc2acc-ebc7-474b-a759-ff54fc3626e4)
这不就手到擒来

![image](https://github.com/user-attachments/assets/bcbcd728-2dfd-4ed8-88bf-e1555f8fd062)
不过最好在不经常用的浏览器下载，主要是我的浏览器肯定是用了不少插件的
![image](https://github.com/user-attachments/assets/5721b0bd-6f64-4066-9586-b9584c50b47f)
这会导致下载一些不属于网站的js
