from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from steps.login_steps import LoginSteps


def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)

    assert catalog_page.get_products_count() > 0, "Ожидаем товары на странице каталога"


def test_login_locked_out_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    error_text = steps.login_page.get_error_text()
    assert "locked out" in error_text, "Ожидаем сообщение о заблокированном пользователе"


def test_logout(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0

    catalog_page.logout()
    expect(page).to_have_url(LoginPage.URL)


def test_logout_visual_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("visual_user", "secret_sauce")

    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0

    catalog_page.logout()
    expect(page).to_have_url(LoginPage.URL)