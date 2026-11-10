import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("--headless=new")  # Оставьте выключенным, чтобы видеть процесс
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_change_city_to_moscow(driver):
    """Тест смены города на сайте caseguru.ru на Москву."""
    driver.get("https://caseguru.ru/")

    # 1. Ждем загрузки страницы
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # 2. Открываем окно выбора города (кликаем по текущему городу в шапке)
    current_city_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'nav-link')]"))
    )
    current_city_btn.click()
    print("Окно выбора города открыто.")

            # 3. Вместо ожидания окна, сразу ждем появления кнопки "Москва" внутри списка городов.
    moscow_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'location-list')]//button[text()='Москва']"))
    )
    
    # Прокручиваем к кнопке и даем время на анимацию окна
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", moscow_btn)
    time.sleep(1)
    
    # Кликаем. Если перекрывает оверлей, кликаем через JS.
    try:
        moscow_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", moscow_btn)
    
    print("Клик по кнопке 'Москва' выполнен.")

    # 4. Проверяем результат
    time.sleep(2)  # Ждем обновления контента
    
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Москва" in page_text, "Город не изменился на Москву"
    
    print("✅ Тест успешно пройден! Город изменен.")

    # 5. Проверяем результат
    # Ждем, пока окно закроется (исчезнет видимость)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "tbwp_locations_choose_modal"))
    )
    
    # Даем странице секунду на обновление данных
    time.sleep(1)
    
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Москва" in page_text, "Город не изменился на Москву"
    
    print("✅ Тест успешно пройден! Город изменен.")

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(["-v", __file__]))