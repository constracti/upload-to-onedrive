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
./simple_upload.py FILE
```
where `FILE` is the file to be uploaded to the root folder in OneDrive.

### Upload large files

For larger files run **resumable_upload.py**:
```
./resumable_upload.py [--block-limit BLOCK_LIMIT] FILE
```
where `FILE` is the file to be uploaded to the root folder in OneDrive
and `BLOCK_LIMIT` is an optional positive integer with the default value of `327,680` = `320K`.
Then the file will be uploaded in blocks of `BLOCK_LIMIT` bytes.
