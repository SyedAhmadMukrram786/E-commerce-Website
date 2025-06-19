from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Product, Contact, Orders, Order_Update
from math import ceil
from datetime import datetime, timedelta
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)

    allProds = []
    catprods = Product.objects.values('category','product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params = {
        'allProds': allProds
    }
    return render(request, 'shop/index.html',params)

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category','product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if len(prod) != 0:
            allProds.append([prod,range(1,nSlides),nSlides])

    params = {
        'allProds': allProds,
        'msg':""
    }
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg':"PLease make sure to enter relevent search query"}
    return render(request, 'shop/search.html', params)

def searchMatch(query, item):
    if query.lower() in item.desc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower():
        return True
    else:
        return False

def ProductsDetail(request):
    Product_data = Product.objects.all()
    context = {
        'Product': Product_data
    }
    return render(request, 'shop/Products.html', context)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thanks = False
    if request.method=="POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name, email=email,phone=phone,desc=desc)
        contact.save()   
        thanks = True 
    return render(request, 'shop/contact.html', {'thanks':thanks})

def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderid, email=email)
            if len(order) > 0:
                update = Order_Update.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"Status":"Success","Update":updates, "ItemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')



JAZZCASH_MERCHANT_ID ="MC173732"
JAZZCASH_PASSWORD = "svvfv56vsa"
JAZZCASH_RETURN_URL = "http://127.0.0.1:8000/shop/success/"
JAZZCASH_INTEGRITY_SALT = "5103tvhs49"

def JazzCash(request):

    product_name = "Gaming PC"
    product_price = 12000

    pp_Amount = int(product_price) * 100

    pp_TxnDateTime = datetime.now().strftime('%Y%m%d%H%M%S')
    pp_TxnExpiryDateTime = (datetime.now() + timedelta(hours=1)).strftime('%Y%m%d%H%M%S') 


    pp_TxnRefNo = "T" +pp_TxnDateTime

    post_Data = {
        "pp_Version": "1.1",
        "pp_TxnType": "MPAY",
        "pp_Language": "EN",
        "pp_MerchantID": JAZZCASH_MERCHANT_ID,
        "pp_SubMerchantID": "",
        "pp_Password": JAZZCASH_PASSWORD,
        "pp_BankID": "TBANK",
        "pp_ProductID": "RETL",
        "pp_TxnRefNo": pp_TxnRefNo,
        "pp_Amount": pp_Amount,  # Must be in paisa
        "pp_TxnCurrency": "PKR",
        "pp_TxnDateTime": pp_TxnDateTime,
        "pp_BillReference": "Ref123",
        "pp_Description": "Gaming PC Payment",
        "pp_TxnExpiryDateTime": pp_TxnExpiryDateTime,
        "pp_ReturnURL": JAZZCASH_RETURN_URL,
        "pp_CNIC": "4210123456789",  # Optional
        "pp_MobileNumber": "03001234567",  # Optional
        "pp_SecureHash": "",  # Set after hashing
        "ppmpf_1": "user123",
        "ppmpf_2": "custom1",
        "ppmpf_3": "custom2",
        "ppmpf_4": "custom3",
        "ppmpf_5": "custom4"
    }
    sorted_string = '&'.join(f"{key}={value}" for key, value in sorted(post_Data.items()) if key != "pp_SecureHash" and value != "")
    pp_SecureHash = hmac.new(
        JAZZCASH_INTEGRITY_SALT.encode(),
        sorted_string.encode(),
        hashlib.sha256
    ).hexdigest()

    post_Data['pp_SecureHash'] = pp_SecureHash

    context = {
        'product_name' : product_name,
        'product_price': product_price,
        'post_data':post_Data
    }

    return render(request, 'shop/Jazzcash.html', context)

@csrf_exempt
def success(request):    
    return render(request, 'shop/success.html')

def productview(request, id):
    #Fetch the Product by using ID
    prod = Product.objects.filter(product_id=id)
    print(prod)
    return render(request, 'shop/productview.html', {'product':prod[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','') + " " + request.POST.get('address2','')
        phone = request.POST.get('phone','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        order = Orders(items_json=items_json, name=name, email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code)
        order.save()    
        update = Order_Update(order_id = order.order_id, update_desc = "The order has been placed")
        update.save()
        thank= True
        Id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'Id':Id})
    return render(request, 'shop/checkout.html')