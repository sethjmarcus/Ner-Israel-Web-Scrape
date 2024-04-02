# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.exceptions import DropItem

# for slugify
import unicodedata
import re

# for saving fails
import csv

class TutorialPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x, meta={'item': item}) for x in item.get(self.FILES_URLS_FIELD, [])]


    def file_path(self, request, response=None, info=None, *, item=None):
        invalid_chars = ':,[]\'"?/'
        
        item = request.meta.get('item')'
            file_name = file_name.replace(char, "")
            folder_name = folder_name.replace(char, "")

        #print('file name', file_name, '\n\n')
        return folder_name + "/" + file_name

    def item_completed(self, results, item, info):
        file_paths = [x["path"] for ok, x in results if ok]
        if not file_paths:
            print(item['original_file_name'])

            with open('/home/seth/Downloads/failed.txt', 'a', encoding='utf-8') as f:
                tsv_writer = tsv_writer = csv.writer(f, delimiter='\t')
                tsv_writer.writerow([item['file_urls'], item['original_file_name'], item['folder_name']])
                
            raise DropItem("Item contains no files")
        #adapter = ItemAdapter(item)
        #adapter["file_paths"] = file_paths
        return item


    # taken from https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    def slugify(value, allow_unicode=True):
        """
        Taken from https://github.com/django/django/blob/master/django/utils/text.py
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
        """
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')
