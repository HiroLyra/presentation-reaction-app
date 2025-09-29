from typing import Any, Dict
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Presentation

@csrf_exempt
@require_http_methods(["POST"])
def create_presentation(request: HttpRequest) -> JsonResponse:
    """
    新しい発表セッションを作成する。

    Args:
        request (HttpRequest): HTTPリクエストオブジェクト。
                               JSONボディにはtitle（必須）とdescription（任意）を含む。

    Returns:
        JsonResponse: 作成結果。成功時はsuccess=Trueと作成されたUUIDを返す。

    Example:
        POST /presentations/create/
        {
            "title": "発表タイトル",
            "description": "発表の説明"
        }
    """
    try:
        data: Dict[str, Any] = json.loads(request.body)

        title: str | None = data.get('title')
        description: str = data.get('description', '')

        if not title:
            return JsonResponse({'success': False, 'error': 'タイトルを入力してください。'})

        presentation: Presentation = Presentation.objects.create(
            title=title,
            description=description
        )

        return JsonResponse({
            'success': True,
            'id': str(presentation.id), 
            'title': presentation.title,
            'description': presentation.description
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSONの形式が不正です。'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def get_presentation(request: HttpRequest, presentation_id: str) -> JsonResponse:
    """
    指定された発表セッションの詳細情報と現在の反応数を取得する。

    Args:
        request (HttpRequest): HTTPリクエストオブジェクト
        presentation_id (str): 発表のUUID

    Returns:
        JsonResponse: 発表情報と反応数。エラー時はsuccess=False。

    Example:
        GET /presentations/123e4567-e89b-12d3-a456-426614174000/
    """
    try:
        presentation: Presentation = Presentation.objects.get(id=presentation_id)
        return JsonResponse({
            'success': True,
            'id': str(presentation.id), 
            'title': presentation.title,
            'description': presentation.description,
            'heart': presentation.heart,
            'thumbs_up': presentation.thumbs_up,
            'laugh': presentation.laugh,
            'surprise': presentation.surprise
        })
    except Presentation.DoesNotExist:
        return JsonResponse({'success': False, 'error':'発表が見つかりません。'})


@csrf_exempt
@require_http_methods(["POST"])
def add_reaction(request: HttpRequest, presentation_id: str) -> JsonResponse:
    """
    指定された発表セッションに反応を追加する。

    Args:
        request (HttpRequest): HTTPリクエストオブジェクト。
                               JSONボディにはreaction_typeを含む。
        presentation_id (str): 発表のUUID

    Returns:
        JsonResponse: 反応追加結果。成功時はsuccess=True。

    Example:
        POST /presentations/123e4567-e89b-12d3-a456-426614174000/reactions/
        {
            "reaction_type": "thumbs_up"
        }
    """
    try:
        data: Dict[str, Any] = json.loads(request.body)

        reaction_type: str = data.get('reaction_type', '')
        if not reaction_type:
            return JsonResponse({'success': False, 'error':'reaction_typeが必要です。'})
        presentation: Presentation = Presentation.objects.get(id=presentation_id)
        presentation.add_reaction(reaction_type)
        return JsonResponse({
            'success': True,
            'id': str(presentation.id),
        })
    except Presentation.DoesNotExist:
        return JsonResponse({'success': False, 'error':'発表が見つかりません。'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSONの形式が不正です。'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}) 