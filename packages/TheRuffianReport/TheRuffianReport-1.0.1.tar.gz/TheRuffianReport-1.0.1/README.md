#Introduction
```shell
    Based on TheRuffianReport development,
     new assertion failure screenshot,
      screenshot display and DingTalk function
```    

#Installing
    pip install TheRuffianReport
    python≥3.0

#Author
    bugpz2779@gmail.com

#Function Introduction

```python
 # screenshot
import unittest
from selenium import webdriver

from TheRuffianReport.HTMLTestRunner import failure_monitor


class Test_demo(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome()
        self.failureException = failure_monitor(self, 'images')
        self.driver.get('https://www.baidu.com')

    def test_baidu(self):
        self.driver.find_element('id', 'kw').send_keys('python')
        self.driver.find_element('id', 'su').click()
        self.assertEqual(self.driver.find_element('id', 'kw').get_attribute('value'), 'selenium')
```