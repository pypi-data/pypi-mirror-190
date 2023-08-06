from arthub_api import (
    OpenAPI,
    api_config_qq
)

# First of all, instantiate OpenAPI object
open_api = OpenAPI(
    api_config_qq  # to access ArtHub extranet domain
)

# Login
res = open_api.login(account_name="joeyding@tencent.com", password="XXX")
if not res.is_succeeded():
    print("login failed, message: %s", res.error_message())
    exit(-1)

# Example 1:
# obtain the account info
res = open_api.get_account_detail()
if res.is_succeeded():
    # email
    email = res.first_result("email")
    # phone
    phone = res.first_result("phone")

# Example 2:
# obtain the info of a node with ID 110347251725157 in the storage disk
res = open_api.depot_get_node_brief_by_ids(asset_hub="trial", ids=[110347251725157])
if res.is_succeeded():
    node_info = res.results.get(0)
    print("node name: " + node_info["name"])
    print("node type: " + node_info["type"])
