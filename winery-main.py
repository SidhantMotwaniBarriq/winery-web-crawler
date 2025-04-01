import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
import json

def getBrowserConfig():
    try:
        return BrowserConfig(
            browser_type="chromium",  # Type of browser to simulate
            text_mode=True,
            headless=False,  # Run in headless mode to avoid GUI issues
            verbose=True  # Enable verbose logging if needed
        )
    except Exception as e:
        print(f"Error in browser configuration: {e}")
        raise

def getRunConfig():
    return CrawlerRunConfig(
        stream=True,
        verbose=True
    )

# main crawler function
async def run_basic_crawler(region):
    base_url = f"https://{region}.guides.winefolly.com/wineries/explore/"
    run_config = CrawlerRunConfig()   # Default crawl run configuration
    browser_config = BrowserConfig()  # Default browser configuration
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=base_url,
            config=run_config
        )
        # Extract only href values matching the desired pattern
    winery_links = [
            link['href'] for link in result.links.get('internal', [])
            if "/wineries/" in link['href'] and not link['href'].endswith("/wineries/explore/")
    ]
    print(f"Extracted {len(winery_links)} links")
    # Write winery_links to a file
    with open(f"winery_links_{region}.json", "w") as file:
        json.dump(winery_links, file, indent=4)
    print("Winery links saved to winery_links.json")

    return

async def run_wine_crawler(region):
    run_config = CrawlerRunConfig()   # Default crawl run configuration
    browser_config = BrowserConfig()  # Default browser configuration
    # Load winery links from the saved JSON file
    with open(f"winery_links_{region}.json", "r") as file:
        winery_links = json.load(file)

    # Initialize a dictionary to store wine links for all wineries
    wine_data = {}

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for link in winery_links:
            try:
                result = await crawler.arun(
                    url=link,
                    config=run_config
                )
                wine_links = [
                    link['href'] for link in result.links.get('internal', [])
                    if "/wines/" in link['href']
                ]
                # Extract winery name from the URL
                winery_name = link.split("/wineries/")[1].split("/")[0]
                # Add the winery and its wine links to the dictionary
                wine_data[winery_name] = wine_links
                print(f"Wine links collected for winery: {winery_name}")
            except Exception as e:
                print(f"Error crawling {link}: {e}")

    # Write the complete wine_data dictionary to the file
    with open(f"wine_links_{region}.json", "w") as file:
        json.dump(wine_data, file, indent=4)
    print(f"All wine links saved to wine_links_{region}.json")

async def main():
    # Prompt the user to enter a region
    region = input("Enter the region: ").strip().lower()
    operation = input("Enter the operation (wineries or wines): ").strip().lower()
    if operation=="wineries":
        await run_basic_crawler(region)
    elif operation=="wines":
        await run_wine_crawler(region)
    else:
        print("Invalid operation. Please enter 'wineries' or 'wines'.")
        return

if __name__ == "__main__":
    asyncio.run(main())  # Use asyncio.run here to execute the main coroutine
