from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://ahara.karnataka.gov.in/SHOPOWNER_MSERVER/shoplogin.aspx")
    # page.click("#start-button")
    # page.wait_for_timeout(100)
   # page.click("ctl00$ContentPlaceHolder1$rblSeluser")
    page.locator("//input[contains(@id,'rblSeluser_1')]").click()
    page.locator("//input[contains(@id,'rdbLang_0')]").click()

    page.locator("//input[contains(@id,'txtMobile')]").click()
    page.locator("//input[contains(@id,'txtMobile')]").fill("9986347891")
    old_url = page.url
    page.wait_for_function(f"() => location.href !== '{old_url}'", timeout=0)

    print("✅ Submit button clicked and page changed. Continuing automation...")

#    Thumb impression, manual work
    page.locator("//img[contains(@id,'Image1')]").click()
    masterxpath = "//a[text()='Masters']"
    rationOption = "//*[contains(text(),'Ration Issue through')]"
    page.locator(masterxpath).hover()
    page.locator("//a[text()='Shop Details']").click()
    page.wait_for_selector(rationOption)
    page.locator(rationOption).click()
#wait for the page to load
    page.locator('''//label[contains(text(),"RC's belong to same State/")]''').click()
    page.locator('//label[contains(text(),"same district")]').click()
    while True:
        time.sleep(100)
    # browser.close()