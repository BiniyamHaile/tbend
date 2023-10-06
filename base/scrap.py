from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
 

async def fetch_url_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return False
            return await response.text()


async def get_url_content(url):
    return await fetch_url_async(url)


async def get_news_from_url(newsLink):
    result = await get_url_content(newsLink)

    if not result:
        return False

    soup = BeautifulSoup(result, 'html.parser')
    title = soup.find('h1').text


    trailings = ""

    for li in soup.find('div', class_='wrapper_1l0t8bn').find('header').find('ul'):
        trailings += li.text + "\n"    


    author = soup.select_one(' h4 > a').text
    img_element = soup.select_one('div.wrapper_1l0t8bn > article.style_1k79xgg > header >  div.wrapper_ctua91 >  div.style_1pa6aqm > figure.base_1kci93k > picture.base_1emrqjj > img')

    fig_caption_first_image = soup.select_one('main > div > div.wrapper_1l0t8bn > article.style_1k79xgg > header > div.wrapper_ctua91 > div.style_1pa6aqm > div.wrapper_h4uv1b > figcaption')

    img_src = img_element['src'] if img_element else False
    fig_caption_first_img = fig_caption_first_image.text if fig_caption_first_image else False


    p_elements = soup.select('main > div > div.wrapper_1l0t8bn > article.style_1k79xgg > div.wrapper_wfxu5h > main > div > p.tagStyle_z4kqwb-o_O-style_1tcxgp3-o_O-style_1pinbx1-o_O-style_48hmcm')

    headlineTextAfterImage = ""

    # print(p_elements[0].children)
    # Loop through each p element's children

    
    for child in p_elements[0]:
        print(child)
        if child.name == 'em':

            # If the element is <em>, find <strong> and then take the text
            strong = child.find_next('strong')
            if strong:
                headlineTextAfterImage += strong.text
        elif child.name == 'a':
            # If the element is <a>, find em, then strong, and then take the text
            em = child.find_next('em')
            if em:
                strong = em.find_next('strong')
                if strong:

                    headlineTextAfterImage += strong.text
        elif child.name == 'strong':
            headlineTextAfterImage += child.text



    allElements = soup.select('main > div > div.wrapper_1l0t8bn > article.style_1k79xgg > div.wrapper_wfxu5h > main > div' )
    # print("element length", len(allElements))

    # allElements.remove(allElements[0])
    pretified = allElements[0]
    # print(pretified) 
    # idx = -1

    articleLists = [
    
        {
            'h1title' : "",
                'h2title' : "",
                'h3title' : "",
                'paragraphs' : "", 
                'imageLink' : False,
                'figCaption' : "", 
                'description' : '' , 
                'tableHead' : [] , 
                'tableBody' : []
            }
    ]

    # paragraphText = ""
    for element in pretified:
        # element = allElements[0][i]
        # print(element)
        if element.name  == 'div' and "wrapper_1go68cf-o_O-style_48hmcm" in element.get('class' , []):
            # idx = i
            articleLists.append({
                
                'h1title' : "",
                'h2title' : "",
                'h3title' : "",
                'paragraphs' : "", 
                'imageLink' : False,
                'figCaption' : "" ,
                'description' : '',
                'tableHead' : [] , 
                'tableBody' : []
            
            })
        elif element.name == "p":
            # p_text = ''.join(element.find_all(text=True, recursive=False)).strip()
            # paragraphText += p_text + "\n"
            elemen  = articleLists.pop()
            # print(elemen)
            # elemen["paragraphs"] += p_text
            for child in element.children:
                elemen["paragraphs"] += child.text
            elemen["paragraphs"] += "\n"    
            articleLists.append(elemen)
        elif element.name == "h2": 
            h2_text = ''.join(element.find_all(text=True, recursive=False)).strip()
            elemen  = articleLists.pop()
            for child in element.children:
                elemen["h2title"] += child.text
            
        
            # elemen["h2title"] += h2_text
            articleLists.append(elemen)
        elif element.name == "h3":
            # h3_text = ''.join(element.find_all(text=True, recursive=False)).strip()
            elemen  = articleLists.pop()
            elemen["h3title"] += element.text
            articleLists.append(elemen)
        elif element.name == "h1":
            
            elemen  = articleLists.pop()
            elemen["h1title"] += element.text
            articleLists.append(elemen)
        elif element.name == 'ul':
        
            elemen  = articleLists.pop()
            for child in element.children:
            
                elemen["description"] += child.text
                elemen["description"] += "\n"
            articleLists.append(elemen)
        
            
        elif element.name == "div":
            # print("element is found " + element.name)
            for elem in element:



                # print(elem.name + " is found")
                className = elem.get('class' , [])
                # print(className)
                classN = ""
                
                if elem.name == 'table':
                    elemen  = articleLists.pop()
                    for el in elem:
                    
                        if el.name == 'thead' :
                            tableHead = []
                            print("thead is found " + el.name)
                            
                            for child in el:
                                print(child.name)
                                if child.name == 'tr':
                                    print("tr is found " + child.name)
                                    for tr in child:
                                        print(tr)
                                        if tr.name == 'th':
                                            tableHead.append(tr.text)
                                            print(tableHead)
                            prevHead = elemen["tableHead"]
                            prevHead.append(tableHead)

                                            
                            elemen["tableHead"] = prevHead
                            
                        elif el.name == 'tbody':
                            print("tbody is found " + elem.name)
                        
                            tableBody = []
                            for child in el:
                                if child.name == 'tr':
                                    tableRow = []
                                    for tr in child.children:
                                        if tr.name == 'td':
                                            tableRow.append(tr.text)
                                    tableBody.append(tableRow)
                            
                            prevData = elemen["tableBody"]
                            prevData.append(tableBody)
                            elemen["tableBody"] = prevData
                    articleLists.append(elemen)
                if(len(className) > 0):
                    classN = className[0]
                if elem.name  == 'div' and 'style_1wszng'  == classN:
                    # print("inside the style_1wszng ----" + elem.name)
                    for e in elem:
                        if e.name ==  'figure':
                            for p in e:
                            
                                if p.name == 'noscript':
                                    for n in p:
                                        # print("inside the noscript ----" + n.name)
                                        if n.name == 'picture':
                                            # print("inside the picture ----" + n.name)
                                            for pi in n:
                                                if pi.name == 'img':
                                                    img_src = pi['src'] if pi else False
                                                    elemen  = articleLists.pop()
                                                    elemen["imageLink"] = img_src
                                                    articleLists.append(elemen)
                        elif e.name == 'div':
                            #  and elem.get('class' , [])[0] == 'wrapper_h4uv1b':
                            # print("inside the wrapper_h4uv1b ----" + e.name)
                            print( e.get('class' , []))
                            if e.get('class' , [])[0] == 'wrapper_h4uv1b':
                                for p in e:
                                    if p.name == 'figcaption':
                                        print("inside the figcaption ----" + p.text)
                                        elemen  = articleLists.pop()
                                        elemen["figCaption"] = p.text
                                        articleLists.append(elemen)

                    # figure = elem.find('figure')
                    # picture = figure.find('picture')
                    # img = picture.find('img')
                    # img_src = img['src'] if img else False
                    # elemen  = articleLists.pop()
                    # elemen["imageLink"] = img_src
                    # articleLists.append(elemen)
                if elem.name  == 'div' and "wrapper_h4uv1b" in element.get('class' , []):
                    figcaption = elem.find('figcaption')
                    elemen  = articleLists.pop()
                    elemen["figCaption"] = figcaption.text
                    articleLists.append(elemen)



    articleLists.pop()
    # articleLists[0]['imageLink'] = img_src
    # print(title)
    # print(trailings)
    # print(author)
    # print(img_src)
    # print(fig_caption_first_img)
    # print(headlineTextAfterImage)


    # print("------------------")
    # print(headlineTextAfterImage)


    # print(articleLists)

    news = {
        "title" : title,
        "description" : trailings,
        "author" : author,
        "mainImage" : img_src,
        "figCaption" : fig_caption_first_img,
        "headlineTextAfterImage" : headlineTextAfterImage,
        "sourceLink" : newsLink, 
        "listOfContent" : articleLists,
        "language" : "en"
    }




    return news
