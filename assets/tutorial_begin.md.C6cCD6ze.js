import{_ as a,o as e,c as o,ae as d}from"./chunks/framework.DJK_dC0-.js";const h=JSON.parse('{"title":"L1 — Hello Python","description":"","frontmatter":{},"headers":[],"relativePath":"tutorial/begin.md","filePath":"tutorial/begin.md"}'),n={name:"tutorial/begin.md"};function s(i,t,l,r,p,u){return e(),o("div",null,[...t[0]||(t[0]=[d(`<h1 id="l1-—-hello-python" tabindex="-1">L1 — Hello Python <a class="header-anchor" href="#l1-—-hello-python" aria-label="Permalink to &quot;L1 — Hello Python&quot;">​</a></h1><blockquote><p>本节目标：掌握 print、变量、注释、模块导入，理解嵌套拆包语法。</p></blockquote><hr><h2 id="基础概念" tabindex="-1">基础概念 <a class="header-anchor" href="#基础概念" aria-label="Permalink to &quot;基础概念&quot;">​</a></h2><h3 id="_1-print-输出" tabindex="-1">1. print 输出 <a class="header-anchor" href="#_1-print-输出" aria-label="Permalink to &quot;1. print 输出&quot;">​</a></h3><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code>print(&quot;Hello world!&quot;)
print(1 + 2)
</code></pre><div class="py-demo-output">Click Run to see output</div></div><p><strong>运行结果：</strong></p><ul><li><code>Hello world!</code></li><li><code>3</code></li></ul><hr><h3 id="_2-变量赋值" tabindex="-1">2. 变量赋值 <a class="header-anchor" href="#_2-变量赋值" aria-label="Permalink to &quot;2. 变量赋值&quot;">​</a></h3><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code>name = &quot;Python&quot;
age = 18
is_student = True
print(f&quot;我叫{name}，今年{age}岁&quot;)
</code></pre><div class="py-demo-output">Click Run to see output</div></div><hr><h3 id="_3-注释" tabindex="-1">3. 注释 <a class="header-anchor" href="#_3-注释" aria-label="Permalink to &quot;3. 注释&quot;">​</a></h3><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code># 这是单行注释
&quot;&quot;&quot;
这是多行注释，
通常用于文档字符串
&quot;&quot;&quot;
</code></pre><div class="py-demo-output">Click Run to see output</div></div><hr><h2 id="🎯-理解嵌套拆包-从-mnist-数据加载说起" tabindex="-1">🎯 理解嵌套拆包：从 MNIST 数据加载说起 <a class="header-anchor" href="#🎯-理解嵌套拆包-从-mnist-数据加载说起" aria-label="Permalink to &quot;🎯 理解嵌套拆包：从 MNIST 数据加载说起&quot;">​</a></h2><h3 id="目标代码" tabindex="-1">目标代码 <a class="header-anchor" href="#目标代码" aria-label="Permalink to &quot;目标代码&quot;">​</a></h3><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code>from mnist.data import load_data
(train_images, train_labels), (test_images, test_labels) = load_data()
</code></pre><div class="py-demo-output">Click Run to see output</div></div><h3 id="多文件模块结构" tabindex="-1">多文件模块结构 <a class="header-anchor" href="#多文件模块结构" aria-label="Permalink to &quot;多文件模块结构&quot;">​</a></h3><div class="language- vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang"></span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>examples/</span></span>
<span class="line"><span>└── mnist/</span></span>
<span class="line"><span>    ├── __init__.py       # 包入口（可省略）</span></span>
<span class="line"><span>    ├── data.py           # 定义 load_data()</span></span>
<span class="line"><span>    └── main.py           # 导入并使用</span></span></code></pre></div><p><strong>data.py</strong> — 定义数据加载函数：</p><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code>def load_data():
    return (训练集图片, 训练集标签), (测试集图片, 测试集标签)
</code></pre><div class="py-demo-output">Click Run to see output</div></div><p><strong>main.py</strong> — 导入并拆包：</p><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code>from mnist.data import load_data
(train_images, train_labels), (test_images, test_labels) = load_data()
</code></pre><div class="py-demo-output">Click Run to see output</div></div><hr><h3 id="嵌套拆包语法拆解" tabindex="-1">嵌套拆包语法拆解 <a class="header-anchor" href="#嵌套拆包语法拆解" aria-label="Permalink to &quot;嵌套拆包语法拆解&quot;">​</a></h3><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code># load_data() 返回的是嵌套元组：
((train_images, train_labels), (test_images, test_labels))

# 左侧有两层括号 → 对应两层拆包
(train_images, train_labels), (test_images, test_labels) = ...
          ↑ 第一层                    ↑ 第一层
            ↑ 第二层                      ↑ 第二层
</code></pre><div class="py-demo-output">Click Run to see output</div></div><h3 id="等价的逐步写法" tabindex="-1">等价的逐步写法 <a class="header-anchor" href="#等价的逐步写法" aria-label="Permalink to &quot;等价的逐步写法&quot;">​</a></h3><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code># 原始返回值
result = load_data()
# result = ((train_images, train_labels), (test_images, test_labels))

# 外层拆包：分出训练集和测试集
train_set, test_set = result

# 内层拆包：分出图片和标签
train_images, train_labels = train_set
test_images, test_labels = test_set
</code></pre><div class="py-demo-output">Click Run to see output</div></div><hr><h2 id="python-模块导入语法" tabindex="-1">Python 模块导入语法 <a class="header-anchor" href="#python-模块导入语法" aria-label="Permalink to &quot;Python 模块导入语法&quot;">​</a></h2><table tabindex="0"><thead><tr><th>场景</th><th>语法</th><th>示例</th></tr></thead><tbody><tr><td>导入模块</td><td><code>import 模块名</code></td><td><code>import mnist</code></td></tr><tr><td>从模块导入函数</td><td><code>from 模块 import 函数</code></td><td><code>from mnist.data import load_data</code></td></tr><tr><td>导入并改名</td><td><code>from 模块 import 函数 as 别名</code></td><td><code>from mnist.data import load_data as ld</code></td></tr><tr><td>导入多个</td><td><code>from 模块 import a, b</code></td><td><code>from mnist.data import a, b</code></td></tr><tr><td>相对导入（包内）</td><td><code>from . import sibling</code></td><td><code>from . import data</code></td></tr></tbody></table><hr><h2 id="对比-python-内置数据类型" tabindex="-1">对比 Python 内置数据类型 <a class="header-anchor" href="#对比-python-内置数据类型" aria-label="Permalink to &quot;对比 Python 内置数据类型&quot;">​</a></h2><table tabindex="0"><thead><tr><th>语法</th><th>类型</th><th>类比</th></tr></thead><tbody><tr><td><code>(a, b)</code></td><td>元组（不可变）</td><td>固定顺序的容器</td></tr><tr><td><code>[a, b]</code></td><td>列表（可变）</td><td>随时可变的容器</td></tr><tr><td><code>{a, b}</code></td><td>集合</td><td>无序、去重</td></tr><tr><td><code>{&#39;x&#39;: a}</code></td><td>字典</td><td>键值对</td></tr></tbody></table><hr><h2 id="练习" tabindex="-1">练习 <a class="header-anchor" href="#练习" aria-label="Permalink to &quot;练习&quot;">​</a></h2><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code># 1. 尝试用一个变量接住整个返回值，打印它的结构
data = load_data()
print(&quot;整体结构:&quot;, type(data))
print(&quot;第1个元素（训练集）:&quot;, data[0])
print(&quot;第2个元素（测试集）:&quot;, data[1])

# 2. 用拆包语法赋值
# (train_images, train_labels), (test_images, test_labels) = load_data()
</code></pre><div class="py-demo-output">Click Run to see output</div></div><hr><blockquote><p>⚠️ 本教程使用 Pyodide（浏览器端 Python），不支持 <code>tensorflow</code>、<code>numpy</code> 等 C 扩展库。MNIST 示例使用纯 Python 模拟返回值结构。</p></blockquote><hr><blockquote><p>⚠️ L2 数据类型 — 敬请期待</p></blockquote>`,42)])])}const m=a(n,[["render",s]]);export{h as __pageData,m as default};
