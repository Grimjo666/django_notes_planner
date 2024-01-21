from .models import TaskColorSettings


class TemplateColorsMixin:
    @staticmethod
    def get_task_priority_colors_dict(request) -> dict | None:
        task_colors = TaskColorSettings.objects.all().filter(user=request.user)
        if task_colors.exists():
            high_priority = task_colors[0].high_priority_color
            medium_priority = task_colors[0].medium_priority_color
            low_priority = task_colors[0].low_priority_color
            context = {
                'high_priority': high_priority,
                'medium_priority': medium_priority,
                'low_priority': low_priority
            }
            return context
        return None
