"""
Simplified Perplexity AI client (Lite Version).

A lightweight client for interacting with Perplexity AI API without browser automation
or account creation features. Focuses on making API calls with existing cookies.
"""

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
    MODEL_MAPPINGS,
    SEARCH_MODES,
    SEARCH_SOURCES,
)


class Client:
    """
    A lightweight client for interacting with the Perplexity AI API.

    This simplified version removes browser automation and account creation,
    focusing only on making API calls with existing authentication.
    """

    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        """
        Initialize the Perplexity client.

        Args:
            cookies: Optional Perplexity account cookies for enhanced features.
                     If provided, enables pro/reasoning modes and file uploads.
        """
        # Initialize HTTP session with Chrome impersonation
        self.session = requests.Session(
            headers=DEFAULT_HEADERS.copy(),
            cookies=cookies or {},
            impersonate="chrome",
        )

        # Track if using own account
        self.own = bool(cookies)
        self.copilot = float("inf") if self.own else 0
        self.file_upload = float("inf") if self.own else 0

        # Generate unique session identifier
        self.timestamp = format(random.getrandbits(32), "08x")

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
        """
        Execute a search query on Perplexity AI.

        Args:
            query: The search query string
            mode: Search mode ('auto', 'pro', 'reasoning', 'deep research')
            model: Specific model to use (depends on mode and account)
            sources: List of sources (['web', 'scholar', 'social'])
            files: Dictionary of files to upload {filename: content}
            stream: Whether to stream the response
            language: Language code (default: 'en-US')
            follow_up: Previous query for context (for follow-up questions)
            incognito: Whether to enable incognito mode

        Returns:
            Response dictionary with 'answer' key, or generator if stream=True

        Raises:
            AssertionError: If parameters are invalid
            Exception: If file upload fails
        """
        # Validate inputs
        if mode not in SEARCH_MODES:
            raise ValueError(f"Invalid mode. Must be one of: {SEARCH_MODES}")

        if sources:
            invalid_sources = [s for s in sources if s not in SEARCH_SOURCES]
            if invalid_sources:
                raise ValueError(f"Invalid sources: {invalid_sources}. Must be in: {SEARCH_SOURCES}")

        # Check model validity
        if model is not None:
            valid_models = list(MODEL_MAPPINGS.get(mode, {}).keys())
            if model not in valid_models:
                raise ValueError(f"Invalid model '{model}' for mode '{mode}'. Valid models: {valid_models}")

        # Check account requirements
        if mode in ["pro", "reasoning", "deep research"] and not self.own:
            raise ValueError(f"Mode '{mode}' requires account cookies")

        # Initialize files dict if None
        files = files or {}

        # Check file upload limits
        if files and not self.own:
            raise ValueError("File upload requires account cookies")

        # Upload files if provided
        uploaded_files = []
        for filename, file_content in files.items():
            uploaded_url = self._upload_file(filename, file_content)
            uploaded_files.append(uploaded_url)

        # Prepare request payload
        json_data = {
            "query_str": query,
            "params": {
                "attachments": uploaded_files + (follow_up.get("attachments", []) if follow_up else []),
                "frontend_context_uuid": str(uuid4()),
                "frontend_uuid": str(uuid4()),
                "is_incognito": incognito,
                "language": language,
                "last_backend_uuid": follow_up.get("backend_uuid") if follow_up else None,
                "mode": "concise" if mode == "auto" else "copilot",
                "model_preference": MODEL_MAPPINGS[mode][model],
                "source": "default",
                "sources": sources,
                "version": "2.18",
            },
        }

        # Send request
        resp = self.session.post(ENDPOINT_SSE_ASK, json=json_data, stream=True)

        if not resp.ok:
            raise Exception(f"API request failed with status {resp.status_code}: {resp.text}")

        # Process response
        if stream:
            return self._stream_response(resp)
        else:
            return self._get_final_response(resp)

    def _upload_file(self, filename: str, file_content: Union[str, bytes]) -> str:
        """
        Upload a file to Perplexity's servers.

        Args:
            filename: Name of the file
            file_content: File content (string or bytes)

        Returns:
            URL of the uploaded file

        Raises:
            Exception: If upload fails
        """
        # Determine file type
        file_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        file_size = sys.getsizeof(file_content)

        # Get upload URL
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

        # Prepare multipart upload
        mp = CurlMime()
        for key, value in upload_info["fields"].items():
            mp.addpart(name=key, data=value)
        mp.addpart(
            name="file",
            content_type=file_type,
            filename=filename,
            data=file_content,
        )

        # Upload file
        upload_resp = self.session.post(upload_info["s3_bucket_url"], multipart=mp)

        if not upload_resp.ok:
            raise Exception(f"File upload failed: {upload_resp.text}")

        # Get uploaded file URL
        if "image/upload" in upload_info["s3_object_url"]:
            uploaded_url = upload_resp.json()["secure_url"]
            uploaded_url = uploaded_url.replace("/private/s--", "/private/")
            uploaded_url = uploaded_url.split("/v")[0] + uploaded_url.split("/user_uploads")[1]
            uploaded_url = uploaded_url.replace("/user_uploads/", "/private/user_uploads/")
        else:
            uploaded_url = upload_info["s3_object_url"]

        return uploaded_url

    def _stream_response(self, resp) -> Generator[Dict[str, Any], None, None]:
        """
        Generator for streaming response chunks.

        Args:
            resp: HTTP response object

        Yields:
            Response chunks as they arrive
        """
        for chunk in resp.iter_lines(delimiter=b"\r\n\r\n"):
            content = chunk.decode("utf-8")

            if content.startswith("event: message\r\n"):
                try:
                    content_json = json.loads(content[len("event: message\r\ndata: ") :])

                    # Parse nested content if present
                    if "text" in content_json and content_json["text"]:
                        content_json = self._parse_response_content(content_json)

                    yield content_json
                except (json.JSONDecodeError, KeyError):
                    continue

            elif content.startswith("event: end_of_stream\r\n"):
                return

    def _get_final_response(self, resp) -> Dict[str, Any]:
        """
        Get the final response after consuming all chunks.

        Args:
            resp: HTTP response object

        Returns:
            Final response dictionary
        """
        chunks = []

        for chunk in resp.iter_lines(delimiter=b"\r\n\r\n"):
            content = chunk.decode("utf-8")

            if content.startswith("event: message\r\n"):
                try:
                    content_json = json.loads(content[len("event: message\r\ndata: ") :])

                    # Parse nested content if present
                    if "text" in content_json and content_json["text"]:
                        content_json = self._parse_response_content(content_json)

                    chunks.append(content_json)
                except (json.JSONDecodeError, KeyError):
                    continue

            elif content.startswith("event: end_of_stream\r\n"):
                break

        return chunks[-1] if chunks else {}

    def _parse_response_content(self, content_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse nested response content to extract answer.

        Args:
            content_json: Response chunk with nested content

        Returns:
            Parsed content with answer extracted if available
        """
        try:
            text_parsed = json.loads(content_json["text"])

            # Extract answer from FINAL step
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