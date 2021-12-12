# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class LaraparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        final_salary = self.process_salary(item['salary'])
        item['min_salary'] = final_salary[0]
        item['max_salary'] = final_salary[1]
        del item['salary']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary):
        if (salary[0] == 'з/п не указана') & (not salary):
            min = None
            max = None
        elif salary[0] == 'до':
            min = None
            max = salary[1].replace('\xa0', '')
        elif salary[0] == 'от':
            min = salary[1].replace('\xa0', '')
            max = None
        else:
            min = salary[1].replace('\xa0', '')
            max = salary[3].replace('\xa0', '')

        return min, max

    def process_salary_sj(self, salary):
        if (salary[0] == 'По договорённости') & (not salary):
            min = None
            max = None
        elif salary[0] == 'до':
            min = None
            max = salary[2].replace('\xa0', '')
            max = max[:-5]
        elif salary[0] == 'от':
            min = salary[2].replace('\xa0', '')
            min = min[:-5]
            max = None
        else:
            min = salary[0].replace('\xa0', '')
            max = salary[4].replace('\xa0', '')

        return min, max
