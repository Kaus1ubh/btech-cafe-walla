"""Screenshots and behaviour checks for both versions, using the installed Edge.
Run with the local server on :5197 (python -m http.server 5197 -d <repo>)."""
import pathlib
from playwright.sync_api import sync_playwright

BASE = "http://localhost:5197"
OUT = pathlib.Path(__file__).parent / "shots"
OUT.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge")
    desk = browser.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
    phone = browser.new_context(**p.devices["iPhone 13"])

    def shot(ctx, path, name, full=True, before=None):
        page = ctx.new_page()
        errors = []
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        page.goto(BASE + path, wait_until="networkidle")
        if before:
            before(page)
        page.screenshot(path=str(OUT / f"{name}.png"), full_page=full)
        over = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        print(f"{name}: horizontal overflow {over}px, console errors {len(errors)}")
        return page

    shot(desk, "/index.html", "00-chooser")
    # Version 1 (AI)
    shot(desk, "/ai-version/index.html", "v1-home-desktop")
    shot(phone, "/ai-version/index.html", "v1-home-phone", full=False)
    shot(desk, "/ai-version/menu.html", "v1-menu-desktop")
    shot(desk, "/ai-version/about.html", "v1-about-desktop")

    def ai_order(page):
        page.fill("#qty", "3")
        page.dispatch_event("#qty", "input")
        print("  v1 total for 3 cappuccinos:", page.inner_text("#total"))
        page.fill("#qty", "-4")
        page.dispatch_event("#qty", "input")
        print("  v1 total for -4:", page.inner_text("#total"))
        page.fill("#qty", "3")
        page.dispatch_event("#qty", "input")
        msgs = []
        page.on("dialog", lambda d: (msgs.append(d.message), d.accept()))
        page.click(".btn")
        print("  v1 empty-name submit alert:", msgs)
        page.fill("#qty", "3")
        page.dispatch_event("#qty", "input")
    shot(desk, "/ai-version/contact.html", "v1-order-desktop", before=ai_order)

    # Version 2 (fixed)
    shot(desk, "/fixed/index.html", "v2-home-desktop")
    shot(phone, "/fixed/index.html", "v2-home-phone", full=False)
    shot(phone, "/fixed/menu.html", "v2-menu-phone")
    shot(desk, "/fixed/about.html", "v2-about-desktop")

    def bad_order(page):
        page.click("button[type=submit]")
        print("  v2 empty submit errors:", page.inner_text("#items-error"), "|", page.inner_text("#name-error"))
        page.fill("#q-masala", "-4")
        print("  v2 -4 snaps to:", page.input_value("#q-masala"))
        page.fill("#q-masala", "2")
        page.fill("#q-cheesemaggi", "1")
        page.fill("#phone", "12345")
        page.fill("#time", "23:30")
        page.click("button[type=submit]")
        print("  v2 bad phone/time:", page.inner_text("#phone-error"), "|", page.inner_text("#time-error"))
    shot(desk, "/fixed/order.html", "v2-order-errors", before=bad_order)

    def good_order(page):
        page.fill("#q-masala", "2")
        page.fill("#q-cheesemaggi", "1")
        page.fill("#q-cold", "1")
        print("  v2 total:", page.inner_text("#total"))
        page.fill("#name", "Shaurya")
        page.fill("#phone", "98765 43210")
        page.fill("#time", "16:30")
        page.click("button[type=submit]")
        print("  v2 done:", page.inner_text("#done-text"))
    shot(phone, "/fixed/order.html", "v2-order-done-phone", before=good_order)

    browser.close()
