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
    options.add_argument("--headless=new")           # безголовый режим
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


def test_caseguru_page_loads(driver):
    """Проверка успешной загрузки главной страницы caseguru.ru."""
    url = "https://caseguru.ru/"
    driver.get(url)

    # 1. Проверяем URL
    assert url.rstrip("/") in driver.current_url, \
        f"Ожидался URL {url}, получен {driver.current_url}"

    # 2. Проверяем, что title содержит название сайта
    WebDriverWait(driver, 10).until(
        lambda d: d.title.strip() != ""
    )
    assert "caseguru" in driver.title.lower(), \
        f"Title не содержит 'caseguru': {driver.title}"

    # 3. Проверяем, что страница полностью загружена (readyState = complete)
    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # 4. Проверяем, что body присутствует и не пустой
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.is_displayed(), "Элемент body не отображается"
    assert len(body.text) > 0, "Страница пустая (body.text пустой)"

    # 5. Проверяем отсутствие явных ошибок на странице
    page_source = driver.page_source.lower()
    for error_marker in ("404 not found", "500 internal server error"):
        assert error_marker not in page_source, \
            f"На странице найдена ошибка: {error_marker}"


def test_caseguru_main_content_visible(driver):
    """Проверка наличия видимого контента на странице."""
    driver.get("https://caseguru.ru/")

    # Ждём, пока появится хотя бы один видимый элемент с контентом
    content = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert content.is_displayed(), "Заголовок H1 не отображается"
    assert content.text.strip() != "", "Заголовок H1 пустой"
    import sys
import pytest
import sys
import pytest

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))