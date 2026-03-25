from config import Theme
from admin import Supervisor
from staff_gudang import StaffGudang
from staff_toko import StaffToko

class Auth:
    def __init__(self, database):
        self.db = database

    def login(self):
        print(f"\n{Theme.OKCYAN}{'='*40}{Theme.ENDC}")
        print(f"{Theme.BOLD}          SISTEM LOGIN LOGIX          {Theme.ENDC}")
        print(f"{Theme.OKCYAN}{'='*40}{Theme.ENDC}")
        
        u_input = input(f"{Theme.ICON_USER} Username : ").lower().strip()
        p_input = input(f"{Theme.LOCK} Password : ").strip()
        
        users = self.db.data.get("users", {})

        if u_input in users:
            user_data = users[u_input]

            # ✅ Tetap pakai logika lama + amanin tipe data
            if str(user_data.get("password")) == p_input:
                role = str(user_data.get("role", "")).lower().strip()
                nama = user_data.get("nama", u_input)

                print(f"\n{Theme.OKGREEN}✅ Login Berhasil! Halo, {nama}.{Theme.ENDC}")

                # ✅ Mapping role lebih aman & scalable
                role_map = {
                    "supervisor": Supervisor,
                    "staff_gudang": StaffGudang,
                    "staff_toko": StaffToko
                }

                if role in role_map:
                    return role_map[role](u_input, p_input, nama)
                else:
                    # ✅ FIX: handle role tidak dikenal
                    print(f"{Theme.WARNING}⚠️ Role '{role}' tidak dikenali sistem!{Theme.ENDC}")
                    return None

        print(f"\n{Theme.FAIL}❌ Username atau Password salah!{Theme.ENDC}")
        return None

    def logout(self, nama):
        print(f"\n{Theme.OKBLUE}User {nama} keluar.{Theme.ENDC}")