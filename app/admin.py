from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class ModelForAdmin(ModelView):
    pass
    # def is_accessible(self):
    #     return current_user.role_id == 1 and current_user.is_authenticated


class WarehouseModel(ModelView):
    pass
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.role_id == 3 or current_user.role_id == 2#4


class SaleModel(ModelView):
    # pass
    def create_model(self, form):
        self.model.decrypt()
        # self.model.set_date_sale(form.date_sale.data)
        # self.model.id_product = form.id_product.data




