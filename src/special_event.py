import settings, utility

from abstract import AbstractManager

class SpecialEventmanager(AbstractManager):
    """
    Special event "On the Nile"
    """
    def go_on_the_nile(self, stage):
        print(f"Let's fight the stage {stage} in On the Nile!")
        try:
            self.driver.request('POST', settings.login_data['ajax_url'] + f"?mod=location&submod=attack&location=nile_bank&stage={stage}&premium=0&a={utility.get_milliseconds()}&sh={self.secureHash}")

            print(f"We finished doing an action in the On the Nile event!")
            return True
        except Exception as e:
            print(f"There was a a problem in go_on_the_nile(): ", e)
            return False
