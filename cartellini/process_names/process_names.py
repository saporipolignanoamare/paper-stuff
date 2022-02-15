import csv

### VARIABLES

csvPath = '/Users/bbtgnn/Desktop/cartellini/get_products/products.csv'

toExclude = [
    "nere inchiostro",
    "rondelle",
    "da aperitivo a rondelle",
    "siciliane",
    "inchiostro snocciolate",
    "greche snocciolate",
    "ceci",
    "brasiliane",
    "fritte intere",
    "brasiliane sgusciate",
    "anacardi",
    "borettane",
    "trifolati",
    "capperi da aperitivo",
    "capperi grossi",
    "friselle",
    "acciughe"
]


### INSTRUCTIONS


# Saving names in list

names = []

with open(csvPath) as f:
    reader = csv.reader(f)
    for row in reader:
        names.append(row)


# Excluding names

filteredNames = []

for entry in names:
    add = True
    for s in toExclude:
        if s.lower() in entry[0].lower():
            add = False
            break
    if add:
        filteredNames.append(entry)


# Writing file

with open('products-processed.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(filteredNames)

# # Shortening names

# shortenedNames = []

# for entry in filteredNames:
#     shortenedEntry = []
#     for lan in entry:
#         newLan = lan.lower()
#         for r in toRemove:
#             if r in newLan:
#                 newLan = newLan.replace(r, "")
#         newLan = newLan.replace("  ", " ").strip().capitalize()
#         shortenedEntry.append(newLan)
#     shortenedNames.append(shortenedEntry)

# print(shortenedNames)
