from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
import tldextract

# Extract base domain and TLD
def extract_base_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

# Function to check if a link is internal (inner) or external (outer)
def is_internal(link_url, base_url, base_domain):
    if not link_url:
        return False
    parsed_link = urlparse(urljoin(base_url, link_url))
    link_base_domain = extract_base_domain(parsed_link.netloc)
    return link_base_domain == base_domain

# Extract structured data into JSON and determine internal vs external links
def extract_texts_and_links(soup, base_url, base_domain):
    elements = []
    text_count = 0
    inner_link_count = 0
    outer_link_count = 0
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'a']):
        text_content = element.get_text(strip=True)
        link = element.get('href')
        if element.name == 'a' and link:
            is_inner = is_internal(link, base_url, base_domain)
            link_type = 'inner' if is_inner else 'outer'
            if is_inner:
                inner_link_count += 1
            else:
                outer_link_count += 1
            elements.append({
                'type': 'link',
                'content': text_content,
                'href': link,
                'tag': element.name,
                'link_type': link_type
            })
        else:
            elements.append({
                'type': 'text',
                'content': text_content,
                'tag': element.name
            })
            text_count += 1
    return elements, text_count, inner_link_count, outer_link_count

# Extract form data
def extract_forms(soup, base_url):
    forms = []
    for form in soup.find_all('form'):
        form_action = form.get('action') or ''
        form_action_full = urljoin(base_url, form_action) if form_action else ''
        form_method = form.get('method', 'GET').upper()
        form_inputs = []

        for input_element in form.find_all(['input', 'select', 'textarea']):
            input_type = input_element.get('type', 'text')
            input_name = input_element.get('name', '')
            form_inputs.append({
                'type': input_type,
                'name': input_name
            })

        # Find submit buttons
        submit_buttons = [
            {'type': 'submit', 'value': btn.get('value', ''), 'name': btn.get('name', '')}
            for btn in form.find_all(['input', 'button']) if btn.get('type') == 'submit'
        ]
        forms.append({
            'action': form_action_full,
            'method': form_method,
            'inputs': form_inputs,
            'submit_buttons': submit_buttons
        })
    return forms

# Extract table data
def extract_tables(soup):
    tables = []
    for table in soup.find_all('table'):
        rows = []
        for row in table.find_all('tr'):
            columns = [col.get_text(strip=True) for col in row.find_all(['th', 'td'])]
            rows.append(columns)
        tables.append({'rows': rows})
    return tables

# Extract metadata (title, description, etc.)
def extract_metadata(soup, base_url):
    title = soup.title.string if soup.title else ''
    description = ''
    for meta in soup.find_all('meta'):
        if meta.get('name', '').lower() == 'description':
            description = meta.get('content', '')
            break
    return {
        'title': title.strip() if title else '',
        'description': description.strip() if description else '',
        'url': base_url
    }

# The primary function to handle the content extraction
def extract_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()

        base_domain = extract_base_domain(url)
        structured_content, text_count, inner_link_count, outer_link_count = extract_texts_and_links(soup, url, base_domain)
        forms_data = extract_forms(soup, url)
        tables_data = extract_tables(soup)
        metadata = extract_metadata(soup, url)

        return {
            "summary": {
                "total_text_items": text_count,
                "total_inner_links": inner_link_count,
                "total_outer_links": outer_link_count,
                "total_forms": len(forms_data),
                "total_tables": len(tables_data),
                "metadata": metadata
            },
            "content": structured_content,
            "forms": forms_data,
            "tables": tables_data
        }
    except requests.RequestException as e:
        return {"error": f"Failed to fetch URL. Error: {str(e)}"}
