import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, LLMExtractionStrategy, CacheMode
from crawl4ai import LLMExtractionStrategy, LLMConfig
from models.wine import Winery, Wine
import os
import json  # Add this import for reading from a file

def getBrowserConfig():
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        # text_mode=True,
        headless=False # Whether to run in headless mode (no GUI)
        # verbose=True,  # Enable verbose logging
    )

def getWineryRunConfig(llm_strategy):
    return CrawlerRunConfig(
        css_selector="section",
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
        # stream=True
        # verbose=True,
        exclude_external_images=True,
        exclude_external_links=True, 
    )

def getWineRunConfig(llm_strategy):
    return CrawlerRunConfig(
        css_selector="section",
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
        # stream=True
        # verbose=True,
        exclude_external_images=True,
        exclude_external_links=True, 
    )

def getWineLLMStrategy():
    return LLMExtractionStrategy(
        # llm_config=LLMConfig(
        #     provider="huggingface/facebook/bart-large-cnn",  # Change to your desired Hugging Face model
        #     api_token=os.getenv("HUGGINGFACE_API_KEY"),  # Ensure your API key is set
        # ),
        llm_config=LLMConfig(
            provider="groq/deepseek-r1-distill-llama-70b",  # Name of the LLM provider
            api_token=os.getenv("GROQ_API_KEY"),  # API token for authentication
        ),
        schema=Winery.model_json_schema(),  # JSON schema of the data model
        extraction_type="schema",  # Type of extraction to perform
        instruction=(
            "Extract details: 'name', 'year', 'region', 'type', "
            "'price', 'abv', 'ph', 'ta', 'rs', 'aging_notes'."
        ),  # Instructions for the LLM
        input_format="markdown",  # Format of the input content
        # verbose=True,  # Enable verbose logging
    )

def getWineryLLMStrategy():
    return LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="groq/deepseek-r1-distill-llama-70b",  # Name of the LLM provider
            api_token=os.getenv("GROQ_API_KEY"),  # API token for authentication
        ),
        schema=Wine.model_json_schema(),  # JSON schema of the data model
        extraction_type="schema",  # Type of extraction to perform
        instruction=(
            "Extract details: 'name', 'address', 'website', 'contact', "
            "'established'."
        ),  # Instructions for the LLM
        input_format="markdown",  # Format of the input content
        # verbose=True,  # Enable verbose logging
    )

async def run_winery_crawler(region):
    browser_config = getBrowserConfig()
    llm_strategy = getWineryLLMStrategy()
    run_config = getWineryRunConfig(llm_strategy)

    # Read winery_links from the file
    with open(f"winery_links_{region}.json", "r") as file:
        winery_links = json.load(file)

    print(f"Using {len(winery_links)} links")

    # Initialize a dictionary to store data for all wineries
    winery_data = {}

    # Use a single AsyncWebCrawler instance
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for link in winery_links[0:1]:
            try:
                result = await crawler.arun(url=link, config=run_config)
                print(f"Crawled {link}")
                print(result.extracted_content)

                # Parse extracted content if it is a string
                if result.success and isinstance(result.extracted_content, str):
                    extracted_content = json.loads(result.extracted_content)
                    for winery in extracted_content:
                        name = winery.get("name")
                        if name:
                            winery_data[name] = winery  # Use the entire winery object
                            winery_data[name].pop("error", None)  # Remove the "error" field if present
            except Exception as e:
                print(f"Error crawling {link}: {e}")
            await asyncio.sleep(2)

    # Write the complete winery_data dictionary to a file
    with open(f"winery-data-{region}.json", "w") as file:
        json.dump(winery_data, file, indent=4)
    print(f"All winery data saved to winery-data-{region}.json")

    llm_strategy.show_usage()

async def run_wine_crawler(region):
    browser_config = getBrowserConfig()
    llm_strategy = getWineLLMStrategy()
    run_config = getWineRunConfig(llm_strategy)

    # Read wine links from the file
    with open(f"wine_links_{region}.json", "r") as file:
        data = json.load(file)
        num_wineries = len(data)
        num_wines = sum(len(wines) for wines in data.values())

    print(f"Analyzing {num_wines} wines from {num_wineries} wineries")

    # Initialize a dictionary to store data for all wineries and their wines
    wine_data = {}

    # Use a single AsyncWebCrawler instance
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for winery, wines in data.items():  # Iterate over dictionary items
            wine_data[winery] = []  # Initialize a list for wines under each winery
            for wine in wines[0:1]:  # Iterate over the list of wine URLs
                try:
                    result = await crawler.arun(url=wine, config=run_config)
                    print(f"Crawled {wine}")
                    print(result.extracted_content)

                    # Parse extracted content if it is a string
                    if result.success and isinstance(result.extracted_content, str):
                        extracted_content = json.loads(result.extracted_content)
                        for wine_entry in extracted_content:
                            wine_entry.pop("error", None)  # Remove the "error" field if present
                        wine_data[winery].extend(extracted_content)  # Append wine data to the winery's list
                except Exception as e:
                    print(f"Error crawling {wine}: {e}")
                await asyncio.sleep(2)

    # Write the complete wine_data dictionary to a file
    with open(f"winefolly-data-{region}.json", "w") as file:
        json.dump(wine_data, file, indent=4)
    print(f"All wine data saved to wine-data-{region}.json")

    llm_strategy.show_usage()

async def main():
    # region = input("Enter the region (e.g., idaho): ").strip().lower()
    # operation = input("Enter the operation (wineries or wines): ").strip().lower()
    region = "idaho"
    operation = "wineries"
    if operation=="wineries":
        await run_winery_crawler(region)
    elif operation=="wines":
        await run_wine_crawler(region)
    else:
        print("Invalid operation. Please enter 'wineries' or 'wines'.")
        return

if __name__ == "__main__":
    asyncio.run(main())  # Use asyncio.run here to execute the main coroutine
