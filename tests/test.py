import time
from multiprocessing.connection import wait
from os import getcwd, path
from unittest import TestCase, main

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TestingPage(TestCase):
    dontCloseBrowser = True
    hideWindow = False

    @classmethod
    def setUpClass(cls):
        chr_options = Options()

        if cls.dontCloseBrowser:
            chr_options.add_experimental_option("detach", True)

        if cls.hideWindow:
            chr_options.add_argument("--headless")

        cls.browser = webdriver.Chrome(options=chr_options)

    # After the last test
    @classmethod
    def tearDownClass(cls):
        pass

    # Before each test
    def setUp(self):
        self.browser.get("http://localhost:8000/index.html")
        time.sleep(5)

    # After each test

    def tearDown(self):
        self.browser.get("about:blank")

    def testNumber(self):
        element = self.browser.find_element(By.LINK_TEXT, "0630‑555‑555")
        self.assertEqual("0630‑555‑555", element.text)

    def testLinkNumber(self):
        self.assertIn("0630555555", self.browser.page_source)

    def testEmail(self):
        self.assertIn("info@ntig-uppsala.github.io", self.browser.page_source)
        self.browser.find_element(By.LINK_TEXT, "info@ntig‑uppsala.github.io")

    def testSocialmediaLinks(self):
        self.browser.find_element(By.ID, "Instagram")
        self.browser.find_element(By.ID, "X")
        self.browser.find_element(By.ID, "Facebook")

    def testMapLink(self):
        self.assertIn(
            "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2127.594234558012!2d14.134204777783458!3d57.77429073450839!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x465a6dfced2b078d%3A0x5e530219f0ce4a2!2zRmrDpGxsZ2F0YW4gMzIsIDU1NCAzOSBKw7Zua8O2cGluZw!5e0!3m2!1ssv!2sse!4v1693829622306!5m2!1ssv!2sse",
            self.browser.page_source,
        )

    def testTitle(self):
        self.assertIn("NTB Biluthyrning", self.browser.page_source)

    def testNavBarTitle(self):
        element = self.browser.find_element(By.CLASS_NAME, "navbar-nav")
        element_text = element.text
        self.assertIn("Kontakta oss", element_text)
        self.assertIn("Hitta hit", element_text)
        self.assertIn("Öppettider", element_text)
        self.assertNotIn("Adress", element_text)

    def testNotTitle(self):
        self.assertNotIn("Bengans Biluthyrning", self.browser.page_source)

    def testFooterTitle(self):
        element = self.browser.find_element(By.CLASS_NAME, "info-section")
        element_text = element.text
        self.assertIn("Hitta hit", element_text)
        self.assertIn("Öppettider", element_text)

    def testAddress(self):
        self.assertIn("Fjällgatan 32H", self.browser.page_source)
        self.assertIn("981 39 Jönköping", self.browser.page_source)

    def testSlideShowText(self):
        element = self.browser.find_element(By.CLASS_NAME, "carousel-content")
        self.assertIn("Välkommen", element.text)
        self.assertIn("Ring", element.text)
        self.assertIn("0630‑555‑555", element.text)
        self.assertIn("vid bokning", element.text)

    def testSlideShowLink(self):
        phone_link = self.browser.find_element(By.ID, "whiteLink")
        self.assertIn("tel:0630555555", phone_link.get_attribute("href"))

    def testImageLoading(self):
        image_elements = self.browser.find_elements(By.TAG_NAME, "img")

        for image_element in image_elements:
            is_loaded = self.browser.execute_script(
                "return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0;",
                image_element,
            )

            if is_loaded:
                print(f"Image '{image_element.get_attribute('src')}' is loaded.")
            else:
                self.fail(
                    f"Image '{image_element.get_attribute('src')}' is not loaded."
                )

    def testZipCodeText(self):
        self.assertIn("Kolla om vår hemleverans når dig", self.browser.page_source)
        self.browser.find_element(By.CLASS_NAME, "checkNumber")

    def helperZipCode(self, zipCodeList, message):
        for currentZip in zipCodeList:
            self.browser.find_element(By.ID, "zipNumber").send_keys(currentZip)
            self.browser.find_element(By.ID, "zipNumber").send_keys(Keys.RETURN)

            time.sleep(1)
            zipOutput = self.browser.find_element(By.ID, "zipCodeCheck")
            self.assertIn(message, zipOutput.text)
            self.browser.get("about:blank")
            self.browser.get("http://127.0.0.1:8000/index.html")

    def testZipCodes(self):
        zipCodeCanBeDelivered = [
            "98132",
            "98140",
            "98147",
        ]
        zipCodeCanNotBeDelivered = [
            "12345",
            "55555",
            "92347",
        ]
        zipCodeListInvalid = [
            "1234",
            "hej",
            "xxxxx",
        ]
        self.helperZipCode(zipCodeCanBeDelivered, "Vi kör ut, ring telefonnumret ovan!")
        self.helperZipCode(zipCodeCanNotBeDelivered, "Vi kör tyvärr inte ut till dig.")
        self.helperZipCode(zipCodeListInvalid, "Inte ett giltigt postnummer.")

    def testOpeningHours(self):
        self.assertIn("Öppettider", self.browser.page_source)
        self.assertIn("Vardagar", self.browser.page_source)
        self.assertIn("10-16", self.browser.page_source)
        self.assertIn("Lördag", self.browser.page_source)
        self.assertIn("12-15", self.browser.page_source)
        self.assertIn("Söndag", self.browser.page_source)

    def helperLiveOpening(self, date, results):
        self.browser.execute_script("setLiveOpeningHours(new Date('" + date + "'))")
        element = self.browser.find_element(By.ID, "storeState")
        self.assertIn(results, element.text)

    def testLiveOpeningHours(self):
        # Monday
        self.helperLiveOpening("2023-09-11T09:15:00", "Öppnar idag kl. 10")
        self.helperLiveOpening("2023-09-11T09:30:00", "Öppnar om 30 minuter")
        self.helperLiveOpening("2023-09-11T10:10:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-11T12:30:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-11T15:45:00", "Stänger snart")
        self.helperLiveOpening("2023-09-11T16:15:00", "Öppnar tisdag kl. 10")

        # Tuesday
        self.helperLiveOpening("2023-09-12T09:15:00", "Öppnar idag kl. 10")
        self.helperLiveOpening("2023-09-12T09:30:00", "Öppnar om 30 minuter")
        self.helperLiveOpening("2023-09-12T10:10:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-12T12:30:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-12T15:45:00", "Stänger snart")
        self.helperLiveOpening("2023-09-12T16:15:00", "Öppnar onsdag kl. 10")

        # Wednesday
        self.helperLiveOpening("2023-09-13T09:15:00", "Öppnar idag kl. 10")
        self.helperLiveOpening("2023-09-13T09:30:00", "Öppnar om 30 minuter")
        self.helperLiveOpening("2023-09-13T10:10:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-13T12:30:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-13T15:45:00", "Stänger snart")
        self.helperLiveOpening("2023-09-13T16:15:00", "Öppnar torsdag kl. 10")

        # Thursday
        self.helperLiveOpening("2023-09-14T09:15:00", "Öppnar idag kl. 10")
        self.helperLiveOpening("2023-09-14T09:30:00", "Öppnar om 30 minuter")
        self.helperLiveOpening("2023-09-14T10:10:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-14T12:30:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-14T15:45:00", "Stänger snart")
        self.helperLiveOpening("2023-09-14T16:15:00", "Öppnar fredag kl. 10")

        # Friday
        self.helperLiveOpening("2023-09-15T09:15:00", "Öppnar idag kl. 10")
        self.helperLiveOpening("2023-09-15T09:30:00", "Öppnar om 30 minuter")
        self.helperLiveOpening("2023-09-15T10:10:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-15T12:30:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-15T15:45:00", "Stänger snart")
        self.helperLiveOpening("2023-09-15T16:15:00", "Öppnar lördag kl. 12")

        # Saturday
        self.helperLiveOpening("2023-09-16T09:45:00", "Öppnar idag kl. 12")
        self.helperLiveOpening("2023-09-16T10:30:00", "Öppnar idag kl. 12")
        self.helperLiveOpening("2023-09-16T11:30:00", "Öppnar om 30 minuter")
        self.helperLiveOpening("2023-09-16T12:10:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-16T14:00:00", "Just nu: Öppet")
        self.helperLiveOpening("2023-09-16T14:45:00", "Stänger snart")
        self.helperLiveOpening("2023-09-16T15:10:00", "Öppnar måndag kl. 10")

        # Sunday
        self.helperLiveOpening("2023-09-17T09:15:00", "Öppnar måndag kl. 10")
        self.helperLiveOpening("2023-09-17T10:30:00", "Öppnar måndag kl. 10")
        self.helperLiveOpening("2023-09-17T12:10:00", "Öppnar måndag kl. 10")
        self.helperLiveOpening("2023-09-17T14:45:00", "Öppnar måndag kl. 10")
        self.helperLiveOpening("2023-09-17T15:45:00", "Öppnar måndag kl. 10")
        self.helperLiveOpening("2023-09-17T16:45:00", "Öppnar måndag kl. 10")

        # Night time
        self.helperLiveOpening("2023-09-13T00:45:00", "Öppnar idag kl. 10")
        self.helperLiveOpening("2023-09-15T23:00:00", "Öppnar lördag kl. 12")

        # Closed days:
        # New year
        self.helperLiveOpening("2023-12-30T16:10:00", "Öppnar tisdag kl. 10")
        self.helperLiveOpening("2023-12-31T10:10:00", "Öppnar tisdag kl. 10")
        self.helperLiveOpening("2024-01-01T16:10:00", "Öppnar tisdag kl. 10")
        self.helperLiveOpening("2024-01-06T14:10:00", "Öppnar måndag kl. 10")

        # Christmas
        self.helperLiveOpening("2023-12-23T15:50:00", "Öppnar onsdag kl. 10")
        self.helperLiveOpening("2023-12-24T16:50:00", "Öppnar onsdag kl. 10")
        self.helperLiveOpening("2023-12-25T02:50:00", "Öppnar onsdag kl. 10")
        self.helperLiveOpening("2023-12-26T10:50:00", "Öppnar onsdag kl. 10")

    def helperClosedDaysAutomaticOrder(self, date, expectedDate):
        time.sleep(2)
        self.browser.execute_script("sortClosedDays(new Date('" + date + "'))")

        firstDate = self.browser.execute_script(
            "return document.getElementById('closedDaysList').getElementsByTagName('li')[0].textContent.match(/[0-9]{1,2}/g)"
        )
        self.assertEqual(firstDate, expectedDate)

    def testClosedDaysAutomaticOrder(self):
        self.helperClosedDaysAutomaticOrder("2023-09-16T14:00:00", ["12", "24"])
        self.helperClosedDaysAutomaticOrder("2023-01-02T14:00:00", ["1", "6"])
        self.helperClosedDaysAutomaticOrder("2023-04-13T14:00:00", ["5", "1"])
        self.helperClosedDaysAutomaticOrder("2023-12-25T14:00:00", ["12", "26"])

    def testCars(self):
        car_list = [
            {"car": "Audi A6", "model": "2011", "price": "800"},
            {"car": "Renault Kadjar", "model": "2020", "price": "450"},
            {"car": "Kia Soul", "model": "2020", "price": "400"},
            {"car": "Subaru", "model": "2020", "price": "300"},
            {"car": "Cadillac Escalade", "model": "1999", "price": "500"},
            {"car": "Mitsubishi Outlander", "model": "2018", "price": "450"},
            {"car": "Volvo XC40", "model": "2018", "price": "800"},
            {"car": "VW Polo", "model": "2022", "price": "300"},
            {"car": "Kia Carens", "model": "2022", "price": "400"},
            {"car": "Audi S3", "model": "2015", "price": "450"},
        ]

        for car_info in car_list:
            car = car_info["car"]
            model = car_info["model"]
            price = car_info["price"]

            self.assertIn(car, self.browser.page_source)
            self.assertIn(model, self.browser.page_source)
            self.assertIn(str(price), self.browser.page_source)

    # Makes sure previous spelling mistakes are completely removed
    def testWrongCars(self):
        self.assertNotIn("Caddilac", self.browser.page_source)
        self.assertNotIn("Mitsubichi", self.browser.page_source)

    def helperProductSort(
        self,
        sortOption,
        expectedFirst,
        expectedLast,
        expectedFirstChecker,
        expectedLastChecker,
    ):
        self.browser.find_element(By.CLASS_NAME, "dropdown-toggle").click()
        self.browser.find_element(By.ID, sortOption).click()
        # Gets the product chart as a list
        sortedCarList = self.browser.execute_script(
            "return Array.from(document.getElementById('productChart').children)[1].children"
        )

        self.assertIn(expectedFirst, sortedCarList[0].text)
        self.assertIn(expectedFirstChecker, sortedCarList[0].text)

        # Checks so that the last product is correct [1] is used because the value [0] is the table header
        self.assertIn(expectedLast, sortedCarList[len(sortedCarList) - 1].text)
        self.assertIn(expectedLastChecker, sortedCarList[len(sortedCarList) - 1].text)

    # Tests the the sort buttons so that they sort the list correctly
    def testProductSort(self):
        self.helperProductSort(
            "priceDecreasing", "800", "250", "Audi A6", "Renault Kadjar"
        )

        self.helperProductSort(
            "yearDecreasing", "2022", "1999", "Kia Carens", "Cadillac Escalade"
        )

        self.helperProductSort("nameDecreasing", "VW Polo", "Audi A6", "300", "800")

        self.helperProductSort("priceRising", "250", "800", "Renault Kadjar", "Audi A6")

        self.helperProductSort(
            "yearRising", "1999", "2022", "Cadillac Escalade", "Kia Carens"
        )

        self.helperProductSort("nameRising", "Audi A6", "VW Polo", "800", "300")

    def helperSortedList(
        self, sortOption, isRising, expectedFirst, ExpectedLast, firstCheck, lastCheck
    ):
        sortedCarList = self.browser.execute_script(
            "return sortCars('" + sortOption + "'" "," + isRising + ");"
        )

        sortedCarList = [str(item) for item in sortedCarList]

        self.assertIn(expectedFirst, sortedCarList[0])
        self.assertIn(firstCheck, sortedCarList[0])

        self.assertIn(ExpectedLast, sortedCarList[len(sortedCarList) - 1])
        self.assertIn(lastCheck, sortedCarList[len(sortedCarList) - 1])

    # Tests the function that sorts the list
    def testSortedList(self):
        self.helperSortedList("name", "true", "Audi A6", "VW Polo", "800", "300")
        self.helperSortedList(
            "year", "true", "1999", "2022", "Cadillac Escalade", "VW Polo"
        )
        self.helperSortedList(
            "price", "false", "800", "250", "Audi A6", "Renault Kadjar"
        )

    def testCompanyPrices(self):
        self.browser.execute_script("window.scrollTo(0, 600);")
        time.sleep(0.5)
        self.browser.find_element(By.ID, "companyLabelClick").click()
        productList = self.browser.execute_script(
            "return Array.from(document.getElementById('productChart').children)[1]"
        )
        time.sleep(0.5)
        self.assertIn("640", productList.text)

        self.browser.find_element(By.ID, "privateLabelClick").click()
        productList = self.browser.execute_script(
            "return Array.from(document.getElementById('productChart').children)[1]"
        )
        time.sleep(0.5)
        self.assertIn("800", productList.text)

    def helperLanguageChange(self, language, testCases):
        self.browser.find_element(By.ID, "activeLang").click()
        time.sleep(1)
        self.browser.find_element(By.ID, language).click()
        testCaseZip = self.browser.find_element(By.ID, "deliveryCheck")

        self.assertIn(testCases, self.browser.page_source)

    def testLanguageChange(self):
        self.helperLanguageChange("no", "Sjekk om hjemleveringen vår når deg")
        self.helperLanguageChange("sv", "Kolla om vår hemleverans når dig")


# will run if the fil running is a normal python file, always end of file
if __name__ == "__main__":
    main(verbosity=2)
