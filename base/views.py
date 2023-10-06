from django.http import HttpResponse , JsonResponse
from . import scrap
import sys
import sys
import json
import os
# print(sys.path)
# sys.path.append(os.path.abspath(os.path.join('..', 'tts')))
# from tts import amharic, oromo, tigrinya, somali
from .tts import amharic , oromo , somali ,  upload_to_azure , getblobdata , tigrai


def about(request): 

    return HttpResponse("   about page  ")


async def scrapNews(request):
    url = request.GET.get('url')

    data = await scrap.get_news_from_url(url)
    if(data == False):
        return JsonResponse({'message': 'Error'}, status=500)
    else:
        return JsonResponse(data, status=200)

async def speechSynthesis(request):
    
    try:
        print("here")
        raw_data = request.body.decode('utf-8')
        # print(raw_data)
        data = json.loads(raw_data , strict=False)
        print(data)
        language = data.get('language', '')
        text = data.get('text', '')
        newsId = data.get('newsId', '')
    
        if(language == 'am'):
            result = await amharic.synthesis(text, newsId)
            
            print("result reaching here is " , result)
            
                
            res =  await upload_to_azure.upload_to_azure(result)
            if res == True: 
                    
                return JsonResponse({'message': 'Success'}, status=200)
            else:
                return JsonResponse({'message': result}, status=500)


        elif(language == 'or'):
            result = await oromo.synthesis(text, newsId)
            
            res =  await upload_to_azure.upload_to_azure(result)

            # if result!= False:
            #     os.remove(result)
            
            if res == True: 
                os.remove(result)
                return JsonResponse({'message': 'Success'}, status=200)
            else:
                return JsonResponse({'message': 'Error'}, status=500)

        elif(language == 'ti'):
            result = await tigrai.synthesis(text, newsId)
            
            print("result reaching here is " , result)
            
                
            res =  await upload_to_azure.upload_to_azure(result)
            if res == True: 
                os.remove(result)
                return JsonResponse({'message': 'Success'}, status=200)
            else:
                return JsonResponse({'message': result}, status=500)

        elif(language == 'so'):
            result = await somali.synthesis(text, newsId)
            
            res =  await upload_to_azure.upload_to_azure(result)
            # if result != False:
            #     os.remove(result)
            if res == True: 
                os.remove(result)
                return JsonResponse({'message': 'Success'}, status=200)
            else:
                return JsonResponse({'message': 'Error'}, status=500) 
    except Exception as ex: 
        print(ex)
        return JsonResponse({'message': 'Error happended '}, status=500) 
    


async def getBlobData(request , newsId):
   
    
    try:
            data = getblobdata.get_blob_data(newsId)
            
            if(data == False):
                return JsonResponse({'message': 'Error'}, status=500)
            else:
                return HttpResponse(data, content_type='audio/wav')
    except Exception as ex:
        print("Error in get blob data " , ex)
        return JsonResponse({'message': 'Error'}, status=500)
