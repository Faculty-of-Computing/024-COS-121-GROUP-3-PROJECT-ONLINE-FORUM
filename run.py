from app import app
import sys
import traceback

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')
    except Exception as e:
        print("-------------------- CRITICAL ERROR --------------------", file=sys.stderr)
        print("The Flask server has stopped unexpectedly.", file=sys.stderr)
        print("Here is the full traceback that caused the crash:", file=sys.stderr)
        print("-" * 50, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("-" * 50, file=sys.stderr)
        print("Error details:", file=sys.stderr)
        print(e, file=sys.stderr)
        print("------------------------------------------------------", file=sys.stderr)
