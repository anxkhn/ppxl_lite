import json
import random
import mimetypes
import sys
from typing import Dict, List, Optional, Union, Generator, Any
from uuid import uuid4
from curl_cffi import CurlMime, requests

from config import (
    DEFAULT_HEADERS,
    ENDPOINT_SSE_ASK,
    ENDPOINT_UPLOAD_URL,
    MODELS,
    SEARCH_MODES,
    SEARCH_SOURCES,
    get_backend_for_model,
)


class Client:
    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        self.session = requests.Session(
            headers=DEFAULT_HEADERS.copy(),
            cookies=cookies or {},
            impersonate="chrome",
        )
        self.own = bool(cookies)
        self.copilot = float("inf") if self.own else 0
        self.file_upload = float("inf") if self.own else 0
        self.timestamp = format(random.getrandbits(32), "08x")

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Returns user info (email, username, subscription_tier) or None."""
        if not self.own:
            return None
        try:
            resp = self.session.get("https://www.perplexity.ai/api/auth/session")
            if resp.ok:
                return resp.json().get("user")
        except Exception:
            pass
        return None

    def get_limits(self) -> Optional[Dict[str, Any]]:
        """Returns usage limits (gpt4_limit, pplx_alpha_limit, etc.) or None."""
        if not self.own:
            return None
        try:
            resp = self.session.get("https://www.perplexity.ai/rest/user/settings")
            if resp.ok:
                return resp.json()
        except Exception:
            pass
        return None

    def search(
        self,
        query: str,
        mode: str = "auto",
        model: Optional[str] = None,
        sources: List[str] = ["web"],
        files: Dict[str, Union[str, bytes]] = None,
        stream: bool = False,
        language: str = "en-US",
        follow_up: Optional[Dict] = None,
        incognito: bool = False,
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        if mode not in SEARCH_MODES:
            raise ValueError(f"Invalid mode. Must be one of: {SEARCH_MODES}")

        if sources:
            invalid_sources = [s for s in sources if s not in SEARCH_SOURCES]
            if invalid_sources:
                raise ValueError(
                    f"Invalid sources: {invalid_sources}. Must be in: {SEARCH_SOURCES}"
                )

        if model is not None:
            valid_models = MODELS.get(mode, [])
            if model not in valid_models:
                raise ValueError(
                    f"Invalid model '{model}' for mode '{mode}'. Valid models: {valid_models}"
                )

        if mode in ["pro", "reasoning", "deep research"] and not self.own:
            raise ValueError(f"Mode '{mode}' requires account cookies")

        files = files or {}

        if files and not self.own:
            raise ValueError("File upload requires account cookies")

        uploaded_files = []
        for filename, file_content in files.items():
            uploaded_url = self._upload_file(filename, file_content)
            uploaded_files.append(uploaded_url)

        json_data = {
            "query_str": query,
            "params": {
                "attachments": uploaded_files
                + (follow_up.get("attachments", []) if follow_up else []),
                "frontend_context_uuid": str(uuid4()),
                "frontend_uuid": str(uuid4()),
                "is_incognito": incognito,
                "language": language,
                "last_backend_uuid": (
                    follow_up.get("backend_uuid") if follow_up else None
                ),
                "mode": "concise" if mode == "auto" else "copilot",
                "model_preference": get_backend_for_model(mode, model),
                "source": "default",
                "sources": sources,
                "version": "2.18",
            },
        }

        resp = self.session.post(ENDPOINT_SSE_ASK, json=json_data, stream=True)

        if not resp.ok:
            raise Exception(
                f"API request failed with status {resp.status_code}: {resp.text}"
            )

        if stream:
            return self._stream_response(resp)
        else:
            return self._get_final_response(resp)

    def _upload_file(self, filename: str, file_content: Union[str, bytes]) -> str:
        file_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        file_size = sys.getsizeof(file_content)

        upload_info = self.session.post(
            ENDPOINT_UPLOAD_URL,
            params={"version": "2.18", "source": "default"},
            json={
                "content_type": file_type,
                "file_size": file_size,
                "filename": filename,
                "force_image": False,
                "source": "default",
            },
        ).json()

        mp = CurlMime()
        for key, value in upload_info["fields"].items():
            mp.addpart(name=key, data=value)
        mp.addpart(
            name="file",
            content_type=file_type,
            filename=filename,
            data=file_content,
        )

        upload_resp = self.session.post(upload_info["s3_bucket_url"], multipart=mp)

        if not upload_resp.ok:
            raise Exception(f"File upload failed: {upload_resp.text}")

        if "image/upload" in upload_info["s3_object_url"]:
            uploaded_url = upload_resp.json()["secure_url"]
            uploaded_url = uploaded_url.replace("/private/s--", "/private/")
            uploaded_url = (
                uploaded_url.split("/v")[0] + uploaded_url.split("/user_uploads")[1]
            )
            uploaded_url = uploaded_url.replace(
                "/user_uploads/", "/private/user_uploads/"
            )
        else:
            uploaded_url = upload_info["s3_object_url"]

        return uploaded_url

    def _stream_response(self, resp) -> Generator[Dict[str, Any], None, None]:
        for chunk in resp.iter_lines(delimiter=b"\r\n\r\n"):
            content = chunk.decode("utf-8")

            if content.startswith("event: message\r\n"):
                try:
                    content_json = json.loads(
                        content[len("event: message\r\ndata: ") :]
                    )
                    if "text" in content_json and content_json["text"]:
                        content_json = self._parse_response_content(content_json)
                    yield content_json
                except (json.JSONDecodeError, KeyError):
                    continue

            elif content.startswith("event: end_of_stream\r\n"):
                return

    def _get_final_response(self, resp) -> Dict[str, Any]:
        chunks = []

        for chunk in resp.iter_lines(delimiter=b"\r\n\r\n"):
            content = chunk.decode("utf-8")

            if content.startswith("event: message\r\n"):
                try:
                    content_json = json.loads(
                        content[len("event: message\r\ndata: ") :]
                    )
                    if "text" in content_json and content_json["text"]:
                        content_json = self._parse_response_content(content_json)
                    chunks.append(content_json)
                except (json.JSONDecodeError, KeyError):
                    continue

            elif content.startswith("event: end_of_stream\r\n"):
                break

        return chunks[-1] if chunks else {}

    def _parse_response_content(self, content_json: Dict[str, Any]) -> Dict[str, Any]:
        try:
            text_parsed = json.loads(content_json["text"])

            if isinstance(text_parsed, list):
                for step in text_parsed:
                    if step.get("step_type") == "FINAL":
                        final_content = step.get("content", {})
                        if "answer" in final_content:
                            answer_data = json.loads(final_content["answer"])
                            content_json["answer"] = answer_data.get("answer", "")
                            content_json["chunks"] = answer_data.get("chunks", [])
                            break

            content_json["text"] = text_parsed
        except (json.JSONDecodeError, TypeError, KeyError):
            pass

        return content_json
