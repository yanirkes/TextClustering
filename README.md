# Patent Claim Scraper and Web Cluster
This project provides an interactive web-based tool designed to scrape patent
claims from multiple URLs, process and clean the text, and allow users
to interact with an intuitive UI for grouping patent claims. The app uses a
Kmeans clustering model in the backend to intelligently group patent 
claims into topics based on their content.

# Features 
* Interactive UI: Users can specify the number of patent groups they want to view directly through the web interface.
* Web Scraping: Scrapes claims from various patent URLs using requests and BeautifulSoup.
* Text Processing: Cleans and processes the scraped claims using various NLP techniques, such as removing list numbers, standardizing claim references, and eliminating unnecessary text elements.
* Clustering and Grouping: Uses a Kmeans clustering model to group patent claims by topic, allowing users to specify the number of groups they wish to view.


# Installation
1. Clone the repository:
```python
git clone https://github.com/yanirkes/TextClustering.git
cd TextClustering

```

2. Create a virtual environment (optional but recommended):
```python
python3 -m venv venv # On Windows: virtualenv --python python3 -m venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install the required dependencies:
```python
pip install -r requirements.txt
```

4. Additionally, download the necessary NLTK data files:

```python
python -m nltk.downloader stopwords punkt
```

# How to Use
## 1.  **Prepare URLs to Scrape** 
In the script there are urls ready to be scraped, you can replace them with your own. 

```python
urls = [
    "https://patents.google.com/patent/GB2478972A/en?q=(phone)&oq=phone",
    "https://patents.google.com/patent/US9634864B2/en?oq=US9634864B2",
    "https://patents.google.com/patent/US9980046B2/en?oq=US9980046B2"
]
```
You can modify this list with other patent URLs from Google Patents.

## 2. **Run the Scraping Script**
You can check the functionality of the scrapper by running the script. Once you have
the URLs set, run the script to scrape the patent claims:

```python
```python
cd scrape
python scrapping.py
```

Otherwise, you can download the save data located at the data directory named 'claims_text.csv'.

## 3. **Review Output**
The claims will be saved as a CSV file in the data/ directory with the filename claims_text.csv.

## 4. **Run the App**

The app will be launched in your browser, after tuning the following in the terminal:

```python
cd ../ # Go back to the root directory
cd src
python app.py
```

Open the given URL on you local browser, and start using.

# File Structure

```bazaar
patent-claim-scraper/
│
├── data/                   # Directory for saving scraped claims as CSV files
│
├── scrppe/          
├──── scraping.py            # Main script to scrape patent claims
│
├── src/     
│        
├──── app.py                # Main script to run the application
│
├── model/   
│          
├──── my_model.py           # Model class for clustering
│
├── README.md               # This README file
│
└── Moveo_task_model_analysis.ipynb.txt        # Python dependencies for the project
│
└── requirements.txt        # Python dependencies for the project

```

