# complete_colonel/models.py


from django.db import models


class Mission(models.Model):
    """
    大佐の実行するミッション
    """

    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_comment = models.CharField(max_length=200, blank=True) # メイトリクスの完了報告
    is_archived = models.BooleanField(default=False) # こいつがあれば消されても復活できるぜ

    def __str__(self):
        return self.title
