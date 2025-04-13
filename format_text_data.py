

def format_text_data():
    content = []
    with open('ira/static/investment_types.txt', 'r') as f:
        lines = []
        for line in f:
            line = line.rstrip()
            if line:
                lines.append(line)
        for i in range(0, 28, 4):
            d = {
                "title": lines[i],
                "description": [lines[i+1],lines[i+2],lines[i+3]],
            }
            content.append(d)
    return content

