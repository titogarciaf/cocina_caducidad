
import time
from datetime import date, datetime, timedelta
from db import list_items
try:
    from plyer import notification
except Exception:
    notification = None

CHECK_HOUR = 8  # 08:00 hora local
LAST_RUN_FILE = "/data/data/org.test.cocina_caducidad/files/last_run.txt"

def should_run_now():
    now = datetime.now()
    # corre si es >= 08:00 y aún no corrió hoy
    try:
        with open(LAST_RUN_FILE, "r") as f:
            last_str = f.read().strip()
        last = datetime.fromisoformat(last_str)
        if last.date() == now.date():
            return False
    except Exception:
        pass
    return now.hour >= CHECK_HOUR

def mark_ran():
    try:
        with open(LAST_RUN_FILE, "w") as f:
            f.write(datetime.now().isoformat())
    except Exception:
        pass

def check_and_notify():
    if notification is None:
        return
    today = date.today()
    for row in list_items():
        _id, nombre, cantidad, caduca_iso, categoria = row
        cad = datetime.fromisoformat(caduca_iso).date()
        if cad == today + timedelta(days=2):
            notification.notify(
                title="Caducidad en 2 días",
                message=f"{nombre} ({categoria}) caduca el {cad.strftime('%d/%m/%Y')}",
                timeout=10
            )
        elif cad < today:
            # (opcional) alerta de caducado
            pass

def main():
    # bucle ligero: se duerme y despierta para revisar la hora
    while True:
        if should_run_now():
            check_and_notify()
            mark_ran()
            # duerme ~22h
            time.sleep(22 * 60 * 60)
        else:
            time.sleep(15 * 60)  # reintenta cada 15 min

if __name__ == "__main__":
    main()
