from core.settings import WEBSITE_TITLE


class ViewDataMixin:
    def get_mixin_context(self, **kwargs):
        context = kwargs

        context.update({
            "title": WEBSITE_TITLE,
        })

        return context
