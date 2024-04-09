python /Backend/api_restore_configuration.py

pytest ./Backend/TestCase --capture=tee-sys --tb=no --alluredir=allure-results --clean-alluredir

pytest ./WebUI/TestCase/test_TC_UI_000_Pre_Settings.py --capture=tee-sys --tb=no --alluredir=allure-results

pytest ./WebUI/TestCase/Input --capture=tee-sys --tb=no --alluredir=allure-results

pytest ./WebUI/TestCase/BackupSource --capture=tee-sys --tb=no --alluredir=allure-results

pytest ./WebUI/TestCase/Output --capture=tee-sys --tb=no --alluredir=allure-results

allure serve --host 127.0.0.1 --port 8081 ./allure-results
