import subprocess
import uuid
import json

CONFIG = 'auto'

# example scan data
'''
{"errors": [], "paths": {"_comment": "<add --verbose for a list of skipped paths>", "scanned": ["/tmp/b1f285e8-ab39-47ed-be60-de839ccd3478/DeepSnow.py", "/tmp/b1f285e8-ab39-47ed-be60-de839ccd3478/README.md", "/tmp/b1f285e8-ab39-47ed-be60-de839ccd3478/train.py"]}, "results": [{"check_id": "python.lang.security.deserialization.pickle.avoid-pickle", "end": {"col": 26, "line": 24, "offset": 556}, "extra": {"engine_kind": "OSS", "fingerprint": "d0dc26a534137765d0cb91b1ddfbe0ea1c9ff3aa90272a920f2f9aa86f6e4a883c7ed21f91bfc320ea63746cd421fb37d3d97fc63eab356ccb2c5e4af2558e38_0", "is_ignored": false, "lines": "    pickle.dump(brain, f)", "message": "Avoid using `pickle`, which is known to lead to code execution vulnerabilities. When unpickling, the serialized data could be manipulated to run arbitrary code. Instead, consider serializing the relevant data as JSON or a similar text-based serialization format.", "metadata": {"category": "security", "confidence": "LOW", "cwe": ["CWE-502: Deserialization of Untrusted Data"], "cwe2021-top25": true, "cwe2022-top25": true, "impact": "MEDIUM", "license": "Commons Clause License Condition v1.0[LGPL-2.1-only]", "likelihood": "LOW", "owasp": ["A08:2017 - Insecure Deserialization", "A08:2021 - Software and Data Integrity Failures"], "references": ["https://docs.python.org/3/library/pickle.html"], "semgrep.dev": {"rule": {"origin": "community", "rule_id": "EwU2BJ", "url": "https://semgrep.dev/playground/r/jQTeDJ/python.lang.security.deserialization.pickle.avoid-pickle", "version_id": "jQTeDJ"}}, "shortlink": "https://sg.run/OPwB", "source": "https://semgrep.dev/r/python.lang.security.deserialization.pickle.avoid-pickle", "subcategory": ["audit"], "technology": ["python"]}, "metavars": {"$FUNC": {"abstract_content": "dump", "end": {"col": 16, "line": 24, "offset": 546}, "start": {"col": 12, "line": 24, "offset": 542}}}, "severity": "WARNING"}, "path": "/tmp/b1f285e8-ab39-47ed-be60-de839ccd3478/DeepSnow.py", "start": {"col": 5, "line": 24, "offset": 535}}, {"check_id": "python.lang.security.deserialization.pickle.avoid-pickle", "end": {"col": 27, "line": 31, "offset": 683}, "extra": {"engine_kind": "OSS", "fingerprint": "98d2d655ecb8d7e0ce3631db5e67fd34756dd90df80ad92d6d9f213ebabcbe55ded5c8a9d341a343e5e53008e7dd6071bb817c167e9ccd0e17fac46be01eb762_0", "is_ignored": false, "lines": "    brain = pickle.load(f)", "message": "Avoid using `pickle`, which is known to lead to code execution vulnerabilities. When unpickling, the serialized data could be manipulated to run arbitrary code. Instead, consider serializing the relevant data as JSON or a similar text-based serialization format.", "metadata": {"category": "security", "confidence": "LOW", "cwe": ["CWE-502: Deserialization of Untrusted Data"], "cwe2021-top25": true, "cwe2022-top25": true, "impact": "MEDIUM", "license": "Commons Clause License Condition v1.0[LGPL-2.1-only]", "likelihood": "LOW", "owasp": ["A08:2017 - Insecure Deserialization", "A08:2021 - Software and Data Integrity Failures"], "references": ["https://docs.python.org/3/library/pickle.html"], "semgrep.dev": {"rule": {"origin": "community", "rule_id": "EwU2BJ", "url": "https://semgrep.dev/playground/r/jQTeDJ/python.lang.security.deserialization.pickle.avoid-pickle", "version_id": "jQTeDJ"}}, "shortlink": "https://sg.run/OPwB", "source": "https://semgrep.dev/r/python.lang.security.deserialization.pickle.avoid-pickle", "subcategory": ["audit"], "technology": ["python"]}, "metavars": {"$FUNC": {"abstract_content": "load", "end": {"col": 24, "line": 31, "offset": 680}, "start": {"col": 20, "line": 31, "offset": 676}}}, "severity": "WARNING"}, "path": "/tmp/b1f285e8-ab39-47ed-be60-de839ccd3478/DeepSnow.py", "start": {"col": 13, "line": 31, "offset": 669}}, {"check_id": "python.lang.security.deserialization.pickle.avoid-pickle", "end": {"col": 26, "line": 37, "offset": 789}, "extra": {"engine_kind": "OSS", "fingerprint": "d0dc26a534137765d0cb91b1ddfbe0ea1c9ff3aa90272a920f2f9aa86f6e4a883c7ed21f91bfc320ea63746cd421fb37d3d97fc63eab356ccb2c5e4af2558e38_1", "is_ignored": false, "lines": "    pickle.dump(brain, f)", "message": "Avoid using `pickle`, which is known to lead to code execution vulnerabilities. When unpickling, the serialized data could be manipulated to run arbitrary code. Instead, consider serializing the relevant data as JSON or a similar text-based serialization format.", "metadata": {"category": "security", "confidence": "LOW", "cwe": ["CWE-502: Deserialization of Untrusted Data"], "cwe2021-top25": true, "cwe2022-top25": true, "impact": "MEDIUM", "license": "Commons Clause License Condition v1.0[LGPL-2.1-only]", "likelihood": "LOW", "owasp": ["A08:2017 - Insecure Deserialization", "A08:2021 - Software and Data Integrity Failures"], "references": ["https://docs.python.org/3/library/pickle.html"], "semgrep.dev": {"rule": {"origin": "community", "rule_id": "EwU2BJ", "url": "https://semgrep.dev/playground/r/jQTeDJ/python.lang.security.deserialization.pickle.avoid-pickle", "version_id": "jQTeDJ"}}, "shortlink": "https://sg.run/OPwB", "source": "https://semgrep.dev/r/python.lang.security.deserialization.pickle.avoid-pickle", "subcategory": ["audit"], "technology": ["python"]}, "metavars": {"$FUNC": {"abstract_content": "dump", "end": {"col": 16, "line": 37, "offset": 779}, "start": {"col": 12, "line": 37, "offset": 775}}}, "severity": "WARNING"}, "path": "/tmp/b1f285e8-ab39-47ed-be60-de839ccd3478/DeepSnow.py", "start": {"col": 5, "line": 37, "offset": 768}}], "version": "1.14.0"}'''


def semgrep_download(github_url: str):
    temp_filename = str(uuid.uuid4())
    subprocess.run(f'git clone {github_url} /tmp/{temp_filename}'.split())

    res = subprocess.run(f'semgrep --json --config {CONFIG} /tmp/{temp_filename}'.split(), capture_output=True)

    scan_data = json.loads(res.stdout.decode('utf-8'))
    # stderr contains some info, but we prob dont need cuz stdout json probably has everything
    #res.stderr.decode('utf-8') 

    subprocess.run(f'rm -drf /tmp/{temp_filename}'.split())
    return scan_data
