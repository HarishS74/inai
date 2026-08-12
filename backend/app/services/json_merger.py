def merge_json(results):
    merged = {}

    for result in results:

        if not isinstance(result, dict):
            continue

        for key, value in result.items():

            if value is None:
                continue

            # New key
            if key not in merged:
                merged[key] = value
                continue

            # Merge dictionaries
            if isinstance(value, dict):

                if not isinstance(merged[key], dict):
                    merged[key] = {}

                for k, v in value.items():

                    if v is None:
                        continue

                    if k not in merged[key]:
                        merged[key][k] = v

                    elif merged[key][k] in [None, "", []]:
                        merged[key][k] = v

            # Merge lists
            elif isinstance(value, list):

                if not isinstance(merged[key], list):
                    merged[key] = []

                for item in value:
                    if item not in merged[key]:
                        merged[key].append(item)

            # Merge strings
            elif isinstance(value, str):

                if merged[key] in [None, ""]:
                    merged[key] = value

    return merged