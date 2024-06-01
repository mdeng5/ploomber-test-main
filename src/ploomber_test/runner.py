import duckdb
from IPython import InteractiveShell

from ploomber_test.parse import iterate_code_chunks


class CodeRunner:
    def __init__(self, text, conn=None):
        self.text = text
        self.shell = InteractiveShell()

        if conn:
            self.conn = conn
        else:
            self.conn = duckdb.connect()

    def run(self):
        for code in iterate_code_chunks(self.text):
            language = code["language"]
            print(f"Running: {code}")

            if language == "python":
                execution = self.shell.run_cell(code["code"])
                execution.raise_error()

                result = execution.result

                print(f"Output: {result}")
            elif language == "sql":
                result = self.conn.execute(code["code"]).fetchall()
                print(f"Output: {result}")
