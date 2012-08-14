ITEMS_PER_PAGE = 8

def count_pages(count):
    return (count + ITEMS_PER_PAGE - 1) / ITEMS_PER_PAGE
