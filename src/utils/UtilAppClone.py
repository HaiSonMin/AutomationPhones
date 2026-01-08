def get_name_app_clone(user_name: str, type_social: str) -> str:
    if type_social == ESocials.Instagram.value:
        return f"i_{user_name}"
    if type_social == ESocials.Threads.value:
        return f"t_{user_name}"
    if type_social == ESocials.Facebook.value:
        return f"f_{user_name}"
    if type_social == ESocials.Medium.value:
        return f"m_{user_name}"
    if type_social == ESocials.Pinterest.value:
        return f"p_{user_name}"
    if type_social == ESocials.Redis.value:
        return f"r_{user_name}"
    if type_social == ESocials.Tumblt.value:
        return f"tum_{user_name}"
    if type_social == ESocials.X.value:
        return f"x_{user_name}"
    if type_social == ESocials.Twitter.value:
        return f"tw_{user_name}"
    if type_social == ESocials.Youtube.value:
        return f"y_{user_name}"
    if type_social == ESocials.Tiktok.value:
        return f"tt_{user_name}"
