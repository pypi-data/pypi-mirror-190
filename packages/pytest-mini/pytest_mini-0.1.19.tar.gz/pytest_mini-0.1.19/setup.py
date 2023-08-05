# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_mini']

package_data = \
{'': ['*'],
 'pytest_mini': ['tools/allure-2.14.0/bin/*',
                 'tools/allure-2.14.0/config/*',
                 'tools/allure-2.14.0/lib/*',
                 'tools/allure-2.14.0/lib/config/*',
                 'tools/allure-2.14.0/plugins/*',
                 'tools/allure-2.14.0/plugins/behaviors-plugin/*',
                 'tools/allure-2.14.0/plugins/behaviors-plugin/static/*',
                 'tools/allure-2.14.0/plugins/custom-logo-plugin/*',
                 'tools/allure-2.14.0/plugins/custom-logo-plugin/static/*',
                 'tools/allure-2.14.0/plugins/jira-plugin/*',
                 'tools/allure-2.14.0/plugins/jira-plugin/lib/*',
                 'tools/allure-2.14.0/plugins/junit-xml-plugin/*',
                 'tools/allure-2.14.0/plugins/packages-plugin/*',
                 'tools/allure-2.14.0/plugins/packages-plugin/static/*',
                 'tools/allure-2.14.0/plugins/screen-diff-plugin/*',
                 'tools/allure-2.14.0/plugins/screen-diff-plugin/static/*',
                 'tools/allure-2.14.0/plugins/trx-plugin/*',
                 'tools/allure-2.14.0/plugins/xctest-plugin/*',
                 'tools/allure-2.14.0/plugins/xctest-plugin/lib/*',
                 'tools/allure-2.14.0/plugins/xray-plugin/*',
                 'tools/allure-2.14.0/plugins/xray-plugin/lib/*',
                 'tools/allure-2.14.0/plugins/xunit-xml-plugin/*']}

install_requires = \
['Faker>=15.3.3,<16.0.0',
 'PyYAML>=6.0,<7.0',
 'allure-pytest>=2.11.1,<3.0.0',
 'allure-python-commons>=2.11.1,<3.0.0',
 'concurrent-log-handler>=0.9.20,<0.10.0',
 'minium>=1.3.1,<2.0.0',
 'pytest-assume>=2.4.3,<3.0.0',
 'pytest-dependency>=0.5.1,<0.6.0',
 'pytest-lazy-fixture>=0.6.3,<0.7.0',
 'pytest-ordering>=0.6,<0.7',
 'pytest>=7.2.0,<8.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'pytest11': ['mini = pytest_mini.mini', 'mp = pytest_mini.plugin:Plugin']}

setup_kwargs = {
    'name': 'pytest-mini',
    'version': '0.1.19',
    'description': 'A plugin to test mp',
    'long_description': '# pytest-mini\n\n> 微信小程序自动化测试pytest插件/工具\n> \n> 基于[MiniTest](https://minitest.weixin.qq.com/)进行pytest改造\n\n## 使用方法\n\n### 准备测试小程序\n\n根据[miniprogram-demo](https://github.com/wechat-miniprogram/miniprogram-demo)项目介绍运行一次项目\n\n成功运行后关闭\n\n### 安装&更新\n\n```shell\npip install pytest-mini --upgrade\n```\n\n### 引入插件\n\n新建`conftest.py`文件\n\n```python\nfrom pytest_mini import plugins\n\npytest_plugins = plugins(\n    "待测试的小程序项目路径",\n    "微信开发者工具路径"\n)\n```\n例如`demo/cases/conftest.py`\n```python\nfrom pytest_mini import plugins\n\npytest_plugins = plugins(\n    "/Users/zhongxin/github/miniprogram-demo",  # 待测试的小程序项目路径\n    "/Applications/wechatwebdevtools.app/Contents/MacOS/cli"  # 微信开发者工具路径\n)\n```\n\n### 编写页面对象\n\n在`demo/pages/components_page.py`编写元素定位\n\n```python\nfrom pytest_mini import Mini, Locator\n\n\nclass ComponentsPage(Mini):\n    view_container = Locator(\'view\', inner_text=\'视图容器\', desc=\'组件页-视图容器\')\n\n```\n在`conftest.py`中添加\n```python\nimport pytest\nfrom pages.components_page import ComponentsPage\n\n@pytest.fixture(scope="session")\ndef components_page(mini):\n    yield ComponentsPage(driver=mini.driver)\n\n```\n\n### 编写测试代码\n`demo/cases/test_home.py`\n```python\nimport allure\n\nfrom pytest_mini import compose\n\n\n@compose(feature="小程序官方组件展示", story="组件", title=\'容器视图操作\')\ndef test_view_container(components_page):\n    with allure.step("点击容器视图"):\n        components_page.click(components_page.view_container)\n        assert False, "故意失败,查看报告截图"\n```\n\n### 编写执行&报告展示脚本\n`demo/cases/allure_debug.py`\n```python\nimport os\nimport pytest\nfrom pytest_mini.constant import Constant\n\ntest_cases = ["test_home.py"]  # 执行的脚本\n\nmain_list = [\n    \'-s\', \'-v\',\n    *test_cases,\n    \'--durations=0\', \'--clean-alluredir\',\n    \'--alluredir\', f\'{Constant().REPORT_PATH}/allure_results\'\n]\npytest.main(main_list)\nif not os.getenv("BUILD_URL"):\n    os.system(f"{Constant.ALLURE_TOOL} serve {Constant().REPORT_PATH}/allure_results")  # 本地执行\n```\n\n### 执行测试\n运行`allure_debug.py`文件\n\n### 查看报告\n![报告截图](imgs/报告截图.png)\n\n![实际项目报告截图](imgs/实际项目.png)',
    'author': '听白',
    'author_email': '490336534@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
