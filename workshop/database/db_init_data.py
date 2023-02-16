import json

from core.settings import BASE_DIR
from workshop.models import JewelryType, Material, Gem, Jewelry, Client, Order


def fill_model_table(model, data):
    model.objects.bulk_create([model(**obj_data) for obj_data in data])


def db_init():
    with open(BASE_DIR / "workshop/database/db_init_data.json", encoding="utf-8") as file:
        db_initial_data = json.load(file)

    fill_model_table(JewelryType, db_initial_data["jewelry_types"])
    fill_model_table(Material, db_initial_data["materials"])
    fill_model_table(Gem, db_initial_data["gems"])
    fill_model_table(Jewelry, db_initial_data["jewelries"])
    fill_model_table(Jewelry.materials.through, db_initial_data["jewelries_materials"])
    fill_model_table(Jewelry.gems.through, db_initial_data["jewelries_gems"])
    fill_model_table(Client, db_initial_data["clients"])
    fill_model_table(Order, db_initial_data["orders"])
