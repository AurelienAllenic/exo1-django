import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dataset
from .forms import DatasetUploadForm
from .utils import analyze_csv, NpEncoder


@login_required
def dataset_list_view(request):
    datasets = Dataset.objects.filter(user=request.user)
    return render(request, 'datasets/list.html', {'datasets': datasets})


@login_required
def dataset_upload_view(request):
    form = DatasetUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        dataset = form.save(commit=False)
        dataset.user = request.user
        dataset.save()
        try:
            analysis = analyze_csv(dataset.file.path)
            dataset.row_count = analysis['shape']['rows']
            dataset.column_count = analysis['shape']['cols']
            dataset.column_names = analysis['headers']
            dataset.save()
            messages.success(request, f'Dataset « {dataset.name} » uploadé avec succès !')
            return redirect('datasets:detail', pk=dataset.pk)
        except Exception as e:
            dataset.delete()
            messages.error(request, f'Erreur lors de la lecture du CSV : {e}')
    return render(request, 'datasets/upload.html', {'form': form})


@login_required
def dataset_detail_view(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
    try:
        analysis = analyze_csv(dataset.file.path)
        charts_json = json.dumps(analysis['charts'], cls=NpEncoder)
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'analyse : {e}')
        analysis = None
        charts_json = '[]'
    return render(request, 'datasets/detail.html', {
        'dataset': dataset,
        'analysis': analysis,
        'charts_json': charts_json,
    })


@login_required
def dataset_delete_view(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
    if request.method == 'POST':
        name = dataset.name
        dataset.delete()
        messages.success(request, f'Dataset « {name} » supprimé.')
    return redirect('datasets:list')
