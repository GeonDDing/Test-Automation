python /Backend/api_restore_configuration.py

pytest ./Backend/TestCase --color=yes --capture=tee-sys --tb=no --alluredir=allure-results --clean-alluredir

pytest ./WebUI/TestCase/test_TC_UI_000_Pre_Settings.py --color=yes --capture=tee-sys --tb=no --alluredir=allure-results

pytest ./WebUI/TestCase/Input --color=yes --capture=tee-sys --tb=no --alluredir=allure-results

pytest ./WebUI/TestCase/BackupSource --color=yes --capture=tee-sys --tb=no --alluredir=allure-results

pytest ./WebUI/TestCase/Output --color=yes --capture=tee-sys --tb=no --alluredir=allure-results

allure serve --host 127.0.0.1 --port 8081 ./allure-results
