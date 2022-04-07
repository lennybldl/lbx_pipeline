### Before releasing
- Perform the tests to make sure the app still works
- Update package version
  - in src/<package_name>/__init__.py
  - in package.py
- Check dependencies/requirements
  - in package.py
  - in setup.cfg
- Build the rez package : rez build --install