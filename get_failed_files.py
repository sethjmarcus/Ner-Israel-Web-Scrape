# get failed files
import csv

import urllib.request




# Open the TSV file using 'csv.reader' with tab delimiter
with open('failed.tsv', 'r') as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    for row in tsv_reader:
        download_url, title, path = row[0], row[1], row[2]
        
        for char in '[]':
            download_url = download_url.replace(char, "")
            title = title.replace(char, "")
            path = path.replace(char, "")
        
        file_name = '/media/seth/SETH_BACKUP/' + path + "/" + title
        print(download_url)
        break
        #urllib.request.urlretrieve(download_url, file_name)
        