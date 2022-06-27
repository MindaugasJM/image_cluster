from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . models import Image

@login_required(login_url='login')
def view_gallery(request):
    user = request.user.id
    images = Image.objects.filter(owner_id=user)
    context = {'images': images}
    return render(request, 'gallery.html', context)

@login_required(login_url='login')
def view_image(request, pk):
    image = Image.objects.get(id=pk)
    return render(request, 'image.html', {'image': image})


@login_required(login_url='login')
def upload_images(request):
    user_conected = request.user
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        for image in images:
            Image.objects.create(
                owner=user_conected,
                image=image,
                image_name=image,
            )
        return redirect('gallery')
    return render(request, 'upload_images.html')

