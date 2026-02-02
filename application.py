import hashlib
import hmac
import json
import os
import urllib.request
from datetime import datetime


def build_json_payload():
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "name": "Tomislav Maricevic",
        "email": "sour.node3049@sorting.me",
        "resume_link": "https://tmarice.dev/tomislav_maricevic_cv.pdf",
        "repository_link": f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}",
        "action_run_link": f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/"
        f"{os.environ['GITHUB_RUN_ID']}",
    }

    return payload


def serialize_payload(payload):
    sorted_payload = dict(sorted(payload.items()))
    serialized_payload = json.dumps(sorted_payload, separators=(",", ":")).encode(
        "utf-8"
    )

    return serialized_payload


def get_x_signature_256(serialized_payload, signing_secret):
    signature = hmac.new(
        key=signing_secret.encode("utf-8"),
        msg=serialized_payload,
        digestmod=hashlib.sha256,
    ).hexdigest()
    return signature


def send_request(serialized_payload, x_signature_256):
    request = urllib.request.Request(
        url=os.environ["TARGET_URL"],
        data=serialized_payload,
        headers={
            "Content-Type": "application/json",
            "X-Signature-256": f"sha256={x_signature_256}",
        },
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        response_body = response.read()
        print(f"Response status: {response.status}")
        print(f"Response body: {response_body.decode('utf-8')}")


def main():
    payload = build_json_payload()
    serialized_payload = serialize_payload(payload=payload)
    x_signature_256 = get_x_signature_256(
        serialized_payload=serialized_payload,
        signing_secret=os.environ["SIGNING_SECRET"],
    )
    send_request(
        serialized_payload=serialized_payload,
        x_signature_256=x_signature_256,
    )


if __name__ == "__main__":
    main()
