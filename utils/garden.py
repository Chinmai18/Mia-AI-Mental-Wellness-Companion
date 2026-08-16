def get_garden_stage(day):

    if day == 0:
        return "🪨 Empty garden"
    elif day < 5:
        return "🌱 Seed growing"
    elif day < 10:
        return "🌿 Small plant"
    elif day < 15:
        return "🌳 Growing strong"
    else:
        return "🌸 Fully bloomed!"