from django.http import HttpRequest
from django.core.cache import cache
from django.conf import settings
from django.utils.translation import gettext as _
from .results import ApiResult
from typing import List, Set, Union
import json
import pickle
from knifes.digests import md5
from knifes import aes
default_func_cache_timeout = 3600


# 装饰器 修饰的方法 第1个参数是 key
def func_cache(cache_key_prefix: Union[tuple, str]):
    if not isinstance(cache_key_prefix, tuple):
        cache_key_prefix = (cache_key_prefix, default_func_cache_timeout)

    def outer_wrapper(func):
        def wrapper(*args, **kwargs):
            if not args:  # 参数校验
                raise Exception('方法缺少缓存key')
            key = cache_key_prefix[0] + md5(str(args[0]))  # 避免args[0]过长
            result = cache.get(key)  # 尝试读取缓存
            if result:
                return pickle.loads(result)  # 使用pickle支持枚举、自定义类等
            result = func(*args, **kwargs)
            cache.set(key, pickle.dumps(result), timeout=cache_key_prefix[1])  # 写缓存
            return result
        return wrapper
    return outer_wrapper


def update_func_cache(cache_key_prefix: Union[tuple, str], args_0, result):
    if not isinstance(cache_key_prefix, tuple):
        cache_key_prefix = (cache_key_prefix, default_func_cache_timeout)
    key = cache_key_prefix[0] + md5(str(args_0))
    cache.set(key, pickle.dumps(result), timeout=cache_key_prefix[1])


def login_required(view_func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if settings.TOKEN_KEY not in request.headers or not request.headers[settings.TOKEN_KEY]:
            return ApiResult.tokenInvalid()
        request.token = request.headers[settings.TOKEN_KEY]
        data = cache.get(settings.TOKEN_KEY + request.token)
        if not data:
            return ApiResult.tokenInvalid()
        # 只能反序列化简单类型数据
        request.user = pickle.loads(data)
        return view_func(request, *args, **kwargs)
    return wrapper


def params_required(param_keys: List, is_get=False):
    def outer_wrapper(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if param_keys and is_get:
                for param_key in param_keys:
                    if param_key not in request.GET or not request.GET[param_key]:
                        return ApiResult.missingParam()
            elif param_keys:
                for param_key in param_keys:
                    if param_key not in request.POST or not request.POST[param_key]:
                        return ApiResult.missingParam()
            return view_func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper


def decrypt_and_check_params(param_keys: Set = None, header_param_keys: Set = None):
    if param_keys is None:
        param_keys = {'timestamp'}
    else:
        param_keys.add('timestamp')

    def outer_wrapper(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not request.body:
                return ApiResult.missingParam()
            request.params = json.loads(request.body)

            # body params   TODO 判断timestamp是否过期
            if next((True for param_key in param_keys if param_key not in request.params), False):
                return ApiResult.missingParam()

            # body params comparison
            if not request.headers.get('xDev') and request.params != json.loads(aes.decrypt(request.headers.get('xBody') or request.params.get('vs'), settings.AES_BODY_KEY)):
                return ApiResult.missingParam(_('参数非法'))

            # header params
            if not (request.headers.get('xHeader') or request.headers.get('vi')):
                ApiResult.missingParam()

            request.header_params = json.loads(aes.decrypt(request.headers.get('xHeader') or request.headers.get('vi'), settings.AES_HEADER_KEY))
            if header_param_keys and next((True for param_key in header_param_keys if param_key not in request.header_params), False):
                return ApiResult.missingParam()

            return view_func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper


def decrypt_and_check_body_params(param_keys: Set = None):
    if param_keys is None:
        param_keys = {'timestamp'}
    else:
        param_keys.add('timestamp')

    def outer_wrapper(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not request.body:
                return ApiResult.missingParam()
            request.params = json.loads(request.body)
            if next((True for param_key in param_keys if param_key not in request.params), False):
                return ApiResult.missingParam()

            if not request.headers.get('xDev') and request.params != json.loads(aes.decrypt(request.headers.get('xBody') or request.params.get('vs'), settings.AES_BODY_KEY)):
                return ApiResult.missingParam(_('参数非法'))
            return view_func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper


def decrypt_and_check_header_params(header_param_keys: Set = None):
    def outer_wrapper(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not (request.headers.get('xHeader') or request.headers.get('vi')):
                ApiResult.missingParam()

            request.header_params = json.loads(aes.decrypt(request.headers.get('xHeader') or request.headers.get('vi'), settings.AES_HEADER_KEY))
            if header_param_keys and next((True for param_key in header_param_keys if param_key not in request.header_params), False):
                return ApiResult.missingParam()
            return view_func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper


# json请求 参数校验
def decode_and_check_body_params(param_keys: Set = None):
    def outer_wrapper(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not request.body:
                return ApiResult.missingParam()
            request.params = json.loads(request.body)
            # 检查参数
            for param_key in param_keys:
                if param_key not in request.params:
                    return ApiResult.missingParam()
            return view_func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper
