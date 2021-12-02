# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


class WikiMiptPipeline:
    def process_item(self, item, spider):
        return item


class StripPipeline:
    """Обычный стрип для полей без оценок.
    Удаляет пробелы и переносы строк в начале и конце.
    """

    def process_item(self, item, spider):
        for field in ("full_name", "birth_day", "teach_place", "degree"):
            if item[field]:
                item[field] = item[field].strip()
        return item


class SelectScorePipeline:
    """Оставляем только оценку, удаляем информацию о колличестве голосов.
    Если нет голосов - ставим None
    """

    def process_item(self, item, spider):
        score_fields = (
            "knowledge",
            "teaching_skill",
            "commication_skill",
            "easy_exam",
            "overall_score",
        )
        for field in score_fields:
            if item[field] == "( нет голосов )":
                item[field] = None
            else:
                item[field] = item[field].split()[0]
        return item
