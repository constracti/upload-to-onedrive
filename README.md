# Upload to OneDrive

Upload a file to OneDrive using Python.

## Dependencies

- **Python 3**
- **Requests** project
```
python3 -m pip install requests
```

## Installation

Download Python source files or clone this repository.

Navigate to https://portal.azure.com/ and create a new app registration.

Give access to your organizational directory.

In the **Redirect URI** section select **Web** as a platform and set http://localhost/auth as the value of the **URI**.

Rename or copy **client_secret.sample.json** to **client_secret.json**.
Edit the resulting file:
* Open your **Endpoints** and copy the **OAuth 2.0 authorization endpoint (v2)** to the **authorization_endpoint** field.
* From the same screen, copy the **OAuth 2.0 token endpoint (v2)** to the **token_endpoint** field.
* Copy the **Application (client) ID** to the **client_id** field.
* Create a **New client secret** and copy its value to the **client_secret** field.

Remove any **API Permissions**.

## Authentication

Run **authorize.py**.
```
./authorize.py
```

Open the printed URL in a browser and follow the instructions.

## Usage

### Upload

Run **simple_upload.py**:
```
./simple_upload.py [--path PATH] FILE
```
where `FILE` is the file to be uploaded to the `PATH` path in OneDrive.

If `PATH` is omitted, the file will be uploaded to the root.

Otherwise, `PATH` should end with a slash `/` character.

### Upload large files

Run **resumable_upload.py**:
```
./resumable_upload.py [--path PATH] [--block-limit BLOCK_LIMIT] FILE
```
to upload the file in blocks of `BLOCK_LIMIT` bytes.

Arguments `FILE` and `PATH` are the same as in **simple_upload.py**.

The optional positive integer `BLOCK_LIMIT` has the default value of `327,680` = `320K`.

### Delete old files

Run **delete_older.py**:
```
./delete_older.py [--days DAYS] PATH
```
to delete files from the `PATH` path in OneDrive, created at least `DAYS` days ago.

`PATH` should not end with a slash `/` character.

The optional non-negative integer `DAYS` has the default value of `7`.

### Keep new files

Run **keep_newer.py**:
```
./keep_newer.py [--count COUNT] PATH PREFIX
```
to delete all files from the `PATH` path in OneDrive, whose name start with `PREFIX`, except for the last `COUNT` files when sorted by name.

`PATH` should not end with a slash `/` character.

The optional non-negative integer `COUNT` has the default value of `7`.
