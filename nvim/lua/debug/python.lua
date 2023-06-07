local mason_path = require('mason-core.path')
require('dap-python').setup(mason_path.package_prefix('debugpy') .. '/venv/bin/python')
