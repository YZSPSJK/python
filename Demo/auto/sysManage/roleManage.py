import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--window-size=1920,1080")
        s = Service('/Users/sjk/workspace/sjk/python/chromedriver')
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
        self.driver.get('http://175.27.232.12:8143/skyrim/#/home')
        self.driver.add_cookie(
            {'domain': '175.27.232.12', 'httpOnly': False, 'name': 'skyrim_admin_token', 'path': '/', 'secure': False,
             'value': 'Bearer%20eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiMTAwMyJdLCJ1c2VyX25hbWUiOiJ1c2VyMSIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSJdLCJleHAiOjE2NTg5MDM3NTcsImF1dGhvcml0aWVzIjpbIlJPTEVfQURNSU4iXSwianRpIjoiMjFhMjU3ZWMtNjk3ZC00OTdiLTg2MDEtYmZjNDhmYjI3ZjhhIiwiY2xpZW50X2lkIjoibWVzc2FnaW5nLWNsaWVudCJ9.UHtKM_9lG3b1xNoGkjicVM4kJDMdQxxU-2z4-Le0scKtSTfLLK4byV2xvCmaD7Legmd1f9XqgPK9eoOHL798MR0Gv3gwZFDWLRakiOfha2CfDh0HJQTJr5EvxB7NNkFYgf9tiuV2vtI-0vVGNmMyo5oOG1wIHYVptEPuj402-nPCz0gM_VFW4v5Pcn1jKu8JQEREYcQpn8UnBzGCopa7Iap1fykRMkItYlawa21E6PuGYGDS_YMAd5pczpif6L3kk0RTUpddqxJUY9gF9cmz3I7p5SKavZvLceXKyWqcoeuNt7GmD1CiZ-UVXf8tTenReweOiA8GK6D17KrEib0Lyg'})
        self.driver.refresh()
        time.sleep(1)

    def test_role_manage(self):
        try:
            self.driver.find_element(By.XPATH, '//span[text()="系统管理"]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//span[text()="角色管理"]').click()
            self.driver.find_elements()
            time.sleep(1)

            el_form_contents = self.driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')
            roleId = el_form_contents[0].find_element(By.CLASS_NAME, 'el-input__inner')
            roleName = el_form_contents[1].find_element(By.CLASS_NAME, 'el-input__inner')

            roleId.clear()
            roleId.send_keys('test')
            self.driver.find_element(By.XPATH, '//span[text()="查询"]').click()
            time.sleep(2)
            el_rows = self.driver.find_elements(By.XPATH, '//tr[@class="el-table__row"]')
            for row in el_rows:
                cols = row.find_elements(By.TAG_NAME, 'span')
                self.assertIn('test', cols[0].text, '根据角色标识查询正确')

            roleId.clear()
            roleName.clear()
            roleName.send_keys('test')
            self.driver.find_element(By.XPATH, '//span[text()="查询"]').click()
            time.sleep(2)
            el_rows = self.driver.find_elements(By.XPATH, '//tr[@class="el-table__row"]')
            for row in el_rows:
                cols = row.find_elements(By.TAG_NAME, 'span')
                self.assertIn('test', cols[3].text, '根据角色名称查询正确')

            roleId.clear()
            roleName.clear()
            roleId.send_keys('test')
            roleName.send_keys('test')
            self.driver.find_element(By.XPATH, '//span[text()="重置"]').click()
            self.assertEqual(roleId.get_attribute('value'), '', '重置功能正确')
            self.assertEqual(roleName.get_attribute('value'), '', '重置功能正确')

            self.driver.find_element(By.XPATH, '//span[text()="新增角色"]').click()
            time.sleep(1)
            dialog = self.driver.find_element(By.XPATH, '//div[@class="el-dialog" and @aria-label="新增角色"]')
            dialogBody = dialog.find_element(By.XPATH, '//div[@class="el-dialog__body"]')
            formInputs = dialogBody.find_elements(By.XPATH, '//input[@class="el-input__inner"]')
            timestamp = int(time.time())
            formInputs[5].send_keys('角色标识-测试')
            formInputs[6].send_keys('角色名称-测试')
            formInputs[8].send_keys(timestamp)
            formInputs[9].send_keys(timestamp)
            self.driver.find_element(By.CSS_SELECTOR,
                                     '.el-dialog__footer:nth-child(3) .el-button--primary > span').click()

            time.sleep(2)
            roleId.clear()
            roleName.clear()
            roleId.send_keys('角色标识-测试')
            roleName.send_keys('角色名称-测试')
            self.driver.find_element(By.XPATH, '//span[text()="查询"]').click()
            time.sleep(2)
            el_rows = self.driver.find_elements(By.XPATH, '//tr[@class="el-table__row"]')
            self.assertEqual(1, len(el_rows), '根据新增参数查询记录为一条')
            cols = el_rows[0].find_elements(By.TAG_NAME, 'span')
            self.assertEqual('机构名称-测试', cols[0].text, '新增和查询记录的机构名称相同')
            self.assertEqual('机构全称-测试', cols[1].text, '新增和查询记录的机构全称相同')
            self.assertEqual('机构简称-测试', cols[2].text, '新增和查询记录的机构简称相同')
            self.assertEqual(str(timestamp), cols[3].text, '新增和查询记录的机构编码相同')
            self.assertEqual(firstTreeNodeText, cols[4].text, '新增和查询记录的上级机构相同')
            self.assertEqual(str(timestamp), cols[5].text, '新增和查询记录的排序相同')

            self.driver.find_element(By.XPATH, '//span[text()="编辑"]').click()
            time.sleep(1)
            dialog = self.driver.find_element(By.XPATH, '//div[@class="el-dialog" and @aria-label="编辑机构"]')
            dialogBody = dialog.find_element(By.XPATH, '//div[@class="el-dialog__body"]')
            formInputs = dialogBody.find_elements(By.XPATH, '//input[@class="el-input__inner"]')
            formInputs[12].clear()
            formInputs[12].send_keys('机构全称-测试编辑')
            saveButton = self.driver.find_elements(By.CSS_SELECTOR,
                                     '.el-dialog__footer:nth-child(3) .el-button--primary > span')
            saveButton[1].click()
            time.sleep(2)
            el_rows = self.driver.find_elements(By.XPATH, '//tr[@class="el-table__row"]')
            cols = el_rows[0].find_elements(By.TAG_NAME, 'span')
            self.assertEqual('机构全称-测试编辑', cols[1].text, '编辑功能正常')

            self.driver.find_element(By.XPATH, '//span[text()="删除"]').click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, '.el-button--default:nth-child(2) > span:nth-child(1)').click()
            time.sleep(1)
            el_rows = self.driver.find_elements(By.XPATH, '//tr[@class="el-table__row"]')
            self.assertEqual(0, len(el_rows), '根据新增参数,删除按钮点击后查询记录为0')

        except Exception as e:
            print(e)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
