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
    for i in range(len(inputs[0].find_element_by_xpath('..').find_elements_by_class_name('result'))):
      inputs[0].clear()
      inputs[0].click()
      res = inputs[0].find_element_by_xpath('..').find_elements_by_class_name('result')[i]
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

def get_books_for_class(lookup_path):
  browser.get(bookstore_url)
  while len(browser.find_elements_by_class_name('bookRowContainer')) == 0:
    time.sleep(1)
  inputs = browser.find_element_by_class_name('bookRowContainer').find_elements_by_class_name('bncbTextInput')
  for i in range(len(lookup_path)):
    inputs[i].click()
    for res in inputs[i].find_element_by_xpath('..').find_elements_by_class_name('result'):
      if res.text.strip() == lookup_path[i]:
        res.click()
        break
    time.sleep(0.5)

  browser.find_element_by_id('findMaterialButton').click()
  while len(browser.find_elements_by_class_name('courseOverView_panel')) == 0:
    time.sleep(1)

  books = []
  for book_el in browser.find_elements_by_class_name('book-list'):
    book_data = {}
    book_data["title"] = book_el.find_element_by_css_selector('h1 a').text
    book_data["author"] = book_el.find_element_by_css_selector('h2 i').text
    book_data["edition"] = ""
    book_data["isbn"] = ""
    for strong in book_el.find_elements_by_css_selector('strong'):
      if "isbn" in strong.text.lower():
        book_data["isbn"] = strong.find_element_by_xpath('..').text
      elif "edition" in strong.text.lower():
        book_data["edition"] = strong.find_element_by_xpath('..').text
    books.append(book_data)
  return books

print(get_books_for_class(['AFST', '112', '0']))
