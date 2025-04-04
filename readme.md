# Menu Scraper

## What?

A python cli tool that scrapes html and transforms it into csv in for a very specific use case.

Feel free to use and customise as needed.

## Why?

One of my client's wanted to change the way their restaurant menu data was being managed for their website. The existing data model was so challenging that it was easier to scrape the frontend for the data
than it was to reverse engineer the existing data model.

## Usage

I use it this way,

```bash
# scrape data and cache locally as html files
python src/main.py scrape https://example.com

# parse html file and generate a csv file
python src/main.py parse \
  data/example-com-location-testing-menu-food.html 
  --output=one.csv

# merge many csv files into a single csv 
python src/main.py merge one.csv two.csv three.csv \
  --output=merged.csv

# or ... if there are many csv files
python -u src/main.py merge-batch \
  --find="data/*.csv" \
  --group-by=".+locations-(.+?)-menu-.+"
```

## Commands
Access via `python src/main.py --help`.

### scrape

Scrape menu data from a website.

- scrape menu data from a website using playwright
- generates one html file for each url
- saves the html file to the `data/` folder

Here's a basic description of what the playwright scraper is doing,

- vist the site url
- find top navigation
- click a Menus link in topnav
- on click topnav.Menus expect a flyout to appear
- flyout contains a list of menus grouped by region
- click each region
- for each location in region pluck the menu urls
- visit each menu url
- click each page of the menu
- save each page to an html file

### parse

Consumes html to generate csv.

- consume the html file to acquire menu data
- generates a csv file from the menu data
- saves csv to `data/` folder

For each model there is a corresponding `Parser` containing a bunch of static methods which are used to extract data from html using `selectolax`.

I use the following models and parsers,

- Menu -> MenuParser
- MenuCategory -> MenuCategoryParser
- MenuItem

MenuItem is a bit of a special case as there are many variations, so, I use a `MenuItemFactory` to select the appropriate `Parser`, but, the classes are,

- MenuItemFactory
- BaseMenuItemParser ( really just an interface )
- SimpleItemParser
- OptionGroupParser
- OptionItemParser
- AddonGroupParser
- AddonItemParser
- WineItemParser

### merge

Combines multiple csv into a single csv

### merge-batch

Combines unknown number of csv into single csv using a glob to locate source files and a regular expression with a single captured group as a tag for the merged output csv.

Usage,

```bash
python -u src/main.py merge-batch \
  --find="data/example-com-*.csv" \
  --group-by=".+locations-(.+?)-menu-.+"
```

For example, given a file list like,

```
data/example-com-locations-one-menu--drink.csv
data/example-com-locations-one-menu--food.csv
data/example-com-locations-one-menu--happy-hour.csv
data/example-com-locations-two-menu--drink.csv
data/example-com-locations-two-menu--food.csv
data/example-com-locations-two-menu--happy-hour.csv
data/example-com-locations-three-menu--drink.csv
data/example-com-locations-three-menu--food.csv
data/example-com-locations-three-menu--happy-hour.csv
```

The `--find="data/example-com*.csv` creates a list of files matching all of the above.

For each file in the list a dictionary of type `dict[str,list[str]]` is created by iterating the file list and grouping files under the match from the regex supplied
in `--group-by=".+locations-(.+?)-menu-.+"`.

In this case the matches would be,

```python
keys = ['one','two','three']
```

Which creates a dictionary like,

```python
dict = {
    "one":[
        'data/example-com-locations-one-menu--drink.csv',
        'data/example-com-locations-one-menu--food.csv',
        'data/example-com-locations-one-menu--happy-hour.csv',
    ],
    "two":[
        data/example-com-locations-two-menu--drink.csv',
        data/example-com-locations-two-menu--food.csv',
        data/example-com-locations-two-menu--happy-hour.csv',
    ],
    "three":[
        'data/example-com-locations-three-menu--drink.csv',
        'data/example-com-locations-three-menu--food.csv',
        'data/example-com-locations-three-menu--happy-hour.csv',
    ]
}
```

Finally one file named `merged_<key>.csv` is generated for each dictionary entry.

```python
merged_files = [
    'merged_one.csv',
    'merged_two.csv',
    'merged_three.csv',
]
```




