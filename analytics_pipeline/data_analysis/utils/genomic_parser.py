from Bio import SeqIO
from django.apps import apps


def parse_fna(file_path):
    GenomicSequence = apps.get_model('data_analysis', 'GenomicSequence')  # Fetch model dynamically
    for record in SeqIO.parse(file_path, "fasta"):
        if not record.id or not record.seq:
            print(f"Skipping invalid record in FNA file: {record}")
            continue
        GenomicSequence.objects.get_or_create(
            accession=record.id,
            description=record.description,
            sequence=str(record.seq)
        )


def parse_gbff(file_path):
    GenomicSequence = apps.get_model('data_analysis', 'GenomicSequence')  # Fetch model dynamically
    GenomicAnnotation = apps.get_model('data_analysis', 'GenomicAnnotation')  # Fetch model dynamically
    annotations = []
    for record in SeqIO.parse(file_path, "genbank"):
        if not record.id or not record.seq:
            print(f"Skipping invalid record in GBFF file: {record}")
            continue
        print(f"id {record.id}\n seq {record.seq[:50]}")
        sequence, _ = GenomicSequence.objects.get(
            accession=record.id,
            description=record.description,
            sequence=str(record.seq)
        )

        for feature in record.features:
            annotations.append(GenomicAnnotation(
                sequence=sequence,
                feature_type=feature.type,
                start=feature.location.start.position,
                end=feature.location.end.position,
                strand='+' if feature.location.strand == 1 else '-',
                qualifiers=feature.qualifiers
            ))

    GenomicAnnotation.objects.bulk_create(annotations)
