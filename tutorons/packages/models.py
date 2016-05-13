from peewee import Model, CharField, IntegerField, ForeignKeyField, DateTimeField, TextField, BooleanField

class NPMPackageTutoron(Model):
    package = CharField(null=True, index=True)
    description = TextField(null=True)
    documented_since = DateTimeField(null=True)
    url = CharField(null=True)
    response_time = CharField(null=True)
    resolution_time = CharField(null=True)
    num_questions = IntegerField(null=True)
    results_with_code = TextField(null=True)

# res = make_request(
#         default_requests_session.get,
#         "https://skimdb.npmjs.com/registry/_all_docs",
#     )
# if res is not None:
#     packages = res.json()['rows']
#     for p in packages:
#         NPMPackageTutoron.get_or_create(package=p['id'])

p = NPMPackageTutoron(
    package="nodemailer",
    description="Easy as cake e-mail sending from your Node.js applications",
    documented_since="2013",
    url="https://www.npmjs.com/package/nodemailer",
    response_time="1 day",
    resolution_time="3.5 days",
    num_questions="50",
    results_with_code="60-90% (typical queries)"
)
p.save()
