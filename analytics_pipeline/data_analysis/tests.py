from django.test import TestCase
from data_analysis.models import GenomicSequence, GenomicAnnotation

class GenomicImportTest(TestCase):
    def test_fna_import(self):
        # Simulate import
        from data_analysis.utils.genomic_parser import parse_fna
        parse_fna('path/to/test_file.fna')

        # Assert sequence was imported
        self.assertTrue(GenomicSequence.objects.exists())

    def test_gbff_import(self):
        # Simulate import
        from data_analysis.utils.genomic_parser import parse_gbff
        parse_gbff('path/to/test_file.gbff')

        # Assert annotations were imported
        self.assertTrue(GenomicAnnotation.objects.exists())