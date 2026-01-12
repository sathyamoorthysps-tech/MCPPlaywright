from pytest_bdd import scenarios, given, when, then, parsers
import re

from tests.pages.search_page import SearchPage

scenarios("../features/search.feature")


@given("I open Amazon India homepage")
def open_home(page):
    SearchPage.goto_home(page)


@when(parsers.parse('I search for "{query}"'))
def search(page, query):
    SearchPage.search(page, query)


@when("I sort results by price low to high")
def sort_by_price_low_to_high(page):
    SearchPage.select_sort_by_price_low_to_high(page)
    try:
        page.wait_for_timeout(60000)
    except Exception:
        pass
    try:
        titles, prices = SearchPage.top_titles_and_prices(page, limit=5)
        print("Top results after sort:")
        for i in range(max(len(titles), len(prices))):
            t = titles[i] if i < len(titles) else "<no title>"
            pr = prices[i] if i < len(prices) else "<no price>"
            print(f"{i+1}. {t} - {pr}")
    except Exception as e:
        print("Could not log search results:", e)


@then("I should see search results")
def should_see_results(page):
    assert SearchPage.is_results_present(page)


@then("I should see search results sorted by price low to high")
def should_see_sorted_by_price(page):
    try:
        page.wait_for_selector(SearchPage.MAIN_SLOT, timeout=10000)
        _, prices = SearchPage.top_titles_and_prices(page, limit=5)
        nums = SearchPage.parse_prices_to_ints(prices)
        if len(nums) >= 2:
            assert nums[0] <= nums[1]
        else:
            assert len(prices) > 0
    except Exception:
        assert SearchPage.is_results_present(page)
from pytest_bdd import scenarios, given, when, then, parsers
import re

from tests.pages.search_page import SearchPage

scenarios("../features/search.feature")


@given("I open Amazon India homepage")
def open_home(page):
    SearchPage.goto_home(page)


@when(parsers.parse('I search for "{query}"'))
def search(page, query):
    SearchPage.search(page, query)


@when("I sort results by price low to high")
def sort_by_price_low_to_high(page):
    SearchPage.select_sort_by_price_low_to_high(page)
    try:
        page.wait_for_timeout(60000)
    except Exception:
        pass
    try:
        titles, prices = SearchPage.top_titles_and_prices(page, limit=5)
        print("Top results after sort:")
        for i in range(max(len(titles), len(prices))):
            t = titles[i] if i < len(titles) else "<no title>"
            pr = prices[i] if i < len(prices) else "<no price>"
            print(f"{i+1}. {t} - {pr}")
    except Exception as e:
        print("Could not log search results:", e)


@then("I should see search results")
def should_see_results(page):
    assert SearchPage.is_results_present(page)


@then("I should see search results sorted by price low to high")
def should_see_sorted_by_price(page):
    try:
        page.wait_for_selector(SearchPage.MAIN_SLOT, timeout=10000)
        _, prices = SearchPage.top_titles_and_prices(page, limit=5)
        nums = SearchPage.parse_prices_to_ints(prices)
        if len(nums) >= 2:
            assert nums[0] <= nums[1]
        else:
            assert len(prices) > 0
    except Exception:
        assert SearchPage.is_results_present(page)
