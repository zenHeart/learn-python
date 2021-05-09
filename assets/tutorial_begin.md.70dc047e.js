import{o as e,c as t,d as l}from"./app.146ab500.js";const o='{"title":"概述","description":"","frontmatter":{},"headers":[{"level":2,"title":"环境搭建","slug":"环境搭建"},{"level":2,"title":"REPL","slug":"repl"},{"level":3,"title":"快捷键","slug":"快捷键"},{"level":2,"title":"python命令","slug":"python命令"},{"level":2,"title":"源码格式","slug":"源码格式"},{"level":2,"title":"知识点","slug":"知识点"}],"relativePath":"tutorial/begin.md","lastUpdated":1620545091167}',r={},n=l('<h1 id="概述"><a class="header-anchor" href="#概述" aria-hidden="true">#</a> 概述</h1><p>本章针对初学者，用于快速搭建 python 环境，熟悉基本使用。</p><h2 id="环境搭建"><a class="header-anchor" href="#环境搭建" aria-hidden="true">#</a> 环境搭建</h2><ol><li>安装 <a href="https://code.visualstudio.com/Download" target="_blank" rel="noopener noreferrer">vscode</a></li><li>安装 <a href="https://www.python.org/downloads/release/python-395/" target="_blank" rel="noopener noreferrer">python3.9</a></li><li>阅读 <a href="https://baike.baidu.com/item/%E5%91%BD%E4%BB%A4%E8%A1%8C%E7%95%8C%E9%9D%A2/9910197?fromtitle=CLI&amp;fromid=2898851" target="_blank" rel="noopener noreferrer">命令行界面</a> ，了解基本概念。</li></ol><h2 id="repl"><a class="header-anchor" href="#repl" aria-hidden="true">#</a> REPL</h2><ol><li><p>打开控制台</p><ul><li>windows 在开始的搜索框查找 <code>cmd</code></li><li>mac 采用 <code>⌘空格键</code> ,唤起 <a href="https://support.apple.com/zh-tw/guide/mac-help/mchlp1008/mac" target="_blank" rel="noopener noreferrer">Spotlight</a>, 输入 <code>terminal</code> 打开命令行工具</li></ul></li><li><p>在控制台中输入 <code>python3.9</code>, 会唤起如下界面 (显示的版本号和时间等可能不同)</p><div class="language-"><pre><code> Python 3.9.4 (default, Apr  5 2021, 01:49:30) \n [Clang 12.0.0 (clang-1200.0.32.29)] on darwin\n Type &quot;help&quot;, &quot;copyright&quot;, &quot;credits&quot; or &quot;license&quot; for more information.\n &gt;&gt;&gt; \n</code></pre></div></li><li><p>此时可以输入 <code>1+1</code>，然后回车，会返回结果 2</p><div class="language-"><pre><code>&gt;&gt;&gt; 1+1\n2\n</code></pre></div><blockquote><p>可以将此环境作为计算器使用，尝试输入其他数学表达式，按回车，查看结果。</p></blockquote></li><li><p>执行 <code>1 + _</code> 此时会返回 <code>3</code>, <strong>_</strong> 表示上次计算的结果</p><div class="language-"><pre><code>&gt;&gt;&gt; 1+1\n2\n&gt;&gt;&gt; 1+_\n3\n</code></pre></div></li><li><p>除了作为计算器，你也可以执行代码。输入 <code>print(&#39;hello world!&#39;)</code> 回车，会输出</p><div class="language-"><pre><code>&gt;&gt;&gt; print(&#39;hello world!&#39;)\nhello world!\n</code></pre></div></li><li><p>输入 <code>quit()</code> 退出环境</p></li></ol><div class="tip custom-block"><p class="custom-block-title">TIP</p><p>该环境可以反复循环的读取输入、执行、并打印结果。这样的交互式环境叫做 <strong>REPL</strong>(read-eval-print loop), 一般利用该环境实现快速代码验证等功能。</p></div><h3 id="快捷键"><a class="header-anchor" href="#快捷键" aria-hidden="true">#</a> 快捷键</h3><table><thead><tr><th style="text-align:left;">快捷键</th><th style="text-align:left;">功能</th></tr></thead><tbody><tr><td style="text-align:left;">↑</td><td style="text-align:left;">返回上一条执行命令，没有则停止</td></tr><tr><td style="text-align:left;">↓</td><td style="text-align:left;">返回下一条执行命令，没有则停止</td></tr><tr><td style="text-align:left;">回车键</td><td style="text-align:left;">执行输入的命令</td></tr><tr><td style="text-align:left;">tab</td><td style="text-align:left;">自动补全(只针对内置的函数名和变量等有效)</td></tr><tr><td style="text-align:left;">ctrl-l</td><td style="text-align:left;">清空屏幕</td></tr><tr><td style="text-align:left;">ctrl-z</td><td style="text-align:left;">windows 退出 <strong>REPL</strong></td></tr><tr><td style="text-align:left;">ctrl-d</td><td style="text-align:left;">mac(类 Unix 系统) 退出 <strong>REPL</strong></td></tr><tr><td style="text-align:left;">ctrl-a</td><td style="text-align:left;">移动到一行的开头</td></tr><tr><td style="text-align:left;">ctrl-e</td><td style="text-align:left;">移动到一行的结尾</td></tr></tbody></table><div class="tip custom-block"><p class="custom-block-title">TIP</p><p>python REPL 中支持了 <a href="https://baike.baidu.com/item/GNU" target="_blank" rel="noopener noreferrer">GNU</a> <a href="https://tiswww.case.edu/php/chet/readline/readline.html#SEC_Contents" target="_blank" rel="noopener noreferrer">Readline</a> 单行文本编辑器的常用功能，阅读 <a href="https://tiswww.case.edu/php/chet/readline/readline.html#SEC3" target="_blank" rel="noopener noreferrer">Readline Interaction</a> 详细了解</p></div><h2 id="python命令"><a class="header-anchor" href="#python命令" aria-hidden="true">#</a> python命令</h2><p>除了使用 <code>python3.9</code> 唤起 <strong>REPL</strong> 环境，也可直接使用 <code>python3.9</code> 命令执行代码。</p><ol><li>确保已退出 <code>REPL</code> 模式</li><li>在控制台窗口输入 <code>python3.9 -c &quot;print(1+1)&quot;</code> 此时，控制台会输出 <code>2</code></li></ol><p>也可直接利用命令行执行文件</p><ol><li><p>创建 <code>print.py</code> 文件，编写如下内容</p><div class="language-py"><pre><code><span class="token keyword">print</span><span class="token punctuation">(</span> <span class="token number">1</span> <span class="token operator">+</span> <span class="token number">2</span><span class="token punctuation">)</span>\n<span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">&quot;hello world!&quot;</span><span class="token punctuation">)</span></code></pre></div></li><li><p>运行 <code>python3.9 print.py</code>，执行输出如下结果</p><div class="language-"><pre><code>3\nhello world!\n</code></pre></div></li></ol><p>python3.9 详细使用参考 <a href="https://docs.python.org/3/using/cmdline.html#using-on-general" target="_blank" rel="noopener noreferrer">python 文档</a></p><h2 id="源码格式"><a class="header-anchor" href="#源码格式" aria-hidden="true">#</a> 源码格式</h2><p>python 解释器在 2 和 3 中存在显著区别。 在 python2 中采用的是 <a href="https://baike.baidu.com/item/ASCII" target="_blank" rel="noopener noreferrer">ASCII</a> 处理的源码文件，而 ASCII 字符集并不支持中文，所以在源码中包含中文时会报错。而在 python3 中默认字符集为 <a href="https://baike.baidu.com/item/UTF-8" target="_blank" rel="noopener noreferrer">utf-8</a> 不存在上述问题。</p><p>一般可在源码开头申明 <code># -*- coding: encoding -*-</code> 内容告知 python 解释器，采用 <code>utf-8</code> 格式解析源码。具体说明详见 <a href="https://docs.python.org/3/library/codecs.html#module-codecs" target="_blank" rel="noopener noreferrer">codes</a></p><h2 id="知识点"><a class="header-anchor" href="#知识点" aria-hidden="true">#</a> 知识点</h2><ol><li><a href="#repl">REPL</a> 用于快速验证 python 代码 <ol><li>熟记 <a href="#%E5%BF%AB%E6%8D%B7%E9%94%AE">快捷键</a> 方便日常使用</li><li><code>_</code> 表示上次运算的结果</li></ol></li><li>采用 <code>python</code> 命令行执行命令 <ol><li><code>python -c &quot;print(1 + 1)&quot;</code> 执行字符串</li><li><code>python &lt;文件名&gt;</code> 执行文件</li></ol></li><li>python2 由于默认采用 <code>ASCII</code> 解析源码，python3 使用 <code>utf-8</code>，为了避免 <code>python2</code> 默认解析中文时报错，在源码开头定义 <code># -*- coding: utf_8 -*-</code> 避免解析错误。</li></ol>',21);r.render=function(l,o,r,a,d,i){return e(),t("div",null,[n])};export default r;export{o as __pageData};