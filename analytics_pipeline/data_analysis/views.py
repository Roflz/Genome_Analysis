from django.shortcuts import render
from django.http import JsonResponse
from data_analysis.utils.genomic_parser import parse_fna, parse_gbff
from .models import GenomicSequence


def upload_genomic_file(request):
    if request.method == "POST" and request.FILES:
        fna_file = request.FILES.get('fna_file')
        gbff_file = request.FILES.get('gbff_file')

        if fna_file:
            parse_fna(fna_file.temporary_file_path())
        if gbff_file:
            parse_gbff(gbff_file.temporary_file_path())

        return JsonResponse({'message': 'Files imported successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def genomic_sequence_view(request):
    sequences = GenomicSequence.objects.all()  # Get all genomic sequences
    return render(request, 'data_analysis/genomic_sequence_list.html', {'sequences': sequences})