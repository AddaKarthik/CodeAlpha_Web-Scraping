import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://books.toscrape.com/"
all_books = []

for page in range(1, 51):  # There are 50 pages on the site
    print(f"Scraping page {page}...")
    response = requests.get(base_url.format(page), headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text.strip()
        availability = book.find('p', class_='instock availability').text.strip()
        rating_class = book.p['class'][1]  # e.g., 'One', 'Two', etc.
        all_books.append({
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating_class
        })

    time.sleep(1)  # Be polite and avoid getting blocked

# Save to CSV
df = pd.DataFrame(all_books)
df.to_csv('books.csv', index=False)
print("Scraping complete! Data saved to books.csv.")



import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('books.csv')

# Convert price to numeric
df['Price'] = df['Price'].str.replace('£', '').astype(float)

# Plot price distribution
plt.figure(figsize=(8, 5))
df['Price'].plot.hist(bins=30, color='skyblue', edgecolor='black')
plt.title('Book Price Distribution')
plt.xlabel('Price (£)')
plt.grid(True)
plt.show()

# Count of ratings
plt.figure(figsize=(7, 4))
df['Rating'].value_counts().plot(kind='bar', color='coral')
plt.title('Book Star Ratings')
plt.xlabel('Rating')
plt.ylabel('Number of Books')
plt.grid(True)
plt.show()
