from arthub_api import (
    OpenAPI,
    Storage,
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

# To use the storage interface, you need to instantiate the Storage object
storage = Storage(open_api)

# Example 1:
# download a directory("sdk_test/storage_test/download" in depot "trial") to "D://test"
res = storage.download_by_path(asset_hub="trial",
                               remote_node_path="sdk_test/storage_test/download",
                               local_dir_path="D:/test",
                               same_name_override=False)
if not res.is_succeeded():
    print("download failed, message: %s", res.error_message())
    exit(-1)

# The download is successful, return the local path
local_downloaded_path = res.data[0]  # should be "D:/test/download"
print("successfully downloaded directory to %s", local_downloaded_path)

# Example 2:
# upload downloaded directory to ArtHub storage
res = storage.upload_to_directory_by_path(asset_hub="trial",
                                          remote_dir_path="sdk_test/storage_test/upload",
                                          local_path=local_downloaded_path,
                                          tags_to_create=["sdk_test"],
                                          same_name_override=False,
                                          need_convert=True,
                                          description= "description test")
if not res.is_succeeded():
    print("upload failed, message: %s", res.error_message())
    exit(-1)

# The upload is successful, return the id of uploaded directory
uploaded_dir_id = res.data[0]
print("the newly uploaded directory id is %d", uploaded_dir_id)

# Example 3:
# delete the directory just uploaded
res = storage.delete_node_by_path(asset_hub="trial",
                                  remote_node_path="sdk_test/storage_test/upload/download")
if not res.is_succeeded():
    print("delete failed, message: %s", res.error_message())
    exit(-1)
print("delete successfully")
