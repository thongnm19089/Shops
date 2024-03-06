from rest_framework_extensions.cache.decorators import CacheResponse
from django.conf import settings


class CustomCacheResponse(CacheResponse):
    def process_cache_response(self, view_instance, view_method, request, args, kwargs):
        if settings.CACHE_ENABLE:
            return super(CustomCacheResponse, self).process_cache_response(
                view_instance, view_method, request, args, kwargs
            )
        response = view_method(view_instance, request, *args, **kwargs)
        response = view_instance.finalize_response(request, response, *args, **kwargs)
        response.render()
        return response


custom_cache_response = CustomCacheResponse
