import json

class JSONExporter():
    def __init__(self, output_path):
        self.output_path = output_path

    def save(self, solutions, metadata):
        result = {"status":"SUCCESS",
                  "system_info":metadata,
                  "solution":solutions}
        with open(self.output_path, 'w') as f:
            json.dump(result, f, indent=2)

    def save_error(self, e):
        result = {
            "status": "ERROR",
            "error_type": type(e).__name__,
            "message": str(e),
            }
        with open(self.output_path, 'w') as f:
            json.dump(result, f, indent=2)