import json
from django.test import Client, TestCase
from django.urls import reverse

from .models import Presentation


class PresentationModelTests(TestCase):
    """Presentationモデルのリアクション処理と基本項目を確認する。"""

    def test_create_presentation_defaults(self):
        """作成時に各フィールドが既定値で初期化されることを確認する。"""

        presentation = Presentation.objects.create(
            title="テスト発表", description="テスト"
        )
        self.assertEqual(presentation.title, "テスト発表")
        self.assertEqual(presentation.description, "テスト")
        self.assertEqual(presentation.thumbs_up, 0)
        self.assertEqual(presentation.heart, 0)
        self.assertEqual(presentation.laugh, 0)
        self.assertEqual(presentation.surprise, 0)

    def test_add_reaction_increments_each_counter(self):
        """各リアクションで対応カウンターのみが増加することを検証する。"""

        presentation = Presentation.objects.create(title="タイトル")

        for reaction_type, field_name in [
            ("thumbs_up", "thumbs_up"),
            ("heart", "heart"),
            ("laugh", "laugh"),
            ("surprise", "surprise"),
        ]:
            with self.subTest(reaction_type=reaction_type):
                presentation.add_reaction(reaction_type)
                presentation.refresh_from_db()
                self.assertEqual(getattr(presentation, field_name), 1)
                other_fields = {"thumbs_up", "heart", "laugh", "surprise"} - {
                    field_name
                }
                for other_field in other_fields:
                    self.assertEqual(getattr(presentation, other_field), 0)
                Presentation.objects.filter(id=presentation.id).update(
                    thumbs_up=0, heart=0, laugh=0, surprise=0
                )
                presentation.refresh_from_db()

    def test_add_reaction_invalid_type_raises_value_error(self):
        """未定義のリアクション指定で ValueError が発生することを確認する。"""

        presentation = Presentation.objects.create(title="タイトル")
        with self.assertRaisesMessage(ValueError, "Invalid reaction type: invalid"):
            presentation.add_reaction("invalid")


class PresentationViewTests(TestCase):
    """プレゼンテーション関連APIの成功・失敗応答を確認する。"""

    def setUp(self):
        """APIクライアントを初期化する。"""
        self.client = Client()

    def test_create_presentation_success(self):
        """タイトル付きリクエストで発表が作成されることを確認する。"""

        payload = {"title": "新しい発表", "description": "詳細"}
        response = self.client.post(
            reverse("create_presentation"),
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["title"], payload["title"])
        self.assertEqual(data["description"], payload["description"])
        self.assertTrue(
            Presentation.objects.filter(id=data["id"], title=payload["title"]).exists()
        )

    def test_create_presentation_requires_title(self):
        """タイトル未指定のリクエストがエラーを返すことを確認する。"""

        response = self.client.post(
            reverse("create_presentation"),
            data=json.dumps({"description": "説明のみ"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "タイトルを入力してください。")

    def test_create_presentation_invalid_json_returns_error(self):
        """壊れたJSON入力でフォーマットエラーを通知することを検証する。"""

        response = self.client.post(
            reverse("create_presentation"),
            data="{",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "JSONの形式が不正です。")

    def test_get_presentation_success(self):
        """登録済み発表の詳細が取得できることを確認する。"""

        presentation = Presentation.objects.create(
            title="取得テスト", description="説明"
        )
        response = self.client.get(reverse("get_presentation", args=[presentation.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["id"], str(presentation.id))
        self.assertEqual(data["title"], "取得テスト")
        self.assertEqual(data["description"], "説明")
        self.assertEqual(data["heart"], 0)
        self.assertEqual(data["thumbs_up"], 0)
        self.assertEqual(data["laugh"], 0)
        self.assertEqual(data["surprise"], 0)

    def test_get_presentation_returns_not_found(self):
        """存在しないIDに対して404相当のレスポンスを返すことを検証する。"""

        response = self.client.get(
            reverse("get_presentation", args=["00000000-0000-0000-0000-000000000000"])
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "発表が見つかりません。")

    def test_add_reaction_successfully_increments_counter(self):
        """適切なリアクション追加でカウンターがインクリメントされる。"""

        presentation = Presentation.objects.create(title="リアクションテスト")
        response = self.client.post(
            reverse("add_reaction", args=[presentation.id]),
            data=json.dumps({"reaction_type": "thumbs_up"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        presentation.refresh_from_db()
        self.assertEqual(presentation.thumbs_up, 1)

    def test_add_reaction_requires_reaction_type(self):
        """リアクション種別欠如時にエラー応答となることを確認する。"""

        presentation = Presentation.objects.create(title="リアクションテスト")
        response = self.client.post(
            reverse("add_reaction", args=[presentation.id]),
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "reaction_typeが必要です。")

    def test_add_reaction_handles_invalid_reaction_type(self):
        """未定義リアクション指定でエラー内容が返されることを検証する。"""

        presentation = Presentation.objects.create(title="リアクションテスト")
        response = self.client.post(
            reverse("add_reaction", args=[presentation.id]),
            data=json.dumps({"reaction_type": "invalid"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "Invalid reaction type: invalid")

    def test_add_reaction_invalid_json_returns_error(self):
        """壊れたJSON入力で形式エラーが返ることを確認する。"""

        presentation = Presentation.objects.create(title="リアクションテスト")
        response = self.client.post(
            reverse("add_reaction", args=[presentation.id]),
            data="{",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "JSONの形式が不正です。")

    def test_add_reaction_returns_not_found_for_missing_presentation(self):
        """存在しない発表にリアクションした際のエラー応答を検証する。"""

        response = self.client.post(
            reverse("add_reaction", args=["00000000-0000-0000-0000-000000000000"]),
            data=json.dumps({"reaction_type": "thumbs_up"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "発表が見つかりません。")
