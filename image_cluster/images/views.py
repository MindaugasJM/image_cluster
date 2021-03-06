from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img 
from tensorflow.keras.preprocessing.image import img_to_array 
from tensorflow.keras.applications.vgg16 import preprocess_input 
from tensorflow.keras.applications.vgg16 import VGG16 
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity
from . models import Image


@login_required(login_url='login')
def view_gallery(request):
    user = request.user.id
    images = Image.objects.filter(owner_id=user)
    all_groups = images.values_list('image_group', flat=True)
    unique_groupes = []
    for group in all_groups:
        if group not in unique_groupes:
            unique_groupes.append(group)
    context = {'images': images, 'unique_groupes': unique_groupes, 'all_groups':all_groups,}
    return render(request, 'gallery.html', context)

@login_required(login_url='login')
def delete_images(request):
    if request.method == 'POST':
        checked_boxes = request.POST.getlist('image_checkbox')
        for id in checked_boxes:
            doomed_img_form_db = Image.objects.filter(id=id)
            doomed_img_from_disc = doomed_img_form_db.values('image_name').get()['image_name']         
            os.remove(os.path.join((settings.MEDIA_ROOT)+'\\images\\user_uploaded_images\\'+str(doomed_img_from_disc)))
            doomed_img_form_db.delete()
    return redirect('gallery')

@login_required(login_url='login')
def upload_images(request):
    user_conected = request.user
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        for image in images:
            last_img_id = Image.objects.values_list('id',flat=True).last()
            Image.objects.create(owner=user_conected, image=image, image_name=str(last_img_id)+str(image))
        return redirect('gallery')
    return render(request, 'upload_images.html')

@api_view(['GET'])
def activate_img_analysis(request):
    if request.method == 'GET':
        physical_device = tf.config.experimental.list_physical_devices('GPU')
        tf.config.experimental.set_memory_growth(physical_device[0], True)
        locating_img_dir = os.path.abspath('./'+'media/images/user_uploaded_images')
        change_dir_to_img = os.chdir(locating_img_dir)
        all_img_form_media = []
        with os.scandir(change_dir_to_img) as files:
            for file in files:
                if file.name.endswith('.png') | file.name.endswith('.jpeg') | file.name.endswith ('.jpg'):
                    all_img_form_media.append(file.name)
        model = VGG16()
        model = Model(inputs = model.inputs, outputs = model.layers[-2].output)
        
        def extract_features(file, model):
            img = load_img(file, target_size=(224,224))
            img = np.array(img) 
            reshaped_img = img.reshape(1,224,224,3) 
            imgx = preprocess_input(reshaped_img)
            features = model.predict(imgx, use_multiprocessing=True)
            return features

        data = {}
        for picture in all_img_form_media:
                feat = extract_features(picture,model)
                data[picture] = feat
        filenames = np.array(list(data.keys()))
        feat = np.array(list(data.values()))

        def cluster(filePaths, features, threshold=0.699):
            features = features.reshape(-1,4096)
            simMatrix = cosine_similarity(features)
            clusters = {}
            for i in range(len(features)):
                dupIdx = list(np.where(simMatrix[i] > threshold)[0])
                if len(dupIdx) > 1:
                    curCluster, clusterMatch = list(dupIdx), None
                    for cIdx in clusters:
                        if curCluster[0] in clusters[cIdx]:
                            clusterMatch = cIdx
                            break
                    if clusterMatch == None: clusters[len(clusters)] = curCluster
            for cIdx in clusters: clusters[cIdx] = [filePaths[x] for x in clusters[cIdx]]
            return clusters

        os.chdir(settings.BASE_DIR)
        img_clusters = cluster(filenames, feat)  
        for group in img_clusters:
            for image_in_group in (img_clusters[group]):
                (str(group)) 
                image_in_group
                image = get_object_or_404(Image, image_name=image_in_group)
                image.image_group = group
                image.save(update_fields=["image_group"]) 
    return redirect('gallery') 
