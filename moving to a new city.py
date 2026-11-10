import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации и закрытия драйвера."""
    options = Options()
    # options.add_argument("--headless=new")  # Раскомментируйте, если не хотите видеть окно браузера
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

    # 2. Находим кнопку с текущим городом (Тюмень) и кликаем по ней.
    current_city_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'nav-link') and contains(text(), 'Тюмень')]"))
    )
    current_city_btn.click()

    # 3. Ждем появления поля ввода для поиска города
    # (Используем несколько вариантов селекторов на случай, если разработчики поменяют верстку)
    search_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[type='search'], input[placeholder*='город']"))
    )

    # 4. Вводим "Москва" в поле поиска
    search_input.clear()
    search_input.send_keys("Москва")

    # 5. Ждем появления результата (кнопки или ссылки с текстом "Москва")
    moscow_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Москва') and not(contains(text(), 'Московская'))]"))
    )
    moscow_option.click()

    # 6. Проверяем, что город в шапке изменился на "Москва".
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, "//header"), "Москва")
    )
    
    header_text = driver.find_element(By.XPATH, "//header").text
    assert "Москва" in header_text, "Город не изменился на Москву"
    assert "Тюмень" not in header_text, "Старый город (Тюмень) всё еще отображается в шапке"


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(["-v", __file__]))