from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes:
      def setup_method(self):
          if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
              print("Conectado ao servidor Urban Routes")
          else:
              print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

          # não modifique, pois precisamos do registro adicional habilitado para recuperar o código de confirmação do telefone
          capabilities = DesiredCapabilities.CHROME
          capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
          self.driver = webdriver.Chrome()
          self.driver.implicitly_wait(3)
          self.driver.get(data.URBAN_ROUTES_URL)
          WebDriverWait(self.driver, 15).until(
              expected.presence_of_element_located((By.ID, 'from'))
          )
          self.routes_page = UrbanRoutesPage(self.driver)

      def teardown_method(self):
          self.driver.quit()

      def test_set_route(self):
          self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
          assert self.routes_page.get_from() == data.ADDRESS_FROM
          assert self.routes_page.get_to() == data.ADDRESS_TO

      def test_select_plan(self):
          self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
          self.routes_page.click_call_taxi()
          self.routes_page.select_comfort_tariff()
          assert self.routes_page.is_comfort_selected()

      def test_fill_phone_number(self):
          self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
          self.routes_page.click_call_taxi()
          self.routes_page.select_comfort_tariff()
          self.routes_page.fill_phone_number(data.PHONE_NUMBER)
          assert self.routes_page.get_phone() == data.PHONE_NUMBER

      def test_fill_card(self):
          self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
          self.routes_page.click_call_taxi()
          self.routes_page.select_comfort_tariff()
          self.routes_page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
          assert self.routes_page.get_current_payment_method() == 'Cartão'

      def test_comment_for_driver(self):
          self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
          self.routes_page.click_call_taxi()
          self.routes_page.select_comfort_tariff()
          self.routes_page.set_comment(data.MESSAGE_FOR_DRIVER)
          assert self.routes_page.get_comment() == data.MESSAGE_FOR_DRIVER

      def test_order_blanket_and_handkerchiefs(self):
          self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
          self.routes_page.click_call_taxi()
          self.routes_page.select_comfort_tariff()
          self.routes_page.click_blanket_switch()
          assert self.routes_page.is_blanket_selected()

      def test_order_2_ice_creams(self):
          self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
          self.routes_page.click_call_taxi()
          self.routes_page.select_comfort_tariff()
          self.routes_page.order_ice_creams(2)
          assert self.routes_page.get_ice_cream_count() == 2

      def test_car_search_model_appears(self):
          self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
          self.routes_page.click_call_taxi()
          self.routes_page.select_comfort_tariff()
          self.routes_page.fill_phone_number(data.PHONE_NUMBER)
          self.routes_page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
          self.routes_page.click_order_taxi()
          assert self.routes_page.is_order_taxi_popup_displayed()