import contentful
import csv


# Client setup

client = contentful.Client(
    '9cbraljlhlcw',
    'YrDMNhz0uvZ9CpB52dFX7r-p29eVUvKADqtErMYD4I0'
)


# Fetching data

content_type = "prodotto"
entries_it = client.entries({'content_type': content_type, 'locale': 'it'})
entries_en = client.entries({'content_type': content_type, 'locale': 'en'})


# Writing file

with open('products.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for it, en in zip(entries_it, entries_en):
        writer.writerow([it.nome, en.nome])
