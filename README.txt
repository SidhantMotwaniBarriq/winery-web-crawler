# Wine Scraper

This project is a web scraping tool designed to extract winery and wine information from the Wine Folly website. It uses asynchronous crawling and LLM-based extraction strategies to gather structured data.

---

## Setup Instructions

1. **Clone the Repository**  
   Clone this repository to your local machine.

2. **Install Dependencies**  
   Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**  
   Create a `.env` file in the root directory (if not already present) and add the required API keys:
   ```
   Example:
   GROQ_API_KEY=<your_groq_api_key>
   ```

---

## Codebase Overview

### Key Files

1. **`winery-main.py`**  
   - Entry point for the application.
   - Allows users to choose between crawling "wineries" or "wines" and the specified region by requesting details when called.
   - Outputs JSON files containing the extracted links.

2. **`winery-scrape.py`**  
   - !!! Under development - LLM strategy is not working as expected !!!
   - Implements LLM-based extraction strategies for the specified links.
   - Allows users to choose between crawling "wineries" or "wines" and the specified region by requesting details when called.
   - Handles extraction and saves winery or wine data.

3. **`.env`**  
   - Stores API keys for external services.

4. **`requirements.txt`**  
   - Lists the Python dependencies required for the project.

5. **`cumulate.py`**  
   - Gets the total data size.

---

## Running the Scraper

1. **Crawling Wineries**  
   Run the `winery-main.py` script and select the `wineries` operation. Enter the desired region (e.g., `napa` or `paso`).  
   Example:
   ```bash
   Enter the region: napa
   Enter the operation (wineries or wines): wineries
   ```
   Output: A JSON file named `winery_links_<region>.json` containing winery links.

2. **Crawling Wines**  
   Run the `winery-main.py` script and select the `wines` operation. Enter the desired region.  
   Example:
   ```bash
   Enter the region: napa
   Enter the operation (wineries or wines): wines
   ```
   Output: A JSON file named `winery-data-<region>.json` containing wine details.

3. **Extracting Data**  
   Run the `winery-scrape.py` script with similar operation inputs (after generating the JSON files from the `winery-main.py` script).  
   Output: Extracted data from the specified links in JSON format.

---

## Output Explanation

- **Winery Links JSON (`winery_links_<region>.json`)**  
  Contains a list of winery URLs for the specified region.

- **Wine Data JSON (`winery-data-<region>.json`)**  
  Contains structured data for each winery, including name, location, website, contact, and established year.

---

