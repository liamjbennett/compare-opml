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
            modified_title = html.escape(title)

            modified_line = line.replace(title, modified_title)
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    with open(opml_file, "w") as f:
        f.writelines(modified_lines)

def compare_opml_files(existing_file, new_file):
    # Extract URLs from both files
    existing_urls = extract_xml_urls(existing_file)
    new_urls = extract_xml_urls(new_file)

    # Sort URLs in alphabetical order
    existing_urls.sort()
    new_urls.sort()

    # Find the URLs that appear in the new list but not in the existing list
    added_urls = set(new_urls) - set(existing_urls)

    return added_urls

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_opml.py existing.opml new.opml")
        sys.exit(1)

    existing_opml_file = sys.argv[1]
    new_opml_file = sys.argv[2]

    # Process both OPML files
    process_opml_file(existing_opml_file)
    process_opml_file(new_opml_file)

    added_urls = compare_opml_files(existing_opml_file, new_opml_file)
    missing_urls = compare_opml_files(new_opml_file, existing_opml_file)

    print('')
    print(f'URLs that do not appear in {existing_opml_file}:')
    if added_urls:
        for url in added_urls:
            print('  :: '+url)
    else:
        print('  None')

    print(f'URLs that do not appear in {new_opml_file}:')
    if missing_urls:
        for url in missing_urls:
            print('  :: '+url)
    else:
        print('  None')
