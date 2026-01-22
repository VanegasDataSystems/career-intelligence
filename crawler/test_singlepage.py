
from playwright.sync_api import sync_playwright

url = "https://remoteok.com/remote-jobs/remote-senior-software-development-engineer-devops-equip-health-1129690"

def main():
    with sync_playwright() as r:
        browser = r.chromium.launch(headless = True)
        page = browser.new_page()

        page.goto(url, timeout = 100000)

        page.wait_for_selector("div.description")

        # only interested in markdown
        markdown = page.query_selector("div.description div.markdown")

        if markdown is None:
            print("No description found")  # got take care of some error to balance rows later
        else:
            dt = markdown.inner_text().strip()
            print(dt[:3000])

        browser.close()

if __name__ == "__main__":
    main()