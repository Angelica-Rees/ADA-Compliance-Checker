import webcolors
import pycountry

#Doc structure errors
def validate_doc_structure(soup):
    errors = []

    #Check for html lang tag invalid
    html_tag = soup.find("html")
    if html_tag:
        lang_attr = html_tag.get("lang")
        if not lang_attr:
            error = build_error(html_tag,"DOC_LANG_MISSING")
            errors.append(error)
        elif not pycountry.languages.get(alpha_2=lang_attr):
            error = build_error(html_tag,"DOC_LANG_MISSING")
            errors.append(error)

    #Check for empty or missing title tag
    title_tag = soup.find("title")
    if not title_tag:
        error = build_error(title_tag,"DOC_TITLE_MISSING")
        errors.append(error)
    elif not title_tag.get_text(strip=True):
        error = build_error(title_tag,"DOC_TITLE_MISSING")
        errors.append(error)
    
    #Check for color contrast ratio 
    styles = {}
    for tag in soup.find_all(True,style=True):
        style = tag['style']
        styles = dict(item.strip().split(":", 1) for item in style.split(";") if ":" in item)
        text_color = styles.get('color')
        bg_color = styles.get('background-color')
        if text_color and bg_color:
            text_color_rgb = tuple(webcolors.name_to_rgb(text_color.strip()))
            bg_color_rgb = tuple(webcolors.name_to_rgb(bg_color.strip()))

            r, g, b = text_color_rgb
            L1 =(0.2126*r + 0.7152*g + 0.0722*b)

            r1, g1, b1 = bg_color_rgb
            L2 =(0.2126*r1 + 0.7152*g1 + 0.0722*b1)

            #tag name is heading
            #not sure what constitutes as 'large text' so this is not very robust -Angel
            if tag.name in ['h1','h2','h3','h4','h5','h6','title']:
                if abs(L1/L2) != abs(3.0/1):
                    error = build_error(tag,"COLOR_CONTRAST")
                    errors.append(error) 
            #tag name is other text
            elif tag.name in ['p','text']:
                if abs(L1/L2) != abs(4.5/1):
                    error = build_error(tag,"COLOR_CONTRAST")
                    errors.append(error)

    return errors


#Img errors
def validate_img_tags(soup):
    errors = []
    images = soup.find_all("img")
    for img in images:
        alt = img.get("alt")
        if not alt:
            error = build_error(img,"IMG_ALT_MISSING")
            errors.append(error)
        elif len(alt) > 120:
            error = build_error(img,"IMG_ALT_LENGTH")
            errors.append(error)
    
    return errors


#link errors
def validate_links(soup):
    errors = []
    links = soup.find_all("a")
    for link in links:
        if link == "click here":
            error = build_error(link,"LINK_GENERIC_TEXT")
            errors.append(error)

    return errors


#heading errors
def validate_headings(soup):
    errors = []
    h1_tags = soup.find_all("h1")

    # Check if more than one h1 tag
    if len(h1_tags) > 1:
        # idk if the build selector will work for this specific one
        for h1 in h1_tags:
            error = build_error(h1,"HEADING_MULTIPLE_H1")
            errors.append(error)
    
    # Check heading heirarchy
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    last_level = 0
    for heading in headings:
        current_level = int(heading.name[1])
        # Check if the heading level skips one or more levels
        if last_level and current_level > last_level + 1:
            error = build_error(heading,"HEADING_ORDER")
            errors.append(error)
        last_level = current_level
            
    return errors


#Building the selector down here
def build_selector(element):
    parts = []
    while element and element.name != '[document]':
        sibling_index = 1
        if element.parent:
            for sibling in element.parent.find_all(element.name, recursive=False):
                if sibling == element:
                    break
                sibling_index += 1
            if sibling_index > 1:
                parts.append(f"{element.name}:nth-of-type({sibling_index})")
            else:
                parts.append(element.name)
        element = element.parent
    return " > ".join(reversed(parts))


#Building the error down here
def build_error(element,error_name):
    selector = build_selector(element)
    error_messages = {
        "DOC_LANG_MISSING": "The <html> element must have a valid lang attribute.",
        "DOC_TITLE_MISSING": "Every page must have a non-empty <title> tag.",
        "COLOR_CONTRAST": "Text must have a contrast ratio of at least 4.5:1 for normal text and 3.0:1 for large text.",
        "IMG_ALT_MISSING": "All <img> tags must have an alt attribute.",
        "IMG_ALT_LENGTH": "The alt attribute text should not exceed 120 characters to remain concise.",
        "LINK_GENERIC_TEXT": "Link text must not be generic (e.g., 'click here').",
        "HEADING_MULTIPLE_H1": "There must be only one <h1> per page.",
        "HEADING_ORDER": "Heading levels must not be skipped."
        
    }

    message = error_messages.get(error_name,"Unknown error")

    # Angel - fix the element name being null (example- title_tag null) 

    if element:
        element_name = element.name
    else:
        element_name = ""

    return {"name": error_name,
            "message": message,
            "element": element_name,
            "selector": selector,
            "codeSnippet":str(element)}
