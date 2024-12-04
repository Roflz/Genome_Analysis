from django.core.management.base import BaseCommand
from Bio import SeqIO

from data_analysis.models import GenomicSequence, GenomicAnnotation, Feature
from django.db import IntegrityError, models

class Command(BaseCommand):
    help = "Import genomic data from .fna and .gbff files"

    def add_arguments(self, parser):
        parser.add_argument('--fna', type=str, help="Path to the .fna file")
        parser.add_argument('--gbff', type=str, help="Path to the .gbff file")

    def handle(self, *args, **kwargs):
        fna_path = kwargs['fna']
        gbff_path = kwargs['gbff']

        if fna_path:
            self.import_fna(fna_path)
        if gbff_path:
            self.import_gbff(gbff_path)

    def import_fna(self, file_path):
        for record in SeqIO.parse(file_path, "fasta"):
            GenomicSequence.objects.get_or_create(
                accession=record.id,
                description=record.description,
                sequence=str(record.seq)
            )
        self.stdout.write(self.style.SUCCESS("FASTA file imported successfully."))

    def import_gbff(self, file_path):
        annotations = []
        for record in SeqIO.parse(file_path, "genbank"):
            try:
                sequence, created = GenomicSequence.objects.get_or_create(
                    accession=record.id,
                    defaults={
                        'description': record.description,
                        'sequence': str(record.seq),
                    }
                )
            except IntegrityError:
                self.stdout.write(f"Duplicate entry for accession {record.id}. Skipping...")

            for feature in record.features:
                if feature.type in ["CDS", "gene"]:  # Example: Filter relevant feature types
                    Feature.objects.create(
                        sequence=sequence,  # Link to the GenomicSequence
                        type=feature.type,
                        start=int(feature.location.start),
                        end=int(feature.location.end),
                        qualifiers=str(feature.qualifiers)
                    )

        GenomicAnnotation.objects.bulk_create(annotations)
        self.stdout.write(self.style.SUCCESS("GenBank file imported successfully."))
