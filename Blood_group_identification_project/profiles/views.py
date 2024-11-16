# # views.py
# from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage
# import cv2
# import numpy as np

# def profiles(request):
#     if request.method == "POST" and request.FILES.get('abo_image'):
#         # Get the uploaded image
#         img_file = request.FILES['abo_image']
#         print(img_file)
        
#         # Save the image to the media directory
#         fs = FileSystemStorage()
#         filename = fs.save(img_file.name, img_file)
        
#         # Get the URL of the uploaded image
#         img_url = fs.url(filename)
#         print(img_url)
        
#         # Pass the image URL to the template
#         return render(request, 'profiles.html', {'img_url': img_url})
    
#     return render(request, 'profiles.html')


from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np

def profiles(request):
    if request.method == "POST" and request.FILES.get('abo_image'):
        # Get the uploaded image
        img_file = request.FILES['abo_image']
        
        # Save the image to a temporary location
        fs = FileSystemStorage()
        filename = fs.save(img_file.name, img_file)
        img_path = fs.path(filename)
        
        blood_group = identify_blood_group(img_path)
        print("Blood type:", blood_group)
        
        img_url = fs.url(filename)
        
        return render(request, 'profiles.html', {'img_url': img_url, 'blood_group': blood_group})
    
    return render(request, 'profiles.html')

def identify_blood_group(img_path):
    # Read the uploaded image
    abo_image = cv2.imread(img_path)
    
    # Convert the image from color to grayscale
    gray = cv2.cvtColor(abo_image, cv2.COLOR_BGR2GRAY)
    
    # blur the image using Gaussian Blur (smoothning the image for more accurate blood cell Image)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
   # blurred to threshold to calculate the threshold values for the given images and will return the image and its value
    val, threshold = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)# sets pixels to either black or white
    
   # finding the contours(continuous curve along the boundary) to find the curved edges of the blood cells in the image
    contours,val2 = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# 2nd parameter is for considering only the outer contour and not any of its inside child contour

    # Determine blood group based on contour length
    contour_length = len(contours)
    if contour_length < 50:
        return 'O'
    elif 50 <= contour_length < 100:
        return 'A'
    elif 100 <= contour_length < 150:
        return 'B'
    else:
        return 'AB'
