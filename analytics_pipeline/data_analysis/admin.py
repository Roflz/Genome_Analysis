from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Feature, GenomicSequence, GenomicAnnotation


class GenomicAnnotationInline(admin.TabularInline):
    model = GenomicAnnotation
    fields = ('feature_type', 'start', 'end', 'strand', 'qualifiers')
    extra = 0  # Disable empty extra rows
    readonly_fields = ('feature_type', 'start', 'end', 'strand', 'qualifiers')


@admin.register(GenomicSequence)
class GenomicSequenceAdmin(admin.ModelAdmin):
    # Exclude the fields that will be automatically populated by the file parser
    exclude = ('accession', 'description', 'sequence')  # These fields will be auto-filled
    inlines = [GenomicAnnotationInline]  # Add inline for annotations

    def truncated_sequence(self, obj):
        return obj.sequence[:50] + "..." if obj.sequence and len(obj.sequence) > 50 else obj.sequence

    # Set a short description for the truncated sequence column
    truncated_sequence.short_description = "Sequence (truncated)"

    # Use the truncated sequence in list_display
    list_display = ('accession', 'description', 'truncated_sequence', 'fna_file', 'gbff_file')

    # If you'd like to filter by file fields or any other field, you can define search_fields or list_filter
    search_fields = ['accession', 'description']
    list_filter = ['accession']

    actions = ['process_gbff_action']

    def process_gbff_action(self, request, queryset):
        """
        Admin action to process GBFF files for selected genomic sequences.
        """
        for obj in queryset:
            try:
                obj.process_gbff()
                self.message_user(request, f"Processed GBFF for accession: {obj.accession}")
            except ValidationError as e:
                self.message_user(request, f"Error processing GBFF: {e}", level='error')

    process_gbff_action.short_description = "Process GBFF files for selected items"


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = '__all__'

    def clean_qualifiers(self):
        # Optional: Add custom validation or formatting for qualifiers
        qualifiers = self.cleaned_data.get('qualifiers')
        return qualifiers.strip()  # Example of cleaning the qualifiers field


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    form = FeatureForm
    list_display = ('sequence', 'type', 'start', 'end', 'qualifiers_summary')
    list_filter = ('type',)
    search_fields = ('type', 'sequence__accession')
    ordering = ('start',)
    list_per_page = 20  # Limit the number of items displayed per page to 20

    class Media:
        css = {
            'all': ('css/admin/feature_custom.css',),  # Link the CSS file
        }
        js = ('js/admin/feature_custom.js',)  # Link the JS file

    # Custom method to display truncated qualifiers in the list view
    def qualifiers_summary(self, obj):
        return f"{obj.qualifiers[:50]}..."  # Shorten qualifiers for easier reading

    qualifiers_summary.short_description = 'Qualifiers'
