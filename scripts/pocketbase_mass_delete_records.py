################################################################################
################################################################################
# Temporarily disabled
################################################################################
################################################################################

import os
import pocketbase
from dotenv import load_dotenv

load_dotenv(".env")

MASS_DELETE_COLLECTION = "moistures"

def run_main():
    # Connect to PocketBase
    client = pocketbase.PocketBase(os.getenv("POCKETBASE_SERVER_URL"))
    client.admins.auth_with_password(os.getenv("POCKETBASE_ADMIN_USERNAME"), os.getenv("POCKETBASE_ADMIN_PASSWORD"))

    RECORDS_PER_PAGE = 500
    page_number = 1

    while True:
        records = client.collection(MASS_DELETE_COLLECTION).get_list(page_number, RECORDS_PER_PAGE)

        if not records.items:
            break  # No more records to fetch
        
        for record in records.items:
            client.collection(MASS_DELETE_COLLECTION).delete(record.id)
        
        if page_number >= records.total_pages:
            break  # All pages have been processed
        
        page_number += 1  # Go to the next page


if __name__ == "__main__":
    run_main()
