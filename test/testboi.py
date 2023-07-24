import time
import subprocess

from env import POCKETBASE_ADMIN_USERNAME, POCKETBASE_ADMIN_PASSWORD

PATH_TO_POCKETBASE = "./pocketbase/pocketbase"

PATH_TO_POCKETBASE_TEST = "./test/pocketbase"
PATH_TO_POCKETBASE_TEST_DATA = "test/pocketbase/pb_data"
PATH_TO_POCKETBASE_TEST_MIGRATIONS = "pocketbase/pb_migrations"


class TestBoi:
    def pocketbase_reset(self):
        print("-> Test: Resetting PocketBase")
        subprocess.run(["rm", "-rf", PATH_TO_POCKETBASE_TEST]) # Delete existing test data
        subprocess.run(["mkdir", PATH_TO_POCKETBASE_TEST])

    def pocketbase_start(self):
        print("-> Test: Starting PocketBase")
        try:
            self.server = subprocess.Popen(
                [
                    PATH_TO_POCKETBASE,
                    "serve",
                    "--dir",
                    PATH_TO_POCKETBASE_TEST_DATA,
                    "--migrationsDir",
                    PATH_TO_POCKETBASE_TEST_MIGRATIONS
                ]
            )

            # Wait for server to start
            time.sleep(1)

            # Create admin account
            subprocess.run(
                [
                    PATH_TO_POCKETBASE,
                    "admin",
                    "create",
                    POCKETBASE_ADMIN_USERNAME,
                    POCKETBASE_ADMIN_PASSWORD,
                    "--dir",
                    PATH_TO_POCKETBASE_TEST_DATA,
                    "--migrationsDir",
                    PATH_TO_POCKETBASE_TEST_MIGRATIONS
                ]
            )

        except KeyboardInterrupt:
            self.pocketbase_stop()
            raise

    def pocketbase_stop(self):
        print("-> Test: Stopping PocketBase")
        try:
            if self.server:
                self.server.terminate()
        except Exception:
            pass
