from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    # Find the table with id 'main-catalog'
    table = soup.find('table', id='main-catalog')
    if not table:
        print("Error: Could not find table with id 'main-catalog'")
        return []
    
    # Extract rows from tbody
    tbody = table.find('tbody')
    if not tbody:
        print("Error: Could not find tbody in table")
        return []
    
    rows = tbody.find_all('tr')
    products = []
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
        
        product_id = cols[0].text.strip()
        product_name = cols[1].text.strip()
        category = cols[2].text.strip()
        price_text = cols[3].text.strip()
        stock = cols[4].text.strip()
        rating = cols[5].text.strip()
        
        # Handle 'N/A' or 'Liên hệ' in the price column
        price_value = None
        if price_text not in ['N/A', 'Liên hệ']:
            # Extract numeric value from price like "28,500,000 VND"
            import re
            price_match = re.search(r'[\d,]+', price_text)
            if price_match:
                price_value = price_match.group().replace(',', '')
        
        # Create document for each product
        product_doc = {
            "document_id": f"html-{product_id}",
            "content": f"Product: {product_name}, Category: {category}, Price: {price_text}, Stock: {stock}, Rating: {rating}",
            "source_type": "HTML",
            "author": "VinShop",
            "timestamp": None,
            "tags": ["product", "catalog", category.lower()],
            "source_metadata": {
                "original_file": "product_catalog.html",
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "price_raw": price_text,
                "price_numeric": price_value,
                "stock": stock,
                "rating": rating
            }
        }
        products.append(product_doc)
    
    return products

