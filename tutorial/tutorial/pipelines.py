# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter
from scrapy import Request

class TutorialPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x, meta={'item': item}) for x in item.get(self.FILES_URLS_FIELD, [])]


    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta.get('item')
        file_name: str =  item['original_file_name'].replace(",", "_")
        print('\n\n', file_name, '\n\n')
        return file_name

