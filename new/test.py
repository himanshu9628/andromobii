from app import app

print("in test")
@app.route('/hell')
def fatch_home_data1():
    print("in test function")
    return "hello in test"