Background
==
When we use cucumber to do our testing, scenarios might be failed. Luckily, cucumber support 'rerun' function to help us rerun failed cases automatically with the following command:
```
cucumber -f rerun --out rerun.txt || cucumber @rerun.txt
```
Talking about writing results to json files, the command could be:
```
cucumber --format json_pretty --strict -o origin-report.json -f pretty -f rerun --out rerun.txt || cucumber @rerun.txt --format json_pretty --strict -o rerun-report.json
```
If we run our cases in Jenkins jobs, the cucumber report plugin can be specified to collect json files to generate the preety html report. However, if you use the command like above, the report will not be perfect.
If there are 10 scenarios, 1 scenario is failed at the first time but passed by rerun. The report will show you 11 scenarios and the scenarios are shown 2 time, one is shown as passed and the other is failed.

How the parser works
==
The parser will collect the passed scenarios from the rerun report, then based on the origin report to get the latest correct report and write the content as one new json report.
With the parser, in the example we mentioned above, after we get the new json report, we can delete other vaild ones, then the cucumber plugin will parser the correct and more meaningful report. We would see 10 scenarios are all passed as we expect.

How to use the parser
==
The simple parser is developed by python3. Some python packages like 'argparse' and 'json' are needed. After you run and rerun your cucumber scenarios, you can use it with the following command:
```
python3 cucumber_rerun_parser.py --rerun-report=rerun-report-name.json --origin-report=origin-report-name.json --new-report=new-report-name.json
```
Logs like below will show us the detailed process:
```
2019-05-27 20:44:46,053 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Read the data from 1558961085-rerun.json
2019-05-27 20:44:46,054 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Get scenarios and results maps from 1558961085-rerun.json
2019-05-27 20:44:46,054 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Have got all scenarios and results:
2019-05-27 20:44:46,054 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO {'login_1;login-as-admin-user;;2': 'passed', 'login_1;login-as-admin-user;;3': 'passed', 'login_3;login-as-qa-user': 'passed', 'login_2;login-as-devel-user': 'passed'}
2019-05-27 20:44:46,054 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Rerun scenarios are all passed.
2019-05-27 20:44:46,054 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Replace the result "passed" as more meaningful scenario content
2019-05-27 20:44:46,054 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Have got all passed scenarios:
2019-05-27 20:44:46,054 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO {'login_1;login-as-admin-user;;2': 'passed', 'login_1;login-as-admin-user;;3': 'passed', 'login_3;login-as-qa-user': 'passed', 'login_2;login-as-devel-user': 'passed'}
2019-05-27 20:44:46,054 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Update the report 1558961085-test.json with rerun results {'login_1;login-as-admin-user;;2': {'id': 'login_1;login-as-admin-user;;2', 'keyword': 'Scenario Outline', 'tags': [{'line': 1, 'name': '@examples'}], 'type': 'scenario', 'name': 'Login as admin user', 'description': '', 'line': 14, 'steps': [{'keyword': 'When ', 'result': {'status': 'passed', 'duration': 12349}, 'line': 8, 'match': {'location': 'features/step_definitions/b.rb:7'}, 'name': 'I visit "errata"'}, {'keyword': 'Then ', 'result': {'status': 'passed', 'duration': 10443}, 'line': 9, 'match': {'location': 'features/step_definitions/b.rb:11'}, 'name': 'I can find content header "Advisories"'}, {'keyword': 'And ', 'result': {'status': 'passed', 'duration': 48286}, 'line': 10, 'match': {'location': 'features/step_definitions/b.rb:19'}, 'name': 'I can find header "Advisories"'}]}, 'login_1;login-as-admin-user;;3': {'id': 'login_1;login-as-admin-user;;3', 'keyword': 'Scenario Outline', 'tags': [{'line': 1, 'name': '@examples'}], 'type': 'scenario', 'name': 'Login as admin user', 'description': '', 'line': 15, 'steps': [{'keyword': 'When ', 'result': {'status': 'passed', 'duration': 12272}, 'line': 8, 'match': {'location': 'features/step_definitions/b.rb:7'}, 'name': 'I visit "bug"'}, {'keyword': 'Then ', 'result': {'status': 'passed', 'duration': 9724}, 'line': 9, 'match': {'location': 'features/step_definitions/b.rb:11'}, 'name': 'I can find content header "Advisories"'}, {'keyword': 'And ', 'result': {'status': 'passed', 'duration': 9461}, 'line': 10, 'match': {'location': 'features/step_definitions/b.rb:19'}, 'name': 'I can find header "Advisories"'}]}, 'login_3;login-as-qa-user': {'id': 'login_3;login-as-qa-user', 'keyword': 'Scenario', 'tags': [{'line': 1, 'name': '@examples'}], 'type': 'scenario', 'name': 'Login as qa user', 'description': '', 'line': 4, 'steps': [{'keyword': 'Given ', 'result': {'status': 'passed', 'duration': 20395}, 'line': 5, 'match': {'location': 'features/step_definitions/b.rb:3'}, 'name': 'I am a "devel" user'}, {'keyword': 'When ', 'result': {'status': 'passed', 'duration': 10753}, 'line': 6, 'match': {'location': 'features/step_definitions/b.rb:7'}, 'name': 'I visit "/errata"'}, {'keyword': 'Then ', 'result': {'status': 'passed', 'duration': 14564}, 'line': 7, 'match': {'location': 'features/step_definitions/b.rb:15'}, 'name': 'I find content header "Advisories"'}]}, 'login_2;login-as-devel-user': {'id': 'login_2;login-as-devel-user', 'keyword': 'Scenario', 'tags': [{'line': 1, 'name': '@examples'}], 'type': 'scenario', 'name': 'Login as devel user', 'description': '', 'line': 4, 'steps': [{'keyword': 'Given ', 'result': {'status': 'passed', 'duration': 35382}, 'line': 5, 'match': {'location': 'features/step_definitions/b.rb:3'}, 'name': 'I am a "devel" user'}, {'keyword': 'When ', 'result': {'status': 'passed', 'duration': 12250}, 'line': 6, 'match': {'location': 'features/step_definitions/b.rb:7'}, 'name': 'I visit "/errata"'}, {'keyword': 'Then ', 'result': {'status': 'passed', 'duration': 11207}, 'line': 7, 'match': {'location': 'features/step_definitions/b.rb:11'}, 'name': 'I can find content header "Advisories"'}]}}
2019-05-27 20:44:46,054 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Get the data from 1558961085-test.json
2019-05-27 20:44:46,055 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO There are 5 scenarios totally.
2019-05-27 20:44:46,055 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Rewrite the results of 4 scenarios
2019-05-27 20:44:46,055 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Complete the result refresh
2019-05-27 20:44:46,055 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Now there are 5 cases passed
2019-05-27 20:44:46,055 [cucumber_rerun_parser.py::write_new_report] INFO Write the new json report 1558961085-new-report.json
2019-05-27 20:44:46,056 [cucumber_rerun_parser.py::write_new_report] INFO Complete to generate the new report 1558961085-new-report.json

```
Have a try before enjoy it on real projects
==
The 'features' dir is just the test dir you can have a try to see how it works. You can try 'test_parser.sh' to do the testing and see the whole process