from usecase.rpa_auto_login_usecase import RpaAutoLoginUsecase

class AutoLoginToTitechController:
    def handle(self) -> None:
        rpa_auto_login_usecase = RpaAutoLoginUsecase()
        rpa_auto_login_usecase.handle()
