import os
import json
import requests
import magic
_mime = magic.Magic(mime=True)
def _get_body_from_headers(headers):
    try:
        body = {
            "content_type": headers["content-type"],
            "size": int(headers["content-length"]),
            "ext": headers["x-ext"],
            "version": headers["x-version"],
            "created_by": headers["x-createdby"],
            "group": headers["x-group"],
            "name": headers["x-name"],
            "updated_at": headers["x-updatedAt"],
            "created_at": headers["x-createdAt"],
            "meta": headers.get("x-meta", {}),
        }
        return body
    except Exception as err:
        raise Exception(f"{err} is required")
def _get_headers_from_body(body, full_path):
    try:
        headers = {
            "content-type": _mime.from_file(full_path),
            "content-length": str(os.path.getsize(full_path)),
            "x-ext": os.path.splitext(full_path)[1][1:],
            "x-createdby": body.get("created_by", ""),
            "x-group": body.get("group", ""),
            "x-meta": json.dumps(body.get("meta", {})),
        }
        return headers
    except Exception as err:
        raise Exception(f"{err} is required")
class FMS:
    def __init__(self, host, port, base_dir_path):
        self._url = f"{host}:{port}"
        self._base_dir_path = base_dir_path
    def download_latest(self, key):
        try:
            response = requests.get(f"http://{self._url}/{key}", stream=True)
            response.raise_for_status()
            body = _get_body_from_headers(response.headers)
            full_path = os.path.join(self._base_dir_path, body["name"])
            with open(full_path, "wb") as f:
                f.write(response.content)
            return body
        except requests.exceptions.HTTPError as e:
            raise Exception(response.json()["message"])
        except requests.exceptions.ConnectionError as err:
            raise Exception("Connection Error: " + str(err))
    def download_by_version(self, key, version):
        try:
            response = requests.get(f"http://{self._url}/{key}/{version}", stream=True)
            response.raise_for_status()
            body = _get_body_from_headers(response.headers)
            full_path = os.path.join(self._base_dir_path, body["name"])
            with open(full_path, "wb") as f:
                f.write(response.content)
            return body
        except requests.exceptions.HTTPError as e:
            raise Exception(response.json()["message"])
        except requests.exceptions.ConnectionError as err:
            raise Exception("Connection Error: " + str(err))
    def upload_file(self, file_name, file_key, body):
        url = f"http://{self._url}/{file_key}"
        full_path = os.path.join(self._base_dir_path, file_name)
        headers = _get_headers_from_body(body, full_path)
        print(full_path)
        with open(full_path, "rb") as f:
            response = requests.post(url, data=f, headers=headers, stream=True)
        body = response.json()
        return {"body": body}