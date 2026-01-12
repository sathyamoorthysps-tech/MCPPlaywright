from typing import List, Tuple
import re


class SearchPage:
    # Selectors / locators
    SEARCH_INPUT = "input#twotabsearchtextbox"
    MAIN_SLOT = "div.s-main-slot"
    SORT_SELECT = "select#s-result-sort-select"
    SORT_DROPDOWN_TRIGGER = "#a-autoid-0-announce"
    RESULT_TITLE = "span.a-size-medium.a-color-base.a-text-normal"
    RESULT_PRICE = "span.a-price-whole"

    CONSENT_CANDIDATES = [
        'text=Accept Cookies', 'text=Accept', 'text=Agree', 'text=Continue', 'text=OK', 'text=Yes',
        "#sp-cc-accept", "input#sp-cc-accept", "button#accept", "button#continue",
        "button[aria-label=\"close\"]",
    ]

    @staticmethod
    def goto_home(page, url: str = "https://www.amazon.in"):
        page.goto(url)
        SearchPage.dismiss_consent(page)
        try:
            page.wait_for_selector(SearchPage.SEARCH_INPUT, timeout=60000)
        except Exception:
            pass

    @staticmethod
    def dismiss_consent(page, timeout: int = 3000):
        def _try_click(sel, to=timeout):
            try:
                page.click(sel, timeout=to)
                return True
            except Exception:
                return False

        for sel in SearchPage.CONSENT_CANDIDATES:
            if _try_click(sel):
                return True

        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        return False

    @staticmethod
    def search(page, query: str):
        try:
            page.bring_to_front()
        except Exception:
            pass
        page.fill(SearchPage.SEARCH_INPUT, query)
        page.press(SearchPage.SEARCH_INPUT, "Enter")
        try:
            page.wait_for_selector(SearchPage.MAIN_SLOT)
        except Exception:
            pass

    @staticmethod
    def is_results_present(page) -> bool:
        try:
            return page.query_selector(SearchPage.MAIN_SLOT) is not None
        except Exception:
            return False

    @staticmethod
    def select_sort_by_price_low_to_high(page):
        try:
            page.bring_to_front()
        except Exception:
            pass

        # Prefer native select if present
        try:
            sel = page.query_selector(SearchPage.SORT_SELECT)
            if sel:
                options = sel.query_selector_all("option")
                target_value = None
                for o in options:
                    try:
                        txt = o.inner_text().strip().lower()
                    except Exception:
                        txt = ""
                    if "price" in txt and "low" in txt:
                        target_value = o.get_attribute("value")
                        break
                if not target_value:
                    target_value = "price-asc-rank"
                page.select_option(SearchPage.SORT_SELECT, target_value)
                try:
                    page.wait_for_selector(SearchPage.MAIN_SLOT)
                except Exception:
                    pass
                return True
        except Exception:
            pass

        # Fallback: click dropdown then option by visible text
        try:
            page.click(SearchPage.SORT_DROPDOWN_TRIGGER, timeout=3000)
        except Exception:
            pass

        for text_sel in [
            "text=Price: Low to High",
            "text=Price -- Low to High",
            "text=Price: Low to high",
            "text=Low to High",
        ]:
            try:
                page.click(text_sel, timeout=4000)
                return True
            except Exception:
                continue

        # fallback heuristic: search for visible elements containing both words
        try:
            candidates = page.query_selector_all("xpath=//li|//a|//div")
            for c in candidates:
                try:
                    txt = c.inner_text().strip().lower()
                except Exception:
                    continue
                if "price" in txt and "low" in txt:
                    try:
                        c.click()
                        return True
                    except Exception:
                        continue
        except Exception:
            pass

        return False

    @staticmethod
    def top_titles_and_prices(page, limit: int = 5) -> Tuple[List[str], List[str]]:
        titles = []
        prices = []
        try:
            titles = [t.inner_text().strip() for t in page.query_selector_all(SearchPage.RESULT_TITLE)][:limit]
        except Exception:
            titles = []
        try:
            prices = [p.inner_text().strip() for p in page.query_selector_all(SearchPage.RESULT_PRICE)][:limit]
        except Exception:
            prices = []
        return titles, prices

    @staticmethod
    def parse_prices_to_ints(price_texts: List[str]) -> List[int]:
        nums = []
        for txt in price_texts:
            s = txt.replace(',', '')
            try:
                n = int(re.sub(r"[^0-9]", "", s))
                nums.append(n)
            except Exception:
                continue
        return nums
