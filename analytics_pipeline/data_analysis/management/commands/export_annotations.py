import csv
import os
import subprocess
from django.core.management.base import BaseCommand
from data_analysis.models import GenomicAnnotation


class Command(BaseCommand):
    help = 'Export genomic annotations to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--output', type=str, default='genomic_annotations.csv', help='Output file name')
        parser.add_argument('--r-script', type=str, default=os.path.join('scripts', 'visualize_annotations.R'), help='Path to the R script')
        parser.add_argument('--output-pdf', type=str, default='visualization.pdf', help='Output PDF file')
        parser.add_argument('--chunk-size', type=int, default=1000, help='Number of records to process at a time')

    def handle(self, *args, **kwargs):
        output_file = kwargs['output']
        r_script = kwargs['r_script']
        output_pdf = kwargs['output_pdf']
        chunk_size = kwargs['chunk_size']

        total_records = GenomicAnnotation.objects.count()
        self.stdout.write(f"Total annotations: {total_records}")

        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Feature Type', 'Start', 'End', 'Strand', 'Qualifiers', 'Sequence Accession'])

            for index, annotation in enumerate(
                GenomicAnnotation.objects.all().iterator(chunk_size=chunk_size), start=1
            ):
                # Print progress
                self.stdout.write(f"Processing annotation {index} of {total_records}")

                writer.writerow([
                    annotation.feature_type,
                    annotation.start,
                    annotation.end,
                    annotation.strand,
                    annotation.qualifiers,
                    annotation.sequence.accession
                ])

        self.stdout.write(self.style.SUCCESS(f'Data exported to {output_file}'))

        # Run the R script
        self.stdout.write(f"Running R script: {r_script}")
        self.stdout.write(f"Using annotations file: {output_file}")
        try:
            subprocess.run(
                ['Rscript', r_script, output_file, output_pdf],
                check=True
            )
            self.stdout.write(self.style.SUCCESS(f"Visualization saved to {output_pdf}"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(f"Error running R script: {e}")
