import os
import configparser
import sys
class palette():
    def __init__(self,pdata):
        self.name = pdata[0]
        self.pants = pdata[1][0]
        self.shirt = pdata[1][1]
        self.gloves = pdata[1][2]
        self.shoes = pdata[1][3]
        self.hair = pdata[1][4]
        self.skin = pdata[1][5]
        self.cap = pdata[1][6]
        self.emblem = pdata[1][7]

    def set_pants(self, rgb):
        self.pants = rgb

    def set_shirt(self, rgb):
        self.shirt = rgb

    def set_gloves(self, rgb):
        self.gloves = rgb

    def set_shoes(self, rgb):
        self.shoes = rgb

    def set_hair(self, rgb):
        self.hair = rgb

    def set_skin(self, rgb):
        self.skin = rgb

    def set_cap(self, rgb):
        self.cap = rgb

    def set_emblem(self, rgb):
        self.emblem = rgb
    def print(self):
        s = ""
        c = []
        for i in range(8):
            match i:
                case 0:
                    s = "pants"
                    c = self.pants
                case 1:
                    s = "shirt"
                    c = self.shirt
                case 2:
                    s = "gloves"
                    c = self.gloves
                case 3:
                    s = "shoes"
                    c = self.shoes
                case 4:
                    s = "hair"
                    c = self.hair
                case 5:
                    s = "skin"
                    c = self.skin
                case 6:
                    s = "cap"
                    c = self.cap
                case 7:
                    s = "emblem"
                    c = self.emblem
            printRGB(f"{self.name}'s {s}", c)
 
def printRGB(s,c):
    print(f'\x1b[38;2;{c[0]};{c[1]};{c[2]}m' + s + '\x1b[0m')
    
def get_palette_list():
    items = os.listdir('.')
    files = [item.split(".")[0] for item in items if os.path.isfile(item) and item.endswith(".ini")]
    return files       
    
def read_ini_pairs(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    pairs = []
    c = 0
    m = 0
    for section in config.sections():
        triple = []
        for key, value in config.items(section):
            c+=1
            m = c%3
            if m == 0:
                triple.append(value)
                pairs.append(triple)
                triple = []
            else:
                triple.append(value)
    return pairs
import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.html_content = None
        self.soup = None
        self.fetch_html()
        self.parse_html()

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.html_content = response.text
            #print("HTML content fetched successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the HTML content!: {e}")
    
    def parse_html(self):
        if self.html_content:
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
            print("HTML content parsed successfully.")
        else:
            print("No HTML content to parse. Please fetch HTML first.")

    def get_elements_by_tag(self, tag_name):
        if self.soup:
            return self.soup.find_all(tag_name)
        else:
            print("No parsed HTML found. Please parse HTML first.")
            return []

    def get_elements_by_class(self, tag_name, class_name):
        if self.soup:
            return self.soup.find_all(tag_name, class_=class_name)
        else:
            print("No parsed HTML found. Please parse HTML first.")
            return []

    def get_element_text(self, tag_name, class_name=None):
        if self.soup:
            element = self.soup.find(tag_name, class_=class_name)
            return element.get_text(strip=True) if element else None
        else:
            print("No parsed HTML found. Please parse HTML first.")
            return None

def get_codes(scraper):
    z = []
    y = scraper.get_elements_by_tag("td")
    for i in y:
        try:
            n = str(i).index("(")
        except:
            n = -1
        if n!=-1:
            p = str(i).removeprefix("<td>(")
            i = str(p).removesuffix(")</td>")
            z.append(i)
    return z

def parse_numbers(strings):
    result = []
    for s in strings:
        numbers = list(map(int, s.split(',')))
        result.append(numbers)
    return result
 
    
x = []
for name in get_palette_list():
    palette_data = [name,read_ini_pairs(f"{name}.ini")]
    x.append(palette(palette_data))

def create_palette_ini_from_list(filename, color_values):
    config = configparser.ConfigParser()
    
    config['PALETTE'] = {}
    
    color_names = ["PANTS", "SHIRT", "GLOVES", "SHOES", "HAIR", "SKIN", "CAP", "EMBLEM"]
    
    for i, name in enumerate(color_names):
        r, g, b = color_values[i]
        config['PALETTE'][f"{name}_R"] = str(r)
        config['PALETTE'][f"{name}_G"] = str(g)
        config['PALETTE'][f"{name}_B"] = str(b)
    
    with open(filename, 'w') as configfile:
        config.write(configfile)
    print(f"{filename} has been created successfully.")

arguments = sys.argv
x = len(arguments)
print(arguments)
url = ""
if x == 1:
    print("This software requires a Pallete URL from the website color-hex.com")
    url = input("Please input a url: ")
elif x == 2:
    url = arguments[1]
    
scraper = WebScraper()
u = scraper.get_elements_by_tag("title")
v = str(u).lower()
u = v.removesuffix(" color palette</title>]")
name = u.removeprefix("[<title>")
cc = parse_numbers(get_codes(scraper))
create_palette_ini_from_list(f"{name.removeprefix("<title>")}.ini", [cc[0],cc[1],cc[2],cc[3],cc[4],[199,146,100],cc[1],cc[1]])