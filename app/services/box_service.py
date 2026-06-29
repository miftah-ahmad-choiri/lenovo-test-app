import os

from box_sdk_gen import (
    BoxClient,
    BoxDeveloperTokenAuth,
    CreateFolderParent,
    UploadFileAttributes,
    UploadFileAttributesParentField,
)
from box_sdk_gen.box.errors import BoxAPIError

from app.config.settings import (
    BOX_TOKEN,
    BOX_UPLOAD_ROOT_FOLDER_ID,
    BOX_UPLOAD_FOLDER_NAME,
)


def _get_client():
    auth = BoxDeveloperTokenAuth(token=BOX_TOKEN)
    return BoxClient(auth=auth)


def _get_or_create_folder(client, folder_name, parent_id):
    """Return an existing Box folder or create it if it doesn't exist."""
    try:
        folder = client.folders.create_folder(
            name=folder_name,
            parent=CreateFolderParent(id=parent_id),
        )
        return folder

    except BoxAPIError as e:
        if e.response_info.status_code == 409:
            # Folder already exists — reuse it
            conflict = e.response_info.body["context_info"]["conflicts"][0]
            return client.folders.get_folder_by_id(conflict["id"])
        raise


def upload_file_to_box(local_path: str, filename: str) -> dict:
    """
    Upload a local file to Box, then delete it from the local filesystem.

    Returns a dict with keys:
        box_file_id   — Box file id of the uploaded file
        box_file_name — name as stored in Box
        deleted_local — True if the local file was removed
    """
    client = _get_client()

    folder = _get_or_create_folder(
        client,
        BOX_UPLOAD_FOLDER_NAME,
        BOX_UPLOAD_ROOT_FOLDER_ID,
    )

    with open(local_path, "rb") as f:
        uploaded = client.uploads.upload_file(
            attributes=UploadFileAttributes(
                name=filename,
                parent=UploadFileAttributesParentField(id=folder.id),
            ),
            file=f,
        )

    if not uploaded.entries:
        raise Exception("Box upload returned no entries")

    box_file = uploaded.entries[0]

    # Delete local copy after a successful Box upload
    os.remove(local_path)

    return {
        "box_file_id": box_file.id,
        "box_file_name": box_file.name,
        "deleted_local": True,
    }
