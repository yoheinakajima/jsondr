# JSONDR (JSON Doctor) 🩺

Welcome to JSONDR, your friendly tool to convert any webpage to JSON. Whether you need structured data for analysis or to collect links for your next web project, JSONDR has you covered.

## Table of Contents
- [Overview](#overview)
- [Using JSONDR Directly](#using-jsondr-directly)
- [Using jsondr.py](#using-jsondr-py)
- [Development and Contributions](#development-and-contributions)

## Overview

JSONDR allows you to effortlessly convert web pages to JSON data by simply adding a prefix to any URL. Inspired by Jina's reader, JSONDR was built specifically to handle web data in a structured format.

## Using JSONDR Directly

To use JSONDR directly, follow these steps:

1. Copy any URL of your choice.
2. Add the prefix `jsondr.com/` to the URL, like so: `jsondr.com/[your-url]`.
3. Replace `[your-url]` with the actual website link, e.g., `jsondr.com/untapped.vc`.
4. Paste the updated link in your browser and see the data presented in JSON format.

This is an easy and efficient way to grab links, texts, and metadata from any static webpage.

## Using jsondr.py

If you'd like to integrate JSONDR directly into your Python projects, you can utilize `jsondr.py`. Here’s how:

1. **Clone or Download**: Clone this repository or copy `jsondr.py` into your project.
2. **Import and Use**:
    ```python
    import jsondr

    # Example usage
    url = 'http://example.com'
    extracted_data = jsondr.extract_content(url)
    print(extracted_data)
    ```

3. **Functions Overview**:
    - `extract_content(url)`: Main function that returns all extracted data (text, links, forms, tables, and metadata) as JSON.
    - `extract_metadata(soup, base_url)`: Extracts the title, description, and other metadata of the page.
    - `extract_texts_and_links(soup, base_url, base_domain)`: Extracts all text elements and links from the page.
    - `extract_forms(soup, base_url)`: Extracts form elements on the page.
    - `extract_tables(soup)`: Extracts table data from the page.

## Development and Contributions

We're open to contributions that improve the project! If you'd like to contribute or suggest features, follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Open a pull request with a clear description.

Thank you for your interest in JSONDR! Feel free to reach out with any questions or issues.
