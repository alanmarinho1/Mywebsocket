import fitz

def keyword_first_page(file, x):

    doc = fitz.open(file)

    positions = doc[x-1].searchFor("Os dados acima")[0]
    bottom = positions[1] - 20
    positions = doc[x-1].searchFor("Data")[0]
    top = positions[1] - 5
    
    area = (top,33.91,bottom,581.145)
    
    return area

def keyword_last_page(file, x):
    
    doc = fitz.open(file)

    positions = doc[x-1].searchFor("Total")[0]
    bottom = positions[1] - 3
    
    area = (121.998,35.469,bottom,573.35)
    
    return area 