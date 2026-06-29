import os

from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth

from app.config.settings import (
    BOX_TOKEN,
    BOX_DOWNLOAD_FOLDER_PATH,
    BOX_DOWNLOAD_FILE_NAME,
    DOWNLOAD_DIR,
)


def _get_client():
    auth = BoxDeveloperTokenAuth(token=BOX_TOKEN)
    return BoxClient(auth=auth)


def _get_folder_id_by_path(client, path: str) -> str:
    """
    Walk a slash-separated Box folder path and return the final folder's id.
    Raises Exception if any segment is not found.
    """
    current_folder_id = "0"  # Box root

    segments = [s for s in path.strip("/").split("/") if s]

    for folder_name in segments:

        items = client.folders.get_folder_items(current_folder_id)

        found_id = None

        for item in items.entries:
            if (
                str(item.type).lower().find("folder") >= 0
                and item.name == folder_name
            ):
                found_id = item.id
                break

        if not found_id:
            raise Exception(
                f"Box folder not found: '{folder_name}' "
                f"(path: {path})"
            )

        current_folder_id = found_id

    return current_folder_id


def download_excel_from_box(
    folder_path: str = None,
    file_name: str = None,
) -> dict:
    """
    Download an Excel file from a Box folder path to DOWNLOAD_DIR.

    Parameters default to settings values so the caller can omit them.

    Returns:
        local_path  — absolute path to the downloaded file
        file_name   — name of the file
        box_file_id — Box id of the downloaded file
    """
    folder_path = folder_path or BOX_DOWNLOAD_FOLDER_PATH
    file_name   = file_name   or BOX_DOWNLOAD_FILE_NAME

    client = _get_client()

    folder_id = _get_folder_id_by_path(client, folder_path)

    # Find the target file inside the folder
    items = client.folders.get_folder_items(folder_id)

    target_file = None

    for item in items.entries:
        if (
            str(item.type).lower().find("file") >= 0
            and item.name == file_name
        ):
            target_file = item
            break

    if target_file is None:
        raise Exception(
            f"File '{file_name}' not found in Box folder '{folder_path}'"
        )

    # Download
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    content = client.downloads.download_file(target_file.id)

    local_path = os.path.join(DOWNLOAD_DIR, target_file.name)

    with open(local_path, "wb") as f:
        for chunk in content:
            f.write(chunk)

    return {
        "local_path":  local_path,
        "file_name":   target_file.name,
        "box_file_id": target_file.id,
    }
