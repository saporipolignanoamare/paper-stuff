import csv
from posixpath import split

# --- VARIABLES --- #

csvPath = "/Users/bbtgnn/Desktop/cartellini/process_names/products-processed-hand.csv"

page_w = 7000
page_h = 10000
page_m = 150

rows = 13
cols = 5


c_page = (1, 1, 1)

product_f = 'Affogato-Medium'
product_f_lh = 1
product_c_it = (0, 0, 0)
product_c_en = (0, 0, 0, 0.6)
product_gap = 30

card_m = 55
card_m_r = card_m

price_w = 380
price_m_h = 50
price_m_v = card_m
price_c_bg = (0.5, 0.5, 0)
price_c_fg = (1, 1, 1)
price_txt_unit = '€/100g'
price_txt_unit_f = 'Affogato-Bold'
price_txt_brand = "Sapori"
price_txt_brand_f = 'Affogato-Regular'
price_box_r = 40

fs_base = 100
fs_increase = 3
lh_increase = 0.002

# --- FUNCTIONS --- #

# UTILITY FUNCTIONS


def roundedRect(x, y, w, h, r):

    # helper variable (diameter)
    d = 2*r

    # error handling
    if d > w or d > h:
        raise Exception(
            "The rounding radius is greater than one of the sides!")

    # Drawing corners
    for i in (0, 1):
        for j in (0, 1):
            corner_x = x + (w-d) * i
            corner_y = y + (h-d) * j
            oval(corner_x, corner_y, d, d)

    # Horizontal rect
    hor_h = h - 2*r
    hor_y = y + r
    rect(x, hor_y, w, hor_h)

    # Vertical rect
    ver_w = w - 2*r
    ver_x = x + r
    rect(ver_x, y, ver_w, h)


def getTextSizeByWidth(txt, wdt):
    # We use a savedState to avoid overwriting canvas properties
    with savedState():

        # Setting a "base" font size
        # In order to proceed with calculations
        testSize = 10

        # Getting the "base" size data
        fontSize(testSize)
        lineHeight(testSize)
        w, h = textSize(txt)

        # Getting size and height
        actualSize = testSize/w*wdt
        actualHeight = fontCapHeight()/w*wdt

        return (actualSize, actualHeight)


def drawTextByWidth(txt, pos, wdt, fromTop=False):
    size, height = getTextSizeByWidth(txt, wdt)
    x, y = pos
    fontSize(size)
    if fromTop:
        y = y - height
    text(txt, (x, y))


def countWords(s: str):
    return len(s.split())


def isMonoword(entry):
    return countWords(entry[0]) == 1 and countWords(entry[1]) == 1


# SHAPE FUNCTIONS

def priceBox(x, y, h):

    with savedState():
        translate(x, y)

        # Main background
        stroke(None)
        fill(*price_c_bg)
        rect(0, 0, price_w, h)

        # Setting color for box and text
        fill(*price_c_fg)

        # Price box
        price_box_s = price_w - 2*price_m_h
        price_box_y = h - price_m_v - price_box_s
        roundedRect(price_m_h, price_box_y, price_box_s,
                    price_box_s, price_box_r)

        # Price text
        font(price_txt_unit_f)
        drawTextByWidth(
            price_txt_unit, (price_m_h, price_box_y - price_m_h), price_box_s, True)

        # Sapori text
        font(price_txt_brand_f)
        drawTextByWidth(
            price_txt_brand, (price_m_h, price_m_v), price_box_s, False)


def productTxt(entry, size, leading):
    l = size*leading
    txt = FormattedString()
    txt.append(entry[0], font=product_f, fill=product_c_it, fontSize=size, lineHeight=l,
               paragraphBottomSpacing=product_gap)
    txt.append('\n')
    txt.append(entry[1], font=product_f, fill=product_c_en,
               fontSize=size, lineHeight=l)
    return txt


def calcMaxSize(entry, box):
    s = fs_base
    s_ok = fs_base
    lh = product_f_lh
    lh_ok = product_f_lh
    txt = productTxt(entry, s, lh)
    while len(textOverflow(txt, box)) == 0:
        if isMonoword(entry) and len(textBoxBaselines(txt, box)) > 2:
            break
        s_ok = s
        s += fs_increase
        lh_ok = lh
        lh -= lh_increase
        txt = productTxt(entry, s, lh)
    print(s_ok, lh_ok)
    return s_ok, lh_ok


def card(x, y, w, h, entry):

    # Background
    # stroke(0)  # For test purpose
    fill(*c_page)
    rect(x, y, w, h)

    # Price
    priceBox(x + w - price_w, y, h)

    # Text box
    txt_box_w = w - card_m - card_m_r - price_w
    txt_box = (x + card_m, y + card_m, txt_box_w, h - 2*card_m)

    # Building string
    s, lh = calcMaxSize(entry, txt_box)
    txt = productTxt(entry, s, lh)

    # Y Correction
    corr = 0
    with savedState():
        fontSize(s)
        font(product_f)
        corr = fontDescender()/3

    # Text
    with savedState():
        translate(0, -corr)
        textBox(txt, txt_box)


# --- INSTRUCTIONS --- #

# Getting names

names = []
with open(csvPath) as f:
    reader = csv.reader(f)
    for row in reader:
        names.append(row)


# Setting page size
size(page_w, page_h)


# Calculating card size
card_w = (width() - 2*page_m) / cols
card_h = (height() - 2*page_m) / rows


# Drawing cards
with savedState():

    # We translate so it's easier to draw
    translate(page_m, page_m)

    # Iterating over the names
    for e, entry in enumerate(names):

        # Getting card coordinates
        i = e % cols
        j = e // cols
        x = i * card_w
        y = j * card_h

        card(x, y, card_w, card_h, entry)


# Crocini

stroke(0)
fill(None)
croc_l = page_m/2

for i in range(cols+1):
    x = page_m + i*card_w
    y1 = page_m/2
    y2 = height()-page_m/2
    line((x, y1), (x, y1 + croc_l))
    line((x, y2), (x, y2 - croc_l))

for i in range(rows+1):
    y = page_m + i*card_h
    x1 = page_m/2
    x2 = width()-page_m/2
    line((x1, y), (x1 + croc_l, y))
    line((x2, y), (x2 - croc_l, y))
