import{_ as e,o as a,c as n,ae as o}from"./chunks/framework.DJK_dC0-.js";const h=JSON.parse('{"title":"L1 — Hello Python","description":"","frontmatter":{},"headers":[],"relativePath":"tutorial/begin.md","filePath":"tutorial/begin.md"}'),s={name:"tutorial/begin.md"};function d(l,t,i,p,r,u){return a(),n("div",null,[...t[0]||(t[0]=[o(`<h1 id="l1-—-hello-python" tabindex="-1">L1 — Hello Python <a class="header-anchor" href="#l1-—-hello-python" aria-label="Permalink to &quot;L1 — Hello Python&quot;">​</a></h1><blockquote><p>本节目标：掌握 print、变量、注释的用法，理解这行 TensorFlow 代码的语法结构。</p></blockquote><hr><h2 id="基础概念" tabindex="-1">基础概念 <a class="header-anchor" href="#基础概念" aria-label="Permalink to &quot;基础概念&quot;">​</a></h2><h3 id="_1-print-输出" tabindex="-1">1. print 输出 <a class="header-anchor" href="#_1-print-输出" aria-label="Permalink to &quot;1. print 输出&quot;">​</a></h3><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code>print(&quot;Hello world!&quot;)
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
</code></pre><div class="py-demo-output">Click Run to see output</div></div><hr><h2 id="🎯-理解这行-tensorflow-代码" tabindex="-1">🎯 理解这行 TensorFlow 代码 <a class="header-anchor" href="#🎯-理解这行-tensorflow-代码" aria-label="Permalink to &quot;🎯 理解这行 TensorFlow 代码&quot;">​</a></h2><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code>from tensorflow.keras.datasets import mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
</code></pre><div class="py-demo-output">Click Run to see output</div></div><p>这是<strong>元组拆包</strong>（Tuple Unpacking）。</p><h3 id="拆解步骤" tabindex="-1">拆解步骤 <a class="header-anchor" href="#拆解步骤" aria-label="Permalink to &quot;拆解步骤&quot;">​</a></h3><p><strong>Step 1</strong> — <code>mnist.load_data()</code> 返回什么？</p><p>它返回一个<strong>嵌套元组</strong>：</p><div class="language- vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang"></span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>(</span></span>
<span class="line"><span>  (train_images, train_labels),   ← 第1个元素</span></span>
<span class="line"><span>  (test_images, test_labels)       ← 第2个元素</span></span>
<span class="line"><span>)</span></span></code></pre></div><p><strong>Step 2</strong> — 外层拆包</p><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code>(train_set, test_set) = mnist.load_data()
# train_set  = (train_images, train_labels)
# test_set   = (test_images, test_labels)
</code></pre><div class="py-demo-output">Click Run to see output</div></div><p><strong>Step 3</strong> — 内层拆包</p><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code>train_images, train_labels = train_set
test_images, test_labels    = test_set
</code></pre><div class="py-demo-output">Click Run to see output</div></div><p><strong>Step 4</strong> — 合并为一行（常用写法）</p><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code>(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
</code></pre><div class="py-demo-output">Click Run to see output</div></div><hr><h2 id="等价的逐步写法" tabindex="-1">等价的逐步写法 <a class="header-anchor" href="#等价的逐步写法" aria-label="Permalink to &quot;等价的逐步写法&quot;">​</a></h2><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code># 原始返回值
result = mnist.load_data()
print(type(result))  # &lt;class &#39;tuple&#39;&gt;
print(len(result))   # 2

# 外层拆包
train_set, test_set = result

# 内层拆包
train_images, train_labels = train_set
test_images, test_labels  = test_set

print(train_images.shape)  # (60000, 28, 28)
print(train_labels.shape)  # (60000,)
</code></pre><div class="py-demo-output">Click Run to see output</div></div><hr><h2 id="对比-python-内置数据类型" tabindex="-1">对比 Python 内置数据类型 <a class="header-anchor" href="#对比-python-内置数据类型" aria-label="Permalink to &quot;对比 Python 内置数据类型&quot;">​</a></h2><table tabindex="0"><thead><tr><th>语法</th><th>类型</th><th>类比</th></tr></thead><tbody><tr><td><code>(a, b)</code></td><td>元组（不可变）</td><td>固定顺序的容器</td></tr><tr><td><code>[a, b]</code></td><td>列表（可变）</td><td>随时可变的容器</td></tr><tr><td><code>{a, b}</code></td><td>集合</td><td>无序、去重</td></tr><tr><td><code>{&#39;x&#39;: a}</code></td><td>字典</td><td>键值对</td></tr></tbody></table><p>TensorFlow 的 <code>load_data()</code> 用的是<strong>嵌套元组</strong>，左侧用<strong>嵌套拆包</strong>接收。</p><hr><h2 id="练习" tabindex="-1">练习 <a class="header-anchor" href="#练习" aria-label="Permalink to &quot;练习&quot;">​</a></h2><div class="py-demo"><div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div><pre class="language-python"><code># 1. 尝试用一个变量接住整个返回值，打印它的结构
data = mnist.load_data()
print(type(data))
print(data[0][0].shape if hasattr(data[0][0], &#39;shape&#39;) else len(data))

# 2. 用拆包语法赋值，观察每个变量的类型和 shape
# (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
</code></pre><div class="py-demo-output">Click Run to see output</div></div><blockquote><p>⚠️ 本教程使用 Pyodide（浏览器端 Python），不包含 TensorFlow。如需运行真正的 MNIST 示例，请在本地 <code>pip install tensorflow</code> 后执行。</p></blockquote><blockquote><p>⚠️ L2 数据类型 — 敬请期待</p></blockquote>`,40)])])}const b=e(s,[["render",d]]);export{h as __pageData,b as default};
