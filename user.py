from abc import ABC, abstractmethod
from config import Theme

class User(ABC):
    """
    Abstract Base Class untuk User.
    Menyediakan kerangka dasar untuk semua jenis peran pengguna di LogiX.
    """
    def __init__(self, username, password, nama):
        self._username = username
        self._password = password
        self._nama = nama
        # Role akan ditentukan secara otomatis berdasarkan nama Class di subclass nanti
        self._role = self.__class__.__name__.lower()

    @property
    def username(self):
        return self._username

    @property
    def nama(self):
        return self._nama

    @property
    def role(self):
        return self._role

    def check_password(self, input_password):
        """Validasi password saat login."""
        return self._password == input_password

    @abstractmethod
    def akses_menu(self):
        """
        Method abstrak yang WAJIB diimplementasikan oleh setiap subclass.
        Menentukan hak akses menu untuk masing-masing peran.
        """
        pass

    def tampilkan_profil(self):
        """Menampilkan identitas user dengan format berwarna."""
        print(f"{Theme.OKCYAN}{Theme.ICON_USER} LOGIN SEBAGAI: {Theme.BOLD}{self._nama} ({self._role.upper()}){Theme.ENDC}")