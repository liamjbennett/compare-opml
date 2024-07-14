import sys
import xml.etree.ElementTree as ET
import html

def extract_xml_urls(opml_file):
    """
    Extract xmlUrl attributes from an OPML file and return a list of URLs.
    """
    tree = ET.parse(opml_file)
    root = tree.getroot()
    urls = []
    for outline in root.findall(".//outline"):
        url = outline.get("xmlUrl")
        if url:
            urls.append(url)
    return urls

def extract_category_urls(opml_file, category):
    """
    Return a list of URLs that have a given category
    """
    tree = ET.parse(opml_file)
    root = tree.getroot()
    urls = []
    for outline in root.findall(".//outline[@category='"+category+"']"):
        url = outline.get("xmlUrl")
        if url:
            urls.append(url)
    return urls

def extract_categories(opml_file):
    """
    Extract categories attributes from an OPML file
    """
    tree = ET.parse(opml_file)
    root = tree.getroot()
    categories = []
    for outline in root.findall(".//outline"):
        category = outline.get("category")
        if (category and (category not in categories)):
            categories.append(category)
    return categories

def is_escaped(s):
    """
    Checks if a string contains HTML entities (escaped characters).
    """
    return any(entity in s for entity in ('&', '<', '>', '"', "'"))

def process_opml_file(opml_file):
    """
    Process an OPML file, replace '&' in titles, and write modified content back.
    """
    with open(opml_file, "r") as f:
        lines = f.readlines()

    modified_lines = []
    for line in lines:
        if 'title="' in line:

            # Find the position of the title attribute
            title_start = line.find('title="') + len('title="')
            title_end = line.find('"', title_start)

            # Extract the title
            title = line[title_start:title_end]
            if is_escaped(title):
                modified_title = title
            else:
                modified_title = html.escape(title)
                

            modified_line = line.replace(title, modified_title)
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    with open(opml_file, "w") as f:
        f.writelines(modified_lines)

def compare_opml_urls(existing_file, new_file):
    # Extract URLs from both files
    existing_urls = extract_xml_urls(existing_file)
    new_urls = extract_xml_urls(new_file)

    # Sort URLs in alphabetical order
    existing_urls.sort()
    new_urls.sort()

    # Find the URLs that appear in the new list but not in the existing list
    added_urls = set(new_urls) - set(existing_urls)

    return added_urls

def compare_urls_with_category(existing_file, new_file, category):
    # Extract URLs from bo