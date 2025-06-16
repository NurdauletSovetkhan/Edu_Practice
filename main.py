import json
import re

nothing = None
# Our point to write 4 functions
# First one is to extract brand, model
# Second one is to extract price_value, currency, country_origin
# Third one is to extract color, weight_g, product_code
# Last one is prints or executes SQL INSERT statements

# SQL Insert must look like that:
# CREATE TABLE products (
#     id INT PRIMARY KEY,
#     brand TEXT,
#     model TEXT,
#     price_value DECIMAL(10,2),
#     currency CHAR(3),
#     country_origin TEXT,
#     color TEXT,
#     weight_g INT,
#     product_code TEXT
# );

def extract_brand_model(description):
    # Chech if description matches by pattern
    brand_match = re.search(r'^(.*?),?\s+model', description)
    # r'^(.*?),?\s+model'
    # ^ matches the start of the string
    # (.*?) lazily captures any characters as the brand name
    # ,? optionally matches a comma after the brand
    # \s+ matches one or more whitespace characters
    # model matches the literal word "model"
    model_match = re.search(r'model\s+([^\s.]+)', description)
    # 'model' matches the literal word "model"
    # '\s+'   matches one or more whitespace characters after it
    # '([^\s.]+)' captures one or more characters excluding space and dot as the model name

    brand = brand_match.group(1).strip() if brand_match else None
    model = model_match.group(1).strip() if model_match else None

    return brand, model

def extract_price_currency_country(description):
    # Search for the price value and currency (e.g., "Price: 123.45 USD")
    price_match = re.search(r'Price:\s*(\d+\.\d{2})\s*([A-Z]{3})?', description)
    price_value = float(price_match.group(1)) if price_match else None

    # Extract currency if present, otherwise default to 'USD'
    currency = price_match.group(2) if price_match and price_match.group(2) else 'USD'

    # Search for the country of origin (e.g., "Origin: Germany")
    country_match = re.search(r'Origin:\s*([^\.]+)', description)
    country_origin = country_match.group(1).strip() if country_match else None
    return price_value, currency, country_origin

def extract_color_weight_code(description):
    color_match = re.search(r'Color:\s*([^\.\n,]+)', description, re.IGNORECASE)
    weight_match = re.search(r'Weight:\s*(\d+)\s*g', description, re.IGNORECASE)
    code_match = re.search(r'(UPC|EAN|Product Code):\s*([A-Za-z0-9\-]+)', description, re.IGNORECASE)
    
    color = color_match.group(1).strip() if color_match else None
    weight_g = int(weight_match.group(1)) if weight_match else None
    product_code = code_match.group(2).strip() if code_match else None
    return color, weight_g, product_code

def parse_product(product):
    """
    Main parser function combining all extractions
    """
    desc = product['description']

    # First Function
    brand, model = extract_brand_model(desc)

    # Second Function
    price_value, currency, country_origin = extract_price_currency_country(desc)

    # Third Function
    color, weight_g, product_code = extract_color_weight_code(desc)

    return {
        'id': product['id'],
        'brand': brand,
        'model': model,
        'price_value': price_value,
        'currency': currency,
        'country_origin': country_origin,
        'color': color,
        'weight_g': weight_g,
        'product_code': product_code
    }

def generate_sql_insert(parsed_product):
    # IDK what I must write here
    return nothing

def main():
    # Open the JSON file and load its content
    with open("products_200.json", "r") as file:
        products = json.load(file)

    for product in products:
        parsed = parse_product(product)
        sql = generate_sql_insert(parsed)
        print(sql)

if __name__ == "__main__":
    main()
# This is the main entry point of the script
