from app.database import supabase


def clean_data(data: dict):

    cleaned = {}

    for key, value in data.items():

        if value is None:
            continue

        if value == "":
            continue

        if value == []:
            continue

        cleaned[key] = value

    return cleaned


def insert(table_name: str, data: dict):

    data = clean_data(data)

    response = (
        supabase
        .table(table_name)
        .insert(data)
        .execute()
    )

    if not response.data:
        raise Exception(f"Insert failed for {table_name}")

    return response.data[0]