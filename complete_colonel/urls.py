# complete_colonel/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ------------------------
    # トップページ：通常任務一覧（GET）＆新規任務作成（POST）
    path("", views.mission_list, name="mission_list"),

    # ------------------------
    # 任務を完了状態にする
    # mission_id: 対象任務のID
    path(
        "complete/<int:mission_id>/", 
        views.complete_mission, 
        name="complete_mission"
    ),

    # ------------------------
    # 任務をアーカイブに移動
    # mission_id: 対象任務のID
    path(
        "archive/<int:mission_id>/", 
        views.archive_mission, 
        name="archive_mission"
    ),

    # ------------------------
    # アーカイブ済み任務一覧
    path(
        "archived/", 
        views.archived_missions, 
        name="archived_missions"
    ),

    # ------------------------
    # アーカイブ済み任務を通常任務に戻す（再任務）
    # mission_id: 対象任務のID
    path(
        "reassign/<int:mission_id>/", 
        views.reassign_mission, 
        name="reassign_mission"
    ),

    # ------------------------
    # アーカイブ済み任務を完全削除
    # mission_id: 対象任務のID
    path(
        "delete_permanently/<int:mission_id>/", 
        views.delete_permanently, 
        name="delete_permanently"
    ),
]
