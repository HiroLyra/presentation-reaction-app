from django.db import models
import uuid

class Presentation(models.Model):
    """
    発表セッションを表すモデル。

    各発表には一意のUUID、タイトル、説明、作成日時、
    および4種類の反応（thumbs_up, heart, laugh, surprise）のカウンターが含まれる。
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbs_up = models.IntegerField(default=0)
    heart = models.IntegerField(default=0)
    laugh = models.IntegerField(default=0)
    surprise = models.IntegerField(default=0)

    class Meta:
        db_table = 'presentations'
        ordering = ['-created_at']

    def __str__(self) -> str:
        """発表のタイトルを文字列として返す。"""
        return self.title

    def add_reaction(self, reaction_type: str) -> None:
        """
        指定された反応タイプのカウンターを1つ増やす。

        Args:
            reaction_type (str): 反応のタイプ。以下のいずれかを指定:
                - 'thumbs_up': 👍
                - 'heart': ❤️
                - 'laugh': 😂
                - 'surprise': 😮

        Raises:
            ValueError: 無効なreaction_typeが指定された場合

        Example:
            >>> presentation = Presentation.objects.get(id=some_id)
            >>> presentation.add_reaction('thumbs_up')
        """
        if reaction_type == 'thumbs_up':
            self.thumbs_up += 1
        elif reaction_type == 'heart':
            self.heart += 1
        elif reaction_type == 'laugh':
            self.laugh += 1
        elif reaction_type == 'surprise':
            self.surprise += 1
        else:
            raise ValueError(f"Invalid reaction type: {reaction_type}")
        self.save()
