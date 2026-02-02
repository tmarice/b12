from unittest import TestCase, mock

from application import main


class TestMain(TestCase):
    MOCK_JSON_PAYLOAD = {
        "timestamp": "2026-01-06T16:59:37.571Z",
        "name": "Your name",
        "email": "you@example.com",
        "resume_link": "https://pdf-or-html-or-linkedin.example.com",
        "repository_link": "https://link-to-github-or-other-forge.example.com/your/repository",
        "action_run_link": "https://link-to-github-or-another-forge.example.com/your/repository/actions/runs/run_id",
    }

    @mock.patch("application.build_json_payload", return_value=MOCK_JSON_PAYLOAD)
    @mock.patch("application.send_request")
    @mock.patch.dict(
        "os.environ",
        {"SIGNING_SECRET": "hello-there-from-b12"},
        clear=False,
    )
    def test_main(self, mock_send_request, mock_build_json_payload):
        main()

        mock_send_request.assert_called_once()
        kwargs = mock_send_request.call_args[1]
        serialized_payload = kwargs.get("serialized_payload")
        x_signature_256 = kwargs.get("x_signature_256")

        self.assertEqual(
            serialized_payload,
            b'{"action_run_link":"https://link-to-github-or-another-forge.example.com/your/repository/actions/runs/run_id","email":"you@example.com","name":"Your name","repository_link":"https://link-to-github-or-other-forge.example.com/your/repository","resume_link":"https://pdf-or-html-or-linkedin.example.com","timestamp":"2026-01-06T16:59:37.571Z"}',
        )

        self.assertEqual(
            x_signature_256,
            "c5db257a56e3c258ec1162459c9a295280871269f4cf70146d2c9f1b52671d45",
        )
