from app import app
# from model.fatch_data import get_data

# obj = get_data()



@app.route('/hello')
def fatch_home_data():
    return "hello"


# def fatch_data():
#     return obj.get_data()