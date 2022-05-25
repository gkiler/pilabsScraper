# PiLabs Medical Information Scraper

### By Gwen Kiler and Ivan Neto

---

## Table of contents

1. [Introduction](#Introduction)
2. [Setup](#Setup)
    - [Step 1: Create Virtual Environment](#SetupStep1)
    - [Step 2: Access Virtual Environment](#SetupStep2)
    - [Step 3: Install Packages](#SetupStep3)
3. [Writing Parser](#ParserTutorial)
4. [Modification](#Modification)
    - [Step 1: Create Parser](#ModifyStep1)
    - [Step 2: Create Parser Thread](#ModifyStep2)
    - [Step 3: Add Thread to `main.py`](#ModifyStep3)
5. [Run Program](#Run)

### Introduction <a name="Introduction"></a>

This project was created to assist individuals in web-scraping. It provides the basic structure by which to organized threaded web-scraping.

For many projects there needs to be some multi-processing involved in web-scraping due to the inordinate amount of time it would be needed to scrape large amounts of data from several websites. Thus, we created this to help modularize this process.

**\*\*Note: This tutorial assumes a working Windows 10 environment.**

### Setup <a name="Setup"></a>

**Step 1**: Create `virtualenv` environment. Run the `virtualenv` package. For installation of `virtualenv` visit https://virtualenv.pypa.io/en/latest/installation.html. We recommend installation through `pip`. <a name="SetupStep1"></a>
```bash
(base) PS C:\documents\project> virtualenv venv
```

**Step 2**: Access your virtual environment named `venv`. <a name="SetupStep2"></a>
```
(base) PS C:\documents\project> ./venv/Scripts/activate
```
You should see:
```
(venv) PS C:\documents\project>
```

**Step 3**: Install required packages. <a name="SetupStep3"></a>
- `beautifulsoup4` - https://pypi.org/project/beautifulsoup4/
- `requests` - https://docs.python-requests.org/en/latest/
- `lxml`- https://lxml.de/
```
(venv) PS C:\documents\project> pip install beautifulsoup4
(venv) PS C:\documents\project> pip install requests
(venv) PS C:\documents\project> pip install lxml
```

### How to write parser <a name="ParserTutorial"></a>

\<Insert Gwen's Parser Tutorial. Please include the modularization (how to create parser class, what method to override, etc).\>
(First draft)

Follow template in scrapeTemplate.py, replacing <var> as needed.
A number of for loops is needed equal to as many pages deep the scraper must iterate through.
For the template, it assumes a first index list, then a sub index of Aa Ab Ac and so on. This can be adjusted by removing the subletter loop and adjusting variable names in the deeper for loop accordingly.
    
Note: This template only works if the given website has an alphabetized index.


### How to modify <a name="Modification"></a>

**Step 1**: Create your parser. <a name="ModifyStep1"></a>

You can follow the "[How to write parser](#ParserTutorial)" section to create your parser.

**Step 2**: Create a WebsiteThread class. <a name="ModifyStep2"></a>

This program works by placing each individual website into a different thread, through inheritance of the Thread class.

Navigate to `~/ClientThreads/ClientThreads.py`. It should look like the following:

```python
from threading import Thread

# Scrapers
from scrapers.DrugsComScraper import DrugsComScraper
from scrapers.MayoclinicScraper import MayoclinicScraper

# Clients
from clients.WebsiteClient import WebsiteClient

class MayoClinicThread(Thread):
    def run(self):
        print("[START] MayoClinicClient")
        mayoClinicClient = WebsiteClient(
            name="Mayoclinic",
            base_url="https://www.mayoclinic.org/",
            ext=["", "drugs-supplements", "drug-list?letter=A"],
            verbose=False
        ).run(MayoclinicScraper)
        print("[END] MayoClinicClient")

class DrugsComThread(Thread):
    def run(self):
        print("[START] DrugsComClient")
        drugsComClient = WebsiteClient(
            name="drugs.com",
            base_url="https://www.drugs.com",
            ext=["", "drug_information.html"],
            verbose=False
        ).run(DrugsComScraper)
        print("[START] DrugsComClient")
```

create your WebsiteThreading class. An example of one is already added by default in `ClientThreads.py`:

```python
class WikiThread(Thread):
    def run(self):
        # Empty for now
        pass
```

Populate WebsiteThread::run() by calling the `WebsiteClient` class with your desired website's specific information. Note that `ext`(url extensions) could possibly be empty, depending on how you originally defined your parser's parse() function on "[How to write Parser](#ParseTutorial)". **Note: Ensure that `etx` has an empty string element at the beginning**.

Your code will look like the following:

```python
class WikiThread(Thread):
    def run(self):
        print("[START] WikiClient")
        drugsComClient = WebsiteClient(
            name="Wikipedia",
            base_url="https://en.wikipedia.org/wiki/Medicine",
            ext=[""], # example of empty extensions
            verbose=False
        ).run(WikiScraper)
        print("[START] WikiClient")
```

Notice the `WikiScraper`, which is the class you defined in the "[How to write parser](#ParserTutorial)" section. Now your parser should be almost ready to run.

**Step 3**: Add your defined class to the `THREAD` list in `main.py`. <a name="ModifyStep3"></a>

Before:

```python
from ClientThreads.ClientThreads import *

THREADS = [DrugsComThread]

def main():
    # Runs every thread at the same time.
    for i in range(len(THREADS)):
        t = THREADS[i]()
        t.start()

if __name__ == "__main__":
    main()
```

After:

```python
from ClientThreads.ClientThreads import *

THREADS = [DrugsComThread, WikiThread]

def main():
    # Runs every thread at the same time.
    for i in range(len(THREADS)):
        t = THREADS[i]()
        t.start()

if __name__ == "__main__":
    main()
```

### How to run <a name="Run"></a>

Creating the parser and the modularization is the complicated part. To run we simply execute `main.py`:

```
(venv) PS C:\documents\project> python main.py
```
