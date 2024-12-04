from django.db import models, IntegrityError
from Bio import SeqIO
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from data_analysis.utils.genomic_parser import parse_fna, parse_gbff
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# Model for genomic sequences
class GenomicSequence(models.Model):
    accession = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    sequence = models.TextField()
    fna_file = models.FileField(upload_to='genomic_sequences/fna/', null=True, blank=True)
    gbff_file = models.FileField(upload_to='genomic_sequences/gbff/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # If an FNA file is uploaded, parse it
        super().save(*args, **kwargs)
        if self.fna_file:
            file_path = self.fna_file.path
            try:
                for record in SeqIO.parse(file_path, "fasta"):
                    self.accession = record.id
                    self.description = record.description
                    self.sequence = str(record.seq)
            except Exception as e:
                raise ValidationError(f"Error parsing FNA file: {e}")

        super().save(*args, **kwargs)

    def process_gbff(self):
        if not self.gbff_file:
            raise ValidationError("No GBFF file found to process.")

        try:
            with self.gbff_file.open('r') as file:
                records = list(SeqIO.parse(file, "genbank"))
                if not records:
                    raise ValidationError("No valid records found in the GBFF file.")

                record = records[0]
                self.accession = record.id
                self.description = record.description
                self.sequence = str(record.seq)
                self.save()

                # Create annotations
                annotations = []
                for feature in record.features:
                    annotations.append(GenomicAnnotation(
                        sequence=self,
                        feature_type=feature.type,
                        start=feature.location.start,
                        end=feature.location.end,
                        strand='+' if feature.location.strand == 1 else '-',
                        qualifiers=feature.qualifiers
                    ))

                GenomicAnnotation.objects.bulk_create(annotations)
                print(f"Processed GBFF for accession {self.accession}. Annotations: {len(annotations)}")

        except Exception as e:
            raise ValidationError(f"Error processing GBFF file: {e}")

    def __str__(self):
        return self.accession or "Unnamed Genomic Sequence"


# Model for annotations
class GenomicAnnotation(models.Model):
    sequence = models.ForeignKey(GenomicSequence, on_delete=models.CASCADE, related_name='annotations')
    feature_type = models.CharField(max_length=50)  # e.g., gene, CDS, exon
    start = models.IntegerField()                  # Start position
    end = models.IntegerField()                    # End position
    strand = models.CharField(max_length=1, choices=[('+', 'Positive'), ('-', 'Negative')])  # Strand
    qualifiers = models.JSONField(blank=True, null=True)  # Additional metadata as JSON

    def __str__(self):
        return f"{self.feature_type} ({self.start}-{self.end})"


class Feature(models.Model):
    sequence = models.ForeignKey("GenomicSequence", on_delete=models.CASCADE, related_name="features")
    type = models.CharField(max_length=100)  # e.g., "CDS"
    start = models.IntegerField()
    end = models.IntegerField()
    qualifiers = models.JSONField()  # Store annotation details as JSON

    def __str__(self):
        return f"{self.type} ({self.start}-{self.end})"
