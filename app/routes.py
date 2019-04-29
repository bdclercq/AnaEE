from flask import render_template, request, redirect
from app import app


@app.route('/')
def home():
    return render_template('admin.html')


@app.route('/commit_config', methods=['POST', 'GET'])
def commit_config():
    if request.method == 'POST':
        result = request.form
        timestamp = result['datetime']
        print(timestamp)
        if 'fati1' in result:
            print(1)
        if 'fati2' in result:
            print(2)
        if 'fati3' in result:
            print(3)
        if 'fati4' in result:
            print(4)
        if 'fati5' in result:
            print("fati 5 found")
        if 'fati6' in result:
            print("fati 6 found")
        if 'fati7' in result:
            print(7)
        if 'fati8' in result:
            print(8)
        if 'fati9' in result:
            print(9)
        if 'fati10' in result:
            print(10)
        if 'fati11' in result:
            print("fati 11 found")
        if 'fati12' in result:
            print("fati 12 found")
        if 'valve1' in result:
            print("valve 1 found")
        if 'valve2' in result:
            print("valve 2 found")
        if 'valve3' in result:
            print("valve 3 found")
        if 'valve4' in result:
            print("valve 4 found")
        if 'valve5' in result:
            print("valve 5 found")
        if 'valve6' in result:
            print("valve 6 found")
        if 'valve7' in result:
            print("valve 7 found")
        if 'valve8' in result:
            print("valve 8 found")
        print(result)
    return redirect("/")
