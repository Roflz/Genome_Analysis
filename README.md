# Genome_Analysis

This pipeline takes in a genomic sequence in fasta (fna) format, as well as an annotation file in genbank (gbff) format. It analyzes the files and stores the data in a PostgreSQL database. The data can be uploaded and seen in a UI by running the Django Server.
Additionally, the app contains commands to visualize the Genomic Data through scripts written in R.

Pre-reqs:
PostGreSQL, Python, R, Django installed and in your PATH


1. Create a PostgreSQL database called data_analysis:
```createdb -h localhost -p 5432 -U postgres data_analysis```

2. Run migrations for the Django Project:
```Genome_Analysis\analytics_pipeline>py manage.py migrate```

3. Create your Django admin login:
```Genome_Analysis\analytics_pipeline>py manage.py createsuperuser```

4. Set your settings and login info for your postgres user in analytics_pipeline/analytics_pipeline/settings.py in the DATABASES section.

5. Run the Django Server:
```Genome_Analysis\analytics_pipeline>py manage.py runserver```

6. Go to the admin page of your server, likely 'http://127.0.0.1:8000/admin/' or 'http://localhost/admin/'

7. Log in with your admin login and you'll see the admin UI




![image](https://github.com/user-attachments/assets/d872d0d7-a442-4788-af89-b4bbe46708dc)



8. Click +Add next to Genomic Sequences, and add the fasta (.fna) and genbank (.gbff) files in Genome_Analysis\Sample_Data\ecoli_data\GCA_000005845.2

![image](https://github.com/user-attachments/assets/40c41caa-9c12-4b59-b1bc-2f75224d7468)

9. Click Save. Now you can see a description of the Genomic Sequence you just uploaded for E. Coli. If you click the link to the Accession ID, it will have limited information.
10. Go back to the Genomic Sequences list. Select the check box next to that Sequence, and set your action to 'Process gbff file for selected items', then hit GO.

![image](https://github.com/user-attachments/assets/07c62bda-4b23-4e09-b370-13ec6e146069)

11. Now if you go to that Accession ID, you will see a list of all the annotated features in that sequence.

![image](https://github.com/user-attachments/assets/67f891bd-c099-4cb3-82de-4575a9784892)


12. This list is very rudimentary and hard to read, so to create a CSV of this feature data, as well as visualizations, do the following:

```Genome_Analysis\analytics_pipeline>py manage.py export_annotations```

13. This will create a csv 'genomic_annotations.csv', and pdf 'Rplots.pdf' in your project folder.

genomic_annotations.csv contains all the raw annotation data for the E.Coli genome. 
Rplots.pdf visualizes this data in plots looking at distribution of feature types and lengths, and Gene Density across the genome.
