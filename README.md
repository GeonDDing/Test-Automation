API & WEB Test Automation code

# Execute Pytest
pytest ./Backend/Tests --capture=tee-sys --tb=no --alluredir=allure-results --clean-alluredir
pytest ./Tests --capture=tee-sys --tb=no --alluredir=allure-results

# Generate Allure Report
allure serve --host 127.0.0.1 --port 8081 ./allure-results

# Dcoekr Build
docker build --no-cache -t <Tag_Name> -f <Docker_File_Name> .
# Docker Run
docker run --rm  <IMAGE_ID>