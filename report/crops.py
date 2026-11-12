"""Tight screenshots of single elements for the report, plus the live 404."""
import pathlib
from playwright.sync_api import sync_playwright

BASE = "http://localhost:5197"
LIVE = "https://kaus1ubh.github.io/btech-cafe-walla"
OUT = pathlib.Path(__file__).parent / "shots"

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    desk = b.new_context(viewport={"width": 1280, "height": 800})
    phone = b.new_context(**p.devices["iPhone 13"])

    pg = desk.new_page()
    pg.goto(BASE + "/ai-version/menu.html", wait_until="networkidle")
    pg.locator(".menu-grid").screenshot(path=str(OUT / "c-v1-menu.png"))

    pg.goto(BASE + "/ai-version/about.html", wait_until="networkidle")
    pg.locator(".about-text").screenshot(path=str(OUT / "c-v1-about.png"))

    pg.goto(BASE + "/fixed/order.html", wait_until="networkidle")
    pg.click("button[type=submit]")
    pg.fill("#q-masala", "2")
    pg.fill("#q-cheesemaggi", "1")
    pg.fill("#q-cold", "1")
    pg.fill("#phone", "12345")
    pg.fill("#time", "23:30")
    pg.click("button[type=submit]")
    pg.locator("fieldset").nth(1).screenshot(path=str(OUT / "c-v2-errors.png"))
    pg.locator(".summary").screenshot(path=str(OUT / "c-v2-cart.png"))

    ph = phone.new_page()
    ph.goto(BASE + "/fixed/order.html", wait_until="networkidle")
    ph.fill("#q-masala", "2"); ph.fill("#q-cheesemaggi", "1"); ph.fill("#q-cold", "1")
    ph.fill("#name", "Shaurya"); ph.fill("#phone", "9876543210"); ph.fill("#time", "16:30")
    ph.click("button[type=submit]")
    ph.wait_for_timeout(600)
    ph.locator("#done").screenshot(path=str(OUT / "c-v2-done.png"))

    ph.goto(BASE + "/fixed/menu.html", wait_until="networkidle")
    ph.screenshot(path=str(OUT / "c-v2-menu-phone.png"))
    ph.goto(BASE + "/ai-version/index.html", wait_until="networkidle")
    ph.screenshot(path=str(OUT / "c-v1-home-phone.png"))
    ph.goto(BASE + "/fixed/index.html", wait_until="networkidle")
    ph.screenshot(path=str(OUT / "c-v2-home-phone.png"))

    live = desk.new_page()
    r = live.goto(LIVE + "/ai-version/Menu.html")
    print("live Menu.html status:", r.status)
    live.screenshot(path=str(OUT / "c-v1-404.png"))
    r = live.goto(LIVE + "/fixed/menu.html")
    print("live fixed menu status:", r.status)
    b.close()
