ITEMS_PER_PAGE = 16

def count_pages(count):
    return (count + ITEMS_PER_PAGE - 1) / ITEMS_PER_PAGE
