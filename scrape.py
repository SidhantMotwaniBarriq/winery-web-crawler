## This is a test file ##
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, LLMExtractionStrategy, CacheMode
from crawl4ai import LLMExtractionStrategy, LLMConfig
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy, BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter
from models.wine import Winery
import os

def getFilterChain():
    region = "idaho"
    # URL patterns to include
    return FilterChain([
        URLPatternFilter(patterns=[f"https://{region}.guides.winefolly.com/wineries/*/", f"https://{region}.guides.winefolly.com/wineries/*/wines/*/"]),
    ])

def getBrowserConfig():
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        text_mode =True,
        headless=False # Whether to run in headless mode (no GUI)
        # verbose=True,  # Enable verbose logging
    )

def getDeepCrawlStrategy(filter):
    return BFSDeepCrawlStrategy(
            max_pages=5, # Limit the number of pages to crawl (tmp)
            max_depth=1, # depth of crawl
            include_external=False,
        )

def getRunConfig(filter, llm_strategy):
    return CrawlerRunConfig(
        deep_crawl_strategy= getDeepCrawlStrategy(filter),
        extraction_strategy=llm_strategy,
        # cache_mode=CacheMode.BYPASS,
        stream=True
        # verbose=True
    )

def getLLMStrategy():
    return LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="groq/deepseek-r1-distill-llama-70b",  # Name of the LLM provider
            api_token=os.getenv("GROQ_API_KEY"),  # API token for authentication
        ),
        schema=Winery.model_json_schema(),  # JSON schema of the data model
        extraction_type="schema",  # Type of extraction to perform
        instruction=(
            "Extract winery details: 'name', 'location', 'website', 'contact', "
            "'established'."
        ),  # Instructions for the LLM
        input_format="markdown",  # Format of the input content
        verbose=True,  # Enable verbose logging
    )

def dsiplay_results(results):
    print(f"Crawled {len(results)} pages")
    # Group by depth and print the number of pages crawled
    depth_counts = {}
    for result in results:
        depth = result.metadata.get("depth", 0)
        depth_counts[depth] = depth_counts.get(depth, 0) + 1
    print("Pages crawled by depth:")
    for depth, count in sorted(depth_counts.items()):
        print(f"  Depth {depth}: {count} pages")

def display_model_results(results):
    print(f"\nCrawled {len(results)} wineries:")
    for idx, winery in enumerate(results, start=1):
        print(f"\nWinery {idx}:")
        print(f"  Name: {winery.name}")
        print(f"  Location: {winery.location}")
        print(f"  Website: {winery.website}")
        print(f"  Contact: {winery.contact}")
        print(f"  Established: {winery.established}")
        print(f"  Description: {winery.description}")
    print("\nCrawl completed.")

#main crawler function
async def run_advanced_crawler():
    base_url = "https://idaho.guides.winefolly.com/wineries/explore/"
    #setup the config
    filter = getFilterChain()
    browser_config = getBrowserConfig()
    llm_strategy = getLLMStrategy()
    run_config = getRunConfig(filter, llm_strategy)
    results = []

    # Execute the crawl
    async with AsyncWebCrawler(config = browser_config) as crawler:
        async for result in await crawler.arun(base_url, config=run_config):
            # Wait for each result to complete before proceeding
            # if result.success:
            #     results.append(result)
            #     depth = result.metadata.get("depth", 0)
            #     print(result.markdown)
            #     print(f"Depth: {depth} | {result.url} | {result.status_code}")
            # else: 
            #     print("Error:", result.error_message)
            # print(result)
            if result.success:
                winery_data = result.extracted_data  # Assuming LLMExtractionStrategy populates this field
                if winery_data:
                    try:
                        # Validate and create Winery model instance
                        winery = Winery(**winery_data)
                        results.append(winery)
                        print(f"Extracted Winery: {winery}")
                    except Exception as e:
                        print(f"Error creating Winery model: {e}")
                else:
                    print("No data extracted by LLM.")
            else:
                print("Error:", result.error_message)
            
    # dsiplay_results(results)
    display_model_results(results)

if __name__ == "__main__":
    asyncio.run(run_advanced_crawler())

##current state:
#scraping winereie/idaho/explore  
#results printing as raw maredown
#currently no filters on content type or domain
#limitied to 5 pages and depth 1.

##next steps:
#1. look at output and possible formats
#2. check important info from winery page to be fetched
#3. fetch info for wineries
#4. format info for winery into json object
#5. look into scraping info re. wines per winery (winefolly itself)
