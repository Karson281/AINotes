---
creation_date: 2026-06-07
source: "豆包"
tags:
  - topic/untagged
status: inbox
---

# Plugin-Sync to 豆包网页端同步Obsidian方案 - 豆包

**Date:** 2026-06-07 03:24
**Source:** 豆包

---

Plug-in Sync to 豆包网页端同步Obsidian方案
内容由豆包 AI 生成，请仔细甄别
给豆包网页端添加「Sync to Obsidian」一键同步按钮（3种方案，从简单到进阶）
 
实现原理：抓取豆包对话→转Markdown→通过Obsidian URI/本地API一键写入库，优先油猴脚本一键加按钮（最简单）。
 
方案一：油猴Tampermonkey脚本（推荐，一键在豆包页面生成按钮）
 
 
 
1.前置准备
 
Chrome/Edge/Firefox安装扩展：Tampermonkey（油猴）
 
Obsidian开启【核心插件→Obsidian URI】（必须开启，用于协议跳转新建笔记）
 
记下你的库名(Vault名称)（Obsidian左下角设置→库名称）
 
2.安装同步脚本
 
打开油猴→新建脚本，粘贴下方代码，修改两处： 你的库名 、 保存目录 
 
js
  
// ==UserScript==
// @name         豆包一键Sync to Obsidian
// @namespace    http://tampermonkey.net/
// @version      1.0
// @match        https://www.doubao.com/chat/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    const VAULT = "你的库名"; //改成自己Obsidian库名称
    const SAVE_PATH = "AI笔记/豆包"; //保存到库内文件夹，可改
    //创建按钮
    const btn = document.createElement('button');
    btn.innerText = "Sync to Obsidian";
    btn.style="margin:6px;padding:6px 12px;background:#6C5CE7;color:#fff;border:none;border-radius:6px;cursor:pointer";
    //插入到输入框旁
    document.querySelector('div[class*=input-wrap]').after(btn);

    //抓取对话内容转MD
    btn.onclick = ()=>{
        let md="# 豆包对话\n\n";
        document.querySelectorAll('div[data-testid="message_text_content"]').forEach(item=>{
            const role = item.closest('div[role]').getAttribute('role')==='user'?"### 用户":"### AI";
            md+=`${role}\n${item.innerText}\n\n---\n\n`;
        })
        //Obsidian URI新建文件
        const fileName = `豆包对话_${new Date().toLocaleDateString()}.md`;
        const uri = `obsidian://new?vault=${encodeURIComponent(VAULT)}&file=${encodeURIComponent(SAVE_PATH+"/"+fileName)}&content=${encodeURIComponent(md)}`;
        window.open(uri);
    }
})();
 
 
保存脚本，刷新豆包网页，输入框旁自动出现【Sync to Obsidian】按钮，点击直接弹出Obsidian并新建对话笔记。
 
方案二：书签按钮（不用装插件，全浏览器通用）
 
浏览器书签栏右键→新建书签
 
名称： Sync to Obsidian ，网址粘贴下面单行代码，修改库名、文件夹
```javascript:(async()=>{let v="你的库名",p="AI笔记/豆包",md="#豆包对话\n\n";document.querySelectorAll('div[data-testid="message_text_content"]').forEach(e=>{let r=e.closest('[role]').role==="user"?"### 用户":"### AI";md+=r+"\n"+e.innerText+"\n\n---\n\n"});let f= 豆包对话_${new Date().toLocaleDateString()}.md ,u= obsidian://new?vault=${encodeURIComponent(v)}&file=${encodeURIComponent(p+"/"+f)}&content=${encodeURIComponent(md)} ;window.open(u)})();
 
plaintext
  
3. 打开豆包对话，点击书签栏按钮一键同步到Obsidian。

## 方案三：本地API高级版（自动静默写入，不弹窗，需Obsidian插件）
适合想要**点击按钮自动存盘、不弹出Obsidian窗口**：
1. Obsidian安装第三方插件：**Local REST API**，开启并设置端口默认27123
2. 修改油猴脚本：把`window.open(uri)`替换为fetch请求，直接POST内容到本地Obsidian接口，实现静默同步。

## 补充：反向用法（Obsidian内嵌豆包）
如果你想在Obsidian侧边栏用豆包：
Obsidian→第三方插件→安装`Custom Frames`→Add Frame填入豆包网址`https://www.doubao.com/chat`，侧边常驻豆包，写完直接复制内容入笔记。

<data-inline type="image-group" value_id="46515712247885058_1_1701" alt="" extra="{}"></data-inline>

### 常见问题
1. 点击按钮没反应：检查Obsidian**Obsidian URI开关开启、库名拼写完全一致**
2. 文件存错位置：修改代码内`SAVE_PATH`文件夹路径
3. Obsidian打不开链接：桌面客户端需设为obsidian://协议默认打开程序。
优化完善版｜豆包网页一键同步 Obsidian（3 套可用方案 + BUG 修复 + 细节优化）
修复原代码选择器失效、日期编码、文件名非法字符、内容换行错乱问题，保留：油猴脚本｜书签｜Local REST 静默 API 三种方案，原理：抓取对话→格式化 Markdown→Obsidian URI / 本地 API 写入库
前置通用准备
Obsidian 客户端开启：设置→核心插件→Obsidian URI（启用）（方案 1/2 必开）
复制 Obsidian【库名称】（设置→关于→库名，大小写、空格必须和代码完全一致）
方案 3 额外：Obsidian 安装Local REST API插件，默认端口27123
方案一：Tampermonkey 油猴脚本（首选，页面常驻 Sync 按钮｜修复完整版）
js
运行
// ==UserScript==
// @name         豆包一键Sync to Obsidian
// @namespace    http://tampermonkey.net/
// @version      1.1
// @match        https://www.doubao.com/chat/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    // =========【必填修改项】=========
    const VAULT_NAME = "你的Obsidian库名";
    const SAVE_FOLDER = "AI笔记/豆包";
    // ==============================

    // 等待页面DOM加载完成再插入按钮
    function addSyncBtn(){
        const inputWrap = document.querySelector('div[class*="input_wrapper"],div[class*="input-wrap"]');
        if(!inputWrap || document.getElementById('sync2obsidian-btn')) return;

        // 创建按钮
        const btn = document.createElement('button');
        btn.id = "sync2obsidian-btn";
        btn.innerText = "Sync to Obsidian";
        btn.style="margin:8px 6px;padding:7px 14px;background:#6C5CE7;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px";
        inputWrap.after(btn);

        // 点击抓取对话
        btn.onclick = function(){
            let mdContent = "# 豆包AI对话记录\n\n";
            // 兼容新版豆包消息DOM
            const msgList = document.querySelectorAll('div[data-testid="message_text_content"],[data-testid="msg-content"]');
            
            msgList.forEach(item=>{
                const parentDom = item.closest('[data-role]') || item.parentElement;
                const isUser = parentDom?.classList.contains('user') || parentDom?.getAttribute('data-sender')==='user';
                const title = isUser ? "### 用户提问" : "### AI回复";
                let text = item.innerText.trim();
                mdContent += `${title}\n${text}\n\n---\n\n`;
            })

            // 规范文件名：去除/\:*?"<>|非法字符
            const now = new Date();
            const dateStr = `${now.getFullYear()}-${now.getMonth()+1}-${now.getDate()}`;
            const fileName = `豆包对话_${dateStr}.md`;
            
            // 拼接Obsidian URI
            const uri = `obsidian://new?vault=${encodeURIComponent(VAULT_NAME)}&file=${encodeURIComponent(`${SAVE_FOLDER}/${fileName}`)}&content=${encodeURIComponent(mdContent)}`;
            window.open(uri);
        }
    }

    // 监听页面动态渲染（豆包SPA页面动态加载）
    const observer = new MutationObserver(()=>addSyncBtn());
    observer.observe(document.body,{childList:true,subtree:true});
    addSyncBtn();
})();

使用步骤
浏览器安装油猴扩展→新建脚本→全量粘贴代码
修改VAULT_NAME（库名）、SAVE_FOLDER（库内保存目录）
Ctrl+S 保存，刷新豆包网页，输入框下方自动出现同步按钮
方案二：浏览器书签（无插件全浏览器通用｜单行压缩可用代码）
书签栏右键→添加书签
名称：Sync to Obsidian
网址填入下方代码，修改前两处引号内库名、保存路径
```javascript:(()=>{let v=" 你的库名 ",p="AI 笔记 / 豆包 ",md="# 豆包 AI 对话记录 \n\n",m=document.querySelectorAll ('div [data-testid="message_text_content"],[data-testid="msg-content"]');for (let i of m){let o=i.closest ('[data-role]'),u=o?.classList.contains ('user')||o?.dataset.sender==="user",t=u?"### 用户提问 ":"### AI 回复 ",c=i.innerText.trim ();md+=t+"\n"+c+"\n\n---\n\n"};let d=new Date (),fn=豆包对话_${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}.md,u=obsidian://new?vault=${encodeURIComponent(v)}&file=${encodeURIComponent(p+"/"+fn)}&content=${encodeURIComponent(md)};window.open(u)})();
plaintext
2. 打开豆包对话页，点击书签一键唤起Obsidian新建笔记

## 方案三：高级静默同步｜Local REST API（不弹窗、后台自动写入文件）
> 需求：Obsidian安装`Local REST API`插件，开启，默认地址：`http://127.0.0.1:27123`
把**方案一油猴脚本内原有window.open(uri);整行替换**为下面代码：
```js
// 静默POST写入本地Obsidian，无弹窗
const now = new Date();
const dateStr = `${now.getFullYear()}-${now.getMonth()+1}-${now.getDate()}`;
const fileName = `${SAVE_FOLDER}/${`豆包对话_${dateStr}.md`}`;
fetch(`http://127.0.0.1:27123/vault/${encodeURIComponent(VAULT_NAME)}/file/${encodeURIComponent(fileName)}`,{
    method:"PUT",
    headers:{"Content-Type":"text/markdown"},
    body:mdContent
}).then(res=>{
    if(res.ok) alert("同步成功！已存入Obsidian");
    else alert("同步失败，检查Local REST API插件开启+端口");
}).catch(e=>alert("链接失败：确认Obsidian客户端和插件已打开"));

拓展：Obsidian 内嵌豆包侧边栏
Obsidian 第三方插件安装Custom Frames
设置→Custom Frames→Add new frame
Name：豆包网页端
URL：https://www.doubao.com/chat
保存后左侧侧边常驻豆包，边提问边整理笔记。
高频报错排查
点击按钮无反应
检查 ObsidianObsidian URI 开启、库名大小写 / 空格完全一致
桌面端：系统默认用 Obsidian 打开obsidian://协议链接
不生成文件
保存路径文件夹不存在：先在 Obsidian 手动创建AI笔记/豆包目录
API 静默同步失败
Obsidian 必须保持打开、Local REST 插件启用、端口默认 27123 未被占用
需要我帮你根据你的Obsidian 库名和自定义保存文件夹，直接生成改好成品代码吗？
已生成代码
一、第一步：先安装「油猴Tampermonkey浏览器插件」（Edge/Chrome通用）
 
Edge浏览器
 
右上角「…菜单→扩展→管理扩展→Microsoft Edge加载项」
 
搜索：Tampermonkey（作者：Jan Biniok，官方黑猴子图标）→点获取→添加扩展
 
装好后浏览器右上角出现黑色小猴图标=安装成功
 
Chrome浏览器
 
打开Chrome网上应用店，搜Tampermonkey→添加至Chrome。
 
打不开商店：官网 tampermonkey.net 下载离线包安装。
 
二、第二步：安装【豆包Sync to Obsidian脚本】（你要用的脚本）
 
点右上角小猴图标 → 仪表盘(Dashboard) → + 添加新脚本
 
全选删除编辑器里自带所有默认代码（Ctrl+A→Delete清空）
 
完整粘贴下面代码，修改两处：库名、保存文件夹
 
js
  
// ==UserScript==
// @name         豆包一键Sync to Obsidian
// @namespace    http://tampermonkey.net/
// @version      1.0
// @match        https://www.doub
