import requests
import json
from jsonschema import validate

# schema = {
#     "type" : "object",
#     "properties" : {
#         "hasError" : {"type" : "boolean"},
#         "content": {
#             "type": "object",
#             "properties": {
#                "data" : {
#                   "type": "object",
#                   "properties": {
#                      "redirect": {
#                         "type": "boolean"
#                      },
#                      "redirectUrl": {
#                         "type": "string"
#                      },
#                      "resultCode": {
#                         "type": "number"
#                      } 
#                   }
#                },
#                 "status": { "type": "number" },
#                 "success": { "type": "string" },
#             },
#             "required": ["status", "data", "success", "a"]
#         }
#     },
#     "required": ["hasError"]
# }
schema = {
   "type": "object",
   "properties": {
      "url": {
         "type": "string"
      }
   },
   "required": ["url"]
}

LOGIN_URL = 'https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0&_bx-v=2.0.31'
def test_login_success():
   respones = requests.post(LOGIN_URL)
   assert respones.status_code == 200

   # 校验返回类型为 json
   assert respones.headers["Content-Type"] == "application/json;charset=UTF-8"

   # 获取返回结果
   resp_body = respones.json()

   # 校验结果和 schema 关系
   print(resp_body)
   validate(instance=resp_body, schema=schema)
   