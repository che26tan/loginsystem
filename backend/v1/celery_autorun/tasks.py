from pathlib import Path
import json
from celery import shared_task
from django.core.cache import caches


@shared_task(bind=True, max_retries=5, default_retry_delay=10)
def metadata_initialised(self, *args, **kwargs):
    try:
        # Resolving the base directory relative to the current file
        base_dir = Path(__file__).resolve().parent.parent

        # Building the path in a more robust way
        json_path = base_dir / "common" / "otherdata" / "countrydetails.json"

        # Debug: Check path being constructed
        print(f"Resolved JSON Path: {json_path}")

        with open(json_path, "r", encoding="utf-8") as file:
            countries_data = json.load(file)
            print(f'open file and show country data{countries_data}')

        metadata_cached = caches['metadata']
        metadata_cached.set("countries_data", countries_data, timeout=None)
        print("Country details cached successfully")

    except Exception as e:
        print(f"Error loading country details: {e}")


# @shared_task
# def payment_confirm_from_portal(): # Payment Gateway
#     print(f"Successfully fetched")
#
# @shared_task
# def payment_confirm_to_email(): # Payment Confirmed msg to User Email
#     print(f"Successfully sent")
#
# @shared_task
# def payment_confirm_to_phone(): # Payment Confirmed msg to User Phone
#     print(f"Successfully sent")
#
# @shared_task
# def payment_failed_to_phone(): # Payment Failed msg to User phone
#     print(f"Successfully sent")
