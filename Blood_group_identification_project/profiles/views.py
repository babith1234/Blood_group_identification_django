# views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def profiles(request):
    if request.method == "POST" and request.FILES.get('abo_image'):
        # Get the uploaded image
        img_file = request.FILES['abo_image']
        print(img_file)
        
        # Save the image to the media directory
        fs = FileSystemStorage()
        filename = fs.save(img_file.name, img_file)
        
        # Get the URL of the uploaded image
        img_url = fs.url(filename)
        print(img_url)
        
        # Pass the image URL to the template
        return render(request, 'profiles.html', {'img_url': img_url})
    
    return render(request, 'profiles.html')
