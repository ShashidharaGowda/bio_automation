from playwright.sync_api import sync_playwright
import time

def open_login_page(page):
    print("🔗 Navigating to login page...")
    page.goto("https://ahara.karnataka.gov.in/SHOPOWNER_MSERVER/shoplogin.aspx")
    page.locator("//input[contains(@id,'rdbLang_0')]").click()
    print("🌐 Login page opened and language selected.")

def enter_mobile_number(page, mobile_number):
    print(f"📱 Entering mobile number: {mobile_number}")
    page.locator("//input[contains(@id,'txtMobile')]").fill(mobile_number)
    old_url = page.url
    print(f"📍 Waiting for page navigation after mobile entry. Old URL: {old_url}")
    page.wait_for_function(f"() => location.href !== '{old_url}'", timeout=0)
    print(f"✅ Mobile number accepted. New URL: {page.url}")
    return page.url

def select_authentication(page):
    print("🔐 Selecting biometric authentication...")
    page.locator("//input[contains(@id,'bio_otp_auth_0')]").click()
    time.sleep(0.5)
    page.locator("//input[contains(@id,'RadioButtonList1_0')]").click()
    page.locator("//input[contains(@id,'device_0')]").click()  # Mantra device
    old_url = page.url
    page.locator("//input[contains(@name,'mantra')]").click()
    print("🖐️ Awaiting thumb impression... Please verify manually on device.")
    page.wait_for_function(f"() => location.href !== '{old_url}'", timeout=0)
    print("🔓 Biometric authentication successful.")

def navigate_to_shop_details(page):
    print("🏠 Navigating to home/dashboard...")
    old_url = page.url
    page.locator("//img[contains(@src,'home.png')]").click()
    page.wait_for_function(f"() => location.href !== '{old_url}'", timeout=0)
    print("📂 Hovering on 'Masters' menu...")
    page.locator("//a[contains(text(),'Masters')]").hover()
    print("📄 wait for visibility on 'Shop Details'...")
    # page.locator("//a[text()='Shop Details']").click()
    time.sleep(1)
    # page.wait_for_selector("//a[text()='Shop Details']", state="visible")
    # page.locator("//a[contains(text(),'Acts')]").nth(0).click()
    print("🔗 Clicking 'Shop Details' section...")
    page.locator("//*[contains(text(),'Ration Issue through')]").nth(0).click()

    print("✅ 'Shop Details' section opened.")

def select_ration_issue_option(page):
    print("📦 Selecting 'Ration Issue through' option...")
    ration_xpath = "//*[contains(text(),'Ration Issue through')]"
    page.wait_for_selector(ration_xpath)
    page.locator(ration_xpath).click()
    print("✅ 'Ration Issue through' option selected.")

def apply_filters(page):
    print("🔍 Applying filters...")
    old_url = page.url
    page.locator("//input[contains(@id,'card_type_0')]").click()
    time.sleep(0.5)
    page.wait_for_function(f"() => location.href !== '{old_url}'", timeout=0)
    page.locator("//input[contains(@id,'rbl_card_type_0')]").click()
    print("✅ Filters applied.")

    # enter ration card nyumber
    page.locator("//input[contains(@name,'txt_rc_no')]").fill("220500201201")
    page.locator("//select[contains(@name,'mems_detls')]").click()
    options = page.locator("//select[contains(@name,'mems_detls')]/option").all_inner_texts()

    print(f"available options are {options}")

    if len(options) == 2:
        page.locator("//select[contains(@name,'mems_detls')]").select_option(value=options[1])
        page.locator("//input[contains(@name,'btn_mbrs')]").click()
    else:
        time.sleep(10)
        print("write logic for more than 2 options")
        print("⏳ Waiting until you manually click the 'btn_mbrs' button...")

        page.wait_for_function("""
            () => {
                const btn = document.querySelector("input[name*='btn_mbrs']");
                return btn && btn.getAttribute('data-clicked') === 'true';
            }
        """, timeout=0)

        print("✅ Button was clicked manually!")

    page.locator("//input[contains(@id,'auth_type_2')]").click()
    page.locator("//input[contains(@id,'RadioButtonList1_0')]").click()
    page.locator("//input[contains(@id,'single_multiple_0')]").click()  # Mantra device
    page.locator("//input[contains(@id,'rdbldevice_0')]").click()
    page.locator("//input[contains(@id,'btnmantra')]").click()


def wait_forever():
    print("⏳ Waiting forever (manual pause). Press Ctrl+C to exit...")
    while True:
        time.sleep(1000)

# === Main Execution ===
with sync_playwright() as p:
    print("🚀 Starting browser...")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    open_login_page(page)
    new_url = enter_mobile_number(page, "9986347891")
    select_authentication(page)
    navigate_to_shop_details(page)
    apply_filters(page)

    # Debugger entry (optional):
    # import ipdb; ipdb.set_trace()

    wait_forever()

# Useful URLs:
# https://ahara.karnataka.gov.in/shopowner_mserver/admin/Disclaimer.aspx
# https://ahara.karnataka.gov.in/shopowner_mserver/main/MainMenu.aspx
