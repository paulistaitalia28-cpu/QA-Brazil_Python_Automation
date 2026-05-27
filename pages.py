from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from helpers import retrieve_phone_code


class UrbanRoutesPage:
      # ===== ENDEREÇO =====
      from_field = (By.ID, 'from')
      to_field = (By.ID, 'to')

      # ===== TELA 1: CHAMAR TÁXI =====
      call_taxi_button = (By.XPATH, '//button[text()="Chamar um táxi"]')

      # ===== TELA 2: TARIFA COMFORT =====
      comfort_tariff = (By.XPATH, '//img[@alt="Comfort"]/../..')

      # ===== TELA 2: BOTÕES QUE ABREM MODAIS =====
      phone_number_field = (By.CLASS_NAME, 'np-button')
      payment_method_button = (By.CLASS_NAME, 'pp-button')
      payment_method_text = (By.CLASS_NAME, 'pp-value-text')

      # ===== TELA 2: MENSAGEM PRO MOTORISTA =====
      comment_field = (By.ID, 'comment')

      # ===== TELA 2: COBERTOR E LENÇÓIS (2 seletores) =====
      blanket_switch = (By.XPATH, '//div[@class="r-sw-container" and .//div[text()="Cobertor e lençóis"]]//span[@class="slider round"]')
      blanket_checkbox = (By.XPATH, '//div[@class="r-sw-container" and .//div[text()="Cobertor e lençóis"]]//input[@type="checkbox"]')

      # ===== TELA 2: SORVETE =====
      ice_cream_plus = (By.CLASS_NAME, 'counter-plus')
      ice_cream_value = (By.CLASS_NAME, 'counter-value')

      # ===== TELA 2: BOTÃO FINAL (pedir táxi) =====
      order_button = (By.CLASS_NAME, 'smart-button')
      order_taxi_modal = (By.CLASS_NAME, 'order-body')

      # ===== MODAL TELEFONE (parte 1) =====
      phone_input = (By.ID, 'phone')
      phone_next_button = (By.XPATH, '//button[text()="Próximo"]')

      # ===== MODAL SMS (parte 2) =====
      sms_code_input = (By.ID, 'code')
      sms_confirm_button = (By.XPATH, '//button[text()="Confirmar"]')

      # ===== MODAL PAGAMENTO → ADICIONAR CARTÃO =====
      add_card_button = (By.XPATH, '//div[@class="pp-title" and text()="Adicionar cartão"]')

      # ===== MODAL CARTÃO =====
      card_number_input = (By.ID, 'number')
      card_code_input = (By.XPATH, '//input[@id="code" and @class="card-input"]')
      card_add_button = (By.XPATH, '//button[@type="submit" and text()="Adicionar"]')


      def __init__(self, driver):
          self.driver = driver

      # ===== ENDEREÇO =====
      def set_from(self, from_address):
          self.driver.find_element(*self.from_field).send_keys(from_address)

      def set_to(self, to_address):
          self.driver.find_element(*self.to_field).send_keys(to_address)

      def set_route(self, from_address, to_address):
          self.set_from(from_address)
          self.set_to(to_address)

      def get_from(self):
          return self.driver.find_element(*self.from_field).get_property('value')

      def get_to(self):
          return self.driver.find_element(*self.to_field).get_property('value')

      # ===== TELA 1: CHAMAR TÁXI =====
      def click_call_taxi(self):
          self.driver.find_element(*self.call_taxi_button).click()

      # ===== TARIFA COMFORT (com if pra idempotência) =====
      def is_comfort_selected(self):
          card = self.driver.find_element(*self.comfort_tariff)
          return "active" in card.get_attribute("class")

      def select_comfort_tariff(self):
          if not self.is_comfort_selected():
              self.driver.find_element(*self.comfort_tariff).click()

      # ===== TELEFONE (fluxo completo com SMS) =====
      def click_phone_number_field(self):
          self.driver.find_element(*self.phone_number_field).click()

      def set_phone_number(self, phone):
          self.driver.find_element(*self.phone_input).send_keys(phone)

      def click_phone_next(self):
          self.driver.find_element(*self.phone_next_button).click()

      def set_sms_code(self, code):
          self.driver.find_element(*self.sms_code_input).send_keys(code)

      def click_sms_confirm(self):
          self.driver.find_element(*self.sms_confirm_button).click()

      def fill_phone_number(self, phone):
          self.click_phone_number_field()
          self.set_phone_number(phone)
          self.click_phone_next()
          code = retrieve_phone_code(self.driver)
          self.set_sms_code(code)
          self.click_sms_confirm()

      def get_phone(self):
          return self.driver.find_element(*self.phone_number_field).text

      # ===== CARTÃO (com Tab pra ativar botão Adicionar) =====
      def click_payment_method(self):
          self.driver.find_element(*self.payment_method_button).click()

      def click_add_card(self):
          self.driver.find_element(*self.add_card_button).click()

      def set_card_number(self, number):
          self.driver.find_element(*self.card_number_input).send_keys(number)

      def set_card_code(self, code):
          card_code = self.driver.find_element(*self.card_code_input)
          card_code.send_keys(code)
          card_code.send_keys(Keys.TAB)

      def click_card_add(self):
          self.driver.find_element(*self.card_add_button).click()

      def fill_card(self, number, code):
          self.click_payment_method()
          WebDriverWait(self.driver, 10).until(
              expected.visibility_of_element_located(self.add_card_button)
          )
          self.click_add_card()
          WebDriverWait(self.driver, 10).until(
              expected.visibility_of_element_located(self.card_number_input)
          )
          self.set_card_number(number)
          self.set_card_code(code)
          self.click_card_add()
          WebDriverWait(self.driver, 10).until(
              expected.invisibility_of_element_located(self.card_number_input)
          )

      def get_current_payment_method(self):
          return self.driver.find_element(*self.payment_method_text).text

      # ===== MENSAGEM PRO MOTORISTA =====
      def set_comment(self, comment):
          self.driver.find_element(*self.comment_field).send_keys(comment)


      def get_comment(self):
          return self.driver.find_element(*self.comment_field).get_property('value')

      # ===== COBERTOR E LENÇÓIS (2 seletores) =====
      def click_blanket_switch(self):
          element =  self.driver.find_element(*self.blanket_switch)
          self.driver.execute_script("arguments[0].click();", element)

      def is_blanket_selected(self):
          return self.driver.find_element(*self.blanket_checkbox).is_selected()

      # ===== SORVETE (com for loop interno) =====
      def order_ice_creams(self, quantity):
          for _ in range(quantity):
              element = self.driver.find_element(*self.ice_cream_plus)
              self.driver.execute_script("arguments[0].click();", element)

      def get_ice_cream_count(self):
          return int(self.driver.find_element(*self.ice_cream_value).text)

      # ===== PEDIR TÁXI =====
      def click_order_taxi(self):
          element = self.driver.find_element(*self.order_button)
          self.driver.execute_script("arguments[0].click();", element)

      def is_order_taxi_popup_displayed(self):
          WebDriverWait(self.driver, 40).until(
              expected.visibility_of_element_located(self.order_taxi_modal)
          )
          return self.driver.find_element(*self.order_taxi_modal).is_displayed()