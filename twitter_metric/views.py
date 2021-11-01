import json

from django.shortcuts import render, redirect
from twitter_metric.forms import TwitterHandleForm
import scrape_twitter_metrics_bearer
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage


def get_twitter_handle_page(request):
    if request.method == 'POST':
        form = TwitterHandleForm(request.POST)
        if form.is_valid():
            twitter_handle = form.cleaned_data['twitter_handle']
            user_id = scrape_twitter_metrics_bearer.get_user_id(twitter_handle)
            if user_id != 0:
                return redirect('show_twitter_metrics', twitter_handle, user_id)
            else:
                error_message = f'Invalid Twitter handle "{twitter_handle}"!'
                form = TwitterHandleForm()
                context = {
                    'form': form,
                    'error': error_message
                }
                return render(request=request, template_name='twitter_metric/twitter_handle.html', context=context)
    else:
        form = TwitterHandleForm()
        context = {'form': form}
        return render(request=request, template_name='twitter_metric/twitter_handle.html', context=context)


def show_twitter_metrics(request, twitter_handle, user_id):
    json_file_rel_address, csv_file_rel_address = scrape_twitter_metrics_bearer.main(user_id, twitter_handle)


    # data = [{'key': 'val'}]
    # response = HttpResponse(json.dumps(data), content_type='application/json')
    # response['Content-Disposition'] = f'attachment; filename={twitter_handle}.json'
    # return response
    context = {"twitter_handle": twitter_handle,
               "json_file_rel_address": json_file_rel_address,
               "csv_file_rel_address": csv_file_rel_address}
    return render(request=request, template_name='twitter_metric/twitter_metrics.html', context=context)


# def download_json(request, twitter_handle):
#     response = HttpResponse(json.dumps(data), content_type='application/json')
#     response['Content-Disposition'] = f'attachment; filename={twitter_handle}.json'
#     return response
