from elasticsearch_dsl import Document, Text, InnerDoc, Nested, Date

class Address(InnerDoc):
    street = Text()
    city = Text()
    state = Text()
    zip_code = Text()

class Restaurant(Document):
    name = Text()
    address = Nested(Address)
    grade = Text()
    updated_at = Date()
