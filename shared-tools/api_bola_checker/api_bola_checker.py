#!/usr/bin/env python3
import argparse, requests, json, time

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--endpoints', required=True)
    p.add_argument('--ids', default='1,2')
    p.add_argument('--method', default='GET', choices=['GET','POST','PUT','DELETE'])
    p.add_argument('--data-template', default=None)
    p.add_argument('--out', default='bola_report.json')
    p.add_argument('--delay', type=float, default=0.3)
    p.add_argument('--headers', default=None)
    return p.parse_args()

def load_endpoints(path):
    with open(path, 'r') as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith('#')]
    return lines

def apply_template(url_template, id_value, data_template=None):
    url = url_template.replace('{id}', str(id_value))
    data = None
    if data_template:
        data = data_template.replace('{id}', str(id_value))
    return url, data

def safe_json(resp):
    try:
        return resp.json()
    except:
        return None

def summarize_response(resp):
    body = resp.text if hasattr(resp, 'text') else ''
    js = safe_json(resp)
    summary = {
        'status_code': resp.status_code,
        'content_length': len(body),
        'json_keys': list(js.keys()) if isinstance(js, dict) else None,
        'body_sample': body[:200].replace('\n',' ') if body else ''
    }
    return summary

def compare_summaries(s1, s2):
    diffs = {}
    if s1['status_code'] != s2['status_code']:
        diffs['status_code'] = (s1['status_code'], s2['status_code'])
    if s1['content_length'] != s2['content_length']:
        diffs['content_length'] = (s1['content_length'], s2['content_length'])
    if s1['json_keys'] != s2['json_keys']:
        diffs['json_keys'] = (s1['json_keys'], s2['json_keys'])
    if s1['body_sample'] != s2['body_sample']:
        diffs['body_sample_sample_diff'] = True
    return diffs

def run_check(session, endpoint_template, ids, method='GET', data_template=None, headers=None, delay=0.3):
    results = {}
    for idv in ids:
        url, data = apply_template(endpoint_template, idv, data_template)
        try:
            if method in ('GET','DELETE'):
                r = session.request(method, url, headers=headers, timeout=15)
            else:
                if data:
                    try:
                        json_data = json.loads(data)
                        r = session.request(method, url, json=json_data, headers=headers, timeout=15)
                    except:
                        r = session.request(method, url, data=data, headers=headers, timeout=15)
                else:
                    r = session.request(method, url, headers=headers, timeout=15)
        except Exception as e:
            results[str(idv)] = {'error': str(e)}
            continue
        summary = summarize_response(r)
        results[str(idv)] = {'summary': summary, 'status': 'ok'}
        time.sleep(delay)

    base = results.get(str(ids[0]))
    anomalies = []
    if base and 'summary' in base:
        for idv in ids[1:]:
            cur = results.get(str(idv))
            if not cur or 'summary' not in cur:
                continue
            diffs = compare_summaries(base['summary'], cur['summary'])
            if diffs:
                anomalies.append({'id_pair': (ids[0], idv), 'diffs': diffs})

    return {'endpoint': endpoint_template, 'results': results, 'anomalies': anomalies}

def main():
    args = parse_args()
    endpoints = load_endpoints(args.endpoints)
    ids = [x.strip() for x in args.ids.split(',') if x.strip()]
    headers = json.loads(args.headers) if args.headers else {}
    session = requests.Session()
    full_report = {'run_at': None, 'checks': []}
    full_report['run_at'] = __import__('datetime').datetime.utcnow().isoformat() + 'Z'
    for ep in endpoints:
        res = run_check(session, ep, ids, method=args.method, data_template=args.data_template, headers=headers, delay=args.delay)
        full_report['checks'].append(res)
    with open(args.out, 'w') as fh:
        json.dump(full_report, fh, indent=2)
    print(f"Report saved to {args.out}")

if __name__ == '__main__':
    main()
