from flask import Flask,render_template,request,Response
from price_comp import comp
from prod_comp import detail
from qr_decoder import generate_frames,__del__
from qr_comp import generate_frames_qrComp,__del__ 
from Popularity_rec_sys import Rec_engine
import os
import pandas as pd
from stegano import decode
app=Flask(__name__)

@app.route("/")
@app.route("/home")
def home_page():
    try:
        return render_template("home.html")
    except:
        return render_template("error.html")

@app.route("/result",methods=['post', 'get'])
def result_page():
    try:
        if request.method=='POST':
            x=request.form.get('nm1')
            print(x)
            x_name=x

            cont=True
            while cont:
                try:
                    items=comp(x)
                    cont=False
                    
                except:
                    cont=True  #change

            #print(z)
            #items=comp(x)
            #print(len(items))
        
        return render_template("result.html",items=items,x_name=x_name) #items=items
    except:
        return render_template("error.html")

@app.route("/price")
def price():
    try:
        return render_template("price_input.html")
    except:
        return render_template("error.html")

@app.route("/prod")
def product():
    try:
        return render_template("prod_input.html")
    except:
        return render_template("error.html")

@app.route('/Reco')
def Rec_sys():
    try:
        Rec_engine()
        rank=[]
        for i in range(10):
            i=i+1
            rank.append(i)
        print(rank)
        dpls=pd.read_csv("top_10.csv")
        dpls['rank']=rank
        print(dpls.columns)
        top=dpls[['name','prod_link','image','score','rank']]
        top=top.to_dict('records')
        print(top)
        return render_template('rec_result.html',top=top)
    except:
        return render_template("error.html")

@app.route("/result2", methods=['post', 'get'])
def product_result():
    try:
       if request.method=='POST':
            one=request.form.get('nm1')
            two=request.form.get('nm2')
            #x_one=one
            #x_two=two
            print(one)
            print(two)
            det=detail(one,two)
            print(det)
            comb=one +' and '+ two
            return render_template("result_2.html",det=det,comb=comb)
    except:
        return render_template("error.html")

@app.route("/result3")
def product_result_qrComp():
    try:
        try:
            lines_list = open('dummy.txt').read().splitlines()
        except:
            return render_template('error_qrComp.html')
        print(lines_list)
        os.remove('dummy.txt') # delete txt file after its use
        #x_two=two
        one=lines_list[0]
        two=lines_list[1]
        det=detail(one,two)
        print(det)
        comb='QR Comparison are: '
        return render_template("result_2.html",det=det,comb=comb)
    except:
        return render_template("error.html")

@app.route('/redeem',methods=['post','get'])
def redeem():
    try:
        if request.method == 'POST':
            img1 = request.form.get("image")
            print(img1)
            rc = decode(img1)
            print(rc)
            return render_template('result_3.html',rc=rc)
        return render_template("redeem.html")
    except:
        return render_template("error.html")

@app.route('/qr')
def qr_disp():
    try:
        return render_template('disp_qr.html')
    except:
        return render_template("error.html")

@app.route('/qrComp')
def qrComp_disp():
    try:
        return render_template('disp_qrComp.html')
    except:
        return render_template("error.html")

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/video')
def video_qr():
    try:
        return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        return render_template("error.html")

@app.route('/VideoQrComp')
def video_qrComp():
    try:
        return Response(generate_frames_qrComp(),mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        return render_template("error.html")

if __name__ == '__main__':
    app.run(debug=True)
