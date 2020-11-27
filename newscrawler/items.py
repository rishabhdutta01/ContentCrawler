# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item
from itemloaders.processors import MapCompose,TakeFirst, Join, Identity

def strip_extra_chars(text):
    return text.strip(' ,:\n')

class DefaultAwareNewscrawlerItem(Item):
    """Item class aware of 'default' metadata of its fields.

    For instance to work, each field, which must have a default value, must
    have a new `default` parameter set in field constructor, e.g.::

        class MyItem(DefaultAwareItem):
            my_defaulted_field = scrapy.Field()
            # Identical to:
            #my_defaulted_field = scrapy.Field(default=None)
            my_other_defaulted_field = scrapy.Field(default='a value')

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field_metadata in self.fields.items():
            self.setdefault(field_name, field_metadata.get('default'))


class NewscrawlerItem(DefaultAwareNewscrawlerItem):
    # define the fields for your item here like:
    id = Field(output_processor=TakeFirst())
    title = Field(default= "", input_processor=MapCompose(strip_extra_chars),
                  output_processor=TakeFirst())
    url = Field(default= "", output_processor=TakeFirst())
    author = Field(default= "", input_processor=MapCompose(strip_extra_chars),
                   output_processor=TakeFirst())
    date = Field(default= "", output_processor=TakeFirst())
    content = Field(default= "", input_processor=MapCompose(strip_extra_chars),
                    output_processor=Join())
    location = Field(default= "", input_processor=MapCompose(strip_extra_chars),
                     output_processor=TakeFirst())
