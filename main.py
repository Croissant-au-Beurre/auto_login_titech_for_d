from controller.auto_login_to_titech_controller import AutoLoginToTitechController

class Job:
    @classmethod
    def run(cls):
        AutoLoginToTitechController().handle()

if __name__ == '__main__':
    Job.run()