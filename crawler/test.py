from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()

        page.goto("https://example.com")

        heading = page.locator("h1").inner_text()
        para = page.locator("p").first.inner_text()
        title = page.title()

        print("Title", title)
        print("Paragraph", para)
        print("heading", heading)

        browser.close()

if __name__ == "__main__":
    main()