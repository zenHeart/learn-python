# API 接口测试

## 准备工作

1. 安装依赖包
   
   ```bash
   # 安装依赖包
   # requests 用于发起请求
   # pytest 单元测试框架
   # pytest-html html 输出测试结果
   # jsonschema json 校验模块
   # pytest-watch 检测文件变化自动运行
   pip install requests pytest pytest-html jsonschema pytest-watch
   ```

2. 运行测试用例
   
   ```bash
   ptw
   ```
3. 生成 html 报告
   
   ```bash
   # 将报告输出到 report 文件夹
   pytest --html=report/index.html 
   ```

   详细参考 [pytest](https://pytest-html.readthedocs.io/en/latest/user_guide.html)