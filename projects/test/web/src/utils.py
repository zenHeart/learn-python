import yaml
import os

FILE_PATH=os.path.abspath(os.path.dirname(os.path.abspath(__file__))+"/_conf.yml")

def readConfig():
   # filePath = os.path.dirname(os.path.abspath(__file__))
   with open(FILE_PATH, 'r') as stream:
      try:
         return yaml.safe_load(stream)
      except yaml.YAMLError as exc:
         print(exc)
