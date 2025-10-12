from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from datetime import datetime, timedelta, date
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.chip import MDChip

from db import list_items, add_item, delete_item, update_item
try:
    from plyer import notification
except Exception:
    notification = None

# utilidades
def parse_iso(dstr):
    return datetime.fromisoformat(dstr).date()

class CocinaApp(MDApp):
    selected_date = None
    selected_category_form = "Otros"
    edit_id = None
    active_filter = "Todos"
    categories = ["Todos","Lácteos","Carnes","Verduras","Frutas","Bebidas","Despensa","Congelados","Panadería","Huevos","Salsas","Snacks","Otros"]

    def build(self):
        self.title = "Caducidad cocina"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file("ui.kv")

    def on_start(self):
        Clock.schedule_once(lambda *_: self._post_build(), 0)

    def _post_build(self):
        self.build_filter_chips()
        self.refresh_list()
        if platform == "android":
            self.start_android_service()

    # ---- UI helpers ----
    def open_search(self):
        MDSnackbar(text="Tip: usa el filtro de categorías o edita un alimento con el lápiz.").open()

    def open_date_picker(self):
        picker = MDDatePicker(mode="picker")
        picker.bind(on_save=self.on_date_picked)
        picker.open()

    def on_date_picked(self, instance, value, date_range):
        self.selected_date = value

    def format_date_display(self, iso_date):
        # Tolerante a '', None o formatos inválidos
        try:
            if not iso_date:
                return ""
            return datetime.fromisoformat(iso_date).strftime("%d/%m/%Y")
        except Exception:
            return ""

    def card_color(self, iso_date):
        # Tolerante a '', None o formatos inválidos
        try:
            if not iso_date:
                return (0.95, 1, 0.95, 1)  # ok por defecto
            d = parse_iso(iso_date)
        except Exception:
            return (0.95, 1, 0.95, 1)
        today = date.today()
        if d < today:
            return (1, 0.9, 0.9, 1)   # caducado
        elif d <= today + timedelta(days=2):
            return (1, 1, 0.9, 1)     # próximo
        return (0.95, 1, 0.95, 1)     # ok

    # ---- Categorías: chips (filtro) sin 'check', compatibles 1.2.0 ----
    def style_chip(self, chip, selected):
        if selected:
            chip.active = True
            chip.selected_color = (0.15, 0.6, 0.2, 1)
            chip.text_color = (1, 1, 1, 1)
            chip.md_bg_color = chip.selected_color
        else:
            chip.active = False
            chip.text_color = (0, 0, 0, 1)
            chip.md_bg_color = (0.92, 0.92, 0.92, 1)

    def build_filter_chips(self):
        box = self.root.ids.cats_box
        box.clear_widgets()
        self._chips = {}
        for cat in self.categories:
            chip = MDChip(text=cat)
            self.style_chip(chip, cat == self.active_filter)
            chip.bind(on_release=lambda chip_obj: self.set_filter(chip_obj.text))
            box.add_widget(chip)
            self._chips[cat] = chip

    def set_filter(self, category):
        self.active_filter = category
        for cat, chip in self._chips.items():
            self.style_chip(chip, cat == category)
        self.refresh_list()

    def open_category_menu(self, anchor_widget):
        menu_items = [{"text": c, "on_release": (lambda x=c: self._select_category(x))}
                      for c in self.categories if c != "Todos"]
        self._menu = MDDropdownMenu(caller=anchor_widget, items=menu_items, width_mult=3)
        self._menu.open()

    def _select_category(self, value):
        self.selected_category_form = value
        try:
            self._menu.dismiss()
        except Exception:
            pass
        self.root.ids.categoria_btn.text = value

    def refresh_list(self):
        data = []
        rows = list_items(self.active_filter)
        for _id, nombre, cantidad, caduca, categoria in rows:
            data.append({
                "id_item": _id,
                "nombre": nombre,
                "cantidad": cantidad or "",
                "caduca": caduca,
                "categoria": categoria or "Otros",
            })
        self.root.ids.rv.data = data

    # ---- CRUD ----
    def save_item(self):
        try:
            nombre = self.root.ids.nombre_field.text.strip()
            cantidad = self.root.ids.cantidad_field.text.strip()
            d = self.selected_date
            categoria = self.selected_category_form or "Otros"

            if not (nombre and d):
                MDSnackbar(text="Rellena nombre y fecha de caducidad.").open()
                return

            iso = d.isoformat()

            if self.edit_id:
                update_item(self.edit_id, nombre, cantidad, iso, categoria)
                self.edit_id = None
            else:
                add_item(nombre, cantidad, iso, categoria)

            # reset form
            self.root.ids.nombre_field.text = ""
            self.root.ids.cantidad_field.text = ""
            self.selected_date = None
            self.selected_category_form = "Otros"
            self.root.ids.categoria_btn.text = "Categoría"

            self.refresh_list()

            # notificación inmediata si corresponde (protegida)
            self.notify_if_due(nombre, d)

            MDSnackbar(text="Guardado ✓").open()

        except Exception as e:
            try:
                MDSnackbar(text=f"Error al guardar: {e}").open()
            except Exception:
                pass

    def open_edit(self, item_id, nombre, cantidad, caduca_iso, categoria):
        self.edit_id = item_id
        self.root.ids.nombre_field.text = nombre
        self.root.ids.cantidad_field.text = cantidad
        self.selected_date = parse_iso(caduca_iso)
        self.selected_category_form = categoria or "Otros"
        self.root.ids.categoria_btn.text = self.selected_category_form

    def delete_item(self, item_id):
        delete_item(item_id)
        self.refresh_list()
        MDSnackbar(text="Eliminado").open()

    # ---- Notificaciones ----
    def notify_if_due(self, nombre, caduca_date):
        try:
            if notification is None:
                return
            aviso = caduca_date - timedelta(days=2)
            now = datetime.now()
            if datetime.combine(aviso, datetime.min.time()) <= now:
                try:
                    notification.notify(
                        title="Caducidad próxima",
                        message=f"{nombre} caduca en 2 días ({caduca_date.strftime('%d/%m')})",
                        timeout=5
                    )
                except Exception:
                    pass
        except Exception:
            pass

    # ---- Servicio Android (ignorado en Raspberry/PC) ----
    def start_android_service(self):
        try:
            from jnius import autoclass
            PythonService = autoclass('org.kivy.android.PythonService')
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            service = PythonService.mService
            if service is None:
                PythonService.start(
                    mActivity,
                    "Caducidad cocina",
                    "Revisando alimentos a diario",
                    "service_check",
                    ""
                )
        except Exception:
            pass

if __name__ == "__main__":
    CocinaApp().run()
