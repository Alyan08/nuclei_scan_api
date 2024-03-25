from flask import Flask, request, make_response, jsonify, send_file
from modules import common
from modules import nucl
from modules.cache import cache
# from modules import db


# db.create_database()

app = Flask(__name__)


@app.route('/api/scan/start', methods=['POST'])
@common.source_ip_allowed()
@common.check_api_key()
@common.scan_params_sent()
def add_scan_task():
    target = request.args.get('target')
    severity = request.args.get('severity')

    scan_result = nucl.run_nuclei(target, severity)

    if not scan_result:
        return f"Host {target} is not available", 400

    return make_response(jsonify(scan_result), 200)


@app.route('/api/scan/reports', methods=['GET'])
@common.source_ip_allowed()
@common.check_api_key()
def get_report():
    report_uuid = request.args.get('report_uuid')
    report_status = cache.get(report_uuid)
    # report_status = db.get_status(report_uuid)
    if report_status is None:
        return f"report uuid {report_uuid} not found", 400

    if report_status == 'completed':
        cache.delete(report_uuid)
        # db.delete_report(report_uuid)
        return send_file(f'reports/{report_uuid}.json', mimetype='application/json'), 200

    if report_status.startswith("error"):
        cache.delete(report_uuid)
        # db.delete_report(report_uuid)
        return make_response(jsonify(
            {"message": f"sorry... report with uuid {report_uuid} has error : {report_status}"}
        ), 202)

    return make_response(jsonify({"message": f"status of scan with uuid {report_uuid} : {report_status}"}), 202)


print("... service started ...")

if __name__ == '__main__':
    app.run(debug=False, port=5001)
