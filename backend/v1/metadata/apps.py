import json
import os
from pathlib import Path
from django.apps import AppConfig
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import BaseCommand

# class Command(BaseCommand):
#     def countries_data(self, *args, **options):
#         try:
#             # Get the absolute path of the JSON file
#             base_dir = Path(__file__).resolve().parent.parent  # Moves up to ecommerce folder
#             json_path = base_dir / "common" / "otherdata" / "countrydetails.json"
#
#             with open(json_path, "r", encoding="utf-8") as file:
#                 countries_data = json.load(file)
#
#             cache.set("countries_data", countries_data, timeout=None)  # Store indefinitely
#             print("Country details cached successfully")
#
#         except Exception as e:
#             print(f"Error loading country details: {e}")


class MetadataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metadata'

    # def ready(self):
    #     call_command('initialize_country_data')


