from requests import get, post, patch
from time import mktime
from lib.pocketbase import PocketBase

pb = PocketBase(get, post, patch, mktime)

print("JWT:", pb.get_jwt())
