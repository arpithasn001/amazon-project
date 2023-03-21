from flask import Flask,render_template,request 
from bs4 import BeautifulSoup as bs
from urllib .request import urlopen as urReq
from selenium import webdriver
import requests
import logging
from datetime import datetime

fileName= datetime.now().strftime('main_%H_%M_%S_%d_%m_%Y.log')
logging.basicConfig(filename=fileName,level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")


app = Flask(__name__)
 
@app.route("/",methods = ['POST','GET'])
def index():
    return render_template('index.html')

@app.route("/review",methods = ['POST','GET'])
def results():



    if request.method == "POST":
        try:

        
            searchString=request.form['content'].replace(" ","")
            amazon_url="https://www.amazon.in/s?k=" + searchString
            response=urReq(amazon_url)
            driver=webdriver.Chrome(r"C:\Users\Admin\Desktop\chromedriver.exe")
            driver.get(amazon_url)
            data_amazon=response.read()

            # response.close()
            soup=bs(driver.page_source,"html.parser")
            all=soup.find_all("div",class_="s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis s-latency-cf-section s-card-border")
            # print(all)
            page=soup.find_all("div",class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16")
            print(page)
            # print(soup)
            amazon=soup.find_all("h2",class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2")[0].a["href"]
            amazon='https://www.amazon.in/sspa/click?ie=UTF8&spc=MTo4MDA0NDE4MjU1NzQ2NjI4OjE2NzY4NjkwNTA6c3BfYXRmOjIwMDc1OTg2MTQxMDk4OjowOjo&url=%2FLG-inches-Ultra-43UQ7500PSF-Ceramic%2Fdp%2FB0B3XY5YT4%2Fref%3Dsr_1_1_sspa%3Fkeywords%3Dtv%26qid%3D1676869050%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1'
            driver.get(amazon)
            soupa=bs(driver.page_source,"html.parser")
            bs(amazon,"html.parser")
            # comm=soupa.find("span",class_="a-size-base review-text").span.text

            reviews=[]

        
        

            com=soupa.find("span",class_="a-size-base review-text").span.text         
            print(com)
            
            comment_h=soupa.find("a",class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold").span.text          
            print(comment_h)
            name=soupa.find("div",class_="a-row a-spacing-mini").span.text
            print(name)
            price=soup.find("span",class_="a-price-whole").text
            print(price)
            ratings=soupa.find('span',class_="a-size-base a-nowrap").text
            print(ratings)



            mydict={"COMMENT":com,"COMMENT_H":comment_h,"NAME":name,"PRICE":price,"RATINGS":ratings}
            reviews.append(mydict)
            return render_template('results.html',reviews=reviews[0:2]) 

        except:
          return render_template('issue in the code')
    else:
        return render_template(index.html)      

if __name__ == '__main__':

    app.run(debug=True)