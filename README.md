![](https://github.com/Treshch1/sporty_inter_wap/blob/main/data/images/wap.gif)


# Selenium automation with Python

[Selenium](https://www.selenium.dev/) automation with `Python` is a test automation framework that uses Selenium to automate web browser interactions. It is a Python library that provides a high-level API to control web browsers.

## Installation guide

1. Setup your virtual environment `virtualenv -p python3 venv`.
2. Activate your environment `source venv/bin/activate`. You should see `(venv)` in your terminal.
3. Install python dependencies `pip install -r requirements.txt`.
4. Install Allure in your system. You can follow the [Allure installation guide](https://docs.qameta.io/allure/#_installing_a_commandline).

## Project structure

- The `conftest.py` file contains the `pytest` fixtures to use in tests.
- Reusable components are stored in `components` folder
- Files which are used in the tests stored in `data` folder
- Page objects stored in `page_objects` folder
- Tests stored in `tests` folder
– Settings are spread between:
  - pytest.ini
  - config.py
- Browser settings are in `browser.py` file
- Screenshots that are taken when tests are failed are placed in `report_screenshot` folder  


## Run guide

### Setup Environment Variables

1. Create `.env` file:

```bash
cp .env.example .env
```

2. Update variables in .env file

#### Alternative with export command

- `export BASE_URL=https://google.com/` - This is the URL prefix which is used after main navigations using the `visit()` method.
- `export BROWSER_TYPE=chromium` - This is the setting to indicate which browser should be used during the test session. Possible options `chromuim`, `firefox`.

### Set up folder for failed tests screenshots
* Create `report_screenshots` folder in the root

### Run tests

- Run tests using command `pytest`
- Run tests in headless mode using command `pytest --headless`
- Or run test using docker via the next command `make run-tests`
- Generate allure report `allure serve ./report/ --port 3060`


## Run in Github Actions guide
### Setup Github Secrets
1. Navigate to Github repository `Settings`
2. Open the `Secret and variables` dropdown in the settings sidebar
3. Click the `Actions` item in the expanded dropdown
4. Click the `New repository secret` button
5. Add a secret with the name `ENVS` and set the value of this secret using the `.env.example` file format

### Run the Github Action workflow
- Push changes to `main` or `develop` branches
- Or run the action manually via the Github repository `Actions` tab
- Allure report zip file can be found in the finished action's artifacts
