def web_page():
    print("open website")
    with open("index.html", 'r') as file:
        webpage = file.read()
    print(type(webpage))
    
    return webpage






