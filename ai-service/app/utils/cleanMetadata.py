def clean_metadata(metadata: dict):
    cleaned = {}

    for key, value in metadata.items():

        # 过滤 None
        if value is None:
            continue

        # 基础类型
        elif isinstance(value, (str, int, float, bool)):
            cleaned[key] = value

        # 复杂类型转字符串
        else:
            cleaned[key] = str(value)

    return cleaned