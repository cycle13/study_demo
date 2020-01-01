from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView, DetailView, TemplateView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
import numpy as np
from django.core.urlresolvers import reverse_lazy
from matplotlib.figure import Figure  
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import random
import datetime
import base64
from io import BytesIO




from netCDF4 import Dataset
import numpy as np
import os
import conda
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
from mpl_toolkits.basemap import Basemap


import cartopy.crs as ccrs
# Create your views here.
def index(request):
    tag = Tag.objects.all()
    post = Post.objects.raw('select * from index_post')
    auther = Auther.objects.raw('select id,auther_name from index_auther')
    return render(request,'index.html',locals())

def plot(request):
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    FigureCanvasAgg(fig)
    buf = BytesIO()
    fig.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return HttpResponse(f"<img src='data:image/png;base64,{data}'/>")

def plotmap(request):
    #fig = Figure()
    fig = plt.figure()
    filepath = '/home/liyuan3970/test_demo/matplotlib/'
    fh = Dataset(filepath+'src/slp.mon.mean.nc')#(meteo_file, mode='r')
    fu = Dataset(filepath+'src/uwnd.mon.mean.nc')
    fv = Dataset(filepath+'src/vwnd.mon.mean.nc')
    
    # 获取每个变量的值
    lons = fh.variables['lon'][:]
    
    lats = fh.variables['lat'][::-1]
    slp = fh.variables['slp'][:]
    slp_units = fh.variables['slp'].units
    # print(lons)
    # print(lats)
    uwnd=fu.variables['uwnd'][:]
    vwnd=fv.variables['vwnd'][:]
    
    u=uwnd[0,5, ::-1, ::]
    v=vwnd[0,5,::-1, ::]
    lons1, lats1 = np.meshgrid(lons, lats)
    m = Basemap(llcrnrlat=15,urcrnrlat=55,llcrnrlon=110,urcrnrlon=180)
    x,y = m(lons1,lats1)
    #nxv nyv控制风场的密度
    nxv =15; nyv = 15
    udat, vdat, xv, yv = m.transform_vector(u,v,lons,lats,nxv,nyv,returnxy=True)
    m.barbs(xv,yv,udat,vdat,length=6,barbcolor='k',flagcolor='r',linewidth=0.5)
    m.drawcoastlines()    
    FigureCanvasAgg(fig)
    buf = BytesIO()
    fig.savefig(buf, format='png')
    data2 = base64.b64encode(buf.getbuffer()).decode('ascii')
    return HttpResponse(f"<img src='data:image/png;base64,{data2}'/>")

def plotmap2(request):
    #fig = Figure()
    fig = plt.figure()
    plt.figure(figsize=(6, 3))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    ax.coastlines(resolution='110m')
    FigureCanvasAgg(fig)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    #fig.savefig(buf, format='png')
    data2 = base64.b64encode(buf.getbuffer()).decode('ascii')
    return HttpResponse(f"<img src='data:image/png;base64,{data2}'/>")
class Listviews(ListView):
    # 定义查询数据的数据表
    model = Post
    # queryset = Post.objects.all()
    # list的翻页功能
    paginate_by = 5
    # 对应查找的querset对象的名称
    context_object_name = 'post'
    # 模板的名称
    template_name = 'list.html'
    # 定义返回数据的querset的数据结构和内容
    def get_queryset(self):
        return Post.objects.all()

class Detailviews(ListView):
    # 定义查询数据的数据表
    model = Post
    # queryset = Post.objects.all()
    # list的翻页功能
    # paginate_by = 5
    # 对应查找的querset对象的名称
    context_object_name = 'post'
    # 模板的名称
    template_name = 'detail.html'
    # 定义返回数据的querset的数据结构和内容
    def get_queryset(self):
        return Post.objects.all()

class MainList(ListView):
    model = Post
    template_name = 'main.html'
    context_object_name = 'post'

class PostUpdate(UpdateView):
    model = Post
    success_url = reverse_lazy('main')
    fields = ['id', 'time','post_name', 'auther', 'tag','content']
    template_name = 'Post_form.html'

class PostCreate(CreateView):
    model = Post
    # 成功后的url
    success_url = reverse_lazy('main')
    fields = ['id', 'time','post_name', 'auther', 'tag','content']
    template_name = 'Post_form.html'
    # def add(request):
    #     form = Post(request.POST or None)
    #     if form.is_valid():
    #         instance.save()
    #     context = {
    #         'form': form,
    #     }
    #     #如果没有有效提交，则仍留在原来页面
    #     return render(request, 'main.html',  context)
def funcpost(request):
    if request.method == 'GET':
        return render(request, 'funcpost.html')
    else:
        post_name = request.POST.get('post_name')
        time = request.POST.get('time')
        auther = request.POST.get('auther')
        tag = request.POST.get('tag')
        content = request.POST.get('content')

        return HttpResponse('获取请求数据成功')
