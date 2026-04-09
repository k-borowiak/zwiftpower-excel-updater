from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Optional

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


LOGIN_URL = (
    "https://secure.zwift.com/auth/realms/zwift/protocol/openid-connect/auth"
    "?client_id=zwiftpower-public"
    "&redirect_uri=https%3A%2F%2Fzwiftpower.com%2Fucp.php%3Fmode%3Dlogin%26login%3Dexternal%26oauth_service%3Doauthzpsso"
    "&response_type=code"
    "&scope=openid"
    "&state=f3d653974daeeb26d49d0ada0b34e2d0"
)

PROFILE_URL = "https://zwiftpower.com/profile.php?z={profile_id}"


@dataclass
class ProfileData:
    weight: float = 0.0
    zftp: float = 0.0
    power_15s: int = 0
    power_1m: int = 0
    power_5m: int = 0
    power_20m: int = 0


class ZwiftPowerClient:
    def __init__(self, headless: bool = True, timeout: int = 15, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger("zp_updater")
        self.timeout = timeout
        self.driver = self._build_driver(headless=headless)
        self.wait = WebDriverWait(self.driver, timeout)

    def _build_driver(self, headless: bool) -> webdriver.Chrome:
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

    def login(self, username: str, password: str) -> None:
        self.driver.get(LOGIN_URL)
        self.wait.until(EC.presence_of_element_located((By.NAME, "username")))

        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        # czekaj na powrót do ZwiftPower
        self.wait.until(EC.url_contains("zwiftpower.com"))
        self.logger.info("Zalogowano poprawnie.")

    def scrape_profile(self, profile_id: int) -> ProfileData:
        url = PROFILE_URL.format(profile_id=profile_id)
        data = ProfileData()

        try:
            self.driver.get(url)
            # element "kotwica" strony
            self.wait.until(EC.presence_of_element_located((By.ID, "profile_information")))

            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            data.weight, data.zftp = self._parse_weight_zftp(soup)

            # moce z wykresu (2 metody)
            p = self._extract_power_from_labels()
            if p is None:
                p = self._extract_power_from_highcharts_js()

            if p and len(p) >= 4:
                data.power_15s, data.power_1m, data.power_5m, data.power_20m = p[:4]

        except Exception:
            self.logger.exception("ID=%s - błąd podczas scrapowania profilu", profile_id)

        return data

    def _parse_weight_zftp(self, soup: BeautifulSoup) -> tuple[float, float]:
        """
        Parsuje tabelę #profile_information.
        """
        weight = 0.0
        zftp = 0.0

        table = soup.find("table", {"id": "profile_information"})
        if not table:
            return weight, zftp

        for row in table.find_all("tr"):
            th = row.find("th")
            tds = row.find_all("td")
            if not th or not tds:
                continue

            key = th.get_text(strip=True)
            val = tds[0].get_text(strip=True)

            if "zFTP" in key:
                zftp = self._safe_float(val.replace("w", "").strip())
            elif "Weight" in key:
                weight = self._safe_float(val.replace("kg", "").strip())

        return weight, zftp

    def _extract_power_from_labels(self) -> Optional[list[int]]:
        """
        Próbuje wyciągnąć moce z etykiet (jeśli wykres je renderuje).
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-data-labels")))
            labels = self.driver.find_elements(By.CSS_SELECTOR, ".highcharts-data-labels span")

            power_values: list[int] = []
            for label in labels:
                text = (label.text or "").strip()
                if "watt" in text.lower():
                    # np. "340 watts"
                    first = text.split()[0]
                    if first.isdigit():
                        power_values.append(int(first))

            return power_values if power_values else None
        except Exception:
            return None

    def _extract_power_from_highcharts_js(self) -> Optional[list[int]]:
        """
        Fallback: pobiera dane bezpośrednio z obiektu Highcharts.
        """
        script = """
        try {
            const charts = (window.Highcharts && Highcharts.charts) ? Highcharts.charts : [];
            const c = charts.find(x => x && x.series && x.series.length > 0);
            if (!c) return [];
            const s = c.series.find(x => x && x.data && x.data.length > 0);
            if (!s) return [];
            return s.data.map(d => d && typeof d.y === 'number' ? Math.round(d.y) : null).filter(x => x !== null);
        } catch(e) { return []; }
        """
        try:
            power_data = self.driver.execute_script(script)
            if isinstance(power_data, list) and power_data:
                return [int(x) for x in power_data]
            return None
        except Exception:
            return None

    @staticmethod
    def _safe_float(x: str) -> float:
        try:
            return float(x)
        except Exception:
            return 0.0

    def close(self) -> None:
        try:
            self.driver.quit()
        except Exception:
            pass