from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import FileResponse
from .forms import DatasetForm, FuncForm
from django.contrib import messages
from .models import DraftDataset, DraftFunc
from django.contrib.auth.decorators import login_required
from user.models import Profile

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from io import BytesIO
import numpy as np

#index
def index(request):
 return render(request, "index.html")

#dataset drafts page
@login_required(login_url="user:login")
def datasetDraft(request):
    datasetDrafts = DraftDataset.objects.filter(creator = request.user)
    profile = Profile.objects.filter(user=request.user).first()
    draft_right_left =  profile.draft_right_left
    context = {
        "drafts":datasetDrafts,
        "left":draft_right_left
    }
    if draft_right_left <=0:
        messages.warning(request, "Contact n.erenacar13@gmail.com in order to buy more draft rights.")
    return render(request, "datasetDraft.html", context=context)

#adding new dataset draft
@login_required(login_url="user:login")
def addDataset(request):
    form = DatasetForm(request.POST or None, request.FILES or None)
    profile = Profile.objects.filter(user=request.user).first()
    draft_right_left =  profile.draft_right_left

    if form.is_valid():
        draft = form.save(commit=False)
        draft.creator = request.user
        draft.save()
        profile.draft_right_left -= 1
        profile.save()
        messages.success(request, "Draft successfully saved.")
        return redirect("drafts:datasetDraft")
    context = {
        "form":form
    }
    if draft_right_left <= 0:
        messages.warning(request, "You dont have any draft rights left!")
        return redirect("drafts:datasetDraft")

    print(draft_right_left)
    return render(request, "addDataset.html", context)

#delete dataset draft
@login_required(login_url="user:login")
def deleteDataset(request, id):
    draft = get_object_or_404(DraftDataset, id=id)
    draft.delete()
    messages.success(request, "Draft Successfully deleted.")
    return redirect("drafts:datasetDraft")

#update dataset draft
@login_required(login_url="user:login")
def updateDataset(request, id):
    draft = get_object_or_404(DraftDataset, id=id)
    form = DatasetForm(request.POST or None, request.FILES or None, instance=draft)
    if form.is_valid():
        draft = form.save(commit=False)
        draft.creator = request.user
        draft.save()
        messages.success(request, "Draft successfully updated.")
        return redirect("drafts:datasetDraft")
    context = {
        "form":form
    }
    return render(request, "updateDatasetDraft.html", context)

#function generating the graph for 2d, 3d datasets and returning file response
def generate_graph(request, id):
    draft = DraftDataset.objects.get(id=id)
    file = draft.file
    url = draft.file_link
    if file and url:
        messages.info(request, "File and Url supplied at the same time.")
        return redirect("drafts:datasetDraft")

    if file:
        # Read the CSV file with a header row
        data = pd.read_csv(file)
    elif url:
        try:
            data = pd.read_csv(url)
        except:
            messages.info(request, "Incorrect data format.")
            return redirect("drafts:datasetDraft")
    #graph properties
    date=draft.created_date
    graph_color = draft.graph_color

    title = draft.title
    title_fontsize = draft.title_fontsize
    title_color = draft.title_color
    
    x_label = draft.x_label
    y_label = draft.y_label
    z_label = draft.z_label



    matplotlib.use('agg') #set matplotlib background mode

    num_columns = data.shape[1]

    # Check the number of columns
    if num_columns == 2:
        # Extract x, y, and z values based on column labels
        x = data['x']
        y = data['y']

        # Create a 2D line plot
        plt.plot(x, y, color=graph_color)

        # Set labels and title
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title, fontsize=title_fontsize, color=title_color)

        # Save the plot as an image file
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Create an HTTP response with the image file
        response = HttpResponse(buffer, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{draft.created_date}.png"'
        
        plt.close()  # Close the figure to free up memory
        return response    
    elif num_columns == 3:
        
        # Extract x, y, and z values based on column labels
        x = data['x']
        y = data['y']
        z = data['z']

        # Create a 3D scatter plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z)

        # Set labels and title
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_zlabel(z_label)
        ax.set_title(title, fontsize=title_fontsize, color=title_color)
        ax.tick_params(color=graph_color, labelcolor=graph_color)

        # Save the plot as an image file
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Create an HTTP response with the image file
        response = HttpResponse(buffer, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{draft.created_date}.png"'
        
        plt.close(fig)  # Close the figure to free up memory
        return response
    else:
        messages.error(request, "The file provided in the draft does not have 2 or 3 columns.")
        return redirect("drafts:datasetDraft")

#download view
@login_required(login_url="user:login")
def downloadDataset(request, id):
    try:
        return generate_graph(request,id)
    except:
        messages.info(request, "Incorrect draft format.")
        return redirect("drafts:datasetDraft")

#function drafts page
@login_required(login_url="user:login")
def funcDraft(request):
    profile = Profile.objects.filter(user=request.user).first()
    draft_right_left =  profile.draft_right_left
    funcDrafts = DraftFunc.objects.filter(creator = request.user)
    context = {
        "drafts":funcDrafts,
        "left":draft_right_left
    }
    if draft_right_left <=0:
        messages.warning(request, "Contact n.erenacar13@gmail.com in order to buy more draft rights.")
    return render(request, "func/funcDraft.html", context=context)

#adding new function draft
@login_required(login_url="user:login")
def addFunc(request):
    form = FuncForm(request.POST or None)
    profile = Profile.objects.filter(user=request.user).first()
    draft_right_left =  profile.draft_right_left

    if form.is_valid():
        draft = form.save(commit=False)
        draft.creator = request.user
        draft.save()
        profile.draft_right_left -= 1
        profile.save()
        messages.success(request, "Draft successfully saved.")
        return redirect("drafts:funcDraft")
    context = {
        "form":form
    }
    if draft_right_left <= 0:
        messages.warning(request, "You dont have any draft rights left!")
        return redirect("drafts:datasetDraft")

    print(draft_right_left)
    return render(request, "func/addFunc.html", context)

#delete function draft
@login_required(login_url="user:login")
def deleteFunc(request, id):
    draft = get_object_or_404(DraftFunc, id=id)
    draft.delete()
    messages.success(request, "Draft Successfully deleted.")
    return redirect("drafts:funcDraft")

#updating function draft
@login_required(login_url="user:login")
def updateFunc(request, id):
    draft = get_object_or_404(DraftFunc, id=id)
    form = FuncForm(request.POST or None, instance=draft)
    if form.is_valid():
        draft = form.save(commit=False)
        draft.creator = request.user
        draft.save()
        messages.success(request, "Draft successfully updated.")
        return redirect("drafts:funcDraft")
    context = {
        "form":form
    }
    return render(request, "func/updateFuncDraft.html", context)

#creating graph from the given function and returning file response
def generateFuncGraph(id):
    draft = DraftFunc.objects.get(id=id)

    #graph properties
    date=draft.created_date
    graph_color = draft.color

    title = draft.title
    title_fontsize = draft.title_fontsize
    title_color = draft.title_color

    equation = draft.equation
    line_type = draft.line_type

    # Create a lambda function
    f = eval("lambda x, y: " + equation)
    x = np.linspace(-10, 10, 100)  # Range for x values
    y = np.linspace(-10, 10, 100)  # Range for y values
    X, Y = np.meshgrid(x, y)  # Create a grid of points
    Z = f(X, Y)  # Evaluate the function for each point

    #bg mode
    matplotlib.use('agg')

    #Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis',linestyle=line_type)  # Use plot_surface for surface plots or scatter for scattered points

    #Set labels and title
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(title, fontsize=title_fontsize, color=title_color)
    ax.tick_params(color=graph_color, labelcolor=graph_color)

    range_list = eval(draft.range_of_func)
    #set graph limits (currently disabled because it messes with graphs.)
    #ax.set_xlim(range_list[0][0], range_list[0][1])
    #ax.set_ylim(range_list[1][0], range_list[1][1])
    #ax.set_zlim(range_list[2][0], range_list[2][1])

    # Save the plot as an image file
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Create an HTTP response with the image file
    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{draft.created_date}.png"'
    
    plt.close(fig)  # Close the figure to free up memory
    return response

#download function graph
@login_required(login_url="user:login")
def downloadFunc(request, id):
    try:
        result = generateFuncGraph(id)
        return result 
    except:
        messages.info(request, "Incorrect draft format. Check function syntax.")
        return redirect("drafts:funcDraft")
