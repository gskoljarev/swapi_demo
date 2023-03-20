import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

import petl as etl

from .models import DatasetMetadata
from .utils import DatasetDownloader


def download_data(request):
    # download & store data
    downloader = DatasetDownloader()
    filename = downloader.download_data()
    
    # save metadata to the database
    DatasetMetadata.objects.create(filename=filename)
    return HttpResponse('Data downloaded and saved successfully.')


def view_datasets(request):
    if request.method == 'POST':
        downloader = DatasetDownloader()
        filename = downloader.download_data()
        DatasetMetadata.objects.create(filename=filename)
        return redirect(reverse('view_datasets'))

    datasets = DatasetMetadata.objects.all().order_by('-id')
    return render(request, 'collect/view_datasets.html', {'datasets': datasets})


def view_dataset(request, dataset_filename):
    dataset = get_object_or_404(DatasetMetadata, filename=dataset_filename)
    # parse request param
    items = int(request.GET.get('items', 10))
    # read from csv file
    table = etl.fromcsv(os.path.join(settings.DATA_PATH, dataset_filename))
    # retrieve column names
    fields = etl.header(table)
    # retrieve first N rows
    table2 = etl.head(table, items)
    # convert data to a list
    data = list(etl.data(table2))
    context = {'dataset': dataset, 'fields': fields, 'data': data, 'items': items}
    return render(request, 'collect/view_dataset.html', context)


def view_dataset_value_count(request, dataset_filename):
    dataset = get_object_or_404(DatasetMetadata, filename=dataset_filename)
    # parse request param
    columns_raw = request.GET.get('columns', '')
    columns = columns_raw.split(',')
    # read from csv file
    table = etl.fromcsv(os.path.join(settings.DATA_PATH, dataset_filename))
    # retrieve column names
    fields = etl.header(table)
    # check if request param empty
    if not columns_raw:
        context = {'dataset': dataset, 'fields': fields, 'selected_fields': tuple(), 'data': list()}
        return render(request, 'collect/view_dataset_value_count.html', context)
    # cut the table according to request param
    table_cut = etl.cut(table, columns)
    # do the value counts
    table_value_counts = etl.valuecounts(table_cut, *columns)
    # cut out the frequency column
    table_final = etl.cutout(table_value_counts, 'frequency')
    # retrieve selected fields
    selected_fields = etl.header(table_final)
    # convert data to a list
    data = list(etl.data(table_final))
    context = {'dataset': dataset, 'fields': fields, 'selected_fields': selected_fields, 'data': data}
    return render(request, 'collect/view_dataset_value_count.html', context)
