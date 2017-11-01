from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()
bookstore_url = "http://carleton.bncollege.com/webapp/wcs/stores/servlet/TBWizardView?catalogId=10001&langId=-1&storeId=87738"

def get_classes():
  def get_dropdown_values(inputs):
    if len(inputs) == 0:
      return []
    time.sleep(1)
    inputs[0].click()
    dropdown_data = {}
    for i in range(len(inputs[0].parent.find_elements_by_class_name('result'))):
      inputs[0].clear()
      inputs[0].click()
      res = inputs[0].parent.find_elements_by_class_name('result')[i]
      res_text = res.text.strip()
      if len(res_text) > 0:
        res.click()
        dropdown_data[res_text] = get_dropdown_values(inputs[1:])

    return dropdown_data

  browser.get(bookstore_url)
  while len(browser.find_elements_by_class_name('bookRowContainer')) == 0:
    time.sleep(1)

  inputs = browser.find_element_by_class_name('bookRowContainer').find_elements_by_class_name('bncbTextInput')
  return get_dropdown_values(inputs)
