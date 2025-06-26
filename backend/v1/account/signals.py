# from bson import ObjectId
# from django.conf import settings
# from django.db.models.signals import pre_delete
# from django.dispatch import receiver
# from account.models import MyUsers
# from product.models import Product  # replace with your actual app name
# from pymongo import MongoClient
#
# @receiver(pre_delete, sender=MyUsers)
# def handle_user_mongo_cleanup(sender, instance, **kwargs):
#     try:
#         # 1. Get related AllProduct entries BEFORE they are deleted
#         all_sites = Product.objects.filter(user=instance)
#
#         if all_sites is None:
#             return
#
#         # 2. Get site IDs or any unique field you need
#         site_ids = list(all_sites.values_list('object_id', flat=True))  # adjust if needed
#
#         # 3. Connect to MongoDB
#         client = MongoClient(settings.MONGO_URI)
#         db = client[settings.MONGO_DB]
#         default_collection = db[settings.MONGO_COLLECTION_DEFAULT]
#
#         # 4. Delete corresponding documents in MongoDB
#         result = default_collection.delete_many({"object_id": {"$in": site_ids}})
#         print(f"Deleted {result.deleted_count} MongoDB docs for site_ids: {site_ids}")
#
#     except Exception as e:
#         print(f"Error cleaning MongoDB before user deletion: {e}")