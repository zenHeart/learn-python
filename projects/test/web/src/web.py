import utils
from selenium import webdriver

driver = webdriver.Chrome()
# 1. 访问淘宝网
driver.get("https://www.taobao.com/")

def login():
   # 查找登录按钮并点击
   elem = driver.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]');
   elem.click();

   # 输入用户名密码登录
   name_elem = driver.find_element_by_xpath('//*[@id="fm-login-id"]'); 
   password_elem = driver.find_element_by_xpath('//*[@id="fm-login-password"]'); 

   config = utils.readConfig() # 读取配置文件
   name_elem.send_keys(config['USER']['name']); # 输入用户名
   password_elem.send_keys(config['USER']['password']); # 输入密码

   # 拖动滑块 TODO: 解决无法找到元素问题
   driver.implicitly_wait(10) # 等待滑块出现
   btn_elem = driver.find_element_by_xpath('//*[@id="nc_2_n1z"]'); 
   slide_elem = driver.find_element_by_xpath('//*[@id="nc_2__scale_text"]'); 
   width = slide_elem.size['width']
   print(width)

# 商品搜索
def search_goods():
   search_input_elem = driver.find_element_by_xpath('//*[@id="q"]'); 
   search_input_elem.send_keys('test')
   search_btn_elem = driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button');
   search_btn_elem.click()
   driver.implicitly_wait(10) # 等待搜索结果页加载成功

# 下单 
def order():
   # 找到第一个商品
   current_window =  driver.current_window_handle
   good_elem = driver.find_element_by_xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[1]'); 
   good_elem.click();
   # TODO: 切换窗口
   all_windows = driver.window_handles
   for window in all_windows
      if window != current_window
         driver.switch_to_window(window)
         break;

   # 下单商品
   order_btn_elem =  driver.find_element_by_xpath('//*[@id="J_LinkBuy"]')
   order_btn_elem.click()
   driver.implicitly_wait(10) # 等待跳转到下单页面
   # 提交订单
   confirm_btn_elem = driver.find_element_by_xpath('//*[@id="submitOrderPC_1"]/div/a')
   confirm_btn_elem.click();
   driver.implicitly_wait(10) # 等待跳转到支付页

def purchase():
   # 输入密码逻辑 TODO: 添加输入支付密码逻辑
   
   # 点击支付逻辑
   purchase_btn = driver.find_element_by_xpath('//*[@id="J_authSubmit"]')
   purchase_btn.click()



# 退出 webdriver
driver.close()