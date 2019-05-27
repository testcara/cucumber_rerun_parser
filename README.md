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
2019-05-24 17:57:18,977 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Read the data from rerun-report-name.json
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Get scenarios and results maps from rerun-report-name.json
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Have got all scenarios and results:
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO {'Login as qa user': 'passed', 'Login as admin user': 'passed'}
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Pop failed scenarios
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO Have got all passed scenarios:
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::get_passed_scenario_from_rerun_report] INFO {'Login as qa user': 'passed', 'Login as admin user': 'passed'}
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Update the origin-report-name.json with rerun results {'Login as qa user': 'passed', 'Login as admin user': 'passed'}
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Get the data from test.json
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO There are 3 scenarios totally.
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Rewrite the results of 2 scenarios
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Pop the outdated faile:d scenarios
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Poping scenario:Login as admin user
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Poping scenario:Login as qa user
2019-05-24 17:57:18,978 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Add the rerun passed scenarios
2019-05-24 17:57:18,979 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Appending the passed scenario:Login as qa user
2019-05-24 17:57:18,979 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Appending the passed scenario:Login as admin user
2019-05-24 17:57:18,979 [cucumber_rerun_parser.py::refresh_report_with_rerun_passed_scenarios] INFO Complete the result refresh
2019-05-24 17:57:18,979 [cucumber_rerun_parser.py::write_new_report] INFO Write the new json report new-report-name.json
2019-05-24 17:57:18,979 [cucumber_rerun_parser.py::write_new_report] INFO Complete to generate the new report new-report-name.json
```
Have a try before enjoy it on real projects
==
The 'features' dir is just the test dir you can have a try to see how it works. You can try 'test_parser.sh' to do the testing and see the whole process.


