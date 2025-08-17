# complete_colonel/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Mission
import random
from typing import Dict, Any

# ------------------------------------------------------------------
# モード切替フラグ
# True: コマンドー風ネタモード、False: 実務向けシンプルモード
COMMANDO_MODE = True

# ------------------------------------------------------------------
# ベネットのセリフ集（ネタモード用）
BENNETT_QUOTES: Dict[str, list[str]] = {
    "incomplete": [
        "大佐ぁ！どうしたそれで終わりか？",
        "大佐ぁ！ウヘヘ...テメーなんざ怖くねぇ！",
        "大佐ぁ！ウハハハ...まだ本気じゃないよな？",
    ],
    "complete": [
        "大佐ぁ！たった一つ片付けたぐらいで調子に乗るなよ！",
        "大佐ぁ！へッへッへッ…少しはやるじゃないか！",
        "大佐ぁ！テメー...俺に勝てると思うなよ！",
    ],
    "all_complete": [
        "大佐ぁ！調子に乗るな！",
        "大佐ぁ！これで終わりと思うなよ！",
        "大佐ぁ！任務ごときでイキがるな！",
        "大佐ぁ！フンッ…まだ勝った気になるな！",
    ],
}

# ------------------------------------------------------------------
def mission_list(request: HttpRequest) -> HttpResponse:
    """
    通常任務一覧を表示するビュー。
    
    GET:
        - 通常任務リストを取得
        - コマンドー風モードならベネットのセリフをランダム表示
    POST:
        - 新規任務を作成
        - 作成後、通常任務リストにリダイレクト
    """

    # アーカイブされていない任務のみ取得、作成順の逆順
    missions = Mission.objects.filter(is_archived=False).order_by("-created_at")

    # ------------------------
    # POSTの場合：新規任務作成
    if request.method == "POST":
        title = request.POST.get("title")  # フォームからタイトル取得
        if title:
            Mission.objects.create(title=title)  # DBに保存
        return redirect("mission_list")  # 作成後はリダイレクト

    # ------------------------
    # ベネットのセリフ選択（ネタモードのみ）
    if COMMANDO_MODE:
        if missions.exists() and all(m.is_completed for m in missions):
            # すべて完了している場合
            quote = random.choice(BENNETT_QUOTES["all_complete"])
        elif any(m.is_completed for m in missions):
            # 一部完了している場合
            quote = random.choice(BENNETT_QUOTES["complete"])
        else:
            # 未完了のみの場合
            quote = random.choice(BENNETT_QUOTES["incomplete"])
    else:
        quote = None  # 通常モードではセリフ表示なし

    # ------------------------
    # タイトル・ラベル切替（モードに応じて文言を変える）
    if COMMANDO_MODE:
        title_text = "大佐、任務完了！"
        list_heading = "通常任務リスト"
        input_placeholder = "任務を入力"
    else:
        title_text = "アーカイブ機能付きTODOリスト"
        list_heading = "タスク一覧"
        input_placeholder = "タスクを入力"

    # contextにまとめてテンプレートへ渡す
    context: Dict[str, Any] = {
        "missions": missions,
        "quote": quote,
        "title": title_text,
        "list_heading": list_heading,
        "input_placeholder": input_placeholder,
        "commando_mode": COMMANDO_MODE,
    }
    return render(request, "complete_colonel/mission_list.html", context)

# ------------------------------------------------------------------
def complete_mission(request: HttpRequest, mission_id: int) -> HttpResponse:
    """
    指定任務を完了状態にする
    - is_completed を True に設定
    - 完了コメントを保存
    - 完了後、通常任務リストにリダイレクト
    """
    mission = get_object_or_404(Mission, id=mission_id)
    mission.is_completed = True
    mission.completed_comment = f"{mission.title} 任務完了。異常なし。"
    mission.save()
    return redirect("mission_list")

# ------------------------------------------------------------------
def archive_mission(request: HttpRequest, mission_id: int) -> HttpResponse:
    """
    指定任務をアーカイブに移動
    - is_archived を True に設定
    - 移動後、通常任務リストにリダイレクト
    """
    mission = get_object_or_404(Mission, id=mission_id)
    mission.is_archived = True
    mission.save()
    return redirect("mission_list")

# ------------------------------------------------------------------
def archived_missions(request: HttpRequest) -> HttpResponse:
    """
    アーカイブ済み任務一覧を表示
    - GET: アーカイブされた任務を取得して表示
    """
    missions = Mission.objects.filter(is_archived=True).order_by("-created_at")

    # タイトルや見出しもモードごとに切替
    if COMMANDO_MODE:
        title_text = "過去の任務"
        list_heading = "完了済任務"
    else:
        title_text = "アーカイブ済みタスク"
        list_heading = "アーカイブ一覧"

    context = {
        "missions": missions,
        "title": title_text,
        "list_heading": list_heading,
        "commando_mode": COMMANDO_MODE,
    }
    return render(request, "complete_colonel/archived_missions.html", context)

# ------------------------------------------------------------------
def reassign_mission(request: HttpRequest, mission_id: int) -> HttpResponse:
    """
    アーカイブ済み任務を通常任務リストに戻す
    - is_archived を False に設定
    - 戻した後、アーカイブリストにリダイレクト
    """
    mission = get_object_or_404(Mission, id=mission_id)
    mission.is_archived = False
    mission.save()
    return redirect("archived_missions")

# ------------------------------------------------------------------
def delete_permanently(request: HttpRequest, mission_id: int) -> HttpResponse:
    """
    アーカイブ済み任務をデータベースから完全削除
    - 任務を削除後、アーカイブリストにリダイレクト
    """
    mission = get_object_or_404(Mission, id=mission_id)
    mission.delete()
    return redirect("archived_missions")
